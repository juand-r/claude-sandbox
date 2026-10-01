"""Generic lane graph: markers of arbitrary (slow) types crossed by
Ebar-speed movers from the right, catalog-level prediction.

markers: list of (type, seed) front (rightmost) first. A crossing is clean
if the marker survives (exactly one product of its type) and every other
product is Ebar-speed (moves on to the next marker)."""
import os, sys
import lane  # noqa: F401  (paths)
from predict import predict, LIB
from collide import canonical_reps
from r110lib import class_key
from fractions import Fraction

EB = Fraction(-4, 15)
EBAR_SPEED = {n for n, g in LIB.gliders.items() if g.p and g.velocity == EB}


def lateral(p):
    g = LIB.gliders[p[0]]
    return p[2] - g.velocity * p[1]


ABSORB = False   # allow a marker to swallow a mover completely


def cross(mtype, seed, mover):
    name, t, x = mover
    try:
        k, prods = predict(mtype, name, (t - seed[0], x - seed[1]), eX=seed)
    except (ValueError, KeyError, AssertionError):
        return None
    ms = [p for p in prods if p[0] == mtype]
    rest = [p for p in prods if p[0] != mtype]
    if len(ms) != 1 or (not rest and not ABSORB) or not all(p[0] in EBAR_SPEED for p in rest):
        return None
    return (ms[0][1], ms[0][2]), rest


def cross_chain(mtypes, seeds, mv):
    r = cross(mtypes[0], seeds[0], mv)
    if r is None:
        return None
    new, outs = [r[0]], r[1]
    for ty, m in zip(mtypes[1:], seeds[1:]):
        nxt = []
        for o in sorted(outs, key=lateral):
            rr = cross(ty, m, o)
            if rr is None:
                return None
            m = rr[0]
            nxt += rr[1]
        new.append(m)
        outs = nxt
    return new, outs


def movers(mtype):
    import json
    rows = json.load(open(os.path.join(lane.COLL, "collisions.json")))
    packs = sorted({r["Y"] for r in rows if r["X"] == mtype and r["Y"] in EBAR_SPEED})
    out = []
    for name in packs:
        for rep in canonical_reps(LIB, mtype, name):
            out.append((name,) + tuple(rep))
    return out
