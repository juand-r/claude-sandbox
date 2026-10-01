"""SAT: a SHUTTLE between two E^n counters' inner faces (theory 05:49).
Unknowns: X = free right-moving train (period PX, width WX, slip sX),
          Y = free left-moving train  (period PY, width WY, slip sY).
Reactions, jointly (one X and one Y for all listed n, m):
  R1 face:  X + E^n -> Y | E^(n-K)       for n in NS1 (X from the left)
  R2 face:  E^m + Y -> E^(m+K) | X       for m in NS2 (Y from the right)
(K = units carried R1 -> R2 per round trip; slip needs sY = sX + 6K.)
Each reaction in a given collision class (--c1, --c2); outputs anywhere
in their region (is_item over all phases/positions), ether elsewhere.
Uses round-1 synth/ (read-only). Results: sat_shuttle_results.jsonl.
Usage: python sat_shuttle.py --py 12,-6 --wy 24 --wx 24 --sx 8 --K 2
        --ns1 3,4 --ns2 3,4 --T1 220 --T2 260 [--c1 k] [--c2 k]
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

MARGIN = 20
OUT = os.path.join(HERE, "sat_shuttle_results.jsonl")


def r1_scene(cnf, X, Y, n, K, c, T, gap):
    E = en_item(cnf, n)
    tauE, xE = placements_by_class(X, (0, 0), E, X.W + gap)[c]
    lo, hi = 0, xE + E.W + tauE
    pY, dY = Y.period
    win = make_window(T, lo, hi, dY / pY, -4 / 15, margin=MARGIN)
    S = Scene(cnf, T, [(X, 0, 0), (E, tauE, xE)], window=win)
    # split: Y left of mid, E^(n-K) right of mid (mid tracks E's left side)
    mid = xE + int(-4 * T / 15) - 6
    S.is_item(T, S.lo - T, mid, Y, far_left=S.p_left)
    S.is_item(T, mid, S.hi + T, en_item(cnf, n - K), far_right=S.p_right)
    return S


def r2_scene(cnf, X, Y, m, K, c, T, gap):
    E = en_item(cnf, m)
    tauY, xY = placements_by_class(E, (0, 0), Y, E.W + gap)[c]
    lo, hi = 0, xY + Y.W + tauY
    pX, dX = X.period
    win = make_window(T, lo, hi, -4 / 15, dX / pX, margin=MARGIN)
    S = Scene(cnf, T, [(E, 0, 0), (Y, tauY, xY)], window=win)
    # E^(m+K) near the left (its right end < mid), X right of mid
    Eo = en_item(cnf, m + K)
    mid = int(-4 * T / 15) + Eo.W + 25
    S.is_item(T, S.lo - T, mid, Eo, far_left=S.p_left)
    S.is_item(T, mid, S.hi + T, X, far_right=S.p_right)
    return S


def build(a):
    cnf = CNF()
    px, dx = a.px
    py, dy = a.py
    sY = (a.sx + 6 * a.K) % TILE
    X = TrainVar(cnf, a.wx, px, dx, a.sx, name="X")
    Y = TrainVar(cnf, a.wy, py, dy, sY, name="Y")
    scenes = []
    if a.only != "r2":
        scenes += [r1_scene(cnf, X, Y, n, a.K, a.c1, a.T1, a.gap) for n in a.ns1]
    if a.only != "r1":
        scenes += [r2_scene(cnf, X, Y, m, a.K, a.c2, a.T2, a.gap) for m in a.ns2]
    return cnf, X, Y, scenes


def pair(s):
    return tuple(int(v) for v in s.split(","))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--px", type=pair, default=(3, 2))
    ap.add_argument("--py", type=pair, default=(12, -6))
    ap.add_argument("--wx", type=int, default=24)
    ap.add_argument("--wy", type=int, default=24)
    ap.add_argument("--sx", type=int, default=8)
    ap.add_argument("--K", type=int, default=2)
    ap.add_argument("--ns1", type=pair, default=(3, 4))
    ap.add_argument("--ns2", type=pair, default=(3, 4))
    ap.add_argument("--T1", type=int, default=220)
    ap.add_argument("--T2", type=int, default=260)
    ap.add_argument("--c1", type=int, default=None)
    ap.add_argument("--c2", type=int, default=None)
    ap.add_argument("--gap", type=int, default=6)
    ap.add_argument("--only", default=None, help="r1 or r2: one face only (controls)")
    a = ap.parse_args()
    n1 = n_classes((15, -4), a.px)
    n2 = n_classes((15, -4), a.py)
    if a.only == "r2":
        a.c1 = 0
    if a.only == "r1":
        a.c2 = 0
    KEYS = ("px", "py", "wx", "wy", "sx", "K", "ns1", "ns2", "T1", "T2", "c1", "c2", "only", "gap")
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            r = json.loads(l)
            done.add(tuple(str(r.get(k)) for k in KEYS))
    C1, C2 = a.c1, a.c2
    for c1 in ([C1] if C1 is not None else range(n1)):
        for c2 in ([C2] if C2 is not None else range(n2)):
            a.c1, a.c2 = c1, c2
            key = tuple(str(list(v) if isinstance(v, tuple) else v) for v in (getattr(a, k) for k in KEYS))
            if key in done:
                print("skip (done)", key, flush=True)
                continue
            t = time.time()
            cnf, X, Y, scenes = build(a)
            sol = cnf.solve()
            rec = {k: (list(v) if isinstance(v, tuple) else v) for k, v in vars(a).items()}
            rec.update(sat=sol is not None, secs=round(time.time() - t, 1))
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
