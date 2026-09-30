"""INC on a moving store (architect's F memory): a command packet P
(free (p, d)-train from the right) meets a glider X (default F) and
leaves X untouched plus a NEW copy X' (a second X) -- i.e. pushes one
more element onto the store:    P + X -> X (same cells as undisturbed) + X'
Slip: slip(P) = slip(X) (forced). The copy is required on the RIGHT of
the old X (the store's top, where the next packet arrives) or, with
--left, on the left. One collision class k at a time.
Usage: python copyspec.py WP p d T2 [--target F] [--k list] [--left]
"""
import argparse, json, time
from lib import load_gliders
from r110sat import CNF, TILE
from react import TrainVar, fixed_from_glider
from scene import Scene, BAND
from classes import placements_by_class, n_classes

G = load_gliders()


def build(WP, p, d, k, T2, target="F", left=False, margin=40, gap=None):
    cnf = CNF()
    X = fixed_from_glider(cnf, G[target], 24)
    P = TrainVar(cnf, WP, p, d, X.pR, name="P")
    pl = placements_by_class(X, (0, 0), P, X.W + 6)
    tau, x = pl[k]
    S = Scene(cnf, T2, [(X, 0, 0), (P, tau, x)])
    ref = Scene(cnf, T2, [(X, 0, 0)])
    # old X at T2 (undisturbed): row t0, shift d0
    t0, d0 = Scene.undisturbed(X, 0, 0, T2)
    e0, e1 = X.extent(t0)
    a, b = d0 + e0 - margin, d0 + e1 + margin
    only = None
    if gap is not None:
        # the new copy in the same phase as the old one, `gap` cells away
        only = (t0, d0 + (-gap if left else gap))
        if left:
            a = min(a, only[1] + e1 + BAND)
        else:
            b = min(b, only[1] + e0 - BAND)
    S.tie(ref, T2, a, b)                       # old X untouched
    if left:
        S.is_item(T2, S.lo - T2, a, X, far_left=S.p_left, only=only)
        S.ether(T2, b, S.hi + T2, S.p_right)
    else:
        S.ether(T2, S.lo - T2, a, S.p_left)
        S.is_item(T2, b, S.hi + T2, X, far_right=S.p_right, only=only)
    return cnf, P, S, len(pl)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("WP", type=int); ap.add_argument("p", type=int)
    ap.add_argument("d", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("--target", default="F")
    ap.add_argument("--k", default=None)
    ap.add_argument("--left", action="store_true")
    ap.add_argument("--gap", type=int, default=None)
    A = ap.parse_args()
    n = n_classes((G[A.target].p, G[A.target].d), (A.p, A.d))
    for k in (range(n) if A.k is None else map(int, A.k.split(","))):
        t = time.time()
        cnf, P, S, _ = build(A.WP, A.p, A.d, k, A.T2, A.target, A.left,
                             gap=A.gap)
        sol = cnf.solve()
        rec = {"spec": "INC-copy", "target": A.target, "WP": A.WP, "p": A.p,
               "d": A.d, "k": k, "T2": A.T2, "left": A.left, "gap": A.gap,
               "sat": sol is not None, "secs": round(time.time() - t, 1)}
        if sol is not None:
            rec["P"] = "".join(map(str, P.decode(sol)))
            rec["sim_ok"] = S.check_sat_vs_sim(sol)
            rec["row0"] = "".join(map(str, S.row(sol, 0)))
            rec["lo"], rec["pl"], rec["pr"] = S.lo, S.p_left, S.p_right
            if not rec["sim_ok"]:
                raise AssertionError("SAT/sim mismatch")
        print(json.dumps({q: v for q, v in rec.items() if q != "row0"}), flush=True)
        with open("copy_results.jsonl", "a") as fh:
            fh.write(json.dumps(rec) + "\n")
