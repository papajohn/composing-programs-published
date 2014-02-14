#!/usr/bin/env python3
"""The mr module is an interface to the Hadoop MapReduce streaming API."""

import inspect
import os
import sys

# Interface for defining mappers and reducers

def parse_key_value_pair(line):
    """Return a key-value pair encoded as a line of text."""
    if line[-1] == '\n':
        line = line[:-1]
    return tuple(eval(s) for s in line.split('\t', 1))

def emit(key, value, check_repr=False):
    """Emit a key-value pair as a line of text.  For this key-value pair to be
    successfully read later, both key and value must have valid repr strings.
    """
    if check_repr:
        assert eval(repr(key)) == key, 'No valid repr for key'
        assert eval(repr(value)) == value, 'No valid repr for value'
    print(repr(key) + '\t' + repr(value))

def values_by_key(line_iterator):
    """Return an iterator over key-(iterator over values) pairs."""
    buffer = KeyValueBuffer(line_iterator)
    while not buffer.done():
        key = buffer.peek()[0]
        yield key, values_for_key(key, buffer)

def get_file():
    """Return the name of the current file from which a mapper is reading."""
    filepath = os.environ.get('map_input_file', 'stdin')
    filename = os.path.split(filepath)[-1]
    return filename


# Helper functions/classes for the interface

class KeyValueBuffer(object):
    """A buffer that allows look-ahead in an iterator of key-value pairs."""
    def __init__(self, line_iterator):
        self._iterator = line_iterator
        self._done = False
        self._advance()

    def _advance(self):
        try:
            self._next = parse_key_value_pair(next(self._iterator))
        except StopIteration:
            self._done = True

    def done(self):
        """Return whether the underlying iterator is exhausted."""
        return self._done

    def peek(self):
        """Return the next key-value pair, but do not advance."""
        assert not self._done, 'No next element'
        return self._next

    def next(self):
        """Return the next key-value pair and advance."""
        assert not self._done, 'No next element'
        result = self._next
        self._advance()
        return result

def values_for_key(key, buffer):
    """Yield the values associated with the given key."""
    while not buffer.done() and buffer.peek()[0] == key:
        yield buffer.next()[1]


# Invoking Hadoop

HADOOP_HOME = '/opt/local/share/java/hadoop-1.1.1'
STREAMING = HADOOP_HOME + '/contrib/streaming/hadoop-streaming-1.1.1.jar'
HADOOP_BIN = HADOOP_HOME + '/bin/hadoop'
OUTPUT_BASE = 'output'

commands = {}

def command(fn):
    """A decorator for command-line commands."""
    commands[fn.__name__] = fn
    return fn

def main(fn):
    """Call fn with command line arguments.  Used as a decorator.

    The main decorator marks the function that starts a program. For example,

    @main
    def my_run_function():
        # function body

    Use this instead of the typical __name__ == "__main__" predicate.
    """
    if inspect.stack()[1][0].f_locals['__name__'] == '__main__':
        args = sys.argv[1:] # Discard the script name from command line
        fn(*args) # Call the main function
    return fn

def execute(cmd, testing=False):
    """Execute a shell command."""
    print('Executing: ' + cmd, file=sys.stderr)
    if not testing:
        os.system(cmd)
    print('Completed: ' + cmd, file=sys.stderr)

@command
def ls():
    """List contents of all output directories."""
    cmd = '{0} dfs -ls {1}/*'.format(HADOOP_BIN, OUTPUT_BASE)
    execute(cmd)

@command
def rm(output_dir):
    """Remove an output directory."""
    assert '..' not in output_dir, 'Please do not remove other\' directories'
    cmd = '{0} dfs -rmr {1}/{2}'.format(HADOOP_BIN, OUTPUT_BASE, output_dir)
    execute(cmd)

@command
def cat(output_dir):
    """Print the contents of all files in output_dir."""
    cmd = '{0} dfs -cat {1}/{2}/*'.format(HADOOP_BIN, OUTPUT_BASE, output_dir)
    execute(cmd)

@command
def run(mapper, reducer, input_dir, output_dir):
    """Run a MapReduction."""

    # Check inputs
    assert mapper.endswith('.py'), 'Mapper must be a Python script.'
    assert reducer.endswith('.py'), 'Reducer must be a Python script.'
    assert '/' not in mapper, 'Mapper must be in the current directory.'
    assert '/' not in reducer, 'Reducer must be in the current directory.'

    # Construct shell command
    cmd = '{0} jar {1}'.format(HADOOP_BIN, STREAMING)
    cmd += ' -mapper {0}'.format(os.path.abspath(mapper))
    cmd += ' -reducer {0}'.format(os.path.abspath(reducer))
    cmd += ' -input {0}'.format(input_dir)
    cmd += ' -output {0}/{1}'.format(OUTPUT_BASE, output_dir)

    # Include all local Python files
    for f in os.listdir('.'):
        if f.endswith('.py'):
            cmd += ' -file {0}'.format(os.path.abspath(f))

    execute(cmd)

def formal_parameters(fn):
    """Return the formal parameters of a function."""
    return fn.__code__.co_varnames[:fn.__code__.co_argcount]

@main
def dispatch(cmd=None, *args):
    """Dispatch on the first command line argument."""
    src = sys.argv[0]
    if cmd not in commands:
        print('Usage: python3 {0} COMMAND [ARGS]'.format(src))
        print('COMMAND [ARGS] options:')
        for name, fn in sorted(commands.items()):
            s = '  {0} {1:' + str(40-len(name)) + '}- {2}'
            args = ' '.join([p.upper() for p in formal_parameters(fn)])
            print(s.format(name, args, fn.__doc__))
        sys.exit(1)

    fn = commands[cmd]
    params = formal_parameters(fn)
    if len(args) != len(params):
        args = ' '.join([p.upper() for p in params])
        print('Usage: python3 {0} {1} {2}'.format(src, cmd, args))
        sys.exit(1)

    arg_string = ', '.join([repr(a) for a in args])
    print('Calling {0}({1})'.format(cmd, arg_string), file=sys.stderr)
    fn(*args)
