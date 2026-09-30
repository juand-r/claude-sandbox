"""Hard gate at G speed (collider's request): a free (42,-14) object H
(width WH, slip 6) that absorbs the zero-answer A cleanly:
    A + H -> GB4 (the NOP packet)     or    A + H -> nothing
(slip: 8 + 6 = 0 = slip(GB4)). A comes from the left, H from the right.
Classes of A vs G-speed: |det|/14 = 9; with a FREE H the class index is not
an anchor (H can shift inside its window), so k only varies the start.
Usage: python hardgate.py WH T2 MODE [--k list]   MODE: none | GB4
"""
import argparse, json, time
from lib import load_gliders
from r110sat import CNF, make_window
from react import TrainVar, fixed_from_glider
from scene import Scene
from classes import placements_by_class

G = load_gliders()


def build(WH, T2, mode, k, slip=6):
    cnf = CNF()
    A = fixed_from_glider(cnf, G["A"], 8)
    H = TrainVar(cnf, WH, 42, -14, slip, name="H")
    tau, x = placements_by_class(A, (0, 0), H, A.W + 4)[k]
    lo, hi = 0, x + H.W + tau
    T = T2 + (42 if mode == "gtrain" else 0)
    win = make_window(T, lo, hi, -14 / 42, 2 / 3, margin=20)
    S = Scene(cnf, T, [(A, 0, 0), (H, tau, x)], window=win)
    if mode == "gtrain":
        # everything left at T2 is one G-speed train (A absorbed, H changed)
        S.invariant(T2, S.lo - T2 - 42, S.hi + T2 + 14, 42, -14)
    elif mode == "none":
        S.ether(T2, S.lo - T2, S.hi + T2, S.p_left)
    else:
        S.is_item(T2, S.lo - T2, S.hi + T2, fixed_from_glider(cnf, G["GB4"], 48),
                  far_left=S.p_left)
    return cnf, H, S


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("WH", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("mode"); ap.add_argument("--k", default="0,1,2")
    ap.add_argument("--slips", default="6")
    a = ap.parse_args()
    for k in map(int, a.k.split(",")):
      for slip in map(int, a.slips.split(",")):
        t = time.time()
        cnf, H, S = build(a.WH, a.T2, a.mode, k, slip)
        sol = cnf.solve()
        rec = {"spec": "hardgate", "WH": a.WH, "T2": a.T2, "mode": a.mode, "k": k, "slip": slip,
               "sat": sol is not None, "secs": round(time.time() - t, 1)}
        if sol is not None:
            rec["H"] = "".join(map(str, H.decode(sol)))
            rec["sim_ok"] = S.check_sat_vs_sim(sol)
            rec["row0"] = "".join(map(str, S.row(sol, 0)))
            rec["lo"], rec["pl"], rec["pr"] = S.lo, S.p_left, S.p_right
            if not rec["sim_ok"]:
                raise AssertionError("SAT/sim mismatch")
        print(json.dumps({q: v for q, v in rec.items() if q != "row0"}), flush=True)
        with open("hardgate_results.jsonl", "a") as fh:
            fh.write(json.dumps(rec) + "\n")
