"""SAT: zero test from the left. A free (p, d)-train Z (width WZ, slip s)
hits E^n; jointly:
  n in --ns (default 2,3): row at T2 = exactly E^(n-1) (DEC),
  n = 1, mode 'A'   : row at T2 = E (any position) | A (any position),
         mode 'wrap': row at T2 = exactly E^7 (0 -> 6, gate's Z6 mirrored),
         mode 'E'   : row at T2 = E | some nonempty right-moving debris? no:
                      'EA2': E | A^2 ... (extra answers can be added here)
Results appended to sat_zero_results.jsonl.
Usage: python sat_zero.py p d WZ T2 MODE [--ns 2,3] [--k 0,1,2] [--s 8]
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
from lib import load_gliders                 # noqa: E402
from react import fixed_from_glider          # noqa: E402

MARGIN = 24
OUT = os.path.join(HERE, "sat_zero_results.jsonl")
G = load_gliders()


def scene_for(cnf, Y, n, k, T2, p, d, gap):
    E = en_item(cnf, n)
    tauE, xE = placements_by_class(Y, (0, 0), E, Y.W + gap)[k]
    lo, hi = 0, xE + E.W + tauE
    win = make_window(T2, lo, hi, -4 / 15, d / p, margin=MARGIN)
    S = Scene(cnf, T2, [(Y, 0, 0), (E, tauE, xE)], window=win)
    return S, xE


def build(p, d, WZ, T2, ns, k, s, mode, gap=6):
    cnf = CNF()
    Y = TrainVar(cnf, WZ, p, d, s, name="Z")
    scenes = []
    for n in ns:
        S, xE = scene_for(cnf, Y, n, k, T2, p, d, gap)
        S.is_item(T2, S.lo - T2, S.hi + T2, en_item(cnf, n - 1),
                  far_left=S.p_left, far_right=S.p_right)
        scenes.append(S)
    S, xE = scene_for(cnf, Y, 1, k, T2, p, d, gap)
    if mode == "wrap":
        S.is_item(T2, S.lo - T2, S.hi + T2, en_item(cnf, 7),
                  far_left=S.p_left, far_right=S.p_right)
    elif mode == "ZL":
        # zero answer = exactly the Z_L train (sat_zero_results #1)
        from react import Fixed
        Zit = Fixed(cnf, "111110111110111000111011", 8, (3, 2), name="ZL")
        mid = xE - (4 * T2) // 15 + 70
        S.is_item(T2, S.lo - T2, mid, en_item(cnf, 1), far_left=S.p_left)
        S.is_item(T2, mid, S.hi + T2, Zit, far_right=S.p_right)
    elif mode in ("A", "A2", "A3"):
        ans = {"A": "A", "A2": "A^2", "A3": "A^3"}[mode]
        Ait = fixed_from_glider(cnf, G[ans], 16) if ans in G else None
        if Ait is None:
            raise KeyError(ans)
        mid = xE - (4 * T2) // 15 + 70
        S.is_item(T2, S.lo - T2, mid, en_item(cnf, 1), far_left=S.p_left)
        S.is_item(T2, mid, S.hi + T2, Ait, far_right=S.p_right)
    else:
        raise ValueError(mode)
    scenes.append(S)
    return cnf, Y, scenes


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("p", type=int); ap.add_argument("d", type=int)
    ap.add_argument("WZ", type=int); ap.add_argument("T2", type=int)
    ap.add_argument("mode")
    ap.add_argument("--ns", default="2,3")
    ap.add_argument("--k", default=None)
    ap.add_argument("--s", type=int, default=8)
    ap.add_argument("--gap", type=int, default=6)
    A = ap.parse_args()
    ns = [int(v) for v in A.ns.split(",")]
    nc = n_classes((15, -4), (A.p, A.d))
    ks = range(nc) if A.k is None else map(int, A.k.split(","))
    for k in ks:
        t = time.time()
        cnf, Y, scenes = build(A.p, A.d, A.WZ, A.T2, ns, k, A.s, A.mode, A.gap)
        sol = cnf.solve()
        rec = {"p": A.p, "d": A.d, "WZ": A.WZ, "T2": A.T2, "mode": A.mode,
               "ns": ns, "k": k, "s": A.s, "gap": A.gap,
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
