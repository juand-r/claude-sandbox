"""Spec F (architect): a command packet P (free (p, d)-train, default
Ebar speed (30,-8)) arriving from the right hits an F glider (the top of
an F memory train):  P + F -> stationary messenger(s) only.
Required at T2: the whole row is ether | a nonempty period-(7,0) object
(inside [a, b)) | ether; nothing moving survives (so no right-mover, and
no left-mover that could hit other memory). One collision class at a
time (12 classes for (30,-8) vs F, 6 for (15,-4)).
Usage: python specf.py WP p d T2 [--k list] [--pR list] [--target NAME]
"""
import argparse, json, time
import numpy as np
from lib import load_gliders
from r110sat import CNF, TILE, ether_bit, neg
from react import TrainVar, fixed_from_glider
from scene import Scene, BAND
from classes import placements_by_class, n_classes

G = load_gliders()


def build(WP, p, d, pRP, k, T2, a=-70, b=40, target="F", fixedP=None):
    cnf = CNF()
    Fi = fixed_from_glider(cnf, G[target], 24)
    P = fixed_from_glider(cnf, G[fixedP], 20) if fixedP else \
        TrainVar(cnf, WP, p, d, pRP, name="P")
    pl = placements_by_class(Fi, (0, 0), P, Fi.W + 6)
    tau, x = pl[k]
    S = Scene(cnf, T2 + 7, [(Fi, 0, 0), (P, tau, x)])
    S.ether(T2, S.lo - T2, a - BAND, S.p_left)
    S.ether(T2, b + BAND, S.hi + T2, S.p_right)
    bl = S.ether(T2, a - BAND, a)
    S.ether(T2, b, b + BAND)
    S.invariant(T2, a - 7, b + 7, 7, 0)
    for ph in range(TILE):      # nonempty messenger
        S.nonempty(T2, a, b, ph, guard=bl[ph])
    return cnf, P, S, len(pl)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("WP", type=int); ap.add_argument("p", type=int)
    ap.add_argument("d", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("--k", default=None)
    ap.add_argument("--pR", default=",".join(map(str, range(TILE))))
    ap.add_argument("--target", default="F")
    ap.add_argument("--fixedP", default=None)
    a = ap.parse_args()
    ncl = n_classes(G[a.target].p and (G[a.target].p, G[a.target].d), (a.p, a.d))
    ks = range(ncl) if a.k is None else map(int, a.k.split(","))
    for k in ks:
        for pRP in map(int, a.pR.split(",")):
            t = time.time()
            cnf, P, S, n = build(a.WP, a.p, a.d, pRP, k, a.T2, target=a.target,
                                 fixedP=a.fixedP)
            sol = cnf.solve()
            rec = {"spec": "F", "target": a.target, "WP": a.WP, "p": a.p,
                   "d": a.d, "k": k, "pRP": pRP, "T2": a.T2,
                   "sat": sol is not None, "secs": round(time.time() - t, 1)}
            if sol is not None:
                rec["P"] = "".join(map(str, P.decode(sol)))
                rec["sim_ok"] = S.check_sat_vs_sim(sol)
                from identify import describe
                h, off = S.simulate(sol, a.T2 + 420)
                rec["products"] = [(x0 - off, x1 - off, per, nm) for x0, x1, per, nm, _
                                   in describe(h, a.T2 + 420, 100, h.shape[1] - 100)]
                rec["row0"] = "".join(map(str, S.row(sol, 0)))
                rec["lo"], rec["pl"], rec["pr"] = S.lo, S.p_left, S.p_right
                if not rec["sim_ok"]:
                    raise AssertionError("SAT/sim mismatch")
            print(json.dumps({q: v for q, v in rec.items() if q != "row0"}), flush=True)
            with open("specf_results.jsonl", "a") as fh:
                fh.write(json.dumps(rec) + "\n")
            if a.fixedP:
                break


if __name__ == "__main__":
    main()
