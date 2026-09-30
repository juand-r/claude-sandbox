"""Classify counter reactions E^n + P into clean behaviours.

For a product list (left to right) of E^n + P:
  - exactly one E-chain object E^m;
  - objects to its LEFT must move left at least as fast as... strictly faster
    than E (-4/15): they escape to -infinity ("left garbage", free);
  - objects to its RIGHT must be right-movers (answers into the stream).
Returns (delta, left_names, right_names) or None (debris).
"""
from fractions import Fraction as F
import re
from common import LIB, CHAIN

VE = F(-4, 15)


def velocity(name):
    if name in LIB.gliders:
        return LIB.gliders[name].velocity
    m = re.match(r"v(-?\d+)/(\d+)s", name)
    if m:
        return F(int(m.group(1)), int(m.group(2)))
    # auto names like 'Bbar_17_B' : compound of base gliders; use first part
    base = re.split(r"[_@]", name)[0]
    return LIB.gliders[base].velocity


def classify(ps, n):
    if "?" in ps:
        return None            # unidentified object = debris
    idx = [i for i, p in enumerate(ps) if p in CHAIN]
    if len(idx) != 1:
        return None
    i = idx[0]
    left, right = ps[:i], ps[i + 1:]
    if any(velocity(p) >= VE for p in left):
        return None
    if any(velocity(p) <= VE for p in right):
        return None
    return CHAIN.index(ps[i]) + 1 - n, tuple(left), tuple(right)
