"""W4 (verify's target, lead 01:2x): enumerate (12,-6)-lattice packets X whose
back reactions on E^m are clean in all THREE classes (rod E^(m+d_c) at the
undisturbed front + only (3,2)-invariant cells right of it at T2) and
class-DEPENDENT (condition --cond: 'notallequal' = the three d_c not all
equal [default], or 'distinct' = pairwise distinct). Each witness X is
re-simulated in all three classes to T = TSIM, typed (round-3 verify typer),
and Delta_c = d_c - nA_c (A's counted from the typed products) is computed;
the target is Delta_c pairwise distinct. The exact X row is then blocked and
the enumeration continues (incremental solver) up to --max witnesses.
Scope caveat: with 'notallequal', reactions with d_0 = d_1 = d_2 whose
A counts differ (by >= 7, charge) are not enumerated.
Usage: python3 w4_enum.py m WX T2 out.jsonl [--s list] [--cond ...] [--max N]"""
import argparse
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "synth")))
from r110sat import CNF, TILE, make_window, neg, Assignment   # noqa: E402
from react import TrainVar                            # noqa: E402
from scene import Scene                               # noqa: E402
from classes import placements_by_class               # noqa: E402
from en import en_item                                # noqa: E402
import objlib as O                                    # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("m", type=int)
ap.add_argument("WX", type=int)
ap.add_argument("T2", type=int)
ap.add_argument("out")
ap.add_argument("--s", default=",".join(map(str, range(TILE))))
ap.add_argument("--dmin", type=int, default=-3)
ap.add_argument("--dmax", type=int, default=17)
ap.add_argument("--margin", type=int, default=30)
ap.add_argument("--cond", default="notallequal")
ap.add_argument("--max", type=int, default=60)
ap.add_argument("--tsim", type=int, default=1200)
ap.add_argument("--fixX", default=None)
A = ap.parse_args()
DSET = [d for d in range(A.dmin, A.dmax + 1) if A.m + d >= 1]


def build(s):
    cnf = CNF()
    E = en_item(cnf, A.m)
    rods = {d: en_item(cnf, A.m + d) for d in DSET}
    X = TrainVar(cnf, A.WX, 12, -6, s, name="X")
    if A.fixX:
        for xx, ch in enumerate(A.fixX):
            v = X.st.lit(0, xx)
            cnf.add([v] if ch == "1" else [-v])
    reps = placements_by_class(E, (0, 0), X, E.W + 6)
    assert len(reps) == 3
    tE, dE = Scene.undisturbed(E, 0, 0, A.T2)
    scenes, ys = [], []
    for c, (tau, x) in enumerate(reps):
        lo, hi = 0, x + X.W + tau
        win = make_window(A.T2 + 3, lo, hi, -0.5, 2 / 3, margin=A.margin)
        S = Scene(cnf, A.T2 + 3, [(E, 0, 0), (X, tau, x)], window=win)
        L, R = S.st.bounds[A.T2]
        L3, R3 = S.st.bounds[A.T2 + 3]
        y = {}
        for d, it in rods.items():
            yv = cnf.new_var()
            y[d] = yv
            ilo, ihi = it.extent(tE)
            mid = dE + ihi + A.margin
            for xx in range(L, mid):
                a = S.lit(A.T2, xx)
                b = it.st.lit(tE, xx - dE)
                if isinstance(b, bool):
                    cnf.add([-yv, a if b else neg(a)])
                else:
                    cnf.add([-yv, neg(a), b])
                    cnf.add([-yv, a, neg(b)])
            for xx in range(mid, min(R, R3 - 2) - 2):
                a = S.lit(A.T2, xx)
                b = S.lit(A.T2 + 3, xx + 2)
                cnf.add([-yv, neg(a), b])
                cnf.add([-yv, a, neg(b)])
        cnf.add(list(y.values()))
        ys.append(y)
        scenes.append(S)
    for d in DSET:
        if A.cond == "distinct":
            for i in range(3):
                for j in range(i + 1, 3):
                    cnf.add([-ys[i][d], -ys[j][d]])
        else:
            cnf.add([-ys[0][d], -ys[1][d], -ys[2][d]])
    return cnf, X, scenes, ys


def n_A(names, charges=None):
    """number of A gliders among typed products; an untyped '?' of charge w
    counts as the smallest n >= 2 with 8 n = w (mod 14) (flagged approx)."""
    n = 0
    approx = False
    for i, nm in enumerate(names):
        if nm == "?" and charges is not None:
            w = charges[i] % 14
            cand = [k for k in range(2, 16) if (8 * k) % 14 == w]
            if not cand:
                return None
            n += cand[0]
            approx = True
            continue
        for tok in nm.replace("+", "_").split("_"):
            if tok == "A":
                n += 1
            elif tok.startswith("A^"):
                n += int(tok[2:])
            elif tok.isdigit() or tok == "":
                continue
            else:
                return None
    return (n, approx)


