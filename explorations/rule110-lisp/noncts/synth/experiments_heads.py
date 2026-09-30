"""Feasibility of phase-free TM heads: a single A (from the left) or B
(from the right) hitting a FREE stationary object O (width W, right phase
pR), with the required outcome:
  reflect: head goes back as a train of the opposite family, O -> O'
  pass:    head continues as a train of the same family, O -> O'
A and B have one collision class with any period-7 object, so the
answers do not depend on the head's placement.

Usage: python experiments_heads.py MODE HEAD W T2 [pR,...]
  MODE in reflect, pass; HEAD in A, B.
"""
import sys, time, json
from react import CNF, ObjectVar, Reaction, fixed_from_glider, verify_reaction
from lib import load_gliders

G = load_gliders()
TR = {"A": ("train", 3, 2), "B": ("train", 4, -2)}


def run(mode, head, W, T2, pR, mL=6, mR=6):
    cnf = CNF()
    obj = ObjectVar(cnf, W, pR)
    tr = fixed_from_glider(cnf, G[head], 16)
    other = "B" if head == "A" else "A"
    if head == "A":
        left = TR["B"] if mode == "reflect" else None
        right = TR["A"] if mode == "pass" else None
    else:
        right = TR["A"] if mode == "reflect" else None
        left = TR["B"] if mode == "pass" else None
    r = Reaction(cnf, obj, tr, T2, left=left, right=right,
                 middle=("stationary",), mL=mL, mR=mR)
    t = time.time()
    sol = cnf.solve()
    dt = time.time() - t
    res = {"mode": mode, "head": head, "W": W, "T2": T2, "pR": pR,
           "sat": sol is not None, "secs": round(dt, 1), "vars": cnf.nvars}
    if sol is not None:
        v = verify_reaction(r, sol)
        res["verify"] = {k: (v[k] if isinstance(v[k], str) else bool(v[k])) for k in v}
        res["O"] = "".join(map(str, obj.decode(sol)))
        res["row0"] = "".join(map(str, r.initial_row(sol)))
        res["lo"], res["pfl"], res["pfr"] = r.lo, r.pfl, r.pfr
        res["rowT2"] = "".join(map(str, r.row(sol, T2)))
        if not v["ok"]:
            raise AssertionError(f"verification failed: {v}")
    return res


if __name__ == "__main__":
    mode, head, W, T2 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    pRs = [int(x) for x in sys.argv[5].split(",")] if len(sys.argv) > 5 else range(14)
    for pR in pRs:
        res = run(mode, head, W, T2, pR)
        print(json.dumps({k: res[k] for k in res if k not in ("row0", "rowT2")}), flush=True)
        with open("heads_results.jsonl", "a") as fh:
            fh.write(json.dumps(res) + "\n")
