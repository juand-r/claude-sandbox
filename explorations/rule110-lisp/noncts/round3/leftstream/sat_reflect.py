"""SAT: reflection at R1's inner (left) face. A free right-moving (3,2)
train X hits E^n from the left; jointly for n in --ns the row at T2 is
exactly  Y | E^(n-k)  with Y a FIXED library left-mover (default Bbar).
(E^n from en.py: front-anchored, so joint n is a valid constraint.)
Slip: s_X = slip(Y) - 6k (mod 14).
Usage: python sat_reflect.py WX k T2 [--Y Bbar] [--ns 3,4] [--kX 0,1,2]
Results appended to sat_reflect_results.jsonl."""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sat_shuttle import scene_R1, CNF, TILE, TrainVar   # noqa: E402 (chdirs to synth)
from react import fixed_from_glider                      # noqa: E402
from lib import load_gliders                             # noqa: E402

G = load_gliders()
OUT = os.path.join(HERE, "sat_reflect_results.jsonl")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("WX", type=int); ap.add_argument("k", type=int)
    ap.add_argument("T2", type=int)
    ap.add_argument("--Y", default="Bbar")
    ap.add_argument("--ns", default="3,4")
    ap.add_argument("--kX", default="0,1,2")
    A = ap.parse_args()
    ns = [int(v) for v in A.ns.split(",")]
    for kX in map(int, A.kX.split(",")):
        t = time.time()
        cnf = CNF()
        Y = fixed_from_glider(cnf, G[A.Y], 40)
        sX = (Y.pR - 6 * A.k) % TILE
        X = TrainVar(cnf, A.WX, 3, 2, sX, name="X")
        scenes = [scene_R1(cnf, X, Y, n, A.k, kX, A.T2) for n in ns]
        sol = cnf.solve()
        rec = {"WX": A.WX, "k": A.k, "T2": A.T2, "Y": A.Y, "sX": sX, "ns": ns,
               "kX": kX, "sat": sol is not None, "secs": round(time.time() - t, 1)}
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
