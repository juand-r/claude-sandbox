"""Perfectly transparent crossings ("ghosts"): a fixed moving glider X
passes a FREE object O and both continue EXACTLY as if the other were
absent (same cells/phases at T2 as undisturbed), or -- with --displaced
-- both survive as themselves with any displacement.
O: free stationary object (period (7,0), width W, right phase pR) or,
with --period p,d, a free moving object.
X arrives from the right if X moves left relative to O, else from the
left. Every collision class of (O, X) is tried separately.
Usage: python ghost.py X W T2 [--pR list] [--period p,d] [--displaced]
"""
import argparse, json, time
from lib import load_gliders
from r110sat import CNF, TILE
from react import ObjectVar, TrainVar, fixed_from_glider
from scene import Scene, BAND
from classes import placements_by_class, n_classes

G = load_gliders()


def build(Xn, W, T2, pR, k, period=(7, 0), displaced=False):
    cnf = CNF()
    X = fixed_from_glider(cnf, G[Xn], 24)
    O = ObjectVar(cnf, W, pR, name="O") if period == (7, 0) else \
        TrainVar(cnf, W, period[0], period[1], pR, name="O")
    vX = X.period[1] / X.period[0]
    vO = period[1] / period[0]
    if vX >= vO:
        raise NotImplementedError("X from the left: TODO")
    pl = placements_by_class(O, (0, 0), X, W + 6)
    tau, x = pl[k]
    S = Scene(cnf, T2, [(O, 0, 0), (X, tau, x)])
    # expected (undisturbed) placements at T2
    oX = Scene.undisturbed(X, tau, x, T2)
    oO = Scene.undisturbed(O, 0, 0, T2)
    mid = (oX[1] + X.W + oO[1]) // 2
    S.is_item(T2, S.lo - T2, mid, X, far_left=S.p_left,
              only=None if displaced else oX)
    S.is_item(T2, mid, S.hi + T2, O, far_right=S.p_right,
              only=None if displaced else oO)
    return cnf, O, S, len(pl)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("X"); ap.add_argument("W", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("--pR", default=",".join(map(str, range(TILE))))
    ap.add_argument("--period", default="7,0")
    ap.add_argument("--displaced", action="store_true")
    ap.add_argument("--k", default=None)
    A = ap.parse_args()
    per = tuple(map(int, A.period.split(",")))
    n = n_classes(per, (G[A.X].p, G[A.X].d))
    for pR in map(int, A.pR.split(",")):
        for k in (range(n) if A.k is None else map(int, A.k.split(","))):
            t = time.time()
            cnf, O, S, _ = build(A.X, A.W, A.T2, pR, k, per, A.displaced)
            sol = cnf.solve()
            rec = {"spec": "ghost", "X": A.X, "W": A.W, "T2": A.T2, "pR": pR,
                   "k": k, "period": per, "displaced": A.displaced,
                   "sat": sol is not None, "secs": round(time.time() - t, 1)}
            if sol is not None:
                rec["O"] = "".join(map(str, O.decode(sol)))
                rec["sim_ok"] = S.check_sat_vs_sim(sol)
                rec["row0"] = "".join(map(str, S.row(sol, 0)))
                rec["lo"], rec["pl"], rec["pr"] = S.lo, S.p_left, S.p_right
                if not rec["sim_ok"]:
                    raise AssertionError("SAT/sim mismatch")
            print(json.dumps({q: v for q, v in rec.items() if q != "row0"}), flush=True)
            with open("ghost_results.jsonl", "a") as fh:
                fh.write(json.dumps(rec) + "\n")
