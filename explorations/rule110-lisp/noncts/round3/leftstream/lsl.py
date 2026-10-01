"""leftstream library: collider's glider library (read-only), placement of
glider seeds with automatic ether snapping, exact Rule 110 simulation and
product typing (collider's objects/identify, independent of synth/'s SAT
code).

Seeds follow collider conventions: (name, t0, x0) = phase 0 of `name` with
bits[0] at column x0 at time t0. Ether: cell(t, x) = ETHER[(x + 4t + c) % 14].
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COLLIDER = os.path.abspath(os.path.join(HERE, "..", "..", "collider"))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, COLLIDER)
sys.path.insert(0, ROOT)
_cwd = os.getcwd()
os.chdir(COLLIDER)
import numpy as np                                   # noqa: E402
from library import Library                          # noqa: E402
from collide import products_of, collide_pair        # noqa: E402
from r110lib import (TILE, build_row, ether_cells, _pack_batch,   # noqa: E402
                     _unpack_batch, _step_state, objects, obj_key)
import engine                                        # noqa: E402
LIB = Library.load()
os.chdir(_cwd)

CHAIN = ["E"] + [f"E^{n}" for n in range(2, 10)]


def _extend_chain(nmax=16):
    """E^10.. are not named in collider's library: register them as the
    single product of E^(n-1) + B (as gate/common.py does, in memory)."""
    os.chdir(COLLIDER)
    try:
        while len(CHAIN) < nmax:
            res = collide_pair(LIB, CHAIN[-1], "B")
            assert len(res) == 1 and res[0]["settled"] and \
                len(res[0]["products"]) == 1, res
            CHAIN.append(res[0]["products"][0][0])
    finally:
        os.chdir(_cwd)


_extend_chain()


def En(n):
    """Library name of E^n (n >= 1)."""
    return CHAIN[n - 1]


def nval(name):
    """n if name is E^n, else None."""
    return CHAIN.index(name) + 1 if name in CHAIN else None


def state(name, t0, x0, t=0):
    return LIB.gliders[name].state_at(t0, x0, t)


def snap(placed, name, t0, x0):
    """Smallest x >= x0 such that (name, t0, x) placed right of the last
    object in `placed` has a consistent ether between them."""
    if not placed:
        return x0
    b1, l1, r1, s1 = state(*placed[-1])
    for x in range(x0, x0 + TILE):
        b2, l2, r2, s2 = state(name, t0, x)
        if (r1 - s1 - (l2 - s2)) % TILE == 0:
            return x
    raise AssertionError("no ether-consistent x")


def row_of(placements, T=0, pad=None):
    """Row at time 0 containing the seeds; pad defaults to T + 200."""
    states = [state(*p) for p in placements]
    pad = pad if pad is not None else int(T) + 200
    return build_row(states, pad=pad)


def evolve(row, T):
    w = engine.pack(row.astype(np.uint8))
    w = engine.step_packed_n(w, T)
    return engine.unpack(w, len(row))


def run(placements, T, pad=None):
    """Exact Rule 110 from the seeds for T steps (cyclic row, wrap seam far
    away). -> (settled, products [(name, t0, x0)])."""
    pad = pad if pad is not None else int(T) + 200
    row, x0 = row_of(placements, T, pad + T + 20)
    cur = evolve(row, T)
    # engine.pack zero-pads to a multiple of 64 cells, so the wrap seam
    # emits junk; it travels <= 1 cell/step: crop T + 20 cells at each end.
    c = T + 20
    cur, x0 = cur[c:len(cur) - c], x0 + c
    os.chdir(COLLIDER)
    try:
        ok, prods, _ = products_of(LIB, cur, x0, T)
    finally:
        os.chdir(_cwd)
    return ok, prods


def parse_row(bits, x0, T=0):
    """Type a row (time T, column 0 = global x0) into seeds."""
    os.chdir(COLLIDER)
    try:
        ok, prods, _ = products_of(LIB, np.asarray(bits, np.uint8), x0, T)
    finally:
        os.chdir(_cwd)
    return ok, prods


def embed(bitstr, lo, pL, pR, pad=300):
    """A finite segment (cells lo..) in ether: left absolute phase pL,
    right phase pR (synth convention = collider's at t = 0)."""
    seg = np.array([int(c) for c in bitstr], np.uint8)
    hi = lo + len(seg)
    left = ether_cells(pL, lo - pad, lo)
    right = ether_cells(pR, hi, hi + pad)
    return np.concatenate([left, seg, right]), lo - pad


def names(prods):
    return [p[0] for p in prods]


def shift(p, P, m):
    """Seed p shifted by m times the spacetime vector P = (dt, dx)."""
    return (p[0], p[1] + m * P[0], p[2] + m * P[1])


def export(placements, T, expect=None, note=""):
    """Compact exact scene: the row at t = 0 between the outermost objects
    (pad 20), with absolute ether phases outside. Anyone can rebuild:
    cell x (x < x0) = ETHER[(x + cL) % 14], cells x0.. = bits,
    cells after = ETHER[(x + cR) % 14]."""
    row, x0 = row_of(placements, 0, pad=20)
    from r110lib import window_phase
    cL = (placements and None)
    st = sorted([state(*p) for p in placements], key=lambda s: s[3])
    cL = (st[0][1] - st[0][3]) % TILE
    cR = (st[-1][2] - st[-1][3]) % TILE
    # trim to the exact extent used by build_row (W adjusted for wrap)
    end = st[-1][3] + len(st[-1][0]) + 20
    bits = "".join(map(str, row[:end - x0]))
    return {"x0": int(x0), "cL": int(cL), "cR": int(cR), "bits": bits,
            "T": int(T), "seeds": [list(p) for p in placements],
            "expect": expect, "note": note}


def rebuild(sc, pad):
    """Row (and global x of column 0) from an exported scene."""
    bits = np.array([int(c) for c in sc["bits"]], np.uint8)
    x0, hi = sc["x0"], sc["x0"] + len(bits)
    left = ether_cells(sc["cL"], x0 - pad, x0)
    right = ether_cells(sc["cR"], hi, hi + pad)
    return np.concatenate([left, bits, right]), x0 - pad


def run_exported(sc):
    T = sc["T"]
    row, x0 = rebuild(sc, 2 * T + 300)
    cur = evolve(row, T)
    c = T + 20
    cur, x0 = cur[c:len(cur) - c], x0 + c
    return parse_row(cur, x0, T)
