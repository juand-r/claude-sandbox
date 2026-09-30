"""k-eaters (for "skip k" = delete the next k stream packets):
stationary objects X_n, ..., X_1 (free, width <= W) with
    X_i + P -> X_{i-1}  (any displacement)      for i = n..2
    X_1 + P -> nothing (pure ether)
for a fixed left-moving packet P (library glider, e.g. Ebar) arriving
from the right in class k (all classes tried). Slip forces
s(X_i) = -i s(P) (mod 14).
Usage: python eater.py P n W T2 [--k list]
"""
import argparse, json, time
from lib import load_gliders
from r110sat import CNF, TILE
from react import ObjectVar, fixed_from_glider
from scene import Scene, BAND
from classes import placements_by_class, n_classes

G = load_gliders()


def build(Pn, n, W, T2, k):
    cnf = CNF()
    sP = G[Pn].slip
    X = [None] + [ObjectVar(cnf, W, (-i * sP) % TILE, name=f"X{i}")
                  for i in range(1, n + 1)]
    scenes = []
    for i in range(1, n + 1):
        P = fixed_from_glider(cnf, G[Pn], 24)
        tau, x = placements_by_class(X[i], (0, 0), P, W + 6)[k]
        S = Scene(cnf, T2, [(X[i], 0, 0), (P, tau, x)])
        if i == 1:
            S.ether(T2, S.lo - T2, S.hi + T2, S.p_left)
        else:
            S.is_item(T2, S.lo - T2, S.hi + T2, X[i - 1], far_left=S.p_left)
        scenes.append(S)
    return cnf, X, scenes


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("P"); ap.add_argument("n", type=int)
    ap.add_argument("W", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("--k", default=None)
    A = ap.parse_args()
    nc = n_classes((7, 0), (G[A.P].p, G[A.P].d))
    for k in (range(nc) if A.k is None else map(int, A.k.split(","))):
        t = time.time()
        cnf, X, scenes = build(A.P, A.n, A.W, A.T2, k)
        sol = cnf.solve()
        rec = {"spec": "eater", "P": A.P, "n": A.n, "W": A.W, "T2": A.T2,
               "k": k, "sat": sol is not None, "secs": round(time.time() - t, 1)}
        if sol is not None:
            rec["X"] = ["".join(map(str, x.decode(sol))) for x in X[1:]]
            rec["slips"] = [x.pR for x in X[1:]]
            rec["sim_ok"] = all(S.check_sat_vs_sim(sol) for S in scenes)
            if not rec["sim_ok"]:
                raise AssertionError("SAT/sim mismatch")
        print(json.dumps(rec), flush=True)
        with open("eater_results.jsonl", "a") as fh:
            fh.write(json.dumps(rec) + "\n")
