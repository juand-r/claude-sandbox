"""Exact influence cones of a periodic Rule 110 background (SAT).

Background: a spatially periodic row `tile` (period p), evolved on a ring of
width p (exact for the infinite periodic row). bg(t, x) = ring_t[x mod p].

Left cone: perturb the initial row ARBITRARILY on x >= x0 (cells x < x0 stay
background). L(T) = leftmost cell at time T that can differ from the
background. Only initial cells [x0, x0 + T) can matter for cells < x0 at
time T, so the free region is [x0, x0 + T) (exact, not a restriction).

Right cone: perturb arbitrarily on x <= x0; R(T) = rightmost cell at time T
that can differ. Free region (x0 - T, x0].

The SAT model has a variable for every cell of the light cone of the free
region; cells outside are background constants (they cannot be influenced).
Answers are exact for the stated T (each SAT answer is re-checked by forward
simulation of the witness; each UNSAT is a proof for that cell).

Block argument (rigorous speed bound): let D(T) = min over all background
phases (time phase tau, start position x0 mod p) of L(T) - x0. A perturbation
confined to x >= x0 at time 0 is confined to x >= x0 + D(T) at time T, and
then (any phase) to x >= x0 + 2 D(T) at 2T, etc. So the left edge speed is
>= D(T)/T for every T (likewise R(T) gives an upper bound on right speed).
"""
import sys
import numpy as np
from pysat.solvers import Solver

RULE_OUT = {(l, c, r): ((c | r) & (1 - (l & c & r))) for l in (0, 1)
            for c in (0, 1) for r in (0, 1)}


def ring_step(c):
    l = np.roll(c, 1)
    r = np.roll(c, -1)
    return ((c | r) & (1 - (l & c & r))).astype(np.uint8)


class Background:
    def __init__(self, tile):
        self.tile = np.array([int(ch) for ch in tile], np.uint8)
        self.p = len(self.tile)
        self.rows = [self.tile]
        # temporal period and shift of the ring orbit
        seen = {self.tile.tobytes(): 0}
        r = self.tile
        while True:
            r = ring_step(r)
            k = r.tobytes()
            # look for any rotation equal to the start
            hit = None
            for s in range(self.p):
                if np.array_equal(np.roll(self.tile, s), r):
                    hit = s
                    break
            self.rows.append(r)
            if hit is not None:
                self.tper = len(self.rows) - 1
                self.shift = hit if hit <= self.p // 2 else hit - self.p
                break
            if len(self.rows) > 4096:
                raise ValueError("tile not on a cycle (transient) or period too long")

    def row_at(self, t):
        """ring row at time t (t may exceed tper)."""
        q, m = divmod(t, self.tper)
        return np.roll(self.rows[m], q * self.shift)

    def bit(self, t, x):
        return int(self.row_at(t)[x % self.p])


def simulate_window(row0, T):
    """Forward Rule 110 on a finite row with fixed (shrinking) edges:
    returns list of rows; row t covers [t, len - t) of the original index."""
    out = [np.asarray(row0, np.uint8)]
    for _ in range(T):
        c = out[-1]
        out.append(((c[1:-1] | c[2:]) & (1 - (c[:-2] & c[1:-1] & c[2:]))).astype(np.uint8))
    return out


