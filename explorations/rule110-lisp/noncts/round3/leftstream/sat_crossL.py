"""SAT: does a LEFT-moving train cross the E^n rod from its back?  Free
train Y (period (p, d), d < 0, width WY, slip s) hits E^n from the right;
for n in --ns the row at T2 is exactly  Y' | E^n (any position), Y' a
free train of the same period and slip (width WO).
Caveat: E^n from en.py is built by B's, so its BACK moves with n; for
families with several classes against E (Bbar, G: 3) a joint-n instance
fixes one placement per n, i.e. a particular combination of classes;
--kY gives one class index per n (default: the same index for all n).
B-trains (4,-2) have ONE class against E^n, so joint n is exact there.
Usage: python sat_crossL.py p d WY WO T2 [--ns 2,3] [--s 0..13] [--kY 0]
Results: sat_crossL_results.jsonl (resumable)."""
import argparse, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sat_inc import CNF, TILE, TrainVar, Scene, make_window, placements_by_class, en_item, n_classes, MARGIN  # noqa

OUT = os.path.join(HERE, "sat_crossL_results.jsonl")


def build(p, d, WY, WO, T2, ns, s, kYs, gap=6):
    cnf = CNF()
    Y = TrainVar(cnf, WY, p, d, s, name="Y")
    Yo = TrainVar(cnf, WO, p, d, s, name="Yo")
    scenes = []
    v = d / p
    for n, kY in zip(ns, kYs):
        E = en_item(cnf, n)
        tau, x = placements_by_class(E, (0, 0), Y, E.W + gap)[kY]
        lo, hi = 0, x + Y.W + tau
        win = make_window(T2, lo, hi, v, -4 / 15, margin=MARGIN)
        S = Scene(cnf, T2, [(E, 0, 0), (Y, tau, x)], window=win)
        front = -4 * T2 / 15
        mid = int(front - 8)
        S.is_item(T2, S.lo - T2, mid, Yo, far_left=S.p_left)
        S.is_item(T2, mid, S.hi + T2, E, far_right=S.p_right)
        scenes.append(S)
    return cnf, Y, Yo, scenes


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for a in ("p", "d", "WY", "WO", "T2"):
        ap.add_argument(a, type=int)
    ap.add_argument("--ns", default="2,3")
    ap.add_argument("--s", default=",".join(map(str, range(14))))
    ap.add_argument("--kY", default="0")
    A = ap.parse_args()
    ns = [int(v) for v in A.ns.split(",")]
    nc = n_classes((15, -4), (A.p, A.d))
    kcombos = []
    for kk in A.kY.split(";"):
        ks = [int(v) for v in kk.split(",")]
        kcombos.append(ks * len(ns) if len(ks) == 1 else ks)
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            r = json.loads(l)
            done.add((r["p"], r["d"], r["WY"], r["WO"], r["T2"], tuple(r["ns"]), r["s"], tuple(r["kY"])))
    for s in map(int, A.s.split(",")):
        for ks in kcombos:
            key = (A.p, A.d, A.WY, A.WO, A.T2, tuple(ns), s, tuple(ks))
            if key in done:
                continue
            t = time.time()
            cnf, Y, Yo, scenes = build(A.p, A.d, A.WY, A.WO, A.T2, ns, s, ks)
            sol = cnf.solve()
            rec = {"p": A.p, "d": A.d, "WY": A.WY, "WO": A.WO, "T2": A.T2,
                   "ns": ns, "s": s, "kY": ks, "nclasses": nc,
                   "sat": sol is not None, "secs": round(time.time() - t, 1)}
            if sol is not None:
                rec["Y"] = "".join(map(str, Y.decode(sol)))
                rec["Yo"] = "".join(map(str, Yo.decode(sol)))
                rec["sim_ok"] = all(S.check_sat_vs_sim(sol) for S in scenes)
                rec["rows0"] = ["".join(map(str, S.row(sol, 0))) for S in scenes]
                rec["frames"] = [(S.lo, S.p_left, S.p_right) for S in scenes]
                if not rec["sim_ok"]:
                    raise AssertionError("SAT/sim mismatch")
            print(json.dumps({q: v for q, v in rec.items() if q != "rows0"}), flush=True)
            with open(OUT, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
