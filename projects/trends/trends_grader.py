"""Automatic grading script for the Trends project.

Expects the following files in the current directory:

trends.py
data.py
geo.py
maps.py
ucb.py
autograder.py

This file uses features of Python not yet covered in the course.
"""

__version__ = '1.2'

from autograder import test, run_tests, check_func, check_doctest, test_eval

try:
    import trends      # Student submission
except (SyntaxError, IndentationError) as e:
    import traceback
    print('Unfortunately, the autograder cannot run because ' +
          'your program contains a syntax error:')
    traceback.print_exc(limit=1)
    exit(1)

from ucb import main
from maps import us_states

datetime = trends.datetime

#########
# TESTS #
#########

@test
def problem1():
    if check_doctest('make_tweet', trends):
        return True
    if check_doctest('make_tweet_fn', trends):
        return True

    expected_texts = [
        'hello, world! !dlrow ,olleh',
        'i mean what person wouldn\'t? it\'s john stamos!',
        "ph'nglui mglw'nafh cthulhu r'lyeh wgah'nagl fhtagn",
        'kfdafj. afjdsal.jfdlsafj. fjd jksa',
        '/never/look up.when dragons!fly overhead.',
        'jeepers, what fools these mortals be!',
    ]

    expected_dates = [datetime(2010, 1, 2, k, 4, 5) for k in range(1, 7)]

    expected_locations = [(38, -120 + k) for k in range(6)]

    import geo
    def location_tuple(tweet_location):
        def location_tuple(tweet):
            location = tweet_location(tweet)
            return (geo.latitude(location), geo.longitude(location))
        return location_tuple

    tweets_as_dicts = tricky_tweets(trends.make_tweet)
    if check_func(trends.tweet_text, zip(tweets_as_dicts, expected_texts)):
        return True
    elif check_func(trends.tweet_time, zip(tweets_as_dicts, expected_dates)):
        return True
    elif check_func(location_tuple(trends.tweet_location),
                    zip(tweets_as_dicts, expected_locations)):
        return True

    tweets_as_fns = tricky_tweets(trends.make_tweet_fn)
    if check_func(trends.tweet_text_fn, zip(tweets_as_fns, expected_texts)):
        return True
    elif check_func(trends.tweet_time_fn, zip(tweets_as_fns, expected_dates)):
        return True
    elif check_func(location_tuple(trends.tweet_location_fn),
                    zip(tweets_as_fns, expected_locations)):
        return True

@test
def problem2():
    if check_doctest('extract_words', trends):
        return True

    import string
    tests = [
        ('You! Shall! Not!...Pass!', ['You', 'Shall', 'Not', 'Pass'],),
        ('This.is`separated!by@only#non$letter%characters^so&you*need(to)use-white+listing{instead}of\\black/listing:or"else<you\'ll>get~the  wrong answer',
        ['This', 'is', 'separated', 'by', 'only', 'non', 'letter', 'characters', 'so', 'you', 'need', 'to', 'use', 'white', 'listing', 'instead', 'of', 'black', 'listing', 'or', 'else', 'you', 'll', 'get', 'the', 'wrong', 'answer']),
        ['', []],  # This test is constructed below.
    ]

    pathological_test = tests[-1]
    for i in range(32,128):
        c = chr(i)
        if (c in string.ascii_letters or not c in string.printable): continue
        pathological_test[0] += chr(i) + 'a'
        pathological_test[1].append('a')

    if check_func(trends.extract_words, tests):
        print('Failed test(s) in extract_words.')
        return True

@test
def problem3():
    if check_doctest('get_word_sentiment', trends):
        return True

    has_sentiment_tests = (
        ((trends.make_sentiment(0.3),), True),
        ((trends.make_sentiment(None),), False),
        ((trends.make_sentiment(-1),), True),
    )
    sentiment_value_tests = (
        ((trends.make_sentiment(-0.3),), -0.3),
        ((trends.make_sentiment(1),), 1),
        ((trends.make_sentiment(-1),), -1),
    )

    if check_func(trends.has_sentiment, has_sentiment_tests):
        return True
    elif check_func(trends.sentiment_value, sentiment_value_tests):
        return True

