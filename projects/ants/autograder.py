"""Common utility functions for automatic grading."""

import sys, os, traceback
from doctest import DocTestFinder, DocTestRunner
from collections import namedtuple, defaultdict
import urllib.request, urllib.error
import re
import argparse

Test = namedtuple('Test', ['name', 'fn'])
TESTS = []

# set path for autograder to test current working directory
sys.path[0:0] = [ os.getcwd() ]

def test(fn):
    """Decorator to register a test. A test returns a true value on failure."""
    TESTS.append(Test(fn.__name__, fn))
    return fn

def test_all(project_name, tests=TESTS):
    """Run all TESTS. Exits with a useful code: 0 for ok, 1 for problems."""
    for test in tests:
        underline('Test {0}'.format(test.name))
        try:
            failure = test.fn(None)
        except Exception as inst:
            traceback.print_exc()
            failure = True
        if failure:
            sys.exit(1)
        print('All released tests passed')
        print()
    sys.exit(0)

class TimeoutError(Exception):
    pass

TIMEOUT = 20
def test_eval(func, inputs, timeout=TIMEOUT, **kwargs):
    if type(inputs) is not tuple:
        inputs = (inputs,)
    result = timed(func, timeout, inputs, kwargs)
    return result

def timed(func, timeout, args=(), kwargs={}):
    """Calls FUNC with arguments ARGS and keyword arguments KWARGS. If it takes
    longer than TIMEOUT seconds to finish executing, a TimeoutError will be
    raised."""
    from threading import Thread
    class ReturningThread(Thread):
        """Creates a daemon Thread with a result variable."""
        def __init__(self):
            Thread.__init__(self)
            self.daemon = True
            self.result = None
            self.error = None
        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except Exception as e:
                e._message = traceback.format_exc(limit=2)
                self.error = e
    submission = ReturningThread()
    submission.start()
    submission.join(timeout)
    if submission.is_alive():
        raise TimeoutError("Evaluation timed out!")
    if submission.error is not None:
        raise submission.error
    return submission.result

def check_func(func, tests,
               comp = lambda x, y: x == y,
               in_print = repr, out_print = repr):
    """Test FUNC according to sequence TESTS.  Each item in TESTS consists of
    (I, V, D=None), where I is a tuple of inputs to FUNC (if not a tuple,
    (I,) is substituted) and V is the proper output according to comparison
    COMP.  Prints erroneous cases.  In case of error, uses D as the test
    description, or constructs a description from I and V otherwise.
    Returns 0 for all correct, or the number of tests failed."""
    code = 0
    for input, output, *desc in tests:
        try:
            val = test_eval(func, input)
        except Exception as e:
            fail_msg = "Function {0} failed".format(func.__name__)
            if desc:
                print(fail_msg, desc[0])
            else:
                print(fail_msg, "with input", in_print(input))
            print(e._message)
            code += 1
            continue
        if not comp(val, output):
            wrong_msg = "Wrong result from {0}:".format(func.__name__)
            if desc:
                print(wrong_msg, desc[0])
            else:
                print(wrong_msg, "input", in_print(input))
                print("   returned", val, "not", out_print(output))
            code += 1
    return code

def check_doctest(func_name, module, run=True):
    """Check that MODULE.FUNC_NAME doctest passes."""
    func = getattr(module, func_name)
    tests = DocTestFinder().find(func)
    if not tests:
        print("No doctests found for " + func_name)
        return True
    fn = lambda: DocTestRunner().run(tests[0])
    result = test_eval(fn, tuple())
    if result.failed != 0:
        print("A doctest example failed for " + func_name + ".")
        return True
    return False

def underline(s):
    """Print string S, double underlined in ASCII."""
    print(s)
    print('='*len(s))

def check_for_updates(index, filenames, version):
    print('You are running version', version, 'of the autograder')
    try:
        remotes = {}
        for filename in filenames:
            path = os.path.join(index, filename)
            data = timed(urllib.request.urlopen, 1, args=(path,))
            remotes[filename] = data.read().decode('utf-8')
    except (urllib.error.URLError, urllib.error.HTTPError):
        print("Couldn't check remote autograder")
        return
    except TimeoutError:
        print("Checking for updates timed out.")
        return
    remote_version = re.search("__version__ = '(.*)'",
                               remotes[filenames[0]])
    if remote_version and remote_version.group(1) != version:
        print('Version', remote_version.group(1),
              'is available with new tests.')
        prompt = input('Do you want to automatically download these files? [y/n]: ')
        if 'y' in prompt.lower():
            for file in filenames:
                with open(file, 'w') as new:
                    new.write(remotes[file])
                    print('\t', file, 'updated')
            exit(0)
        else:
            print('You can download the new autograder from the following links:')
            for file in filenames:
                print('\t' + os.path.join(index, file))
            print()

def run_tests(name, remote_index, autograder_files, version, **kwargs):
    parser = argparse.ArgumentParser(description='Autograder for CS 61A.')
    parser.add_argument('-q', '--question', type=int,
                        help='Run tests for the specified question')
    parser.add_argument('-v', '--version', action='store_true',
                        help='Prints autograder version and exits')
    args = parser.parse_args()

    check_for_updates(remote_index, autograder_files, version)
    if args.version:
        exit(0)
    elif args.question and 0 < args.question <= len(TESTS):
        tests = [TESTS[args.question-1]]
    else:
        tests = TESTS
    test_all(name, tests)
