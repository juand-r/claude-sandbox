"""SAT shuttle synthesis (theory 05:49 item 3): a left-moving train Y and a
right-moving (3,2) train X such that, jointly,
  R2 side (Y from the RIGHT hits E^m's back):  Y + E^m -> E^(m+k) | X
  R1 side (X from the LEFT hits E^n's front):  X + E^n -> Y | E^(n-k)
for every m in --ms and n in --ns (one X, one Y for all). X and Y are free
trains (TrainVar); "| X" means the row region right of the counter is
exactly X (some time phase / position), likewise for Y. Slip forces
s_X = s_Y - 6k (mod 14).
Usage: python sat_shuttle.py pY dY WY sY WX k T2 [--ms 2,3] [--ns 3,4]
       [--kY 0] [--kX 0,1,2]
Results appended to sat_shuttle_results.jsonl.
"""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
SYNTH = os.path.abspath(os.path.join(HERE, "..", "..", "synth"))
sys.path.insert(0, SYNTH)
os.chdir(SYNTH)
from r110sat import CNF, TILE, make_window   # noqa: E402
from react import TrainVar                   # noqa: E402
from scene import Scene                      # noqa: E402
from classes import placements_by_class, n_classes   # noqa: E402
from en import en_item                       # noqa: E402

MARGIN = 24
OUT = os.path.join(HERE, "sat_shuttle_results.jsonl")
TC = 60          # rough collision + reaction time (sets the split points)


def scene_R2(cnf, X, Y, m, k, kY, T2, gap=6):
    E = en_item(cnf, m)
    tau, x = placements_by_class(E, (0, 0), Y, E.W + gap)[kY]
    lo, hi = 0, x + Y.W + tau
    vY = Y.period[1] / Y.period[0]
    win = make_window(T2, lo, hi, -4 / 15, 2 / 3, margin=MARGIN)
    S = Scene(cnf, T2, [(E, 0, 0), (Y, tau, x)], window=win)
    xc = E.W + gap / 2                      # collision near E's back
    tc = int(gap / (abs(vY) - 4 / 15)) + TC
    xE_end = xc - 4 * T2 / 15 + 3.5 * k + 10
    xX = xc + 2 * (T2 - tc) / 3
    mid = int((xE_end + xX) / 2)
    Eo = en_item(cnf, m + k)
    S.is_item(T2, S.lo - T2, mid, Eo, far_left=S.p_left)
    S.is_item(T2, mid, S.hi + T2, X, far_right=S.p_right)
    return S


def scene_R1(cnf, X, Y, n, k, kX, T2, gap=6):
    E = en_item(cnf, n)
    tauE, xE = placements_by_class(X, (0, 0), E, X.W + gap)[kX]
    lo, hi = 0, xE + E.W + tauE
    vY = Y.period[1] / Y.period[0]
    win = make_window(T2, lo, hi, vY, 0.0, margin=MARGIN)
    S = Scene(cnf, T2, [(X, 0, 0), (E, tauE, xE)], window=win)
    tc = TC
    xE_front = xE - 4 * T2 / 15
    # split just left of the counter's undisturbed front: Y (faster than
    # E) must be entirely left of it by T2 (T2 must be large enough)
    mid = int(xE_front - 8)
    Eo = en_item(cnf, n - k)
    S.is_item(T2, S.lo - T2, mid, Y, far_left=S.p_left)
    S.is_item(T2, mid, S.hi + T2, Eo, far_right=S.p_right)
    return S


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for a in ("pY", "dY", "WY", "sY", "WX", "k", "T2"):
        ap.add_argument(a, type=int)
    ap.add_argument("--ms", default="2,3")
    ap.add_argument("--ns", default="3,4")
    ap.add_argument("--kY", default=None)
    ap.add_argument("--kX", default="0,1,2")
    A = ap.parse_args()
    sX = (A.sY - 6 * A.k) % TILE
    ms = [int(v) for v in A.ms.split(",") if v]
    ns = [int(v) for v in A.ns.split(",") if v]
    nY = n_classes((15, -4), (A.pY, A.dY))
    kYs = range(nY) if A.kY is None else [int(v) for v in A.kY.split(",")]
    kXs = [int(v) for v in A.kX.split(",")]
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            r = json.loads(l)
            done.add((r["pY"], r["dY"], r["WY"], r["sY"], r["WX"], r["k"],
                      r["T2"], tuple(r["ms"]), tuple(r["ns"]), r["kY"], r["kX"]))
    for kY in kYs:
        for kX in kXs:
            key = (A.pY, A.dY, A.WY, A.sY, A.WX, A.k, A.T2, tuple(ms),
                   tuple(ns), kY, kX)
            if key in done:          # resumable: skip finished instances
                continue
            t = time.time()
            cnf = CNF()
            X = TrainVar(cnf, A.WX, 3, 2, sX, name="X")
            Y = TrainVar(cnf, A.WY, A.pY, A.dY, A.sY, name="Y")
            scenes = [scene_R2(cnf, X, Y, m, A.k, kY, A.T2) for m in ms] + \
                     [scene_R1(cnf, X, Y, n, A.k, kX, A.T2) for n in ns]
            sol = cnf.solve()
            rec = {"pY": A.pY, "dY": A.dY, "WY": A.WY, "sY": A.sY, "WX": A.WX,
                   "sX": sX, "k": A.k, "T2": A.T2, "ms": ms, "ns": ns,
                   "kY": kY, "kX": kX, "sat": sol is not None,
                   "secs": round(time.time() - t, 1)}
            if sol is not None:
                rec["X"] = "".join(map(str, X.decode(sol)))
                rec["Y"] = "".join(map(str, Y.decode(sol)))
                rec["sim_ok"] = all(S.check_sat_vs_sim(sol) for S in scenes)
                rec["rows0"] = ["".join(map(str, S.row(sol, 0))) for S in scenes]
                rec["frames"] = [(S.lo, S.p_left, S.p_right) for S in scenes]
                if not rec["sim_ok"]:
                    raise AssertionError("SAT/sim mismatch")
            print(json.dumps({q: v for q, v in rec.items() if q != "rows0"}), flush=True)
            with open(OUT, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
