"""SAT: does a right-moving (3,2) train cross the E^n rod?  Free train X
(width WX, slip s) hits E^n from the left; jointly for n in --ns the row at
T2 is exactly  E^n (any position) | X'  with X' a free (3,2) train of
width WO and the same slip (mode 'conv'), or X' = X itself (mode 'same').
E^n from en.py (front-anchored, so one placement = one class for all n).
Usage: python sat_cross.py WX WO T2 MODE [--ns 2,3] [--s 0..13] [--k 0,1,2]
Results: sat_cross_results.jsonl (resumable: finished instances skipped)."""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sat_inc import CNF, TILE, TrainVar, Scene, make_window, placements_by_class, en_item, MARGIN  # noqa

OUT = os.path.join(HERE, "sat_cross_results.jsonl")


def build(WX, WO, T2, mode, ns, s, k, gap=6):
    cnf = CNF()
    X = TrainVar(cnf, WX, 3, 2, s, name="X")
    Xo = X if mode == "same" else TrainVar(cnf, WO, 3, 2, s, name="Xo")
    scenes = []
    for n in ns:
        E = en_item(cnf, n)
        tauE, xE = placements_by_class(X, (0, 0), E, X.W + gap)[k]
        lo, hi = 0, xE + E.W + tauE
        win = make_window(T2, lo, hi, -4 / 15, 2 / 3, margin=MARGIN)
        S = Scene(cnf, T2, [(X, 0, 0), (E, tauE, xE)], window=win)
        back = xE + E.W - 4 * T2 / 15
        mid = int(back + 12)
        S.is_item(T2, S.lo - T2, mid, E, far_left=S.p_left)
        S.is_item(T2, mid, S.hi + T2, Xo, far_right=S.p_right)
        scenes.append(S)
    return cnf, X, Xo, scenes


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("WX", type=int); ap.add_argument("WO", type=int)
    ap.add_argument("T2", type=int); ap.add_argument("mode")
    ap.add_argument("--ns", default="2,3")
    ap.add_argument("--s", default=",".join(map(str, range(14))))
    ap.add_argument("--k", default="0,1,2")
    A = ap.parse_args()
    ns = [int(v) for v in A.ns.split(",")]
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            r = json.loads(l)
            done.add((r["WX"], r["WO"], r["T2"], r["mode"], tuple(r["ns"]), r["s"], r["k"]))
    for s in map(int, A.s.split(",")):
        for k in map(int, A.k.split(",")):
            key = (A.WX, A.WO, A.T2, A.mode, tuple(ns), s, k)
            if key in done:
                continue
            t = time.time()
            cnf, X, Xo, scenes = build(A.WX, A.WO, A.T2, A.mode, ns, s, k)
            sol = cnf.solve()
            rec = dict(zip(("WX", "WO", "T2", "mode", "ns", "s", "k"), key))
            rec["ns"] = ns
            rec.update(sat=sol is not None, secs=round(time.time() - t, 1))
            if sol is not None:
                rec["X"] = "".join(map(str, X.decode(sol)))
                rec["Xo"] = "".join(map(str, Xo.decode(sol)))
                rec["sim_ok"] = all(S.check_sat_vs_sim(sol) for S in scenes)
                rec["rows0"] = ["".join(map(str, S.row(sol, 0))) for S in scenes]
                rec["frames"] = [(S.lo, S.p_left, S.p_right) for S in scenes]
                if not rec["sim_ok"]:
                    raise AssertionError("SAT/sim mismatch")
            print(json.dumps({q: v for q, v in rec.items() if q != "rows0"}), flush=True)
            with open(OUT, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
