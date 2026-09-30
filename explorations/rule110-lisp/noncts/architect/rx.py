"""Reaction experiments on top of collider's library (read-only import).

Gliders are placed by seed events (name, t0, x0) in collider's convention
(r110lib docstring): phase 0 at time t0 with bits[0] at column x0.
`run` simulates from time 0 and returns the settled product list
[(name, t0, x0)] (same coordinates), or raises if not settled.
"""
import sys
sys.path.insert(0, "../collider")
from library import Library
from collide import simulate, collide_pair, canonical_reps
from r110lib import build_row, evolve_hist, objects, obj_key, TILE

LIB = Library.load()
G = LIB.gliders


def run(placements, T, must_settle=True):
    res = simulate(LIB, placements, T)
    if must_settle and not res["settled"]:
        raise RuntimeError(f"not settled by T={T}: {res['products']}")
    return res["products"]


def rep(X, Y, cls):
    """Seed event of Y (X at (0,0)) for collision class cls of collider's
    enumeration (X left, faster)."""
    return canonical_reps(LIB, X, Y)[cls]


def norm(name, t0, x0):
    """Canonical seed of a glider: t0 in [0, p)."""
    g = G[name]
    q, r = divmod(t0, g.p)
    return (name, r, x0 - q * g.d)


def history(placements, T, pad=None):
    """(hist, x0): full spacetime of the placements for T steps."""
    states = [G[n].state_at(t0, x0, 0) for n, t0, x0 in placements]
    row, xo = build_row(states, pad=pad or T + 100)
    return evolve_hist(row, T), xo


def abs_right_phase(name, t0, x0, t=0):
    """Absolute ether phase (collider convention) right of the glider at t."""
    bits, lph, rph, s = G[name].state_at(t0, x0, t)
    return (rph - s) % TILE


def abs_left_phase(name, t0, x0, t=0):
    bits, lph, rph, s = G[name].state_at(t0, x0, t)
    return (lph - s) % TILE


def span0(name, t0, x0, t=0):
    bits, lph, rph, s = G[name].state_at(t0, x0, t)
    return s, s + len(bits)


def place_after(prev, name, t0, gap):
    """Seed (name, t0, x0) with the smallest x0 such that the glider starts
    >= `gap` cells right of glider `prev` at time 0, ether-consistently."""
    c = abs_right_phase(*prev)
    end = span0(*prev)[1]
    x = end + gap - span0(name, t0, 0)[0]
    while abs_left_phase(name, t0, x) != c:
        x += 1
    return (name, t0, x)


def chain(first, rest):
    """first = (name, t0, x0); rest = [(name, t0, gap), ...] placed left to
    right with place_after. -> list of seeds."""
    out = [first]
    for name, t0, gap in rest:
        out.append(place_after(out[-1], name, t0, gap))
    return out


from r110lib import class_key as _class_key


def cls_of(X, xseed, Y, yseed):
    """Collision class index (collider's enumeration order) of glider Y at
    seed yseed relative to X at xseed (X on the left). None if the pair
    is not in the enumerator's form."""
    gx, gy = G[X], G[Y]
    PX, PY = (gx.p, gx.d), (gy.p, gy.d)
    r = (yseed[0] - xseed[0], yseed[1] - xseed[1])
    k = _class_key(r, PX, PY)
    reps = canonical_reps(LIB, X, Y)
    for i, rp in enumerate(reps):
        if _class_key(rp, PX, PY) == k:
            return i
    raise AssertionError("class not found")
