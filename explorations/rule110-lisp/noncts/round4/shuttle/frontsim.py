"""Exhaustive exact simulation of trains X against a rod's FRONT.

For each train X (from trains.py files: bits on [0, W) with left phase 0,
right phase pR at t = 0, (p,d) period), each collision class k (X advanced
k steps along the ether lattice vector (1,-4): k = 0..ncls-1), and rod
sizes n in NS: simulate  ether | X | gap | E^n  for T steps and test
whether the rod survives with its front moved by K units and its back
moved by J units (J != 0 means a wall reached the back):
   row T == bg(T-5K, x-2K) on [front-2, mid),  bg(T-5J, x-2J) on [mid, ..).
Survivors with something left of the rod are reported with the collider
names of the left objects.
Usage: python frontsim.py trains_file.jsonl ncls(ignored) T out.jsonl [n1,n2]
"""
import os
import sys
import json
import time
sys.dont_write_bytecode = True
import numpy as np
from rod import TILE, ether_bit, simulate
from pert import BG
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "collider"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from engine import pack, unpack, step_packed_n  # noqa
from fractions import Fraction  # noqa
from rod import SYNTH  # noqa

GAP = 30
KS = range(-4, 7)
JS = range(-3, 4)
_LIB = None


def lib():
    global _LIB
    if _LIB is None:
        from library import Library
        _LIB = Library.load()
    return _LIB


def run_row(row, T):
    w = len(row)
    a = pack(row)
    a = step_packed_n(a, T)
    return unpack(a, w)


def placements(bits, pR, p, d, phig, x_end, PE=(15, -4)):
    """One placement per collision class of the train (period (p,d)) against
    the rod (period PE): list of (lo_x, seg, phiL, cls_offset). The train's
    frame row is evolved dt steps (0 <= dt < p) and translated by s
    (frame col f -> global f + s); its seed event is then (-dt, s).
    s must give the right ether phase phig; segments end <= x_end."""
    sys.path.insert(0, SYNTH)
    from classes import same_class, n_classes
    ncls = n_classes((p, d), PE)
    W = len(bits)
    out = []
    for dt in range(p):
        pad = 3 * dt + 20
        xs = range(-pad, W + pad)
        r0 = np.array([ether_bit(0, 0, x) if x < 0 else (bits[x] if x < W else ether_bit(pR, 0, x))
                       for x in xs], np.uint8)
        rk = simulate(r0, dt)[dt] if dt else r0
        fr = np.arange(-pad, W + pad)
        le = np.array([ether_bit(0, dt, x) for x in fr])
        re = np.array([ether_bit(pR, dt, x) for x in fr])
        edge = dt + 3                                  # cyclic-seam debris zone
        dl = np.nonzero(rk[edge:-edge] != le[edge:-edge])[0] + edge
        dr = np.nonzero(rk[edge:-edge] != re[edge:-edge])[0] + edge
        a, b = dl[0], dr[-1] + 1
        seg = rk[a:b]
        fa = fr[a]
        s0 = (pR + 4 * dt - phig) % TILE
        s = x_end - (fa + len(seg))
        s -= (s - s0) % TILE
        for j in range(ncls + 1):
            sj = s - TILE * j
            off = (-dt, sj)
            if any(same_class(off, o[3], (p, d), PE) for o in out):
                continue
            out.append((fa + sj, seg, (4 * dt - sj) % TILE, off))
        if len(out) == ncls:
            break
    assert len(out) == ncls, (len(out), ncls)
    return out


def classify(place, n, T, bgs):
    bg = bgs[n]
    lo_x, seg, phiL, _ = place
    span_lo, span_hi = lo_x - 2 * T - 100, bg.W + 2 * T + 100
    xs = np.arange(span_lo, span_hi)
    row = np.array([ether_bit(phiL, 0, x) if x < lo_x else
                    (seg[x - lo_x] if x < lo_x + len(seg) else bg(0, x)) for x in xs], np.uint8)
    rT = run_row(row, T)
    a0, b0 = T + 5, len(xs) - T - 5        # valid region (no seam influence)
    mid = bg.front(T) + bg.W // 2
    found = None
    for K in KS:
        fK = bg.front(T - 5 * K) + 2 * K
        lo = fK - 2
        hi = span_lo + b0
        if lo >= mid - 4:
            continue
        assert span_lo + a0 + 20 < lo and mid < hi - 20, (span_lo + a0, lo, mid, hi)
        ok_front = all(rT[x - span_lo] == bg(T - 5 * K, x - 2 * K) for x in range(lo, mid))
        if not ok_front:
            continue
        for J in JS:
            if all(rT[x - span_lo] == bg(T - 5 * J, x - 2 * J) for x in range(mid, hi)):
                found = (K, J, fK)
                break
        if found:
            break
    if not found:
        return None
    K, J, fK = found
    left = rT[a0: fK - 2 - span_lo]
    lx0 = span_lo + a0
    empty = all(left[i] == ether_bit(phiL, T, lx0 + i) for i in range(len(left)))
    return dict(K=K, J=J, empty=empty, left=left, lx0=lx0, phiL=phiL,
                whole=rT[a0:b0], wx0=span_lo + a0)


def names_left(res, T):
    from collide import products_of
    left = res["left"]
    try:
        ok, prods, _ = products_of(lib(), left, res["lx0"], T)
    except RuntimeError as e:
        return [str(e)]
    return [p[0] for p in prods]


if __name__ == "__main__":
    fn, ncls, T, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    NS = [int(v) for v in sys.argv[5].split(",")] if len(sys.argv) > 5 else [10, 11]
    trains = [json.loads(l) for l in open(fn)]
    bgs = {n: BG(n, T + 60, -2 * T - 600, 4 * n + 2 * T + 300) for n in NS}
    done = 0
    if os.path.exists(out):
        done = sum(1 for _ in open(out))
    t0 = time.time()
    with open(out, "a") as fh:
        for i, tr in enumerate(trains):
            if i < done:
                continue
            bits = [int(c) for c in tr["bits"]]
            rec = dict(i=i, bits=tr["bits"], pR=tr["pR"], p=tr["p"], d=tr["d"], res=[])
            pls = {n: placements(bits, tr["pR"], tr["p"], tr["d"], bgs[n].phi_left, -GAP) for n in NS}
            for k in range(len(pls[NS[0]])):
                for n in NS:
                    r = classify(pls[n][k], n, T, bgs)
                    if r is None:
                        rec["res"].append([k, n, None])
                    else:
                        item = [k, n, r["K"], r["J"], r["empty"]]
                        if not r["empty"]:
                            item.append(names_left(r, T))
                        # full product list of the whole valid row (incl. right side)
                        item.append(names_left(dict(left=r["whole"], lx0=r["wx0"]), T))
                        rec["res"].append(item)
            fh.write(json.dumps(rec) + "\n")
            if i % 200 == 0:
                print(i, round(time.time() - t0, 1), flush=True)
