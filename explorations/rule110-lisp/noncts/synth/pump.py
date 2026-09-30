"""Can a crossing packet PUMP a two-marker distance register?
(architect's "no winding" result covers single gliders; this covers free
multi-glider packets.)
Markers: two C1 (fixed) at pieces (0, 0) and (0, D0). Packet P: free
(30,-8)-train (width WP, slip s) arriving from the right in class k
against the right marker. Required at T2: P re-emerged (any position/
phase) left of both markers, both markers are C1 again (any displacement),
nothing else; and (pump) the change of the marker distance
    Delta = delta_2 - delta_1  (spacetime, t mod 7)
is NONZERO and lies in M = <(7,0), (30,-8)>, so that an identical later
packet sees the same geometry and pumps again (unbounded counter by pure
crossings). --nopump drops the pump condition (positive control).
Usage: python pump.py WP T2 [--D0 list] [--k list] [--s list] [--nopump]
       [--fixedP NAME]
"""
import argparse, json, time
from lib import load_gliders
from r110sat import CNF, TILE
from react import TrainVar, fixed_from_glider
from scene import Scene
from classes import placements_by_class

G = load_gliders()


def in_M(dt, dx):
    # (dt mod 7, dx) in <(7,0),(30,-8)>  <=>  dx = -8 j and dt = 2 j (mod 7)
    if dx % 8:
        return False
    j = -dx // 8
    return (dt - 2 * j) % 7 == 0


def build(WP, T2, D0, k, s, pump=True, fixedP=None, win=24):
    cnf = CNF()
    M1 = fixed_from_glider(cnf, G["C1"], 16)
    M2 = fixed_from_glider(cnf, G["C1"], 16)
    P = fixed_from_glider(cnf, G[fixedP], 24) if fixedP else \
        TrainVar(cnf, WP, 30, -8, s, name="P")
    tau, x = placements_by_class(M2, (0, D0), P, D0 + M2.W + 6)[k]
    S = Scene(cnf, T2, [(M1, 0, 0), (M2, 0, D0), (P, tau, x)])
    mid = D0 // 2 + 8
    a = -win
    o1 = S.is_item(T2, a, mid, M1, window=(-win, win))
    o2 = S.is_item(T2, mid, S.hi + T2, M2, far_right=S.p_right,
                   window=(D0 - win, D0 + win))
    S.is_item(T2, S.lo - T2, a, P, far_left=S.p_left)
    if pump:
        bad = 0
        for (t1, d1), v1 in o1:
            for (t2, d2), v2 in o2:
                # marker i displacement: time (T2 - tau_i) - 0, space delta_i - x_i
                dt = ((T2 - t2) - (T2 - t1)) % 7
                dx = (d2 - D0) - (d1 - 0)
                if dx == 0 and dt == 0 or not in_M(dt, dx):
                    cnf.add([-v1, -v2]); bad += 1
    return cnf, P, S, o1, o2


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("WP", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("--D0", default="37,51,65,79")
    ap.add_argument("--k", default="0,1,2,3")
    ap.add_argument("--s", default=",".join(map(str, range(TILE))))
    ap.add_argument("--nopump", action="store_true")
    ap.add_argument("--fixedP", default=None)
    A = ap.parse_args()
    for D0 in map(int, A.D0.split(",")):
        for k in map(int, A.k.split(",")):
            for s in (map(int, A.s.split(",")) if not A.fixedP else [None]):
                t = time.time()
                cnf, P, S, o1, o2 = build(A.WP, A.T2, D0, k, s, not A.nopump, A.fixedP)
                sol = cnf.solve()
                rec = {"spec": "pump", "WP": A.WP, "T2": A.T2, "D0": D0, "k": k,
                       "s": s, "pump": not A.nopump, "fixedP": A.fixedP,
                       "sat": sol is not None, "secs": round(time.time() - t, 1)}
                if sol is not None:
                    rec["m1"] = [o for o, v in o1 if sol.val(v)][0]
                    rec["m2"] = [o for o, v in o2 if sol.val(v)][0]
                    if not A.fixedP:
                        rec["P"] = "".join(map(str, P.decode(sol)))
                    rec["sim_ok"] = S.check_sat_vs_sim(sol)
                    rec["row0"] = "".join(map(str, S.row(sol, 0)))
                    rec["lo"], rec["pl"], rec["pr"] = S.lo, S.p_left, S.p_right
                    if not rec["sim_ok"]:
                        raise AssertionError("SAT/sim mismatch")
                print(json.dumps({q: v for q, v in rec.items() if q != "row0"}), flush=True)
                with open("pump_results.jsonl", "a") as fh:
                    fh.write(json.dumps(rec) + "\n")
