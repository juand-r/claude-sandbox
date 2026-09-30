"""Perfect phase-free mirror: free A-train H_in ((3,2), width WI) from the
left hits a free stationary wall O (width W) and comes back as a free
B-train H_out ((4,-2), width WO), with O restored EXACTLY (same object,
any position/phase):   H_in + O -> O + H_out.
Slip conservation: slip(H_in) = slip(H_out) (even, since 8n = 6m mod 14
means n + m = 0 mod 7 for n A's and m B's).
One collision class (A-trains vs period-7 objects), so placement-free.
Usage: python mirror.py WI WO W T2 [--pR list] [--s list]
"""
import argparse, json, time
from r110sat import CNF, TILE
from react import ObjectVar, TrainVar, Reaction, verify_reaction

ap = argparse.ArgumentParser()
ap.add_argument("WI", type=int); ap.add_argument("WO", type=int)
ap.add_argument("W", type=int); ap.add_argument("T2", type=int)
ap.add_argument("--pR", default=",".join(map(str, range(TILE))))
ap.add_argument("--s", default="0,2,4,6,8,10,12")
a = ap.parse_args()
for pR in map(int, a.pR.split(",")):
    for s in map(int, a.s.split(",")):
        t = time.time()
        cnf = CNF()
        O = ObjectVar(cnf, a.W, pR, name="O")
        Hin = TrainVar(cnf, a.WI, 3, 2, s, name="Hin")
        Hout = TrainVar(cnf, a.WO, 4, -2, s, name="Hout")
        r = Reaction(cnf, O, Hin, a.T2, left=("is", Hout), middle=("is", O),
                     right=None, mL=6, mR=6)
        sol = cnf.solve()
        rec = {"WI": a.WI, "WO": a.WO, "W": a.W, "T2": a.T2, "pR": pR,
               "slip": s, "sat": sol is not None, "secs": round(time.time() - t, 1)}
        if sol is not None:
            v = verify_reaction(r, sol)
            rec["verify_ok"] = bool(v["ok"])
            for it in (O, Hin, Hout):
                rec[it.name] = "".join(map(str, it.decode(sol)))
            rec["row0"] = "".join(map(str, r.initial_row(sol)))
            rec["lo"], rec["pfl"], rec["pfr"] = r.lo, r.pfl, r.pfr
            if not v["ok"]:
                raise AssertionError(v)
        print(json.dumps({k: v for k, v in rec.items() if k != "row0"}), flush=True)
        with open("mirror_results.jsonl", "a") as fh:
            fh.write(json.dumps(rec) + "\n")
