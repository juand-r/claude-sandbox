"""Collision classes, computed exactly.

For each glider phase string we find an anchor: the first time t (< period)
and column offset x at which the glider, evolved alone, shows its family's
canonical phase string. Two gliders X, Y in a configuration then have a
relative anchor vector r = anchor_Y - anchor_X (in spacetime, taking the
concatenation offsets into account). The collision class is r modulo the
lattice spanned by the two period vectors P_X, P_Y (reduced by Hermite
normal form). Theory: the number of classes is |det(P_X, P_Y)| / 14 and
the outcome is a function of the class.
"""
import numpy as np
import r110check as r
from engine import ETHER, parse

CANON = {}   # family -> canonical phase name
for k in r.PHASES:
    fam = k.split("(")[0]
    if fam not in CANON and fam not in ("e", "Gun"):
        CANON[fam] = k
PERIOD = {"A": (3, 2), "B": (4, -2), "B-": (12, -6), "B^": (12, -6),
          "C1": (7, 0), "C2": (7, 0), "C3": (7, 0), "D1": (10, 2),
          "D2": (10, 2), "E": (15, -4), "E-": (30, -8), "F": (36, -4),
          "G": (42, -14), "H": (92, -18)}


def anchor(name):
    fam = name.split("(")[0]
    canon = parse(ETHER * 2 + r.PHASES[CANON[fam]] + ETHER * 2)
    pad = 30
    row = parse(ETHER * pad + r.PHASES[name] + ETHER * pad)
    p = PERIOD[fam][0]
    h = r.evolve(row, p + 1)
    c0 = 14 * pad
    for t in range(p):
        for x in range(c0 - 100, c0 + 100):
            if np.array_equal(h[t, x:x + len(canon)], canon):
                return t, x + 28 - c0
    raise ValueError(f"no anchor for {name}")


def reduce_mod(v, P, Q):
    """Canonical representative of integer vector v modulo lattice <P, Q>."""
    M = np.array([P, Q], dtype=object).T          # columns P, Q
    det = M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]
    # coordinates of v in basis (P, Q), times det -> integers
    a = (v[0] * M[1, 1] - v[1] * M[0, 1])
    b = (-v[0] * M[1, 0] + v[1] * M[0, 0])
    # fractional parts (mod det) identify the class
    return (a % abs(det), b % abs(det))


def cls(spec_x, n, spec_y):
    """Class of configuration  X-ne-Y  ."""
    fx, fy = spec_x.split("(")[0], spec_y.split("(")[0]
    tx, xx = anchor(spec_x)
    ty, xy = anchor(spec_y)
    off = len(r.PHASES[spec_x]) + 14 * n          # column where Y starts
    # anchors at different times: move both to a common reference by
    # expressing r = (ty - tx, off + xy - xx) (a spacetime vector)
    v = (ty - tx, off + xy - xx)
    return reduce_mod(v, PERIOD[fx], PERIOD[fy])
