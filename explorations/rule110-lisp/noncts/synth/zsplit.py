"""Architect's near-miss (board, session ~18:10): the identity packet pair
turns an F pair of residue D = (19,23) into F + messengers. Missing: a
packet K that is the IDENTITY on normal pairs but turns the value-0
compound F_19_F#3 into the (19,23) pair. One CNF, shared free K:
 (a) K + compound -> F pair with seed difference (19,23) (common position
     free) [+ Ebar-speed debris on the left with --debris];
 (b) K + value-1 pair (F seeds (0,0), (24,31)) -> same pair, D unchanged,
     K's output an Ebar-speed train on the left.
Placements of K against the compound and against the pair are searched
independently (see zc.py); a hit must then be checked in one stream slot.
Usage: python zsplit.py WK T2 [--s list] [--pk list] [--debris]
"""
import argparse, json, time
from zc import G, CNF, TILE, make_window, TrainVar, fixed_from_glider, Scene, BAND, placements_by_class
from specz import packet_item


def pair_scene(cnf, K, pk, T2, seeds, name):
    Pr = packet_item(cnf, seeds, 72, name)
    tau, x = placements_by_class(Pr, (0, 0), K, Pr.W + 4)[pk]
    win = make_window(T2 + 30, 0, x + K.W + tau, -8 / 30, 0.0, margin=24)
    S = Scene(cnf, T2 + 30, [(Pr, 0, 0), (K, tau, x)], window=win)
    return Pr, S


def build(WK, T2, s, pk, debris, only_a=False):
    cnf = CNF()
    K = TrainVar(cnf, WK, 30, -8, s, name="K")
    # (a) compound -> (19,23) pair
    Cmp = fixed_from_glider(cnf, G["F_19_F#3"], 52)
    tau, x = placements_by_class(Cmp, (0, 0), K, Cmp.W + 4)[0]
    win = make_window(T2 + 30, 0, x + K.W + tau, -8 / 30, 0.0, margin=24)
    S1 = Scene(cnf, T2 + 30, [(Cmp, 0, 0), (K, tau, x)], window=win)
    Tgt = packet_item(cnf, [("F", 0, 0), ("F", 19, 23)], 72, "pair1923")
    oC = Scene.undisturbed(Cmp, 0, 0, T2)
    cut = oC[1] - 60
    S1.is_item(T2, cut, S1.hi + T2, Tgt, far_right=S1.p_right,
               window=(oC[1] - 50, oC[1] + 30))
    if debris:
        S1.invariant(T2, S1.lo - T2 - 30, cut - 16, 30, -8)
        S1.ether(T2, cut - 16, cut, None)
    else:
        S1.ether(T2, S1.lo - T2, cut, S1.p_left)
    if only_a:
        return cnf, K, [S1]
    # (b) identity on the value-1 pair
    Pr, S2 = pair_scene(cnf, K, pk, T2, [("F", 0, 0), ("F", 24, 31)], "pair1")
    oP = Scene.undisturbed(Pr, 0, 0, T2)
    e0, _ = Pr.extent(oP[0])
    c2 = oP[1] + e0 - 30
    S2.is_item(T2, c2, S2.hi + T2, Pr, far_right=S2.p_right,
               window=(oP[1] - 40, oP[1] + 20))
    S2.invariant(T2, S2.lo - T2 - 30, c2 - 16, 30, -8)
    S2.ether(T2, c2 - 16, c2, None)
    return cnf, K, [S1, S2]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("WK", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("--s", default=",".join(map(str, range(TILE))))
    ap.add_argument("--pk", default=",".join(map(str, range(12))))
    ap.add_argument("--debris", action="store_true")
    ap.add_argument("--only-a", action="store_true")
    A = ap.parse_args()
    for pk in map(int, A.pk.split(",")):
        for s in map(int, A.s.split(",")):
            t = time.time()
            cnf, K, Ss = build(A.WK, A.T2, s, pk, A.debris, A.only_a)
            sol = cnf.solve()
            rec = {"spec": "zsplit", "WK": A.WK, "T2": A.T2, "s": s, "pk": pk,
                   "only_a": A.only_a,
                   "debris": A.debris, "sat": sol is not None,
                   "secs": round(time.time() - t, 1)}
            if sol is not None:
                rec["K"] = "".join(map(str, K.decode(sol)))
                rec["sim_ok"] = all(S.check_sat_vs_sim(sol) for S in Ss)
                rec["rows0"] = ["".join(map(str, S.row(sol, 0))) for S in Ss]
                rec["frames"] = [(S.lo, S.p_left, S.p_right) for S in Ss]
                if not rec["sim_ok"]:
                    raise AssertionError("SAT/sim mismatch")
            print(json.dumps({q: v for q, v in rec.items() if q != "rows0"}), flush=True)
            with open("zsplit_results.jsonl", "a") as fh:
                fh.write(json.dumps(rec) + "\n")
