"""This module implements a declarative Logic language using Scheme syntax.

Logic is a variant of the Prolog language, based on scmlog by Paul Hilfinger
and the logic programming example in SICP.

All valid logic expressions are Scheme lists.  Valid forms include:

(fact ...):  Assert a consequent, followed by zero or more hypotheses
(query ...): Query zero or more relations simultaneously
(load PATH): Load a .logic file by evaluating its expressions
"""

from scheme import Frame
from scheme_reader import Pair, nil, read_line
from scheme_primitives import *
from ucb import main, trace

import scheme
import scheme_reader
import scheme_test

facts = []

#############
# Inference #
#############

def do_query(clauses):
    """Yield all bindings that simultaneously satisfy clauses."""
    for env in search(clauses, Frame(None), 0):
        yield [(v, ground(v, env)) for v in get_vars(clauses)]

DEPTH_LIMIT = 20
def search(clauses, env, depth):
    """Search for an application of rules to establish all the clauses,
    non-destructively extending the unifier env.  Limit the search to
    the nested application of depth rules."""
    if clauses is nil:
        yield env
    elif DEPTH_LIMIT is None or depth <= DEPTH_LIMIT:
        for fact in facts:
            fact = rename_variables(fact, get_unique_id())
            env_head = Frame(env)
            if unify(fact.first, clauses.first, env_head):
                for env_rule in search(fact.second, env_head, depth+1):
                    for result in search(clauses.second, env_rule, depth+1):
                        yield result

def unify(e, f, env):
    """Destructively extend env so as to unify (make equal) e and f, returning
    True if this succeeds and False otherwise.  env may be modified in either
    case (its existing bindings are never changed)."""
    e = lookup(e, env)
    f = lookup(f, env)
    if e == f:
        return True
    elif isvar(e):
        env.define(e, f)
        return True
    elif isvar(f):
        env.define(f, e)
        return True
    elif scheme_atomp(e) or scheme_atomp(f):
        return False
    else:
        return unify(e.first, f.first, env) and unify(e.second, f.second, env)

################
# Environments #
################

def lookup(sym, env):
    """Look up a symbol repeatedly until it is fully resolved."""
    try:
        return lookup(env.lookup(sym), env)
    except:
        return sym

def ground(expr, env):
    """Replace all variables with their values in expr."""
    if scheme_symbolp(expr):
        resolved = lookup(expr, env)
        if expr != resolved:
            return ground(resolved, env)
        else:
            return expr
    elif scheme_pairp(expr):
        return Pair(ground(expr.first, env), ground(expr.second, env))
    else:
        return expr

def get_vars(expr):
    """Return all logical vars in expr as a list."""
    if isvar(expr):
        return [expr]
    elif scheme_pairp(expr):
        vs = get_vars(expr.first)
        for v in get_vars(expr.second):
            if v not in vs:
                vs.append(v)
        return vs
    else:
        return []

IDENTIFIER = 0
def get_unique_id():
    """Return a unique identifier."""
    global IDENTIFIER
    IDENTIFIER += 1
    return IDENTIFIER

def rename_variables(expr, n):
    """Rename all variables in expr with an identifier N."""
    if isvar(expr):
        return expr + '_' + str(n)
    elif scheme_pairp(expr):
        return Pair(rename_variables(expr.first, n),
                    rename_variables(expr.second, n))
    else:
        return expr

def isvar(symbol):
    """Return whether symbol is a logical variable."""
    return scheme_symbolp(symbol) and symbol.startswith("?")

##################
# User Interface #
##################

def process_input(expr, env):
    """Process an input expr, which may be a fact or query."""
    if expr == 'exit':
        print("Goodbye")
        sys.exit(0)

    if not scheme_listp(expr):
        print('Improperly formed expression.')
    elif expr.first in ("fact", "!"):
        facts.append(expr.second)
    elif expr.first in ("query", "?"):
        results = do_query(expr.second)
        success = False
        for result in results:
            if not success:
                print('Success!')
            success = True
            output = "\t".join("{0}: {1}".format(k[1:], v) for k, v in result)
            if output:
                print(output)
        if not success:
            print('Failed.')
    elif expr.first == "load":
        scheme.scheme_load(expr.second.first, env)
    else:
        print("Please provide a fact or query.")

@main
def run(*argv):
    scheme_reader.buffer_input.__defaults__ = ('logic> ',)
    scheme_reader.buffer_lines.__defaults__ = ('logic> ', False)
    scheme.scheme_eval = process_input
    if len(argv) == 2 and argv[0] == '-t':
        scheme_test.run_tests(argv[1])
    else:
        scheme.run(*argv)
