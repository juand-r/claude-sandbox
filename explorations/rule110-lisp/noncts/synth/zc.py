"""Architect's zero test (session ~15:10): packet K (free Ebar-speed
(30,-8)-train, width WK, slip s) arriving from the right turns the
value-0 compound F_19_F into F_19_F (any displacement) + ONE stationary
messenger (nonempty period-7 object), with (default) nothing else, or
(--debris) additionally any Ebar-speed train further left.
The identity requirement on a separated F pair is checked afterwards.
Usage: python zc.py WK T2 [--s list] [--k list] [--debris]
"""
import argparse, json, time
from lib import load_gliders
from r110sat import CNF, TILE, make_window
from react import TrainVar, fixed_from_glider
from scene import Scene, BAND
from classes import placements_by_class

G = load_gliders()
# architect's value-0 compound (architect/zero_state.json), NOT the same
# glider as the library's F_19_F (different phase relation of the two F's)
import os
from lib import Glider
_Z = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "architect",
                  "zero_state.json")
if os.path.exists(_Z):
    G["F_19_F#3"] = Glider(json.load(open(_Z))["compound"])


def build(WK, T2, s, k, debris=False, target="F_19_F#3", fixedK=None,
          pair_k=None):
    cnf = CNF()
    Cmp = fixed_from_glider(cnf, G[target], 52)
    if fixedK is not None:
        from specz import packet_item
        K = packet_item(cnf, fixedK, 48, "K")
    else:
        K = TrainVar(cnf, WK, 30, -8, s, name="K")
    tau, x = placements_by_class(Cmp, (0, 0), K, Cmp.W + 4)[k]
    lo, hi = 0, x + K.W + tau
    T = T2 + (30 if debris else 7)
    win = make_window(T, lo, hi, -8 / 30, 0.0, margin=24)
    S = Scene(cnf, T, [(Cmp, 0, 0), (K, tau, x)], window=win)
    # meeting point: compound right edge (Cmp.W - t/9) meets K's left edge
    # (x - tau - 4t/15)
    tm = (x - tau - Cmp.W) / (4 / 15 - 1 / 9)
    xm = int(Cmp.W - tm / 9)
    oC = Scene.undisturbed(Cmp, 0, 0, T2)
    # messenger region: from well right of the (possibly displaced)
    # compound to the right of the estimated meeting point
    a, b = oC[1] + Cmp.extent(oC[0])[1] + 30, xm + 40
    if b - a < 30:
        raise ValueError("T2 too small to separate compound and messenger")
    bl = S.ether(T2, a - BAND, a)
    S.ether(T2, b, b + BAND)
    S.ether(T2, b + BAND, S.hi + T2, S.p_right)
    S.invariant(T2, a - 7, b + 7, 7, 0)
    for ph in range(TILE):
        S.nonempty(T2, a, b, ph, guard=bl[ph])
    c0 = oC[1] - 60
    S.is_item(T2, c0, a - BAND, Cmp, window=(oC[1] - 50, oC[1] + 16))
    if debris:
        # left of the compound: any Ebar-speed train (possibly empty)
        S.invariant(T2, S.lo - T2 - 30, c0 - 10, 30, -8)
        S.ether(T2, c0 - 10, c0, None)
    else:
        S.ether(T2, S.lo - T2, c0, S.p_left)
    if pair_k is not None:
        # (ii) K crosses a separated value-1 pair: pair survives with the
        # same seed difference (any common displacement), K's output is an
        # Ebar-speed train (possibly K itself) on the left
        from specz import packet_item
        Pr = packet_item(cnf, [("F", 0, 0), ("F", 24, 31)], 72, "pair")
        tau2, x2 = placements_by_class(Pr, (0, 0), K, Pr.W + 4)[pair_k]
        lo2, hi2 = 0, x2 + K.W + tau2
        T2b = T2
        win2 = make_window(T2b + 30, lo2, hi2, -8 / 30, 0.0, margin=24)
        S2 = Scene(cnf, T2b + 30, [(Pr, 0, 0), (K, tau2, x2)], window=win2)
        oP = Scene.undisturbed(Pr, 0, 0, T2b)
        e0, e1 = Pr.extent(oP[0])
        cut = oP[1] + e0 - 30
        S2.is_item(T2b, cut, S2.hi + T2b, Pr, far_right=S2.p_right,
                   window=(oP[1] - 40, oP[1] + 20))
        S2.invariant(T2b, S2.lo - T2b - 30, cut - 16, 30, -8)
        S2.ether(T2b, cut - 16, cut, None)
        S.extra = S2
    return cnf, K, S


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("WK", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("--s", default=",".join(map(str, range(TILE))))
    ap.add_argument("--k", default="0")
    ap.add_argument("--debris", action="store_true")
    ap.add_argument("--pair", default=None, help="pair-scene classes, e.g. 0,1,...")
    A = ap.parse_args()
    pks = [None] if A.pair is None else [int(v) for v in A.pair.split(",")]
    for k in map(int, A.k.split(",")):
      for pk in pks:
        for s in map(int, A.s.split(",")):
            t = time.time()
            cnf, K, S = build(A.WK, A.T2, s, k, A.debris, pair_k=pk)
            sol = cnf.solve()
            rec = {"spec": "zc", "WK": A.WK, "T2": A.T2, "s": s, "k": k, "pair_k": pk,
                   "debris": A.debris, "sat": sol is not None,
                   "secs": round(time.time() - t, 1)}
            if sol is not None:
                rec["K"] = "".join(map(str, K.decode(sol)))
                rec["sim_ok"] = S.check_sat_vs_sim(sol) and (
                    not hasattr(S, "extra") or S.extra.check_sat_vs_sim(sol))
                rec["row0"] = "".join(map(str, S.row(sol, 0)))
                rec["lo"], rec["pl"], rec["pr"] = S.lo, S.p_left, S.p_right
                if not rec["sim_ok"]:
                    raise AssertionError("SAT/sim mismatch")
            print(json.dumps({q: v for q, v in rec.items() if q != "row0"}), flush=True)
            with open("zc_results.jsonl", "a") as fh:
                fh.write(json.dumps(rec) + "\n")
