"""Transport through E_n counters (scholar's one-glider unary counter):
a free train Y crosses E_n for EVERY n in a list, re-emerging identical
(any displacement), each E_n surviving as itself; with --exact the E_n must
be exactly undisturbed (same trajectory and phase), so the counter's DEC
class is unaffected.
Y from the right: (4,-2) B-trains (single class vs E_n) or other left-
movers faster than -4/15; Y from the left: (3,2) A-trains (3 classes).
Usage: python encross.py p d WY T2 [--ns 1,2,3] [--k list] [--s list] [--exact]
"""
import argparse, json, time
from r110sat import CNF, TILE, make_window
from react import TrainVar
from scene import Scene
from classes import placements_by_class, n_classes
from en import en_item


MARGIN = 24   # window slack (cells) around the moving pair


def build(p, d, WY, T2, ns, k, s, exact):
    cnf = CNF()
    Y = TrainVar(cnf, WY, p, d, s, name="Y")
    scenes = []
    for n in ns:
        E = en_item(cnf, n)
        if d < 0:
            tau, x = placements_by_class(E, (0, 0), Y, E.W + 6)[k]
            lo, hi = 0, x + Y.W + tau
            win = make_window(T2, lo, hi, d / p, -4 / 15, margin=MARGIN)
            S = Scene(cnf, T2, [(E, 0, 0), (Y, tau, x)], window=win)
        else:
            raise NotImplementedError("A-trains from the left: TODO")
        oE = Scene.undisturbed(E, 0, 0, T2)
        oY = Scene.undisturbed(Y, tau, x, T2)
        mid = oE[1] - 8       # Y must be entirely left of E_n by T2
        S.is_item(T2, S.lo - T2, mid, Y, far_left=S.p_left)
        S.is_item(T2, mid, S.hi + T2, E, far_right=S.p_right,
                  only=oE if exact else None)
        scenes.append(S)
    return cnf, Y, scenes


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("p", type=int); ap.add_argument("d", type=int)
    ap.add_argument("WY", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("--ns", default="1,2,3")
    ap.add_argument("--k", default=None)
    ap.add_argument("--s", default=",".join(map(str, range(TILE))))
    ap.add_argument("--exact", action="store_true")
    A = ap.parse_args()
    ns = [int(v) for v in A.ns.split(",")]
    nc = n_classes((15, -4), (A.p, A.d))
    for k in (range(nc) if A.k is None else map(int, A.k.split(","))):
        for s in map(int, A.s.split(",")):
            t = time.time()
            cnf, Y, scenes = build(A.p, A.d, A.WY, A.T2, ns, k, s, A.exact)
            sol = cnf.solve()
            rec = {"spec": "encross", "p": A.p, "d": A.d, "WY": A.WY, "T2": A.T2,
                   "ns": ns, "k": k, "s": s, "exact": A.exact,
                   "sat": sol is not None, "secs": round(time.time() - t, 1)}
            if sol is not None:
                rec["Y"] = "".join(map(str, Y.decode(sol)))
                rec["sim_ok"] = all(S.check_sat_vs_sim(sol) for S in scenes)
                rec["rows0"] = ["".join(map(str, S.row(sol, 0))) for S in scenes]
                rec["frames"] = [(S.lo, S.p_left, S.p_right) for S in scenes]
                if not rec["sim_ok"]:
                    raise AssertionError("SAT/sim mismatch")
            print(json.dumps({q: v for q, v in rec.items() if q != "rows0"}), flush=True)
            with open("encross_results.jsonl", "a") as fh:
                fh.write(json.dumps(rec) + "\n")
