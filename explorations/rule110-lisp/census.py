"""Glider census: locate and type the gliders in a Rule 110 row.

Ether filtering by phase. A 14-cell window that equals a rotation of the
ether tile fixes the ether's absolute phase c: cell y reads
ETHER[(c + y) mod 14]. Consecutive matching windows with the same c form
an ether run. A defect lies between two runs whenever matching is
interrupted or the phase changes. Coverage alone is not enough: an A
glider is essentially a phase slip, and in some of its phases every cell
lies in some matching window, so only the phase change reveals it. When
the two runs' windows overlap, the defect is the overlap (cells both
phases explain); otherwise it is the gap between them.

Typing by invariance. The ether is invariant under the spacetime shifts
(dt, dx) = (7, 0) and (3, 2), hence under every integer combination of
them. Each glider family used by Cook's construction is invariant under
exactly one of the following combinations:

    C  (7, 0)     stationary C gliders: tape data
    A  (3, 2)     A gliders, speed 2/3: ossifiers, acceptors, rejectors
    E  (30, -8)   Ebar gliders, speed -4/15: moving data, table data,
                  leaders, invisibles

A cluster at time t whose cells (plus a margin) satisfy
row_t[x] == row_{t-dt}[x - dx] for exactly one family is given that
family's label; otherwise it is '?' (mixed or colliding). Bundles such as
A^4 come out as one cluster of type A.

Input is a short history: an array whose last row is time t and whose
row -1-k is time t-k, at least MAX_DT + 1 rows deep, all over the same
cell window.
"""

import numpy as np

from engine import ETHER

TILE = len(ETHER)
FAMILIES = {"C": (7, 0), "A": (3, 2), "E": (30, -8)}
MAX_DT = max(dt for dt, _ in FAMILIES.values())
# cells of ether on each side of a cluster included in the invariance test
MARGIN = 2

_WEIGHTS = (1 << np.arange(TILE, dtype=np.int64))
# window code -> rotation r (window == ETHER[r:] + ETHER[:r])
_ROTATION = {int(sum(int(c) << k for k, c in enumerate(ETHER[r:] + ETHER[:r]))): r
             for r in range(TILE)}
_CODES = np.array(sorted(_ROTATION), dtype=np.int64)
_ROT_OF_CODE = np.array([_ROTATION[c] for c in _CODES], dtype=np.int64)


def ether_phase(row):
    """Per window start x: the ether phase c in 0..13, or -1 if the
    window at x is not ether."""
    windows = np.lib.stride_tricks.sliding_window_view(row.astype(np.int64),
                                                        TILE)
    codes = windows @ _WEIGHTS
    pos = np.searchsorted(_CODES, codes).clip(0, len(_CODES) - 1)
    matched = _CODES[pos] == codes
    x = np.arange(len(codes))
    return np.where(matched, (_ROT_OF_CODE[pos] - x) % TILE, -1)


def clusters(row):
    """Defect regions of a row as (start, end) half-open pairs: the regions
    between consecutive ether runs (see module docstring). Regions touching
    the row's ends are omitted (no ether on the far side to compare)."""
    phase = ether_phase(row)
    xs = np.nonzero(phase >= 0)[0]
    if len(xs) == 0:
        return []
    ph = phase[xs]
    # a run breaks where windows stop being consecutive or phase changes
    breaks = np.nonzero((np.diff(xs) != 1) | (np.diff(ph) != 0))[0]
    out = []
    for i in breaks:
        left_last, right_first = xs[i], xs[i + 1]
        a, b = left_last + TILE, right_first
        if b <= a:                    # overlapping windows: the overlap
            a, b = right_first, left_last + TILE
        out.append((int(a), int(b)))
    return out


def _invariant(hist, a, b, dt, dx):
    now = hist[-1]
    then = hist[-1 - dt]
    lo, hi = a - MARGIN, b + MARGIN
    lo2, hi2 = lo - dx, hi - dx
    if lo < 0 or lo2 < 0 or hi > len(now) or hi2 > len(then):
        return False          # too close to the window edge to judge
    return np.array_equal(now[lo:hi], then[lo2:hi2])


def classify(hist, a, b):
    kinds = [k for k, (dt, dx) in FAMILIES.items()
             if _invariant(hist, a, b, dt, dx)]
    return kinds[0] if len(kinds) == 1 else "?"


def census(hist):
    """-> list of (start, end, kind) for the clusters in the last row."""
    if len(hist) < MAX_DT + 1:
        raise ValueError(f"need at least {MAX_DT + 1} rows of history")
    return [(a, b, classify(hist, a, b)) for a, b in clusters(hist[-1])]
