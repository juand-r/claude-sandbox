"""Translate collider-convention placements (name, t, x) - used by collider,
gate, synth via collider/r110lib - into my vlib convention, WITHOUT using
their row builder for the actual runs: for each glider type I find once my
(T_g, X_g) whose row equals theirs for seed (0,0); seeds then translate.
After that, scenes are rebuilt and typed entirely with my own code."""
import os, sys
import numpy as np
import vlib, libgen

HERE = os.path.dirname(os.path.abspath(__file__))
COLL = os.path.abspath(os.path.join(HERE, "..", "..", "collider"))
_cwd = os.getcwd()
sys.path.insert(0, COLL)
os.chdir(COLL)
from predict import LIB as CLIB          # noqa: E402  (read-only)
from r110lib import build_row            # noqa: E402
os.chdir(_cwd)

libgen.load()
_MAP = {}


def their_row(scene):
    sts = [CLIB.gliders[g].state_at(t, x, 0) for g, t, x in scene]
    row, x0 = build_row(sts, pad=200)
    return row.astype(np.uint8), x0


def mapping(g):
    """my (T, X, c0) such that my build([(g, T, X)], c0) equals collider's
    seed (0,0) row on the overlap."""
    if g in _MAP:
        return _MAP[g]
    row, x0 = their_row([(g, 0, 0)])
    ph = vlib.window_phase(row)
    c_left = (int(ph[5]) - x0) % 14        # my phase convention, global x
    want = [(n, lo + x0) for n, lo, w, k in vlib.identify(row)]
    G = vlib.LIB[g]
    for T in range(G.P):
        for X in range(-80, 80):
            if (X + 4 * T + c_left) % 14:
                continue
            mine, org, placed = vlib.build([(g, T, X)], c0=c_left, pad=200)
            got = [(n, lo + org) for n, lo, w, k in vlib.identify(mine)]
            if got == want:
                _MAP[g] = (T, X, c_left)
                return _MAP[g]
    raise ValueError(f"no mapping for {g}: their {want}")


def translate(scene):
    """collider scene [(g, t, x)] -> (my items, c0)."""
    items = []
    c0 = None
    for g, t, x in scene:
        T, X, c = mapping(g)
        items.append((g, T + t, X + x))
        if c0 is None:
            c0 = c        # phase left of the first object (first item is leftmost)
    return items, c0


def check(scene, T=0):
    """Rebuild a collider scene with my builder; assert no snapping and that
    the initial rows agree cell for cell on the common span."""
    items, c0 = translate(scene)
    mine, org, placed = vlib.build(items, c0=c0, T=T)
    assert [p[2] for p in placed] == [i[2] for i in items], "snapped: convention mismatch"
    row, x0 = their_row(scene)
    lo, hi = max(org, x0), min(org + len(mine), x0 + len(row))
    same = np.array_equal(mine[lo - org:hi - org], row[lo - x0:hi - x0])
    return items, c0, same


if __name__ == "__main__":
    for g in ["E", "E^2", "G", "GB1", "GB3", "GB4", "GB5", "A"]:
        print(g, mapping(g))
    print(check([("E", 0, 0), ("GB3", 0, 120), ("GB4", -25, 166)])[2])


def expand(scene):
    """Split collider compound packets 'A@(t,x)+B@(t,x)' into parts with
    absolute seeds (part seed = packet seed + part offset), sorted by the
    part's position at time 0."""
    import re
    out = []
    for g, t, x in scene:
        if "@" not in g:
            out.append((g, t, x))
            continue
        for part in g.split("+"):
            m = re.fullmatch(r"(.+)@\((-?\d+),(-?\d+)\)", part)
            out.append((m.group(1), t + int(m.group(2)), x + int(m.group(3))))
    key = lambda it: CLIB.gliders[it[0]].state_at(it[1], it[2], 0)[3]
    return sorted(out, key=key)
