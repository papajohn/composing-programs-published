"""A simple web crawler that checks for dead links on a given website.
Recursively checks all links to pages hosted by the same site. Supports
multithreaded execution.

Usage: python3 crawler.py [-p <num_threads>] [-t <timeout>] <site>

The -p flag enables multithreading, with the given number of threads.
The -t flag specifies the request timeout in seconds; default is 5.

The crawler prints out URLs as they are being handled and reports bad links.
This printing is intentionally unsynchronized to demonstrate when URLs are
handled.

The crawler does not spoof its user agent, so links from sites such as Google
and Wikipedia, which reject crawlers, are reported as bad.
"""

from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser
from threading import Thread, Lock
from queue import Queue
from time import time
from ucb import main
import socket
import sys

default_timeout = 5

#################
# URL Functions #
#################

def make_url(url, base):
    """Construct a full URL from the given URL fragment and base URL. Filters
    out non-http links.

    >>> make_url('../sp13', 'http://inst.eecs.berkeley.edu/~cs61a/fa12/')
    'http://inst.eecs.berkeley.edu/~cs61a/sp13'
    >>> make_url('http://espn.com', 'http://mlb.com/')
    'http://espn.com'
    >>> make_url('ftp://some-site.com', 'http://mlb.com/')
    """
    parsed = urlparse(url)
    scheme = parsed.scheme if parsed.scheme else 'http'
    netloc = parsed.netloc
    if scheme != 'http':
        return None
    elif not netloc:
        if not parsed.path:
            return None
        elif parsed.path[0] != '/':
            return simplify_url(base + parsed.path)
        netloc = urlparse(base).netloc
    return simplify_url(scheme + '://' + netloc + parsed.path)

def simplify_url(url):
    """Simplify a URL by processing .'s and ..'s, and replacing double slashes
    with single slashes.

    >>> simplify_url('http://inst.eecs.berkeley.edu/~cs61a/./sp13/projects/../..')
    'http://inst.eecs.berkeley.edu/~cs61a'
    """
    pieces = url.split('/')
    result = [pieces[0] + '/']
    for i in range(1, len(pieces)):
        piece = pieces[i]
        if piece == '..':
            result.pop()
        elif piece and piece != '.':
            result.append(piece)
    return '/'.join(result)

def get_base(url):
    """Extract the base directory of a URL.

    >>> get_base('http://inst.eecs.berkeley.edu/~cs61a/sp13/index.html')
    'http://inst.eecs.berkeley.edu/~cs61a/sp13/'
    """
    return url[:url.rindex('/')+1]

######################
# Parser and Crawler #
######################

class LinkParser(HTMLParser):
    """A parser that parses an HTML page for links, adding them to the Crawler
    associated with this parser."""
    def __init__(self, crawler):
        HTMLParser.__init__(self, False)
        self.crawler = crawler
        self.base = None
        self.page = None

    def reset_with_page(self, page):
        """Reset this parser for the given page."""
        self.reset()
        self.base = get_base(page)
        self.page = page

    def handle_starttag(self, tag, attrs):
        """Queue <a href=...> links found in the page in this parser's
        Crawler."""
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.crawler.queue_url(attr[1], self.base, self.page)


