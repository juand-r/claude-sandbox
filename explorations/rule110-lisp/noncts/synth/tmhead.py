"""TM-head feasibility with train heads (all phase-free):
head H = free A-train ((3,2)-invariant, width WH) arriving from the left,
cell O = free stationary object (width W, right phase pR).
  reflect: H + O -> O' (stationary) + nonempty B-train to the left
  pass:    H + O -> O' (stationary) + nonempty A-train to the right
Any collision of an A-train with a period-7 object is in the single
class, so the result is placement-independent.
Usage: python tmhead.py MODE WH W T2 [pR,...]  (head pR looped inside)
"""
import json, sys, time
from r110sat import CNF, TILE
from react import ObjectVar, TrainVar, Reaction, verify_reaction

TR = {"A": ("train", 3, 2), "B": ("train", 4, -2)}


def run(mode, WH, W, T2, pR, pRH):
    cnf = CNF()
    obj = ObjectVar(cnf, W, pR)
    head = TrainVar(cnf, WH, 3, 2, pRH, name="H")
    left = TR["B"] if mode == "reflect" else None
    right = TR["A"] if mode == "pass" else None
    r = Reaction(cnf, obj, head, T2, left=left, right=right,
                 middle=("stationary",), mL=6, mR=6)
    t = time.time()
    sol = cnf.solve()
    rec = {"mode": mode, "WH": WH, "W": W, "T2": T2, "pR": pR, "pRH": pRH,
           "sat": sol is not None, "secs": round(time.time() - t, 1)}
    if sol is not None:
        v = verify_reaction(r, sol)
        rec["verify"] = {k: (v[k] if isinstance(v[k], str) else bool(v[k])) for k in v}
        rec["O"] = "".join(map(str, obj.decode(sol)))
        rec["H"] = "".join(map(str, head.decode(sol)))
        rec["row0"] = "".join(map(str, r.initial_row(sol)))
        rec["lo"], rec["pfl"], rec["pfr"] = r.lo, r.pfl, r.pfr
        if not v["ok"]:
            raise AssertionError(f"verification failed {v}")
    return rec


if __name__ == "__main__":
    mode, WH, W, T2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    pRs = [int(x) for x in sys.argv[5].split(",")] if len(sys.argv) > 5 else range(TILE)
    for pR in pRs:
        for pRH in range(TILE):
            rec = run(mode, WH, W, T2, pR, pRH)
            print(json.dumps({k: rec[k] for k in rec if k != "row0"}), flush=True)
            with open("tmhead_results.jsonl", "a") as fh:
                fh.write(json.dumps(rec) + "\n")
