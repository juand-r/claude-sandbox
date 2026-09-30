"""Collisions that have a single class (|det(P_X,P_Y)|/14 == 1): outcome
must be independent of phases. X is on the left, Y on the right.
Prints the outcome types for every phase combination (should be one set)."""
from collections import defaultdict
import r110check as r

PAIRS = [("A", "C1"), ("A", "C2"), ("A", "C3"), ("A", "D1"), ("A", "D2"),
         ("C1", "B"), ("C2", "B"), ("C3", "B"), ("A", "B"),
         ("D1", "B"), ("D2", "B")]

def phases(p):
    return [k for k in r.PHASES if k.startswith(p + "(")]

for xp, yp in PAIRS:
    res = defaultdict(int)
    for x in phases(xp):
        for y in phases(yp):
            e, l, _ = r.outcome(f"{x}-7e-{y}", T=1200, pad=260)
            res[tuple(sorted(l)) + (() if e == l else ("UNSETTLED",))] += 1
    print(f"{xp} + {yp}:", dict(res))
