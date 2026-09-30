"""Spec I (architect): a left-moving packet X (free (p, d)-train) with
    X + C2 -> C2 (unchanged, same cells) + C2' (a new C2 to its right)
= INC on a pile of cells. Slip conservation: slip(X) + 11 = 22 (mod 14),
so X must have slip 11 (pR = 11 in its canonical frame).

For each class k of X against C2 (4 classes for (30,-8), 2 for (15,-4))
the scene is C2 + X at T2 -> row exactly: ether | C2 at the SAME cells as
an undisturbed C2 at time T2 | ether | C2 (any phase/position in
[b, b + span)) | ether.
Usage: python inc.py WX p d T2 [k,...]
"""
import json, sys, time
from lib import load_gliders
from r110sat import CNF, TILE, ether_bit
from react import TrainVar, fixed_from_glider
from relay import placements_right
from scene import Scene

G = load_gliders()


def build(WX, p, d, k, T2, span=60, nclass=4):
    cnf = CNF()
    C = fixed_from_glider(cnf, G["C2"], 16)
    X = TrainVar(cnf, WX, p, d, 11, name="X")
    pl = placements_right(WX, C.W + 4, C.pR, p, nclass)
    tauX, xX = pl[k]
    S = Scene(cnf, T2, [(C, 0, 0), (X, tauX, xX)])
    ref = Scene(cnf, T2, [(C, 0, 0)])          # undisturbed C2 (all constant)
    a, b = -10, C.W + 4
    S.ether(T2, S.lo - T2, a, S.p_left)
    S.tie(ref, T2, a, b)                        # old C2 unchanged
    S.is_item(T2, b - 4, S.hi + T2, C, far_right=S.p_right)   # new C2
    return cnf, X, S


if __name__ == "__main__":
    WX, p, d, T2 = map(int, sys.argv[1:5])
    nclass = abs(p * 0 - d * 7) // 14
    ks = [int(x) for x in sys.argv[5].split(",")] if len(sys.argv) > 5 else range(nclass)
    for k in ks:
        t = time.time()
        cnf, X, S = build(WX, p, d, k, T2, nclass=nclass)
        sol = cnf.solve()
        rec = {"spec": "I", "WX": WX, "p": p, "d": d, "k": k, "T2": T2,
               "sat": sol is not None, "vars": cnf.nvars,
               "secs": round(time.time() - t, 1)}
        if sol is not None:
            rec["X"] = "".join(map(str, X.decode(sol)))
            rec["sim_ok"] = S.check_sat_vs_sim(sol)
            if not rec["sim_ok"]:
                raise AssertionError("SAT/simulation mismatch")
        print(json.dumps(rec), flush=True)
        with open("inc_results.jsonl", "a") as fh:
            fh.write(json.dumps(rec) + "\n")
