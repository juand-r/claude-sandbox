"""W4 (route 23): ONE back reaction X (left-mover, period (pX, dX)) with
    X + E^m -> E^(m + d_c) + A-family only     in all three classes c,
jointly (the same X bits in three scenes whose rod background is shifted
by (k, -4k), k = 0, 1, 2 = the three classes against (12,-6) or (42,-14)).
Rod pinned to the exact background (window's left edge 'depth' cells
inside the rod), so solutions hold for every m above the window.
d_c are free (one-hot over [dmin, dmax]); X is also tied to its own
isolated periodic spacetime. Each solution is re-simulated exactly
(E^N and E^N2, every class), the A's are counted, and the net effect
Delta_c = d_c - a_c (what remains after trailing B's eat the A's) is
reported; X is then blocked and the search continues.
Usage: python w4.py --px 12,-6 --wx 20 --phiR all [--dset -1,6,13] [--max 50]
"""
import sys, json, time, math, argparse
sys.dont_write_bytecode = True
import numpy as np
from rod import TILE, ether_bit, simulate
from pert import BG, Pert, smooth_window
from r110sat import CNF, neg


def build(a, bg, phiR, cnf=None):
    cnf = cnf or CNF()
    pX, dX = a.px
    vX = dX / pX
    T = a.T
    phib = bg.phi_right
    b0 = max(bg.back(k) + 4 * k for k in range(3))     # shifted rods' backs
    x0 = b0 + a.gap
    x1 = x0 + a.wx
    X = {x: cnf.new_var() for x in range(x0, x1)}
    # X alone: periodic train in ether (phib | X | phiR)
    al = Pert(cnf, pX, x0, x1, lambda x: ether_bit(phib, 0, x) if x < x0 else ether_bit(phiR, 0, x),
              lambda t, x: ether_bit(phib, t, x), lambda t, x: ether_bit(phiR, t, x),
              lambda t: (x0 - t, x1 + t), init_lits=X)
    for x in range(x0 - pX - 2, x1 + pX + 2):
        cnf.equal(al.lit(pX, x + dX), al.lit(0, x))
    if phiR == phib:
        cnf.add([(-X[x] if ether_bit(phib, 0, x) else X[x]) for x in X])
    ds = list(range(a.dmin, a.dmax + 1))
    scenes = []
    for k in range(3):
        bgk = (lambda k: (lambda t, x: bg(t + k, x - 4 * k)))(k)
        backk = (lambda k: (lambda t: bg.back(t + k) + 4 * k))(k)
        bk0 = backk(0)
        tc = max(1.0, (x0 - bk0) / (abs(vX) - 4 / 15))
        xc = bk0 - 4 * tc / 15

        def Lstar(t, bk0=bk0):
            return bk0 - a.depth - 4 * t / 15

        def Rstar(t, bk0=bk0):
            # generous: X's right end, or any A leaving the back from t = 0
            return max(x1 + vX * t, bk0 + (2 / 3) * t) + a.margin
        win = smooth_window(T, Lstar, Rstar)
        S = Pert(cnf, T, x0, x1,
                 (lambda bgk: (lambda x: bgk(0, x) if x < x0 else ether_bit(phiR, 0, x)))(bgk),
                 (lambda bgk: (lambda t, x: bgk(t, x)))(bgk),
                 lambda t, x: ether_bit(phiR, t, x), win, init_lits=X)
        L, R = S.bounds[T]
        sel = {}
        for d in ds:
            s = cnf.new_var()
            sel[d] = s
            bS = backk(T - 5 * d) + 2 * d
            ok = True
            for x in range(L - 2, (R + 2) if a.noA else (bS + a.band)):
                l = S.lit(T, x)
                v = bgk(T - 5 * d, x - 2 * d)
                if isinstance(l, bool):
                    if l != bool(v):
                        ok = False
                        break
                    continue
                cnf.add([-s, l if v else -l])
            if not ok:
                cnf.add([-s])
                continue
            for x in range(bS + a.band, R + 2) if not a.noA else []:
                l1, l2 = S.lit(T, x), S.lit(T - 3, x - 2)
                if isinstance(l1, bool) and isinstance(l2, bool):
                    if l1 != l2:
                        cnf.add([-s])
                    continue
                cnf.add([-s, neg(l1), l2])
                cnf.add([-s, l1, neg(l2)])
        # Delta(d) = d - a(d), a(d) in [0,7) from the A-region's slip:
        # 8 a = phiR - (ether phase right of the shifted rod)  (mod 14)
        delta = {}
        for d in ds:
            bS = backk(T - 5 * d) + 2 * d
            ps = [p for p in range(14) if all(bgk(T - 5 * d, x - 2 * d) == ether_bit(p, T, x)
                                              for x in range(bS + 2, bS + 16))]
            if len(ps) == 1:
                aa = [q for q in range(7) if (8 * q - (phiR - ps[0])) % 14 == 0]
                if aa:
                    delta[d] = d - aa[0]
        cnf.add(list(sel.values()))
        for d1 in ds:
            for d2 in ds:
                if d1 < d2:
                    cnf.add([-sel[d1], -sel[d2]])
        scenes.append((S, sel, delta))
    if a.distinct_delta:            # Delta pairwise distinct (if every a <= 6)
        for i in range(3):
            for j in range(i + 1, 3):
                for d1 in ds:
                    for d2 in ds:
                        D1, D2 = scenes[i][2].get(d1), scenes[j][2].get(d2)
                        if D1 is not None and D1 == D2:
                            cnf.add([-scenes[i][1][d1], -scenes[j][1][d2]])
    scenes = [(S, sel) for S, sel, _ in scenes]
    if a.dset:                      # optional: the three d's (any order) are this set
        want = sorted(a.dset)
        # each d in want used by exactly... simple: every scene's d in want, all distinct
        for S, sel in scenes:
            cnf.add([sel[d] for d in want if d in sel])
        for d in want:
            for i in range(3):
                for j in range(i + 1, 3):
                    if d in scenes[i][1] and d in scenes[j][1]:
                        cnf.add([-scenes[i][1][d], -scenes[j][1][d]])
    if a.not_all_equal:             # exclude class-free outcomes
        for d in ds:
            cnf.add([-scenes[0][1][d], -scenes[1][1][d], -scenes[2][1][d]])
    if a.distinct_d:
        for d in ds:
            for i in range(3):
                for j in range(i + 1, 3):
                    cnf.add([-scenes[i][1][d], -scenes[j][1][d]])
    return cnf, X, scenes, (x0, x1)


