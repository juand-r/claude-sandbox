"""delayline toolkit: imports round-3 coupler's cl/two (read-only) and adds
helpers for window (zero-rod) experiments."""
import sys, os
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
COUP = os.path.abspath(os.path.join(HERE, "..", "..", "round3", "coupler"))
sys.path.insert(0, COUP)
from two import *  # noqa  (cl.*, rafast Program, left_stream, ...)
HERE = os.path.dirname(os.path.abspath(__file__))  # re-set: two/cl export their own HERE
assert HERE.endswith("round4/delayline"), HERE


def lat(g):
    """trajectory intercept x - v t of glider event g=(name,t0,x0)"""
    from fractions import Fraction
    G_ = LIB.gliders[g[0]]
    return Fraction(g[2]) - G_.velocity * g[1]


def chain_items(state):
    return sorted([g for g in state if g[0] in CHAIN], key=lambda g: pos(g, 0))
