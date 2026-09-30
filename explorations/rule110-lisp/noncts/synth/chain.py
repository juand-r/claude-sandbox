"""Multi-cell crossing (scholar's request): free A-trains Q0, Q1, ..., Qn
with
   Q_i + C -> C (same glider, any displacement) + Q_{i+1},  i < n
and Q_n nonempty. Then Q0 crosses n cells in a row (A vs period-7
objects is single-class, so cell spacing does not matter once each
reaction has finished). All Q_i have the same slip s (cells restored).
Usage: python chain.py CELLS W0,W1,..,Wn T2 [--s list]
  CELLS: comma list of cell glider names, e.g. C2,C2
"""
import argparse, json, time
from lib import load_gliders
from r110sat import CNF
from react import TrainVar, Reaction, fixed_from_glider, verify_reaction

G = load_gliders()
ap = argparse.ArgumentParser()
ap.add_argument("cells"); ap.add_argument("widths"); ap.add_argument("T2", type=int)
ap.add_argument("--s", default="8,2,10,4,12,6,0")
A = ap.parse_args()
cells = A.cells.split(",")
Ws = [int(w) for w in A.widths.split(",")]
assert len(Ws) == len(cells) + 1
for s in map(int, A.s.split(",")):
    t = time.time()
    cnf = CNF()
    Q = [TrainVar(cnf, W, 3, 2, s, name=f"Q{i}") for i, W in enumerate(Ws)]
    R = []
    for i, c in enumerate(cells):
        obj = fixed_from_glider(cnf, G[c], 16)
        right = ("is", Q[i + 1]) if i + 1 < len(cells) else ("train", 3, 2)
        R.append(Reaction(cnf, obj, Q[i], A.T2, left=None, middle=("is", obj),
                          right=right, mL=6, mR=16))
    sol = cnf.solve()
    rec = {"cells": cells, "widths": Ws, "T2": A.T2, "slip": s,
           "sat": sol is not None, "secs": round(time.time() - t, 1)}
    if sol is not None:
        rec["Q"] = ["".join(map(str, q.decode(sol))) for q in Q]
        vs = [verify_reaction(r, sol) for r in R]
        rec["verify_ok"] = all(bool(v["ok"]) for v in vs)
        rec["rows0"] = ["".join(map(str, r.initial_row(sol))) for r in R]
        rec["frames"] = [(r.lo, r.pfl, r.pfr) for r in R]
        if not rec["verify_ok"]:
            raise AssertionError([{k: v[k] for k in v} for v in vs])
    print(json.dumps({k: v for k, v in rec.items() if k != "rows0"}), flush=True)
    with open("chain_results.jsonl", "a") as fh:
        fh.write(json.dumps(rec) + "\n")
