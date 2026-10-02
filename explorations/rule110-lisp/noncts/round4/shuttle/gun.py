"""SAT search for GUNS attached to a rod face: spacetime-periodic structures
with period V = K*u + j*P_E (u = (5,2), P_E = (15,-4)), i.e. the face moves
by K crystal units per cycle of Tc = 5K + 15j steps, emitting a periodic
train of gliders (one glider G_out per cycle, seeds s0 + k*V).

FRONT gun (face = front of rod, K = 1 eats one unit per cycle): emits a
left-moving train (default B (4,-2)) out of the window's left edge.
BACK gun (face = back, K = 1 adds one unit per cycle): emits a right-moving
train (default A (3,2)) out of the window's right edge.

Window: moves with the rod (velocity -4/15), [face - wL, face + wR).
Outside: rod background (exact simulation of E^N) on the rod side, the
infinite glider train (exact simulation) on the other side. All cells in
the window at t = 0 .. Tc are unknown; Rule 110 is enforced on a 2-cell
border; row Tc equals row 0 translated by V. Any solution is therefore a
genuine periodic gun (re-verified by simulation: verify_gun).

Usage: python gun.py --face front --j 0 [--K 1] [--out f.jsonl]
"""
import os, sys, json, time, argparse
sys.dont_write_bytecode = True
import numpy as np
from rod import TILE, ether_bit, simulate, GL, SYNTH  # noqa
from pert import BG
from r110sat import CNF, neg  # noqa
from lib import compose  # noqa


def train_bg(name, seeds, t_max, lo, hi):
    """Spacetime (t in [0, t_max]) of gliders `name` at seeds (t0, x0),
    composed at time 0 (left phase chosen so that phases are consistent),
    on columns [lo, hi). Returns (h, lo) or None if phases inconsistent."""
    g = GL[name]
    sts = [g.state(t0, x0, 0) for (t0, x0) in seeds]
    sts.sort(key=lambda s: s[3])
    # left phase of the first state
    pad = t_max + 30
    lo = min(lo, sts[0][3] - 50)
    hi = max(hi, sts[-1][3] + len(sts[-1][0]) + 50)
    try:
        cells, pl, pr = compose(sts, 0, lo - pad, hi + pad)
    except ValueError as e:
        print("train_bg:", e)
        return None
    h = simulate(cells, t_max)
    return h, lo - pad


