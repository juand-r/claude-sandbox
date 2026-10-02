"""verify 00:53 W4 target (route 23): ONE back reaction X + E^m -> E^(m+d_c) +
right-moving A-family debris only, in all THREE collision classes c, with
the three d_c pairwise distinct (charge forces them congruent mod 7).

X: free train on the (12,-6) lattice (B speed; 3 classes against E^n:
|det((15,-4),(12,-6))|/14 = 3), width WX, right ether phase s (looped).
Three scenes share X's variables; scene c places X at the class-c
representative (synth classes.placements_by_class). At T2 in scene c:
- left part: E^(m+d) for exactly one d in DSET, at the UNDISTURBED front
  placement of E^m (the rod's front cannot move: X acts at the back);
- right part (from the rod's undisturbed back + MARGIN on): invariant under
  (3,2), i.e. ether or right-moving A-lattice trains only;
- the three chosen d's pairwise distinct.
Every solution: each scene re-simulated (SAT rows = forward simulation).
Usage: python3 w4_sat.py m WX T2 out.jsonl [--s list] [--dmin -3] [--dmax 17]"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "synth")))
from r110sat import CNF, TILE, make_window, neg      # noqa: E402
from react import TrainVar                            # noqa: E402
from scene import Scene                               # noqa: E402
from classes import placements_by_class               # noqa: E402
from en import en_item                                # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("m", type=int)
ap.add_argument("WX", type=int)
ap.add_argument("T2", type=int)
ap.add_argument("out")
ap.add_argument("--s", default=",".join(map(str, range(TILE))))
ap.add_argument("--dmin", type=int, default=-3)
ap.add_argument("--dmax", type=int, default=17)
ap.add_argument("--margin", type=int, default=30)
ap.add_argument("--fixX", default=None, help="force X's row 0 (W_X cells), e.g. a Bbar, for the positive control")
ap.add_argument("--vL", type=float, default=-0.5, help="window left-edge speed")
ap.add_argument("--nodistinct", action="store_true", help="positive control: drop the pairwise-distinct condition")
A = ap.parse_args()
DSET = [d for d in range(A.dmin, A.dmax + 1) if A.m + d >= 1]

for s in map(int, A.s.split(",")):
    t0 = time.time()
    cnf = CNF()
    E = en_item(cnf, A.m)
    rods = {d: en_item(cnf, A.m + d) for d in DSET}
    X = TrainVar(cnf, A.WX, 12, -6, s, name="X")
    if A.fixX:
        assert len(A.fixX) == A.WX
        for xx, ch in enumerate(A.fixX):
            v = X.st.lit(0, xx)
            cnf.add([v] if ch == "1" else [-v])
    reps = placements_by_class(E, (0, 0), X, E.W + 6)
    assert len(reps) == 3, reps
    tE, dE = Scene.undisturbed(E, 0, 0, A.T2)
    scenes, ys = [], []
    for c, (tau, x) in enumerate(reps):
        lo, hi = 0, x + X.W + tau
        win = make_window(A.T2 + 3, lo, hi, A.vL, 2 / 3, margin=A.margin)
        S = Scene(cnf, A.T2 + 3, [(E, 0, 0), (X, tau, x)], window=win)
        L, R = S.st.bounds[A.T2]
        L3, R3 = S.st.bounds[A.T2 + 3]
        y = {}
        for d, it in rods.items():
            yv = cnf.new_var()
            y[d] = yv
            ilo, ihi = it.extent(tE)
            mid = dE + ihi + A.margin            # right of this rod's back
            # cells [L, mid) equal the rod E^(m+d) at the undisturbed placement
            for xx in range(L, mid):
                a = S.lit(A.T2, xx)
                b = it.st.lit(tE, xx - dE)
                if isinstance(b, bool):
                    cnf.add([-yv, a if b else neg(a)])
                else:
                    cnf.add([-yv, neg(a), b])
                    cnf.add([-yv, a, neg(b)])
            # right of it: (3,2)-invariant (ether or A-lattice trains only)
            for xx in range(mid, min(R, R3 - 2) - 2):
                a = S.lit(A.T2, xx)
                b = S.lit(A.T2 + 3, xx + 2)
                cnf.add([-yv, neg(a), b])
                cnf.add([-yv, a, neg(b)])
        cnf.add(list(y.values()))
        ys.append(y)
        scenes.append(S)
    for d in (DSET if not A.nodistinct else []):          # pairwise distinct
        for i in range(3):
            for j in range(i + 1, 3):
                cnf.add([-ys[i][d], -ys[j][d]])
    sol = cnf.solve()
    rec = {"m": A.m, "WX": A.WX, "T2": A.T2, "s": s, "dset": [DSET[0], DSET[-1]],
           "nodistinct": A.nodistinct, "sat": sol is not None, "secs": round(time.time() - t0, 1)}
    if sol is not None:
        rec["d"] = [[d for d in DSET if sol.val(ys[c][d])] for c in range(3)]
        rec["sim_ok"] = [bool(S.check_sat_vs_sim(sol)) for S in scenes]
        rec["X"] = "".join(map(str, X.decode(sol)))
        rec["rows0"] = ["".join(map(str, S.row(sol, 0))) for S in scenes]
        rec["frames"] = [(S.lo, S.p_left, S.p_right) for S in scenes]
    print(json.dumps({k: v for k, v in rec.items() if k != "rows0"}), flush=True)
    with open(A.out, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
