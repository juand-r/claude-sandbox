"""Perturbation SAT around a fixed background spacetime (a long rod).

Scene (FRONT face, R1's inner face), all at t = 0:
    ether(phiL) | X (unknown, (pX,dX)-train, width WX) | gap ether | E^N rod
The rod's first cell is at column 0. bg(t, x) is the exact evolution of
the rod alone (computed by simulation). Variables are the cells inside a
moving window [L_t, R_t) intersected with the light cone of the unknown
X region; cells outside are constants: ether(phiL) on the left, bg on the
right. The Rule 110 update is checked on a 2-cell border, so a solution is
an exact evolution in which NOTHING leaves the window. Since the window's
right edge stays inside the rod (rod-speed, fixed depth), the solution is
valid for every rod E^n whose back lies beyond the window (n >= n_min):
no wall can travel to the back (a deliberate restriction).

Output at time T: [L_T, yb): a (pY,dY)-periodic left-moving pattern Y
(checked as row T == row T-pY shifted, then post-verified in isolation),
[yb, ...): bg(T - 5K, x - 2K), i.e. the rod with K units removed at the
front (crystal unit vector u = (5,2), measured in rod.py: the rod
interior is invariant under (5,2) and (15,-4)), with >= `band` ether
cells between Y and the new front.

Mirror scene (BACK face, R2's inner face): ether | rod E^N | gap | Y (unknown
left-mover) | ether; output X right-mover right of the rod and the rod's
back moved by +K units: bg(T - 5K, x - 2K) on the rod side.

Every SAT solution is re-simulated (verify.py does full-n checks).
"""
import os
import sys
import json
import time
import math
import argparse
sys.dont_write_bytecode = True
from rod import build_rod, embed, rod_piece, TILE, ether_bit, simulate, SYNTH  # noqa
from r110sat import CNF, neg  # noqa
import numpy as np  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))


class BG:
    """Exact spacetime of a rod E^N alone (front cell at column 0 at t=0)."""

    def __init__(self, N, T, xlo, xhi):
        self.r = build_rod(N)
        pad = T + 60
        self.lo = xlo - pad
        row = embed([rod_piece(self.r, 0)], self.lo, xhi + pad)
        self.h = simulate(row, T + 5 * 8 + 15)     # allow t - 5K lookups
        self.T = T
        self.phi_left = (self.r["pl"]) % TILE      # global phase left of rod
        self.phi_right = (self.r["pr"] - self.r["W"]) % TILE
        self.W = self.r["W"]

    def __call__(self, t, x):
        if t < 0:                                   # rod is (15,-4)-periodic
            q = (-t + 14) // 15
            t, x = t + 15 * q, x - 4 * q
        return int(self.h[t, x - self.lo])

    def front(self, t):
        """leftmost cell of the rod that differs from the left ether."""
        x = -60 - (4 * t) // 15
        while self(t, x) == ether_bit(self.phi_left, t, x):
            x += 1
        return x

    def back(self, t):
        x = self.W + 60 - (4 * t) // 15
        while self(t, x) == ether_bit(self.phi_right, t, x):
            x -= 1
        return x + 1


class Pert:
    """Generic: unknown t=0 cells on [ulo, uhi); everything else at t=0 is
    `const0(x)`; for t >= 1, cells left of the window/cone are left(t,x),
    right of it right(t,x)."""

    def __init__(self, cnf, T, ulo, uhi, init_const, left_const, right_const, window):
        self.cnf, self.T = cnf, T
        self.left_const, self.right_const = left_const, right_const
        self.cells = {}
        self.bounds = {}
        for x in range(ulo, uhi):
            self.cells[(0, x)] = cnf.new_var()
        self.init_const = init_const
        self.bounds[0] = (ulo, uhi)
        for t in range(1, T + 1):
            L, R = ulo - t, uhi + t
            wl, wr = window(t)
            L, R = max(L, wl), min(R, wr)
            pl, pr = self.bounds[t - 1]
            if L - pl > 1 or pl - L > 1 or R - pr > 1 or pr - R > 1:
                raise ValueError(f"window jumps at t={t}: {(pl, pr)} -> {(L, R)}")
            if L >= R:
                raise ValueError(f"empty window at t={t}")
            self.bounds[t] = (L, R)
            for x in range(L, R):
                self.cells[(t, x)] = cnf.new_var()
        for t in range(1, T + 1):
            L, R = self.bounds[t]
            for x in range(L - 2, R + 2):
                self._rule(self.lit(t - 1, x - 1), self.lit(t - 1, x),
                           self.lit(t - 1, x + 1), self.lit(t, x))

    def lit(self, t, x):
        v = self.cells.get((t, x))
        if v is not None:
            return v
        if t == 0:
            return bool(self.init_const(x))
        L, R = self.bounds[t]
        if x < L:
            return bool(self.left_const(t, x))
        if x >= R:
            return bool(self.right_const(t, x))
        raise KeyError((t, x))

    def _rule(self, l, c, r, n):
        add, N = self.cnf.add, neg
        add([N(n), c, r])
        add([N(n), N(l), N(c), N(r)])
        add([N(c), r, n])
        add([c, N(r), n])
        add([l, N(c), N(r), n])

    def fix(self, t, x, v):
        l = self.lit(t, x)
        self.cnf.add([l if v else neg(l)])

    def equal(self, t1, x1, t2, x2):
        self.cnf.equal(self.lit(t1, x1), self.lit(t2, x2))

    def differs(self, t, lo, hi, f):
        cl = []
        for x in range(lo, hi):
            l = self.lit(t, x)
            cl.append(neg(l) if f(x) else l)
        self.cnf.add(cl)

    def val(self, sol, t, x):
        return sol.val(self.lit(t, x))