def simulate_class(S, sol):
    row0 = S.row(sol, 0)
    pad = 2 * A.tsim + 200
    big = np.concatenate([O.ether(S.p_left, S.lo - pad, S.lo), row0,
                          O.ether(S.p_right, S.hi, S.hi + pad)])
    x0 = S.lo - pad
    a = O.evolve(big, A.tsim)
    ty = O.types(a, x0 + A.tsim)
    rods = [t for t in ty if t[0] == "E" or t[0].startswith("E^")]
    if len(rods) != 1:
        return None, [t[0] for t in ty]
    k = 1 if rods[0][0] == "E" else int(rods[0][0][2:])
    right = [t for t in ty if t[1] > rods[0][1]]
    left = [t[0] for t in ty if t[1] < rods[0][1]]
    r = n_A([t[0] for t in right], [t[2] for t in right])
    if left or r is None:
        return None, [t[0] for t in ty]
    return (k - A.m, r[0], r[1]), [t[0] for t in ty]


def object_rows(xrow, s):
    """all W-cell rows (left ether phase 0, right phase s) that are the same
    isolated packet at another time phase / position (12 phases)."""
    W = A.WX
    pad = 80
    row = np.array([int(c) for c in xrow], np.uint8)
    full = np.concatenate([O.ether(0, -pad, 0), row, O.ether(s, W, W + pad)])
    out = set()
    for tau in range(12):
        r = O.evolve(full, tau)            # covers [-pad+tau, W+pad-tau)
        x0 = -pad + tau
        for dl in range(-pad + tau + 20, pad - tau - 20):
            # candidate: cell x of new row = r at x + dl  (x in [-14, W+14))
            xs = np.arange(-14, W + 14) + dl - x0
            if xs[0] < 0 or xs[-1] >= len(r):
                continue
            seg = r[xs]
            if not np.array_equal(seg[:14], O.ether(0, -14, 0)):
                continue
            if not np.array_equal(seg[14 + W:], O.ether(s, W, W + 14)):
                continue
            out.add(tuple(int(v) for v in seg[14:14 + W]))
    out.add(tuple(int(c) for c in xrow))
    return [list(t) for t in out]


done_s = set()
if os.path.exists(A.out):
    for l in open(A.out):
        r = json.loads(l)
        if r.get("done") and r["WX"] == A.WX and r["T2"] == A.T2 and r["cond"] == A.cond:
            done_s.add(r["s"])
for s in map(int, A.s.split(",")):
    if s in done_s:
        continue
    t0 = time.time()
    cnf, X, scenes, ys = build(s)
    xl = [X.st.lit(0, xx) for xx in range(A.WX)]
    nw = 0
    with cnf.solver() as sv:
        while nw < A.max:
            ok = sv.solve()
            if not ok:
                break
            sol = Assignment(set(l for l in sv.get_model() if l > 0))
            nw += 1
            xrow = "".join(str(sol.val(l)) for l in xl)
            d_sat = [[d for d in DSET if sol.val(ys[c][d])][0] for c in range(3)]
            sims = [simulate_class(S, sol) for S in scenes]
            res = [r for r, _ in sims]
            delta = [None if r is None else r[0] - r[1] for r in res]
            approx = any(r is not None and r[2] for r in res)
            dist = None not in delta and len(set(delta)) == 3
            rec = {"m": A.m, "WX": A.WX, "T2": A.T2, "s": s, "cond": A.cond, "i": nw,
                   "X": xrow, "d_sat": d_sat, "sim": [list(r) if r else None for r in res],
                   "types": [t for _, t in sims], "Delta": delta, "Delta_distinct": dist, "nA_approx": approx,
                   "sat_eq_sim": [bool(S.check_sat_vs_sim(sol)) for S in scenes]}
            print(json.dumps(rec), flush=True)
            with open(A.out, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
            for row in object_rows(xrow, s):           # block every phase/shift copy
                sv.add_clause([(-l if row[i] else l) for i, l in enumerate(xl)])
    rec = {"m": A.m, "WX": A.WX, "T2": A.T2, "s": s, "cond": A.cond, "done": True,
           "witnesses": nw, "exhausted": nw < A.max, "secs": round(time.time() - t0, 1)}
    print(json.dumps(rec), flush=True)
    with open(A.out, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