def simulate_scene(Xbits, x0, phiR, N, k, T):
    """exact run of class k with rod E^N; returns product names."""
    from frontsim import lib, run_row
    from collide import products_of
    bg = BG(N, 20, -2 * T - 900, 4 * N + 2 * T + 900)
    lo, hi = -T - 400, x0 + len(Xbits) + 2 * T + 400
    xs = np.arange(lo, hi)
    row = np.array([bg(k, x - 4 * k) if x < x0 else (Xbits[x - x0] if x < x0 + len(Xbits) else ether_bit(phiR, 0, x))
                    for x in xs], np.uint8)
    rT = run_row(row, T)
    a_, b_ = T + 5, len(row) - T - 5
    try:
        ok, pr, _ = products_of(lib(), rT[a_:b_], lo + a_, T)
    except RuntimeError as e:
        return None, str(e)
    return ok, [p[0] for p in pr]


def rodsize(name):
    import re
    if name == "E":
        return 1
    m = re.match(r"E\^(\d+)$", name)
    if m:
        return int(m.group(1))
    m = re.match(r"v-4/15s(\d+)w(\d+)", name)
    if m:      # long rods: width W(n) = 2 + floor((10(n-1)+...)/3); use table
        return ("w", int(m.group(2)))
    return None


def pair(s):
    return tuple(int(v) for v in s.split(","))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--px", type=pair, default=(12, -6))
    ap.add_argument("--wx", type=int, default=20)
    ap.add_argument("--N", type=int, default=16)
    ap.add_argument("--T", type=int, default=160)
    ap.add_argument("--gap", type=int, default=4)
    ap.add_argument("--depth", type=int, default=30)
    ap.add_argument("--band", type=int, default=8)
    ap.add_argument("--margin", type=int, default=6)
    ap.add_argument("--dmin", type=int, default=-6)
    ap.add_argument("--dmax", type=int, default=6)
    ap.add_argument("--phiR", default="all")
    ap.add_argument("--dset", type=pair, default=None)
    ap.add_argument("--distinct_d", action="store_true")
    ap.add_argument("--not_all_equal", action="store_true")
    ap.add_argument("--noA", action="store_true", help="pure outcome: nothing but the rod")
    ap.add_argument("--distinct_delta", action="store_true",
                    help="net effects Delta = d - #A pairwise distinct (assumes <= 6 A's per class)")
    ap.add_argument("--max", type=int, default=20)
    ap.add_argument("--out", default="w4_results.jsonl")
    a = ap.parse_args()
    bg = BG(a.N, a.T + 120, -a.T - 400, 4 * a.N + a.T + 400)
    phis = range(TILE) if a.phiR == "all" else [int(v) for v in a.phiR.split(",")]
    phis = [p for p in phis if (p - bg.phi_right) % 2 == 0]     # even slips only
    for phiR in phis:
        t0 = time.time()
        cnf, X, scenes, (x0, x1) = build(a, bg, phiR)
        s = cnf.solver()
        n = 0
        while n < a.max and s.solve():
            m = set(l for l in s.get_model() if l > 0)
            bits = [int(X[x] in m) for x in range(x0, x1)]
            dks = [next(d for d, v in sel.items() if v in m) for S, sel in scenes]
            rec = dict(px=a.px, wx=a.wx, phiR=phiR, x0=x0, X="".join(map(str, bits)), d=dks,
                       secs=round(time.time() - t0, 1))
            sims = {}
            for N2 in (a.N, a.N - 7):   # same right ether phase (7 units = slip 42)
                for k in range(3):
                    sims[f"{N2}:{k}"] = simulate_scene(bits, x0, phiR, N2, k, a.T + 400)
            rec["sims"] = sims
            print(json.dumps(rec), flush=True)
            with open(a.out, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
            s.add_clause([(-X[x] if b else X[x]) for x, b in zip(range(x0, x1), bits)])
            n += 1
        s.delete()
        print("phiR", phiR, "solutions", n, round(time.time() - t0, 1), "s", flush=True)