def smooth_window(T, Lstar, Rstar):
    """Window edges following target functions, moving <= 1 per step."""
    Ls, Rs = {}, {}
    pl, pr = None, None
    out = {}
    for t in range(1, T + 1):
        l, r = int(math.floor(Lstar(t))), int(math.ceil(Rstar(t)))
        if pl is not None:
            l = min(max(l, pl - 1), pl + 1)
            r = min(max(r, pr - 1), pr + 1)
        out[t] = (l, r)
        pl, pr = l, r
    return lambda t: out[t]


def front_scene(a, bg):
    """Build the FRONT-face problem. Returns (cnf, P, info)."""
    cnf = CNF()
    pX, dX = a.px
    pY, dY = a.py
    vX, vY = dX / pX, dY / pY
    T, K = a.T, a.K
    phig = bg.phi_left                         # ether between X and rod
    x1 = -a.gap                                # X region [x0, x1)
    x0 = x1 - a.wx
    phiL = a.phiL
    # time when X (front edge) meets the rod front
    if vX > -4 / 15:
        tc = a.gap / (vX + 4 / 15)
        xc = -4 * tc / 15
    else:                       # control: X moves away (it is its own Y)
        tc, xc = 0.0, float(x1)

    def Lstar(t):
        return min(x0 + vX * t, xc + vY * (t - tc) - a.wy) - a.margin

    def Rstar(t):
        return -4 * t / 15 + a.depth

    # initial window must include [x0, x1) and the rod front region
    win = smooth_window(T, Lstar, Rstar)
    init_const = lambda x: ether_bit(phiL, 0, x) if x < x0 else bg(0, x)
    left_const = lambda t, x: ether_bit(phiL, t, x)
    right_const = lambda t, x: bg(t, x)
    P = Pert(cnf, T, x0, x1, init_const, left_const, right_const, win)
    # X: (pX, dX)-periodic as an isolated train (before it meets the rod)
    for x in range(x0 - pX - 2, x1 + 3):
        P.equal(pX, x + dX, 0, x)
    if phiL == phig and not a.allow_empty:   # nonempty X
        P.differs(0, x0, x1, lambda x: ether_bit(phiL, 0, x))
    # output at T: shifted rod (K units removed) right of yb
    fT = bg.front(T - 5 * K) + 2 * K
    yb = fT - a.band
    L, R = P.bounds[T]
    for x in range(yb, R + 2):
        P.fix(T, x, bg(T - 5 * K, x - 2 * K))
    # Y region [L, yb): (pY, dY)-periodic (row T == row T - pY shifted)
    for x in range(L - 2, yb):
        P.equal(T, x, T - pY, x - dY)
    phiY_right = None
    for p in range(TILE):
        if all(bg(T - 5 * K, x - 2 * K) == ether_bit(p, T, x) for x in range(yb, yb + 14)):
            phiY_right = p
    if phiY_right == phiL and not a.allow_empty:
        P.differs(T, L, yb, lambda x: ether_bit(phiL, T, x))
    info = dict(x0=x0, x1=x1, yb=yb, fT=fT, tc=tc, phig=phig, phiY_right=phiY_right,
                L_T=L, R_T=R)
    return cnf, P, info


def decode_front(a, bg, P, sol, info):
    X = [P.val(sol, 0, x) for x in range(info["x0"], info["x1"])]
    L = info["L_T"]
    Y = [P.val(sol, a.T, x) for x in range(L, info["yb"])]
    return "".join(map(str, X)), "".join(map(str, Y))


def pair(s):
    return tuple(int(v) for v in s.split(","))


def args(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--face", default="front")
    ap.add_argument("--px", type=pair, default=(3, 2))
    ap.add_argument("--py", type=pair, default=(42, -14))
    ap.add_argument("--wx", type=int, default=24)
    ap.add_argument("--wy", type=int, default=40)
    ap.add_argument("--K", type=int, default=1)
    ap.add_argument("--N", type=int, default=16)
    ap.add_argument("--T", type=int, default=300)
    ap.add_argument("--gap", type=int, default=8)
    ap.add_argument("--phiL", type=int, default=0)
    ap.add_argument("--band", type=int, default=14)
    ap.add_argument("--depth", type=int, default=24)
    ap.add_argument("--margin", type=int, default=4)
    ap.add_argument("--out", default=None)
    ap.add_argument("--allow_empty", action="store_true",
                    help="controls only: Y (and X) may be pure ether")
    return ap.parse_args(argv)


def run(a):
    bg = BG(a.N, a.T, -a.T - a.gap - a.wx - a.wy - 100, 60)
    t0 = time.time()
    cnf, P, info = front_scene(a, bg)
    nv, nc = cnf.nvars, len(cnf.clauses)
    sol = cnf.solve()
    rec = dict(vars(a))
    rec.update(sat=sol is not None, secs=round(time.time() - t0, 1), nvars=nv,
               nclauses=nc, phig=info["phig"], phiYr=info["phiY_right"])
    if sol is not None:
        X, Y = decode_front(a, bg, P, sol, info)
        rec.update(X=X, Y=Y, x0=info["x0"], L_T=info["L_T"])
    return rec


if __name__ == "__main__":
    a = args()
    rec = run(a)
    print(json.dumps(rec), flush=True)
    if a.out:
        with open(a.out, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
