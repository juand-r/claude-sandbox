"""Can a right-moving train cross a stationary C cell cleanly?
(architect's one-way-transparency obstruction; scholar's adversarial check)

Train H: free (p, d)-train from the left (A-speed (3,2) or D-speed (10,2);
both have ONE collision class against any period-7 object, so the answer
is placement-independent). Object: C1, C2 or C3 (fixed).
Required at T2: middle = the same C glider (any position/phase), right =
  --same : exactly H again (any position/phase)
  default: any nonempty (p, d)-train
left = pure ether (nothing reflected).
Usage: python cross.py C WH p d T2 [--same] [--pR list]
"""
import argparse, json, time
from lib import load_gliders
from r110sat import CNF, TILE
from react import TrainVar, Reaction, fixed_from_glider, verify_reaction

G = load_gliders()

ap = argparse.ArgumentParser()
ap.add_argument("C"); ap.add_argument("WH", type=int)
ap.add_argument("p", type=int); ap.add_argument("d", type=int)
ap.add_argument("T2", type=int)
ap.add_argument("--same", action="store_true")
ap.add_argument("--pR", default=",".join(map(str, range(TILE))))
a = ap.parse_args()
for pR in map(int, a.pR.split(",")):
    t = time.time()
    cnf = CNF()
    obj = fixed_from_glider(cnf, G[a.C], 16)
    H = TrainVar(cnf, a.WH, a.p, a.d, pR, name="H")
    right = ("is", H) if a.same else ("train", a.p, a.d)
    r = Reaction(cnf, obj, H, a.T2, left=None, middle=("is", obj),
                 right=right, mL=6, mR=16)
    sol = cnf.solve()
    rec = {"C": a.C, "WH": a.WH, "p": a.p, "d": a.d, "T2": a.T2,
           "same": a.same, "pR": pR, "sat": sol is not None,
           "secs": round(time.time() - t, 1)}
    if sol is not None:
        v = verify_reaction(r, sol)
        rec["verify_ok"] = bool(v["ok"])
        rec["H"] = "".join(map(str, H.decode(sol)))
        if not v["ok"]:
            raise AssertionError(v)
    print(json.dumps(rec), flush=True)
    with open("cross_results.jsonl", "a") as fh:
        fh.write(json.dumps(rec) + "\n")