class Gun:
    def __init__(self, a):
        self.a = a
        K, j = a.K, a.j
        self.Tc = 5 * K + 15 * j
        self.dxV = 2 * K - 4 * j
        self.T = self.Tc

    def build(self, s0, bg):
        a, T, Tc, dxV = self.a, self.T, self.Tc, self.dxV
        cnf = CNF()
        face = (lambda t: bg.front(0) - (4 * t) // 15) if a.face == "front" else \
               (lambda t: bg.back(0) - (4 * t) // 15)
        f0 = face(0)
        L = {t: f0 - (4 * t) // 15 - a.wL for t in range(T + 1)}
        R = {t: f0 - (4 * t) // 15 + a.wR for t in range(T + 1)}
        # train background
        name = a.glider
        p = GL[name].p
        d = GL[name].d
        seeds = train_seeds(s0, Tc, dxV, p, d, f0 - a.wL - 700, f0 + a.wR + 700)
        lo, hi = f0 - a.wL - T - 200, f0 + a.wR + T + 200
        tb = train_bg(name, seeds, T + 2, lo - 400, hi + 400)
        if tb is None:
            return None
        th, tlo = tb
        # the train region must not contain the rod: we use train cells only
        # on the far side of the window.
        cells = {}
        for t in range(T + 1):
            for x in range(L[t], R[t]):
                cells[(t, x)] = cnf.new_var()

        def lit(t, x):
            v = cells.get((t, x))
            if v is not None:
                return v
            if (x < L[t]) == (a.face == "front"):
                return bool(th[t, x - tlo])          # train side
            return bool(bg(t, x))                    # rod side

        for t in range(1, T + 1):
            for x in range(L[t] - 2, R[t] + 2):
                l, c, r_, n = lit(t - 1, x - 1), lit(t - 1, x), lit(t - 1, x + 1), lit(t, x)
                add, N = cnf.add, neg
                add([N(n), c, r_])
                add([N(n), N(l), N(c), N(r_)])
                add([N(c), r_, n])
                add([c, N(r_), n])
                add([l, N(c), N(r_), n])
        # periodicity: row Tc at x + dxV == row 0 at x (window + border)
        for x in range(L[0] - 3, R[0] + 3):
            a1, b1 = lit(Tc, x + dxV), lit(0, x)
            if isinstance(a1, bool) and isinstance(b1, bool):
                if a1 != b1:
                    return "inconsistent"
                continue
            cnf.equal(a1, b1)
        self.cells, self.lit, self.L, self.R = cells, lit, L, R
        return cnf


def train_seeds(s0, Tc, dxV, p, d, xlo, xhi):
    """seeds s0 + k V whose glider sits in [xlo, xhi) at t = 0."""
    out = []
    for k in range(-5000, 5000):
        t0, x0 = s0[0] + k * Tc, s0[1] + k * dxV
        x = x0 - t0 * d / p
        if xlo <= x < xhi:
            out.append((t0, x0))
    assert len(out) >= 5, "train too sparse in range"
    return out


def pair(s):
    return tuple(int(v) for v in s.split(","))


def args(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--face", default="front")
    ap.add_argument("--K", type=int, default=1)
    ap.add_argument("--j", type=int, default=0)
    ap.add_argument("--glider", default=None)
    ap.add_argument("--wL", type=int, default=16)
    ap.add_argument("--wR", type=int, default=16)
    ap.add_argument("--N", type=int, default=16)
    ap.add_argument("--nk", type=int, default=40)
    ap.add_argument("--out", default=None)
    ap.add_argument("--first", action="store_true", help="stop at first SAT")
    a = ap.parse_args(argv)
    if a.glider is None:
        a.glider = "B" if a.face == "front" else "A"
    return a


def seeds_mod(Tc, dxV, P, span):
    """representatives of seeds (t0, x0), 0 <= t0 < p, modulo <V, P>."""
    from fractions import Fraction
    V = (Tc, dxV)
    det = V[0] * P[1] - V[1] * P[0]
    reps = []
    keys = set()
    for t0 in range(P[0]):
        for x0 in range(-span, span):
            # coordinates of (t0, x0) in basis (V, P): solve
            u = Fraction(t0 * P[1] - x0 * P[0], det)
            w = Fraction(V[0] * x0 - V[1] * t0, det)
            key = (u % 1, w % 1)
            if key not in keys:
                keys.add(key)
                reps.append((t0, x0))
    return reps, abs(det)


if __name__ == "__main__" and not (len(sys.argv) > 1 and sys.argv[1] == "--verify"):
    a = args()
    G = Gun(a)
    bg = BG(a.N, G.T + 20, -G.T - 600, 4 * a.N + G.T + 600)
    P = (GL[a.glider].p, GL[a.glider].d)
    # seeds near the window edge on the train side
    f0 = bg.front(0) if a.face == "front" else bg.back(0)
    reps, det = seeds_mod(G.Tc, G.dxV, P, 400)
    print("Tc", G.Tc, "dxV", G.dxV, "classes", len(reps), "det", det, flush=True)
    nsat = 0
    t0 = time.time()
    for (st, sx) in reps:
        s0 = (st, f0 + sx) if True else None
        cnf = G.build((st, sx), bg)
        if cnf is None or cnf == "inconsistent":
            continue
        sol = cnf.solve()
        if sol is not None:
            nsat += 1
            row0 = "".join(str(sol.val(G.lit(0, x))) for x in range(G.L[0], G.R[0]))
            rec = dict(vars(a), seed=(st, sx), Tc=G.Tc, dxV=G.dxV, row0=row0, L0=G.L[0])
            print("SAT", json.dumps(rec), flush=True)
            if a.out:
                with open(a.out, "a") as fh:
                    fh.write(json.dumps(rec) + "\n")
            if a.first:
                break
    print("done", "sat", nsat, "of", len(reps), round(time.time() - t0, 1), "s", flush=True)


def verify_gun(rec, cycles=12, n_rod=None):
    """Exact simulation of a gun record: the t = 0 row (train | window row0 |
    rod) is evolved for `cycles` periods; checks that the window region,
    followed along V, repeats exactly every cycle. Returns list of bools."""
    a = argparse.Namespace(**{k: rec[k] for k in ("face", "K", "j", "glider", "wL", "wR", "N", "nk")})
    if n_rod:
        a.N = n_rod
    G = Gun(a)
    Ttot = G.Tc * cycles
    bg = BG(a.N, Ttot + 20, -Ttot - 800, 4 * a.N + Ttot + 800)
    st, sx = rec["seed"]
    L0 = rec["L0"]
    R0 = L0 + len(rec["row0"])
    lo, hi = L0 - Ttot - 300, R0 + Ttot + 300
    p, d = GL[a.glider].p, GL[a.glider].d
    seeds = train_seeds((st, sx), G.Tc, G.dxV, p, d, lo - 300, hi + 300)
    th, tlo = train_bg(a.glider, seeds, 1, lo - 400, hi + 400)
    xs = range(lo, hi)
    front = a.face == "front"
    row = np.array([(th[0, x - tlo] if front else bg(0, x)) if x < L0 else
                    (int(rec["row0"][x - L0]) if x < R0 else (bg(0, x) if front else th[0, x - tlo]))
                    for x in xs], np.uint8)
    h = simulate(row, Ttot)
    out = []
    for k in range(1, cycles):
        t = k * G.Tc
        ok = all(h[t, x + k * G.dxV - lo] == h[0, x - lo] for x in range(L0 - 10, R0 + 10)
                 if lo + t + 5 <= x + k * G.dxV < hi - t - 5)
        out.append(ok)
    return out, h, lo


if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[1] == "--verify":
    # python gun.py --verify gun_records.jsonl [cycles]
    cyc = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    for l in open(sys.argv[2]):
        rec = json.loads(l)
        ok, h, lo = verify_gun(rec, cycles=cyc)
        print(rec["face"], rec["j"], rec["seed"], "periodic for", cyc, "cycles:", all(ok))
    sys.exit(0)
