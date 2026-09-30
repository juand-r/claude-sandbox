"""Predict the products of any X-Y collision at any relative event from the
catalog, without simulating.

If Y's seed event relative to X is r and the catalog representative of
r's class is rep, then r - rep = a*P_X + b*P_Y for integers a, b, and the
configuration (X at 0, Y at r) is the catalog configuration translated by
a*P_X (Y's trajectory is unchanged by b*P_Y). So the products are the
catalog products translated by a*P_X. Events are normalized to
0 <= t0 < p.
"""

import json
from collections import defaultdict
from fractions import Fraction

from collide import canonical_reps
from library import Library
from r110lib import class_key

LIB = Library.load()
_BY = None


def _by():
    global _BY
    if _BY is None:
        _BY = defaultdict(dict)
        for r in json.load(open("collisions.json")):
            _BY[(r["X"], r["Y"])][r["cls"]] = r
    return _BY


def norm(name, t, x):
    g = LIB.gliders[name]
    t2 = t % g.p
    return (name, t2, x - (t - t2) // g.p * g.d)


def predict(X, Y, r, eX=(0, 0)):
    """Products (normalized events, absolute coordinates) when X is seeded
    at eX and Y at eX + r. Raises if r is not ether-compatible or the pair
    is not in the catalog."""
    gx, gy = LIB.gliders[X], LIB.gliders[Y]
    PX, PY = (gx.p, gx.d), (gy.p, gy.d)
    reps = canonical_reps(LIB, X, Y)
    key = class_key(r, PX, PY)
    keys = [class_key(q, PX, PY) for q in reps]
    if key not in keys:
        raise ValueError(f"relative event {r} is not ether-compatible")
    k = keys.index(key)
    rep = reps[k]
    d = (r[0] - rep[0], r[1] - rep[1])
    det = PX[0] * PY[1] - PX[1] * PY[0]
    a = Fraction(d[0] * PY[1] - d[1] * PY[0], det)
    b = Fraction(PX[0] * d[1] - PX[1] * d[0], det)
    if a.denominator != 1 or b.denominator != 1:
        raise AssertionError("class key equal but not in lattice")
    a = int(a)
    row = _by()[(X, Y)][k]
    if list(row["Y_event"]) != list(rep):
        raise AssertionError("catalog representative mismatch")
    sh = (eX[0] + a * PX[0], eX[1] + a * PX[1])
    return k, sorted(norm(n, t + sh[0], x + sh[1]) for n, t, x in row["products"])
