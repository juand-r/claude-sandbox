"""Exact glider location: find every occurrence of a glider family's
canonical phase (with 2 ether tiles of context on each side) in row t.
Returns (x, t) anchors; for a glider with period (p, d) we scan t..t+p-1."""
import numpy as np
import r110check as r
from engine import ETHER, parse
import classes as C


def find(h, t, fam, lo=0, hi=None):
    canon = parse(ETHER * 2 + r.PHASES[C.CANON[fam]] + ETHER * 2)
    p = C.PERIOD[fam][0]
    hi = h.shape[1] if hi is None else hi
    out = []
    n = len(canon)
    for tt in range(t, min(t + p, h.shape[0])):
        row = h[tt]
        win = np.lib.stride_tricks.sliding_window_view(row[lo:hi], n)
        hits = np.nonzero((win == canon).all(axis=1))[0]
        out += [(tt, lo + x + 28) for x in hits]
    return out
