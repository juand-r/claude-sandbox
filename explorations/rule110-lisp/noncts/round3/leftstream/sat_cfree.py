"""SAT: a CLASS-FREE operation from the left. One free (3,2) train X with
X + E^n -> E^(n+delta) exactly, for every n in --ns AND every collision
class in --ks (the same X placed in each class). E^n from en.py
(front-anchored). Usage: python sat_cfree.py WX T2 [--s 8] [--delta -1]
[--ns 2,3] [--ks 0,1,2]. Results: sat_cfree_results.jsonl."""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sat_inc import CNF, TrainVar, Scene, make_window, placements_by_class, en_item, MARGIN  # noqa

OUT = os.path.join(HERE, "sat_cfree_results.jsonl")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("WX", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("--s", type=int, default=8)
    ap.add_argument("--delta", type=int, default=-1)
    ap.add_argument("--ns", default="2,3")
    ap.add_argument("--ks", default="0,1,2")
    ap.add_argument("--gap", type=int, default=6)
    A = ap.parse_args()
    ns = [int(v) for v in A.ns.split(",")]
    ks = [int(v) for v in A.ks.split(",")]
    t = time.time()
    cnf = CNF()
    X = TrainVar(cnf, A.WX, 3, 2, A.s, name="X")
    scenes = []
    for n in ns:
        for k in ks:
            E = en_item(cnf, n)
            tauE, xE = placements_by_class(X, (0, 0), E, X.W + A.gap)[k]
            lo, hi = 0, xE + E.W + tauE
            win = make_window(A.T2, lo, hi, -4 / 15, 2 / 3, margin=MARGIN)
            S = Scene(cnf, A.T2, [(X, 0, 0), (E, tauE, xE)], window=win)
            S.is_item(A.T2, S.lo - A.T2, S.hi + A.T2, en_item(cnf, n + A.delta),
                      far_left=S.p_left, far_right=S.p_right)
            scenes.append(S)
    sol = cnf.solve()
    rec = {"WX": A.WX, "T2": A.T2, "s": A.s, "delta": A.delta, "ns": ns,
           "ks": ks, "sat": sol is not None, "secs": round(time.time() - t, 1)}
    if sol is not None:
        rec["X"] = "".join(map(str, X.decode(sol)))
        rec["sim_ok"] = all(S.check_sat_vs_sim(sol) for S in scenes)
        rec["rows0"] = ["".join(map(str, S.row(sol, 0))) for S in scenes]
        rec["frames"] = [(S.lo, S.p_left, S.p_right) for S in scenes]
        if not rec["sim_ok"]:
            raise AssertionError("SAT/sim mismatch")
    print(json.dumps({q: v for q, v in rec.items() if q != "rows0"}), flush=True)
    with open(OUT, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