class ConeModel:
    """Free initial region [a, b) over background phase tau; T steps."""

    def __init__(self, bg, tau, a, b, T):
        self.bg, self.tau, self.a, self.b, self.T = bg, tau, a, b, T
        self.nv = 0
        self.cl = []
        self.var = {}
        self.rowc = [bg.row_at(tau + t) for t in range(T + 1)]
        for t in range(T + 1):
            for x in range(a - t, b + t):
                self.nv += 1
                self.var[(t, x)] = self.nv
        for t in range(1, T + 1):
            for x in range(a - t, b + t):
                self._rule(self.lit(t - 1, x - 1), self.lit(t - 1, x),
                           self.lit(t - 1, x + 1), self.var[(t, x)])

    def bgbit(self, t, x):
        return int(self.rowc[t][x % self.bg.p])

    def lit(self, t, x):
        v = self.var.get((t, x))
        if v is not None:
            return v
        return bool(self.bgbit(t, x))

    def _add(self, clause):
        out = []
        for l in clause:
            if l is True:
                return
            if l is False:
                continue
            out.append(l)
        assert out, "empty clause"
        self.cl.append(out)

    def _rule(self, l, c, r, n):
        N = lambda z: (not z) if isinstance(z, bool) else -z
        self._add([N(n), c, r])
        self._add([N(n), N(l), N(c), N(r)])
        self._add([N(c), r, n])
        self._add([c, N(r), n])
        self._add([l, N(c), N(r), n])

    def diff_lit(self, t, x):
        """literal true iff cell (t, x) differs from background"""
        v = self.lit(t, x)
        if isinstance(v, bool):
            return False
        return -v if self.bgbit(t, x) else v

    def extreme(self, side):
        """side='left': leftmost x with cell (T, x) able to differ;
        side='right': rightmost. Returns (x, witness_row0) or (None, None)."""
        T = self.T
        xs = list(range(self.a - T, self.b + T))
        if side == "right":
            xs = xs[::-1]
        # prefix OR vars: P_k <-> some diff among xs[0..k]
        nv = self.nv
        P = []
        cl = list(self.cl)
        for k, x in enumerate(xs):
            nv += 1
            pk = nv
            d = self.diff_lit(T, x)
            body = ([P[-1]] if P else []) + ([d] if d is not False else [])
            cl.append([-pk] + body) if body else cl.append([-pk])
            P.append(pk)
        with Solver(name="cadical153", bootstrap_with=cl) as s:
            if not s.solve(assumptions=[P[-1]]):
                return None, None
            lo, hi = 0, len(xs) - 1   # smallest k with SAT(P_k)
            while lo < hi:
                mid = (lo + hi) // 2
                if s.solve(assumptions=[P[mid]]):
                    hi = mid
                else:
                    lo = mid + 1
            ok = s.solve(assumptions=[P[lo]])
            assert ok
            m = set(l for l in s.get_model() if l > 0)
        row0 = np.array([1 if self.var[(0, x)] in m else 0
                         for x in range(self.a, self.b)], np.uint8)
        x = xs[lo]
        self._check(row0, x)
        return x, row0

    def _check(self, row0, x):
        """forward-simulate the witness embedded in background; cell (T, x)
        must differ from background."""
        T = self.T
        pad = 2 * T + 4
        lo = self.a - pad
        full = np.array([self.bgbit(0, y) for y in range(lo, self.b + pad)],
                        np.uint8)
        full[self.a - lo:self.b - lo] = row0
        rows = simulate_window(full, T)
        # row T index i corresponds to x = lo + T + i
        i = x - (lo + T)
        assert 0 <= i < len(rows[T])
        cell = rows[T][i]
        assert cell != self.bgbit(T, x), "witness does not reproduce"


def left_D(bg, T, taus=None, x0s=None):
    """min over phases of L(T) - x0 (and per-phase list)."""
    taus = range(bg.tper) if taus is None else taus
    x0s = range(bg.p) if x0s is None else x0s
    res = {}
    for tau in taus:
        for x0 in x0s:
            m = ConeModel(bg, tau, x0, x0 + T, T)
            x, _ = m.extreme("left")
            res[(tau, x0)] = None if x is None else x - x0
    return res


def right_D(bg, T, taus=None, x0s=None):
    taus = range(bg.tper) if taus is None else taus
    x0s = range(bg.p) if x0s is None else x0s
    res = {}
    for tau in taus:
        for x0 in x0s:
            m = ConeModel(bg, tau, x0 - T + 1, x0 + 1, T)
            x, _ = m.extreme("right")
            res[(tau, x0)] = None if x is None else x - x0
    return res


if __name__ == "__main__":
    tile = sys.argv[1]
    Ts = [int(v) for v in sys.argv[2].split(",")]
    bg = Background(tile)
    print(f"tile={tile} p={bg.p} tper={bg.tper} shift={bg.shift}", flush=True)
    for T in Ts:
        L = left_D(bg, T)
        R = right_D(bg, T)
        Lv = [v for v in L.values() if v is not None]
        Rv = [v for v in R.values() if v is not None]
        print(f"T={T} left D=min {min(Lv)} max {max(Lv)} speed>={min(Lv)/T:+.4f} | "
              f"right D=max {max(Rv)} min {min(Rv)} speed<={max(Rv)/T:+.4f}", flush=True)
