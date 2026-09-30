"""Pairwise glider collisions: enumerate every distinct collision, simulate
it to completion, and record the products exactly.

Geometry. Glider X's seed event is fixed at (t, x) = (0, 0); glider Y's
seed event is r = (tY, xY). Two placements give the same collision (up to
spacetime translation) iff their r differ by an element of the lattice
M = <P_X, P_Y> spanned by the two period vectors; r must also make the
ether between them consistent. Hence there are |det(P_X, P_Y)| / 14
distinct collisions (r110lib.n_classes); the enumeration below checks that
it finds exactly that many classes. For each class the canonical
representative is the one with the smallest initial gap >= GAP (then the
smallest -tY).

Products. Each product is (name, t0, x0): a library glider whose seed
event is (t0, x0) with 0 <= t0 < p (r110lib conventions), in the same
coordinates as the inputs. A collision is *settled* when every object is
a library glider (unknown periodic objects are auto-registered after
standalone verification) and left-to-right velocities are non-decreasing,
so no further interaction is possible.
"""

import math
import sys

import numpy as np

from r110lib import (TILE, build_row, class_key, evolve_batch, n_classes,
                     obj_key, objects, _pack_batch, _unpack_batch, _step_state)

GAP = 40          # minimum ether cells between the inputs at time 0
CHUNK = 100       # generations between settle checks
EXTRA = 2500      # generations allowed after the nominal meeting time
EDGE = 30         # objects this close to a row end mean the row is too small


def canonical_reps(lib, X, Y, gap=GAP):
    """-> list of (tY, xY) canonical representatives, one per class."""
    gx, gy = lib.gliders[X], lib.gliders[Y]
    if not gx.velocity > gy.velocity:
        raise ValueError(f"{X} (v={gx.velocity}) must be faster than "
                         f"{Y} (v={gy.velocity}) to catch it from the left")
    PX, PY = (gx.p, gx.d), (gy.p, gy.d)
    n = n_classes(PX, PY)
    bx, lx, rx, sx = gx.state_at(0, 0, 0)
    endx = sx + len(bx)
    reps = {}
    for j in range(n + 2):
        for tY in range(0, -gy.p, -1):
            by, ly, ry, s_rel = gy.state_at(tY, 0, 0)
            # ether match: (rx - 0) == (ly - (xY + s_rel)) mod 14
            base = (ly - s_rel - rx) % TILE
            xmin = endx + gap - s_rel
            xY = xmin + (base - xmin) % TILE + TILE * j
            key = class_key((tY, xY), PX, PY)
            if key not in reps:
                reps[key] = (tY, xY)
        if len(reps) == n:
            break
    if len(reps) != n:
        raise AssertionError(f"{X}-{Y}: found {len(reps)} classes, "
                             f"expected {n}")
    return [reps[k] for k in sorted(reps, key=lambda k: reps[k][::-1])]


def products_of(lib, row, x0, T, auto=True):
    """Identify all objects of a row. -> (settled, products, raw) where
    products = [(name, t0, x0g)] left to right, raw = object list."""
    W = len(row)
    objs = objects(row)
    if objs and (objs[0][0] < EDGE or objs[-1][1] > W - EDGE):
        raise RuntimeError("object near the row edge: row too small")
    prods = []
    ok = True
    for a, b, cl, cr in objs:
        key = obj_key(row, a, b, cl, cr)
        hit = lib.identify(key, auto=auto)
        if hit is None:
            ok = False
            prods.append(("?", None, x0 + a))
            continue
        name, k = hit
        g = lib.gliders[name]
        s = x0 + a
        t0 = (T - k) % g.p
        m = (T - t0 - k) // g.p
        prods.append((name, t0, s - g.phases[k][3] - m * g.d))
    if ok:
        vs = [lib.gliders[n].velocity for n, _, _ in prods]
        ok = all(v1 <= v2 for v1, v2 in zip(vs, vs[1:]))
    return ok, prods, objs


def simulate(lib, placements, T_max, auto=True, pad=None):
    """Simulate glider placements [(name, t0, x0)] from time 0 until
    settled or T_max. -> dict(settled, T, products)."""
    gl = lib.gliders
    states = [gl[n].state_at(t0, x0, 0) for n, t0, x0 in placements]
    vmax = 1.0
    pad = pad or int(vmax * T_max) + 100
    row, x0 = build_row(states, pad=pad)
    s = _pack_batch(row[None, :])
    T = 0
    while T < T_max:
        for _ in range(CHUNK):
            s = _step_state(s)
        T += CHUNK
        cur = _unpack_batch(s, 1)[0]
        ok, prods, _ = products_of(lib, cur, x0, T, auto=auto)
        if ok:
            return {"settled": True, "T": T, "products": prods}
    return {"settled": False, "T": T, "products": prods}


def meet_time(lib, X, Y, rep):
    gx, gy = lib.gliders[X], lib.gliders[Y]
    dv = float(gx.velocity - gy.velocity)
    by, ly, ry, sy = gy.state_at(rep[0], rep[1], 0)
    return int(sy / dv) + 1


def collide_pair(lib, X, Y):
    """All distinct collisions of X (left, faster) with Y. -> list of dicts."""
    out = []
    for i, rep in enumerate(canonical_reps(lib, X, Y)):
        tm = meet_time(lib, X, Y, rep)
        res = simulate(lib, [(X, 0, 0), (Y, rep[0], rep[1])], tm + EXTRA)
        res.update({"X": X, "Y": Y, "cls": i, "Y_event": list(rep)})
        out.append(res)
    return out


def describe(res):
    names = [p[0] for p in res["products"]]
    tag = "" if res["settled"] else " (UNSETTLED)"
    return f"{res['X']}+{res['Y']}#{res['cls']} -> {' '.join(names) or '(nothing)'}{tag}"


if __name__ == "__main__":
    from library import Library
    lib = Library.load()
    X, Y = sys.argv[1], sys.argv[2]
    for r in collide_pair(lib, X, Y):
        print(describe(r), "T=", r["T"], r["products"])