class Crawler(object):
    """A web crawler that processes links in a given website, recursively
    following all links on that site. This crawler supports parallel execution.
    Crawling is done by calling crawl with a page parser that queues new tasks
    in this Crawler."""
    def __init__(self, site, timeout, parallel=False):
        self.site = site
        self.timeout = timeout
        self.parallel = parallel
        self.queued = set() # set of URLs that have already been seen
        if parallel:
            # Synchronize access both to the set of seen URLs and the task queue
            self.queued_lock = Lock()
            self.queue = Queue()
        else:
            self.queue = []
        self.url_count = 0
        self.queue_url(site, site, None)

    def put_task(self, task):
        """Queue the given task in this Crawler."""
        if self.parallel:
            self.queue.put(task)
        else:
            self.queue.append(task)

    def get_task(self):
        """Retrieve a task from this Crawler. The caller should first check that
        tasks remain."""
        if self.parallel:
            return self.queue.get()
        else:
            return self.queue.pop()

    def task_done(self):
        """Inform the Crawler that a task has completed. This should be done
        every time a task is finished."""
        if self.parallel:
            self.queue.task_done()

    def all_done(self):
        """Check whether or not all tasks have completed."""
        if self.parallel:
            # No synchronization needed; unfinished_tasks will never hit 0
            # unless everything is done
            return self.queue.unfinished_tasks == 0
        else:
            return len(self.queue) == 0

    def unsynchronized_already_seen(self, url):
        """Check if a URL has already been seen, adding it to the set of seen
        URLs if not already there. Access to the set should be synchronized by
        the caller if necessary."""
        if not url or url in self.queued:
            return True
        self.queued.add(url)
        self.url_count += 1
        return False

    def already_seen(self, url):
        """Check if the given URL has already been seen. Locks access to the set
        of seen URLs if crawling is being done in parallel."""
        if self.parallel:
            with self.queued_lock: # lock access to set
                return self.unsynchronized_already_seen(url)
        else:
            return self.unsynchronized_already_seen(url)

    def queue_url(self, url, base, parent):
        """Queue the givn URL for reading, if it hasn't been seen before."""
        url = make_url(url, base) # construct and/or simplify the URL
        if self.already_seen(url):
            return

        # Only read the page if it is on this site and is HTML
        read = url.startswith(self.site)
        index = url.rindex('/')
        page = url[index+1:]
        index = page.rfind('.')
        if index >= 0:
            ext = page[index+1:]
            if ext != 'html' and ext != 'htm':
                read = False

        # Safely queue a new task to process the URL
        self.put_task((url, parent, read))

    def handle_url(self, url_info, parser):
        """Process the URL specified by url_info with the given parser. Messages
        produced by this method are intentionally unsynchronized."""
        url, parent, read = url_info
        print('handling:', url)

        # Request, but don't read the page
        try:
            opened = urlopen(url, timeout=self.timeout)
        except (HTTPError, URLError, socket.timeout) as e:
            print('bad link in {0}: {1}'.format(parent, url))
            print('error:', e)
            return

        if not read:
            return

        # Now read the page and send data to the parser
        parser.reset_with_page(opened.geturl())
        try:
            data = opened.read().decode()
            parser.feed(data)
        except Exception as e:
            print('error while reading {0}: {1}'.format(url, e))

    def crawl(self, parser):
        """Crawl the site with the given parser."""
        while not self.all_done():
            self.handle_url(self.get_task(), parser)
            self.task_done()
        
#################
# Crawl Masters #
#################

def serial_crawl(site, timeout, num_threads=1):
    """Crawl the given site sequentially for dead links. timeout is the request
    timeout in seconds. num_threads should always be 1."""
    assert num_threads == 1, 'serial_crawl cannot use multiple threads'

    crawler = Crawler(site, timeout)
    parser = LinkParser(crawler)

    start = time()
    crawler.crawl(parser)
    total = round(time() - start, 2)

    msg = 'serial crawl took {0} seconds, examined {1} urls'
    print(msg.format(total, crawler.url_count))


def parallel_crawl(site, timeout, num_threads=4):
    """Crawl the given site in parallel for dead links. timeout is the request
    timeout in seconds. num_threads is the number of threads to use for
    crawling."""
    crawler = Crawler(site, timeout, parallel=True)
    parsers = [LinkParser(crawler) for _ in range(num_threads)]
    threads = [Thread(target=crawler.crawl, args=(parsers[i],))
               for i in range(num_threads)]

    start = time()
    for t in threads:
        t.daemon = True # don't wait for spawned threads to exit
        t.start()
    crawler.queue.join() # wait for all tasks to be finished
    total = round(time() - start, 2)

    msg = 'parallel crawl took {0} seconds, examined {1} urls'
    print(msg.format(total, crawler.url_count))

##########################
# Command Line Interface #
##########################

@main
def run(*args):
    crawl, num_threads = serial_crawl, 1
    url, timeout = None, default_timeout
    i = 0
    while i < len(args):
        if args[i] == '-p':
            crawl = parallel_crawl
            num_threads = int(args[i+1])
        elif args[i] == '-t':
            timeout = int(args[i+1])
        elif args[i].startswith('http://'):
            if url:
                print('only one URL may be provided', file=sys.stderr)
                return
            url = args[i]
            i -= 1
        else:
            if args[i] != '-h' and args[i] != '-help':
                print('unknown argument:', args[i], file=sys.stderr)
            print('Options:\n' +
                  '  -p <num>     run with <num> threads\n' +
                  '  -t <num>     use <num> as the request timeout',
                  file=sys.stderr)
            return
        i += 2
    crawl(url, timeout, num_threads)
