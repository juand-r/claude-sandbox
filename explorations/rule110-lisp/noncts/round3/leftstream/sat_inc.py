"""SAT: a free right-moving (p, d)-train Y (width WY, slip s) hits E^n from
the left; at T2 the row is exactly E^(n+delta) in ether (Y absorbed, nothing
else), jointly for every n in --ns (one Y for all n).
delta = +1: INC from the left (needs s = 6 by slip conservation).
Uses round-1 synth/ (read-only). Results appended to sat_inc_results.jsonl.
Usage: python sat_inc.py p d WY T2 [--ns 1,2,3] [--k 0,1,2] [--s 6]
       [--delta 1] [--front]   (--front: E^(n+delta)'s front fixed to
       the same trajectory offset for all n is NOT imposed; we report it)
"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
SYNTH = os.path.abspath(os.path.join(HERE, "..", "..", "synth"))
sys.path.insert(0, SYNTH)
os.chdir(SYNTH)       # synth modules load data relative to cwd
from r110sat import CNF, TILE, make_window   # noqa: E402
from react import TrainVar                   # noqa: E402
from scene import Scene                      # noqa: E402
from classes import placements_by_class, n_classes   # noqa: E402
from en import en_item                       # noqa: E402

MARGIN = 24
OUT = os.path.join(HERE, "sat_inc_results.jsonl")


def build(p, d, WY, T2, ns, k, s, delta, gap=6):
    cnf = CNF()
    Y = TrainVar(cnf, WY, p, d, s, name="Y")
    scenes = []
    for n in ns:
        E = en_item(cnf, n)
        Eo = en_item(cnf, n + delta)
        tauE, xE = placements_by_class(Y, (0, 0), E, Y.W + gap)[k]
        lo, hi = 0, xE + E.W + tauE
        win = make_window(T2, lo, hi, -4 / 15, d / p, margin=MARGIN)
        S = Scene(cnf, T2, [(Y, 0, 0), (E, tauE, xE)], window=win)
        S.is_item(T2, S.lo - T2, S.hi + T2, Eo, far_left=S.p_left,
                  far_right=S.p_right)
        scenes.append(S)
    return cnf, Y, scenes


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("p", type=int); ap.add_argument("d", type=int)
    ap.add_argument("WY", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("--ns", default="1,2,3")
    ap.add_argument("--k", default=None)
    ap.add_argument("--s", type=int, default=6)
    ap.add_argument("--delta", type=int, default=1)
    ap.add_argument("--gap", type=int, default=6)
    A = ap.parse_args()
    ns = [int(v) for v in A.ns.split(",")]
    nc = n_classes((15, -4), (A.p, A.d))
    ks = range(nc) if A.k is None else map(int, A.k.split(","))
    for k in ks:
        t = time.time()
        cnf, Y, scenes = build(A.p, A.d, A.WY, A.T2, ns, k, A.s, A.delta, A.gap)
        sol = cnf.solve()
        rec = {"p": A.p, "d": A.d, "WY": A.WY, "T2": A.T2, "ns": ns, "k": k,
               "s": A.s, "delta": A.delta, "gap": A.gap,
               "sat": sol is not None, "secs": round(time.time() - t, 1)}
        if sol is not None:
            rec["Y"] = "".join(map(str, Y.decode(sol)))
            rec["sim_ok"] = all(S.check_sat_vs_sim(sol) for S in scenes)
            rec["rows0"] = ["".join(map(str, S.row(sol, 0))) for S in scenes]
            rec["frames"] = [(S.lo, S.p_left, S.p_right) for S in scenes]
            if not rec["sim_ok"]:
                raise AssertionError("SAT/sim mismatch")
        print(json.dumps({q: v for q, v in rec.items() if q != "rows0"}), flush=True)
        with open(OUT, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
