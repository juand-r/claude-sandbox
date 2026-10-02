"""Detailed check of a C-stack reaction: for k in a range, place glider (all
phases), simulate, and compare the stationary product with the canonical
stack of k + dk tiles (exact cell equality of the whole row at time T with
a freshly built stack of k+dk tiles at some shift, modulo 7 time phases),
listing which phases give an exact clean result.
Usage: python3 srod_check.py tile idx side glider dk kmin kmax T"""
import sys, json
import numpy as np
import objlib as O
import srod

tile, idx, side, g = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
dk, kmin, kmax, T = int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])
L = O.lib()


def canon_rows(k, n_extra=600):
    """the 7 time phases of the stack of k tiles: list of (string, rp)"""
    bits, rp = srod.rod_row(tile, idx, k)
    row = np.array([int(c) for c in bits], np.uint8)
    big = np.concatenate([O.ether(0, -n_extra, 0), row, O.ether(rp, len(row), len(row) + n_extra)])
    out = []
    for t in range(7):
        a = O.evolve(big, t)
        out.append("".join(map(str, a[n_extra - t - 20:n_extra - t + len(row) + 20])))
    return out


for k in range(kmin, kmax + 1):
    target = canon_rows(k + dk)
    good, bad = [], []
    for kg in range(L[g]["p"]):
        bits, rp = srod.rod_row(tile, idx, k)
        if side == "L":
            items = [("g", g, kg, 0), ("raw", bits, 0, rp, srod.GAP + 6, "rod")]
        else:
            items = [("raw", bits, 0, rp, 0, "rod"), ("g", g, kg, srod.GAP)]
        row, x_lo, objs, c = O.build(items, pad=2 * T + 200)
        a = O.evolve(row, T)
        s = "".join(map(str, a))
        hit = any(tgt in s for tgt in target)
        # nothing else: types must be a single object
        ty = O.types(a, x_lo + T)
        (good if hit and len(ty) == 1 else bad).append(kg)
    print(json.dumps({"tile": tile, "idx": idx, "side": side, "g": g, "k": k, "dk": dk,
                      "clean_phases": good, "other_phases": bad}), flush=True)