@test
def problem4():
    # Change the representation of sentiments to validate abstraction barrier.
    original_make_sentiment = trends.make_sentiment
    original_sentiment_value = trends.sentiment_value
    original_has_sentiment = trends.has_sentiment
    trends.make_sentiment = lambda s: lambda : s
    trends.sentiment_value = lambda s: s()
    trends.has_sentiment = lambda s: s() != None

    sentiment_tests = (
        ((trends.make_tweet('Help, I\'m trapped in an autograder factory and I can\'t get out!'.lower(), None, 0, 0),), -0.416666667),
        ((trends.make_tweet('The thing that I love about hating things that I love is that I hate loving that I hate doing it.'.lower(), None, 0, 0),), 0.075),
    )
    no_sentiment_tests = (
        ((trends.make_tweet('Peter Piper picked a peck of pickled peppers'.lower(), None, 0, 0),), None),
    )

    def analyze(tweet):
        return trends.sentiment_value(trends.analyze_tweet_sentiment(tweet))

    if check_func(analyze, sentiment_tests, comp=comp_float):
        return True
    if check_func(analyze, no_sentiment_tests):
        return True

    trends.make_sentiment = original_make_sentiment
    trends.sentiment_value = original_sentiment_value
    trends.has_sentiment = original_has_sentiment

@test
def problem5():
    if check_doctest('find_centroid', trends):
        return True

    from geo import make_position as mp
    import geo

    def make_tests():
        return (
            ([mp(49, -17), mp(83, -18), mp(-33, -54), mp(27, 82), mp(15, -97),
              mp(10, 97), mp(-37, -68), mp(26, 66), mp(49, -17)], (24.031793687451884, -10.597882986913008, 4330.0)),
            ([mp(-98, 55), mp(84, 27), mp(-81, 4), mp(94, -25), mp(-26, 42), mp(-98, 55)],
              (2.5294117647058822, -27.17647058823529, 1445.0)),
            ([mp(-53, 68), mp(-52, -23), mp(-74, -65), mp(-44, 46), mp(-61, 68), mp(-14, 12), mp(33, 58), mp(-53, 68)],
              (-7.561094365870623, 59.29600432800061, 2156.5)),
            ([mp(60, -90), mp(59.5117046837911, -96.9829483518188), mp(59.3721917363029, -98.9780764523384),
              mp(60.2790258949765, -86.0097437989607), mp(60.4185388424647, -84.014615698441), mp(60, -90)], (60, -90, 0)),
            ([mp(90, 50), mp(88, 46.5358983848623), mp(83.5, 38.7416697508023), mp(86, 43.0717967697245),
              mp(87, 44.8038475772934), mp(84.5, 40.4737205583712), mp(90, 50)], (90, 50, 0)),
        )
    tests = make_tests()

    if check_func(trends.find_centroid, tests, comp=comp_tuple):
        return True

    print("Testing abstraction barriers.")
    try:
        original_geo = trends.make_position, trends.latitude, trends.longitude
        trends.make_position = geo.make_position = lambda lat,long: lambda z: z*lat+(1-z)*long
        trends.latitude      = geo.latitude      = lambda p: p(1)
        trends.longitude     = geo.longitude     = lambda p: p(0)
        mp = geo.make_position
        tests = make_tests()

        if check_func(trends.find_centroid, tests, comp=comp_tuple):
            return True
    finally:
        geo.make_position = trends.make_position = original_geo[0]
        geo.latitude      = trends.latitude      = original_geo[1]
        geo.longitude     = trends.longitude     = original_geo[2]


