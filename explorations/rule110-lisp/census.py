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


# 14-bit window code -> rotation r, or -1 if the window is not ether
_ROT_LUT = np.full(1 << TILE, -1, dtype=np.int16)
for _code, _r in _ROTATION.items():
    _ROT_LUT[_code] = _r


def ether_phase(row):
    """Per window start x: the ether phase c in 0..13, or -1 if the
    window at x is not ether. (Window codes built by shifted ors and read
    from a lookup table: 2.3x faster than a matrix product and a search.)"""
    n = len(row) - TILE + 1
    if n <= 0:
        raise ValueError("row shorter than one ether tile")
    r = row.astype(np.uint16)
    codes = np.zeros(n, dtype=np.uint16)
    for k in range(TILE):
        codes |= r[k:k + n] << np.uint16(k)
    rot = _ROT_LUT[codes].astype(np.int64)
    return np.where(rot >= 0, (rot - np.arange(n)) % TILE, -1)


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
    """-> list of (start, end, kind) for the clusters in the last row.

    Vectorized form of classify() over all clusters at once (same result):
    per family, a prefix sum of the cells where row t differs from row
    t - dt shifted by dx answers each cluster's invariance test in O(1)."""
    if len(hist) < MAX_DT + 1:
        raise ValueError(f"need at least {MAX_DT + 1} rows of history")
    cl = clusters(hist[-1])
    if not cl:
        return []
    now, width = hist[-1], hist.shape[1]
    a, b = np.array(cl).T
    lo, hi = a - MARGIN, b + MARGIN
    hits = []
    for dt, dx in FAMILIES.values():
        then = hist[-1 - dt]
        inside = (lo >= 0) & (lo - dx >= 0) & (hi <= width) & (hi - dx <= width)
        diff = np.ones(width, dtype=np.int64)
        s, e = max(0, dx), min(width, width + dx)
        diff[s:e] = now[s:e] != then[s - dx:e - dx]
        cs = np.concatenate([[0], np.cumsum(diff)])
        mism = cs[np.clip(hi, 0, width)] - cs[np.clip(lo, 0, width)]
        hits.append(inside & (mism == 0))
    hits = np.array(hits)
    names = np.array(list(FAMILIES) + ["?"])
    label = np.where(hits.sum(axis=0) == 1, hits.argmax(axis=0), len(FAMILIES))
    return list(zip(a.tolist(), b.tolist(), names[label].tolist()))
