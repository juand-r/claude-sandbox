"""pairscan.py - all collision classes of two objects, my builder + my typer.

X (left) and Y (right) are placed with my builder at events (0, 0) and
(t, x0 + dx) for t over one period of Y and a few x shifts. Each placement's
class is the fractional part of the relative event in the basis of the two
period vectors (two placements are the same class iff their relative events
differ by an integer combination of P_X and P_Y). Every class must give one
outcome at every placement (asserted: a test that can fail).

classes(X, Y, x0, T) -> {class_key: (product names, positions of X-like
survivors relative to the X-alone run)}"""
from fractions import Fraction

import hrun

vlib = hrun.vlib


def cls_key(PX, PY, dt, dx):
    (p1, d1), (p2, d2) = PX, PY
    det = p1 * d2 - d1 * p2
    a = Fraction(dt * d2 - dx * p2, det)
    b = Fraction(p1 * dx - d1 * dt, det)
    return (a % 1, b % 1)


def run_items(items, T, pad=400):
    row, org, placed = vlib.build(items, pad=pad)
    h = hrun.HRun(row, org)
    h.goto(T)
    objs = h.objects(org - T - pad, org + len(row) + T + pad)
    return objs, placed


def classes(X, Y, x0, T, xshifts=(0, 14, 28), n_expected=None):
    G1, G2 = vlib.LIB[X], vlib.LIB[Y]
    PX, PY = (G1.P, G1.D), (G2.P, G2.D)
    out = {}
    for t in range(G2.P):
        for dx in xshifts:
            objs, placed = run_items([(X, 0, 0), (Y, t, x0 + dx)], T)
            (_, tx, xx), (_, ty, xy) = placed
            k = cls_key(PX, PY, ty - tx, xy - xx)
            res = tuple((n, x) for n, x, w in objs)
            names = tuple(n.split("@")[0] for n, x in res)
            if k in out:
                assert out[k][0] == names, (X, Y, k, out[k][0], names)
            else:
                out[k] = (names, res, placed)
    if n_expected is not None:
        assert len(out) == n_expected, (len(out), n_expected)
    return out
