"""Stationary rods (C-stacks): reaction table from both faces. Exact CA.

Rod: ether(phase 0) | tile^k | ether(phase rp) with tile from srods.json
(SAT-found face-free rods, stable for every k). A library glider (all time
phases k_g) is placed left of the rod (right-movers) or right of it
(left-movers), gap >= GAP. After T steps:
  value  = number of whole tiles in the longest run of the rod's interior
           pattern (any of its 7 time phases) at the rod's place, read on the
           row at T (and the rod is checked stationary: row T == row T+7 there)
  faces  = whether the cells just outside that run still read as the
           canonical rod's faces (ether of the canonical phases)
  movers = typer names of objects outside the rod region
Usage: python3 srod.py TILEKEY side(L|R) k T names... (or 'set:A' etc.)"""
import json
import sys
import numpy as np
import objlib as O

SR = json.load(open("srods.json"))
GAP = 6


def rod_row(tilekey, idx, k):
    s, rp = SR[tilekey][idx]
    p = len(tilekey)
    per = s[:p]
    assert s == per * (len(s) // p)
    bits = per * k
    rp_k = (rp - p * (k - len(s) // p)) % 14
    return bits, rp_k


def interior_patterns(tilekey, idx):
    """the rod's interior period at each of the 7 time phases"""
    s, rp = SR[tilekey][idx]
    p = len(tilekey)
    row = np.array([int(c) for c in s], np.uint8)
    big = np.concatenate([O.ether(0, -60, 0), row, O.ether(rp, len(row), len(row) + 60)])
    h = O.history(big, 7)
    pats = []
    for t in range(7):
        r = h[t]
        mid = 60 - t + len(row) // 2
        pats.append("".join(map(str, r[mid:mid + p])))
    return pats


def measure(row, x_lo, tilekey, idx, around):
    """longest run of whole tiles near column `around`"""
    p = len(tilekey)
    s = "".join(map(str, row))
    best = (0, None)
    for pat in set(interior_patterns(tilekey, idx)):
        # any rotation of pat is also a valid start
        for rot in range(p):
            q = pat[rot:] + pat[:rot]
            i = 0
            while True:
                j = s.find(q, i)
                if j < 0:
                    break
                n = 0
                while s[j + n * p:j + (n + 1) * p] == q:
                    n += 1
                if n > best[0] and abs(x_lo + j - around) < 400:
                    best = (n, x_lo + j)
                i = j + 1
    return best


def run(tilekey, idx, side, k, T, name, kg):
    bits, rp = rod_row(tilekey, idx, k)
    if side == "L":
        items = [("g", name, kg, 0), ("raw", bits, 0, rp, GAP + 6, "rod")]
    else:
        items = [("raw", bits, 0, rp, 0, "rod"), ("g", name, kg, GAP)]
    row, x_lo, objs, c = O.build(items, pad=2 * T + 200)
    rod_s = [o for o in objs if o[0] == "rod"][0][1]
    a = O.evolve(row, T)
    xa = x_lo + T
    a7 = O.evolve(a, 7)
    n, xs = measure(a, xa, tilekey, idx, rod_s + len(bits) // 2)
    # baseline: the rod alone, same T (the run measure can overcount by
    # face cells that continue the pattern)
    rb, xb, ob, cb = O.build([("raw", bits, 0, rp, 0, "rod")], pad=2 * T + 200)
    ab = O.evolve(rb, T)
    n0, xs0 = measure(ab, xb + T, tilekey, idx, ob[0][1] + len(bits) // 2)
    n_base, x_base = n0, xs0 - ob[0][1]
    p = len(tilekey)
    # stationarity of the rod region
    stat = None
    if xs is not None:
        i0 = xs - xa
        seg = a[i0 - 20:i0 + n * p + 20]
        seg7 = a7[i0 - 20 - 7:i0 - 7 + n * p + 20]
        stat = bool(np.array_equal(seg, seg7))
    ty = O.types(a, xa)
    movers = [t[0] for t in ty if xs is None or not (xs - 30 <= t[1] <= xs + n * p + 30)]
    return {"tile": tilekey, "idx": idx, "side": side, "k": k, "T": T, "g": name,
            "kg": kg, "k_out": n, "dk": n - n_base, "shift": None if xs is None else xs - rod_s - x_base,
            "stationary": stat, "movers": movers}


if __name__ == "__main__":
    tilekey, side, k, T = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    idx = int(sys.argv[5])
    names = sys.argv[6:]
    L = O.lib()
    for name in names:
        res = {}
        for kg in range(L[name]["p"]):
            r = run(tilekey, idx, side, k, T, name, kg)
            key = (r["dk"], r["shift"], r["stationary"], tuple(r["movers"]))
            res.setdefault(key, []).append(kg)
        for key, kgs in res.items():
            print(json.dumps({"tile": tilekey, "idx": idx, "side": side, "k": k, "g": name,
                              "dk": key[0], "shift": key[1], "stationary": key[2],
                              "movers": list(key[3]), "phases": kgs}), flush=True)