@test
def problem6():
    if check_doctest('find_state_center', trends):
        return True

    from geo import make_position as mp
    import geo

    def center_as_tuple(state):
        center = trends.find_state_center(state)
        return (geo.latitude(center), geo.longitude(center))

    def make_tests():
        return (
            (([[mp(49, -17), mp(83, -18), mp(-33, -54), mp(27, 82), mp(15, -97),
                mp(10, 97), mp(-37, -68), mp(26, 66), mp(49, -17)],
               [mp(-98, 55), mp(84, 27), mp(-81, 4), mp(94, -25), mp(-26, 42), mp(-98, 55)],
               [mp(60, -90), mp(59.5117046837911, -96.9829483518188), mp(59.3721917363029, -98.9780764523384),
                mp(60.2790258949765, -86.0097437989607), mp(60.4185388424647, -84.014615698441), mp(60, -90)],
              ],), (18.65154401154401, -14.746118326118323)),
            (([[mp(-53, 68), mp(-52, -23), mp(-74, -65), mp(-44, 46), mp(-61, 68), mp(-14, 12), mp(33, 58), mp(-53, 68)],
               [mp(-30, -70), mp(-91, 40), mp(46, -93), mp(-4, -35), mp(29, 28), mp(-30,-70)],
               [mp(90, 50), mp(88, 46.5358983848623), mp(83.5, 38.7416697508023), mp(86, 43.0717967697245),
                mp(87, 44.8038475772934), mp(84.5, 40.4737205583712), mp(90, 50)],
              ],), (-29.056049940231105, 26.2892371718245)),
        )
    tests = make_tests()

    if check_func(center_as_tuple, tests, comp=comp_tuple):
        return True

    print("Testing abstraction barriers.")
    try:
        original_geo = trends.make_position, trends.latitude, trends.longitude
        trends.make_position = geo.make_position = lambda lat,long: lambda z: z*lat+(1-z)*long
        trends.latitude      = geo.latitude      = lambda p: p(1)
        trends.longitude     = geo.longitude     = lambda p: p(0)
        mp = geo.make_position
        tests = make_tests()
        if check_func(center_as_tuple, tests, comp=comp_tuple):
            return True
    finally:
        geo.make_position = trends.make_position = original_geo[0]
        geo.latitude      = trends.latitude      = original_geo[1]
        geo.longitude     = trends.longitude     = original_geo[2]


@test
def problem7():
    def test_groups():
        tweets = pirate_tweets(trends.make_tweet)
        expected = {
          'MI': [tweets[0], tweets[4]],
          'MT': [tweets[1], tweets[5]],
          'ND': [tweets[2], tweets[6]],
          'FL': [tweets[3], tweets[7]],
        }
        tests = ( ((tweets,), expected), )
        if check_func(trends.group_tweets_by_state, tests, comp=comp_group):
            return True

    if test_groups():
        return True
    print("Testing abstraction barriers.")
    try:
        trends.swap_tweet_representation()
        if test_groups():
            return True
    finally:
        trends.swap_tweet_representation()

@test
def problem8():
    def test_average():
        tweets = pirate_tweets(trends.make_tweet) + (
          trends.make_tweet('This tweet is without a sentiment', None, None, None),
          trends.make_tweet('This tweet is also without a sentiment', None, None, None),
        )
        tweets_by_state = {
            'MT': [ tweets[1], tweets[5] ],
            'MI': [ tweets[0], tweets[4] ],
            'FL': [ tweets[3], tweets[7] ],
            'ND': [ tweets[2], tweets[6] ],
            'AA': [ tweets[8], tweets[9] ],
        }
        expected = {
            'MT': -0.08333333333333333,
            'MI': 0.325,
            'FL': 0.5,
            'ND': 0.020833333333333332
        }
        tests = ( ((tweets_by_state,),expected) ,)
        if check_func(trends.average_sentiments, tests, comp=comp_dict):
            return True

    if test_average():
        return True
    print("Testing abstraction barriers.")
    try:
        trends.swap_tweet_representation()
        old = trends.make_sentiment, trends.has_sentiment, trends.sentiment_value
        trends.make_sentiment = lambda s: lambda: s
        trends.has_sentiment = lambda s: s() is not None
        trends.sentiment_value = lambda s: s()
        if test_average():
            return True
    finally:
        trends.swap_tweet_representation()
        trends.make_sentiment, trends.has_sentiment, trends.sentiment_value = old

#############
# UTILITIES #
#############

