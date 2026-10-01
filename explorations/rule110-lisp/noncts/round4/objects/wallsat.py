"""SAT search for periodic domain walls (and gliders, g = 0) in a periodic
Rule 110 background.

Left domain: background at phase (0, 0): cell(t, x) = bg(t, x).
Right domain: background at phase g = (tg, sg): cell(t, x) = bg(t + tg, x - sg).
A wall of period (P, D): row P equals row 0 shifted by D. The variable cells
at time t lie in a window [a(t), a(t) + W) with a(t) = floor(D t / P) - M
(window follows the wall); cells left of it are the left domain, right of it
the right domain, and the Rule 110 update is enforced on the window plus a
border of 2, so the forcing is exact. (P, D) must be a background lattice
vector (both domains return).

For g = 0, require the row to differ from the background somewhere at t = 0
(a glider in the background).

Every solution is re-checked by forward simulation (embedding the row in
the two domains, evolving P steps, comparing).
"""
import sys
import json
import numpy as np
from pysat.solvers import Solver
import cone


def lattice_ok(bg, P, D):
    r0 = bg.row_at(0)
    rP = bg.row_at(P)
    return all(rP[(x + D) % bg.p] == r0[x % bg.p] for x in range(bg.p))


class WallModel:
    def __init__(self, bg, g, P, D, W, M=0):
        self.bg, self.g, self.P, self.D, self.W = bg, g, P, D, W
        tg, sg = g
        self.L = lambda t, x: bg.bit(t, x)
        self.R = lambda t, x: bg.bit(t + tg, x - sg)
        self.a = [(D * t) // P - M for t in range(P + 1)]
        self.nv = 0
        self.var = {}
        self.cl = []
        for t in range(P + 1):
            for x in range(self.a[t], self.a[t] + W):
                self.nv += 1
                self.var[(t, x)] = self.nv
        for t in range(1, P + 1):
            for x in range(self.a[t] - 2, self.a[t] + W + 2):
                self._rule(self.lit(t - 1, x - 1), self.lit(t - 1, x),
                           self.lit(t - 1, x + 1), self.lit(t, x))
        # periodicity: row P at x + D == row 0 at x
        for x in range(self.a[0], self.a[0] + W):
            self._eq(self.lit(P, x + D), self.lit(0, x))

    def lit(self, t, x):
        v = self.var.get((t, x))
        if v is not None:
            return v
        if x < self.a[t]:
            return bool(self.L(t, x))
        return bool(self.R(t, x))

    def _add(self, clause):
        out = []
        for l in clause:
            if l is True:
                return
            if l is False:
                continue
            out.append(l)
        if not out:
            self.cl.append([])     # unsatisfiable marker
            return
        self.cl.append(out)

    def _eq(self, a, b):
        N = lambda z: (not z) if isinstance(z, bool) else -z
        self._add([N(a), b])
        self._add([a, N(b)])

    def _rule(self, l, c, r, n):
        N = lambda z: (not z) if isinstance(z, bool) else -z
        self._add([N(n), c, r])
        self._add([N(n), N(l), N(c), N(r)])
        self._add([N(c), r, n])
        self._add([c, N(r), n])
        self._add([l, N(c), N(r), n])

    def nontrivial_clause(self):
        """for g == 0: row 0 differs from background somewhere."""
        c = []
        for x in range(self.a[0], self.a[0] + self.W):
            v = self.var[(0, x)]
            c.append(-v if self.L(0, x) else v)
        return c

    def solve(self, extra=()):
        if any(len(c) == 0 for c in self.cl):
            return None
        cl = self.cl + list(extra)
        with Solver(name="cadical153", bootstrap_with=cl) as s:
            if not s.solve():
                return None
            m = set(l for l in s.get_model() if l > 0)
        row = np.array([1 if self.var[(0, x)] in m else 0
                        for x in range(self.a[0], self.a[0] + self.W)], np.uint8)
        self.check(row)
        return row

    def check(self, row):
        """forward simulation: embed row 0 between the domains, evolve P,
        compare the window shifted by D."""
        P, D, W = self.P, self.D, self.W
        pad = 2 * P + 30
        x_lo = self.a[0] - pad
        x_hi = self.a[0] + W + pad
        full = np.array([self.L(0, x) if x < self.a[0] else
                         (row[x - self.a[0]] if x < self.a[0] + W else self.R(0, x))
                         for x in range(x_lo, x_hi)], np.uint8)
        r = full
        for _ in range(P):
            r = ((r[1:-1] | r[2:]) & (1 - (r[:-2] & r[1:-1] & r[2:]))).astype(np.uint8)
        # r covers [x_lo + P, x_hi - P)
        for x in range(x_lo + P, x_hi - P):
            if x - D < x_lo + P or x - D >= x_hi - P:
                continue
            exp = (self.L(P, x) if x < self.a[P] else
                   (full[x - D - x_lo] if x < self.a[P] + W else self.R(P, x)))
            # inside window: expect row0 shifted; outside: domains
            if self.a[P] <= x < self.a[P] + W:
                exp = row[x - D - self.a[0]]
            assert r[x - (x_lo + P)] == exp, f"sim mismatch at x={x}"


def scan(tile, g_list, Pmax, Wmax, out):
    bg = cone.Background(tile)
    res = []
    for g in g_list:
        for P in range(1, Pmax + 1):
            for D in range(-P, P + 1):
                if not lattice_ok(bg, P, D):
                    continue
                found = None
                for W in range(2, Wmax + 1, 2):
                    wm = WallModel(bg, g, P, D, W)
                    extra = [wm.nontrivial_clause()] if g == (0, 0) else []
                    row = wm.solve(extra)
                    if row is not None:
                        found = (W, "".join(map(str, row)))
                        break
                rec = {"tile": tile, "g": list(g), "P": P, "D": D,
                       "v": D / P, "Wmax": Wmax,
                       "found": found is not None}
                if found:
                    rec["W"], rec["row0"] = found
                    rec["a0"] = wm.a[0]
                print(json.dumps(rec), flush=True)
                with open(out, "a") as fh:
                    fh.write(json.dumps(rec) + "\n")
                res.append(rec)
    return res


if __name__ == "__main__":
    tile = sys.argv[1]
    Pmax, Wmax = int(sys.argv[2]), int(sys.argv[3])
    out = sys.argv[4]
    bg = cone.Background(tile)
    if len(sys.argv) > 5:
        gl = [tuple(map(int, s.split(":"))) for s in sys.argv[5].split(",")]
    else:
        gl = [(t, s) for t in range(bg.tper) for s in range(bg.p)]
    scan(tile, gl, Pmax, Wmax, out)


class InterfaceModel(WallModel):
    """Interface between two DIFFERENT backgrounds: left = bgL at phase 0,
    right = bgR at phase g = (tg, sg). (P, D) must be in both lattices."""

    def __init__(self, bgL, bgR, g, P, D, W, M=0):
        tg, sg = g
        self.bg = bgL
        self.g, self.P, self.D, self.W = g, P, D, W
        self.L = lambda t, x: bgL.bit(t, x)
        self.R = lambda t, x: bgR.bit(t + tg, x - sg)
        self.a = [(D * t) // P - M for t in range(P + 1)]
        self.nv = 0
        self.var = {}
        self.cl = []
        for t in range(P + 1):
            for x in range(self.a[t], self.a[t] + W):
                self.nv += 1
                self.var[(t, x)] = self.nv
        for t in range(1, P + 1):
            for x in range(self.a[t] - 2, self.a[t] + W + 2):
                self._rule(self.lit(t - 1, x - 1), self.lit(t - 1, x),
                           self.lit(t - 1, x + 1), self.lit(t, x))
        for x in range(self.a[0], self.a[0] + W):
            self._eq(self.lit(P, x + D), self.lit(0, x))


def interfaces(tileL, tileR, P, D, Wmax):
    """All phases g of the right background: smallest W with an interface of
    period (P, D). Returns {g: (W, row0)}."""
    bL, bR = cone.Background(tileL), cone.Background(tileR)
    assert lattice_ok(bL, P, D) and lattice_ok(bR, P, D)
    out = {}
    for tg in range(bR.tper):
        for sg in range(bR.p):
            for W in range(2, Wmax + 1, 2):
                m = InterfaceModel(bL, bR, (tg, sg), P, D, W)
                r = m.solve()
                if r is not None:
                    out[(tg, sg)] = (W, "".join(map(str, r)))
                    break
    return out
