"""Automatic grading script for the Hog project.

Expects the following files in the current directory:

hog.py
dice.py
ucb.py
autograder.py

This file uses features of Python not yet covered in the course.
"""

__version__ = '2.2'

from autograder import test, run_tests, check_func, check_doctest, test_eval, run_tests

try:
    import hog      # Student submission
except (SyntaxError, IndentationError) as e:
    import traceback
    print('Unfortunately, the autograder cannot run because ' +
          'your program contains a syntax error:')
    traceback.print_exc(limit=1)
    exit(1)

from dice import make_test_dice, four_sided, six_sided
from ucb import main

#########
# TESTS #
#########

@test
def problem1(grades):
    """Test roll_dice."""
    counted_dice = make_test_dice(4, 1, 2)
    test_suite1 = [((2, make_test_dice(4, 6, 1)),           10),
                   ((3, make_test_dice(4, 6, 1)),            1),
                   ((3, make_test_dice(1, 2, 3)),            1),
                   ((3, counted_dice),                       1),
                   ((1, counted_dice),                       4)]
    test_suite2 = [((5, make_test_dice(4, 2, 3, 3, 4, 1)),  16),
                   ((2, make_test_dice(1)),                  1)]

    if check_func(hog.roll_dice, test_suite1):
        return True
    if check_func(hog.roll_dice, test_suite2):
        return True

@test
def problem2(grades):
    """Test take_turn."""
    test_suite1 = [((2,  0, make_test_dice(4, 6, 1)), 10),
                   ((3, 20, make_test_dice(4, 6, 1)),  1),
                   ((2,  0, make_test_dice(6)),       12),
                   ((0, 34),                           5),# Free bacon
                   ((0, 71),                           8),
                   ((0,  7),                           8)]
    test_suite2 = [((0, 99),                          10),
                   ((0,  0),                           1),
                   ((0,  50),                          6)]
    if check_func(hog.take_turn, test_suite1):
        return True
    if check_func(hog.take_turn, test_suite2):
        return True

@test
def problem3(grades):
    """Test select_dice."""
    return check_doctest('select_dice', hog)


@test
def problem4(grades):
    """Test play using fixed dice."""
    always = hog.always_roll
    hog.four_sided = make_test_dice(1)
    hog.six_sided = make_test_dice(3)

    test_suite = [((always(5),  always(5)), (92, 106)),
                  ((always(2),  always(2)), (17, 102)),
                  ((always(2), always(10)), (19, 120)),
                  ((always(0),  always(0)), (91, 103)), # always roll 0
                  ((always(0),  always(2)), (106, 56))]

    try:
        failure = False
        if check_func(hog.play, test_suite):
            failure = True
    finally:
        # Revert dice
        hog.four_sided = four_sided
        hog.six_sided = six_sided
    print('Note: Not all tests have been released for problem4.',
          'Submit your project to the actual autograder to get more results!',
          sep='\n', end='\n')
    return failure


@test
def problem5(grades):
    """Test make_averaged."""
    # hundred_dice cycle from 1 to 99 repeatedly
    hundred_range = range(1, 100)
    hundred_dice = make_test_dice(*hundred_range)
    averaged_hundred_dice = test_eval(hog.make_averaged,
                                      (hundred_dice, 5 * len(hundred_range)))
    correct_average = sum(range(1, 100)) / len(hundred_range)

    test_suite = [((), correct_average)] * 2

    if check_doctest('make_averaged', hog):
        return True
    if check_func(averaged_hundred_dice, test_suite):
        return True

@test
def problem6(grades):
    """Test max_scoring_num_rolls."""
    return check_doctest('max_scoring_num_rolls', hog)

@test
def problem7(grades):
    """Test bacon_strategy."""
    if check_doctest('bacon_strategy', hog):
        return True
    old_bacon = hog.BACON_MARGIN, hog.BASELINE_NUM_ROLLS
    hog.BACON_MARGIN, hog.BASELINE_NUM_ROLLS = 5, 4
    test_suite = [((32, 34), 0),
                  ((20, 23), 4),
                  ((20, 4),  0),
                  ((20, 99), 0)]
    failed = check_func(hog.bacon_strategy, test_suite)
    hog.BACON_MARGIN, hog.BASELINE_NUM_ROLLS = old_bacon
    return failed

@test
def problem8(grades):
    """Test swap_strategy."""
    if check_doctest('swap_strategy', hog):
        return True
    old_bacon = hog.BACON_MARGIN, hog.BASELINE_NUM_ROLLS
    hog.BACON_MARGIN, hog.BASELINE_NUM_ROLLS = 5, 4
    test_suite = [((12, 34), 0),    # beneficial swap
                  ((8, 9),   4),    # harmful swap
                  ((32, 43), 0),    # lots of free bacon
                  ((20, 32), 4)]    # baseline
    failed = check_func(hog.swap_strategy, test_suite)
    hog.BACON_MARGIN, hog.BASELINE_NUM_ROLLS = old_bacon
    return failed


@test
def problem9(grades):
    """Test final_strategy."""
    print('Note: Tests for problem9 are not included here.',
          'Submit your project to the actual autograder to get results!',
          sep='\n', end='\n')


##########################
# COMMAND LINE INTERFACE #
##########################

project_info = {
    'name': 'Project 1: Hog',
    'remote_index': 'http://inst.eecs.berkeley.edu/~cs61a/fa13/proj/hog/',
    'autograder_files': [
        'hog_grader.py',
        'autograder.py',
    ],
    'version': __version__,
}

@main
def run(*args):
    run_tests(**project_info)