def comp_float(x, y):
    """Approximate comparison of floats."""
    return abs(x - y) <= 1e-5

def comp_tuple(x, y):
    """Approximate comparison of tuples."""
    if type(x) != type(y):
        try:
            x = tuple(x)
            y = tuple(y)
        except:
            return False
    if len(x) != len(y):
        return False
    for a, b in zip(x, y):
        if not comp_float(a, b):
            return False
    return True

def comp_dict(x, y):
    """Approximate comparison of dictionaries."""
    if type(x) != type(y):
        try:
            x = dict(x)
            y = dict(y)
        except:
            return False
    if len(x) != len(y):
        return False
    for k, v in x.items():
        if k not in y:
            return False
        if not comp_float(v, y[k]):
            return False
    return True

def comp_fn(x, y):
    """Approximate comparison of functional pairs."""
    if type(x) != type(y):
        return False
    for i in [0, 1]:
        if not comp_float(x(i), y(i)):
            return False
    return True

def comp_unordered(x, y):
    """Compare x to y in either order."""
    if type(x) != type(y) or len(x) != len(y):
        return False
    for el in x:
        if el not in y:
            return False
    return True

def comp_group(x, y):
    """Compare tweets grouped by key, ignoring empty lists."""
    if type(x) != type(y):
        try:
            x = dict(x)
            y = dict(y)
        except:
            return False
    for k, v in x.items():
        if v and not comp_unordered(v, y.get(k, [])):
            return False
    for k, v in y.items():
        if v and not comp_unordered(v, x.get(k, [])):
            return False
    return True

def tricky_tweets(make_tweet):
    return (
        make_tweet('Hello, world! !dlrow ,olleH'.lower(),
            datetime.strptime('2010-01-02 01:04:05', '%Y-%m-%d %H:%M:%S'),
            38, -120),
        make_tweet("I mean what person wouldn't? It's John Stamos!".lower(),
            datetime.strptime('2010-01-02 02:04:05', '%Y-%m-%d %H:%M:%S'),
            38, -119),
        make_tweet("Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn".lower(),
            datetime.strptime('2010-01-02 03:04:05', '%Y-%m-%d %H:%M:%S'),
            38, -118),
        make_tweet('kfdafj. afjdsal.jfdlsafj. fjd jksa'.lower(),
            datetime.strptime('2010-01-02 04:04:05', '%Y-%m-%d %H:%M:%S'),
            38, -117),
        make_tweet("/Never/look up.when dragons!fly overhead.".lower(),
            datetime.strptime('2010-01-02 05:04:05', '%Y-%m-%d %H:%M:%S'),
            38, -116),
        make_tweet("Jeepers, what fools these mortals be!".lower(),
            datetime.strptime('2010-01-02 06:04:05', '%Y-%m-%d %H:%M:%S'),
            38, -115),
    )

def pirate_tweets(make_tweet):
    return (
        make_tweet('I am the very model of a modern Major-General'.lower(), None, 43, -84),
        make_tweet('I\'ve information vegetable, animal, and mineral'.lower(), None, 58, -112),
        make_tweet('I know the kings of England, and I quote the fights historical'.lower(), None, 49, -104),
        make_tweet('From Marathon to Waterloo, in order categorical'.lower(), None, 19, -87),
        make_tweet('I\'m very well acquainted, too, with matters mathematical'.lower(), None, 44, -85),
        make_tweet('I understand equations, both the simple and quadratical'.lower(), None, 59, -110),
        make_tweet('About binomial theorem I\'m teeming with a lot o\' news'.lower(), None, 50, -100),
        make_tweet('With many cheerful facts about the square of the hypotenuse'.lower(), None, 15, -87),
    )

##########################
# COMMAND LINE INTERFACE #
##########################

project_info = {
    'name': 'Project 2: Trends',
    'remote_index': 'http://inst.eecs.berkeley.edu/~cs61a/fa13/proj/trends/',
    'autograder_files': [
        'trends_grader.py',
        'autograder.py',
    ],
    'version': __version__,
}

@main
def run(*args):
    run_tests(**project_info)
