"""SAT model of Rule 110 spacetime embedded in ether.

Coordinates: cell (t, x), t >= 0 time (downward), x any integer.
Ether with phase p:  cell(t, x) = ETHER[(x + 4 t + p) mod 14]
(verified: one step shifts the ether tile by 4 mod 14; lattice (7,0),(3,2)).
This equals collider's "absolute phase" c = p + 4t at time t.

A `CNF` holds variables and clauses. A `Spacetime` lives in a CNF: its
cells at t = 0 on [lo, hi) are literals (fresh, or supplied through
`init` so several spacetimes can share unknown cells). Left of lo the row
is ether with phase `left_phase`; right of hi it is ether with phase
`right_phase`, which may be None = "chosen by the solver" (one-hot
selector over the 14 phases). By the speed-1 light cone, at time t the
cells in [lo - t, hi + t) are SAT variables tied by the Rule 110 update and
everything outside is the corresponding ether constant.

`lit(t, x)` returns a literal (int) or a Python bool constant. All clause
helpers simplify constants away. Every solution must be re-verified by
forward simulation (`run_embedded` / `simulate_row`, using ../../engine.py).

`Model(T, lo, hi, ...)` = a Spacetime with its own CNF (single-spacetime
problems such as gliders.py).
"""

import itertools
import os
import sys

import numpy as np
from pysat.solvers import Solver

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

ETHER = "11111000100110"
TILE = 14
ETHER_BITS = [int(c) for c in ETHER]


def ether_bit(phase, t, x):
    return ETHER_BITS[(x + 4 * t + phase) % TILE]


def ether_row(phase, t, lo, hi):
    return np.array([ether_bit(phase, t, x) for x in range(lo, hi)],
                    dtype=np.uint8)


def phase_of(cells, x0, t=0):
    """Phase p such that cells (starting at global x0, time t) equal
    ether(p); None if they are not ether. Needs >= 14 cells."""
    if len(cells) < TILE:
        raise ValueError("need at least 14 cells to determine a phase")
    for p in range(TILE):
        if all(cells[i] == ether_bit(p, t, x0 + i) for i in range(len(cells))):
            return p
    return None


def neg(l):
    return (not l) if isinstance(l, bool) else -l


class CNF:
    def __init__(self, solver="cadical153"):
        self.nvars = 0
        self.clauses = []
        self.solver_name = solver

    def new_var(self):
        self.nvars += 1
        return self.nvars

    def add(self, clause):
        """Add a clause; entries may be ints (literals) or bools."""
        out = []
        for l in clause:
            if l is True:
                return
            if l is False:
                continue
            out.append(l)
        if not out:
            raise ValueError("empty clause added: model is trivially UNSAT")
        self.clauses.append(out)

    def exactly_one(self, lits):
        self.add(list(lits))
        for a, b in itertools.combinations(lits, 2):
            self.add([-a, -b])

    def equal(self, a, b):
        self.add([neg(a), b])
        self.add([a, neg(b)])

    def xor_var(self, a, b):
        """Fresh var v <-> (a xor b)."""
        v = self.new_var()
        self.add([-v, a, b])
        self.add([-v, neg(a), neg(b)])
        self.add([v, neg(a), b])
        self.add([v, a, neg(b)])
        return v

    def solve(self, assumptions=()):
        with Solver(name=self.solver_name, bootstrap_with=self.clauses) as s:
            if not s.solve(assumptions=list(assumptions)):
                return None
            return Assignment(set(l for l in s.get_model() if l > 0))

    def solver(self):
        return Solver(name=self.solver_name, bootstrap_with=self.clauses)


class Assignment:
    def __init__(self, true_set):
        self.true = true_set

    def val(self, lit):
        if isinstance(lit, (bool, np.bool_)):
            return int(lit)
        return int(lit in self.true) if lit > 0 else int(-lit not in self.true)


class Spacetime:
    def __init__(self, cnf, T, lo, hi, left_phase=0, right_phase=0,
                 init=None, window=None):
        """window: optional function t -> (L, R) for t >= 1 restricting the
        variable cells at time t to [L, R) (intersected with the light
        cone); cells outside are FORCED to be the far ether (left of L:
        left phase, right of R: right phase), with the Rule 110 update
        checked on a 1-cell border so the forcing is exact. This is a
        restriction of the search space (nothing may leave the window
        at any time) that makes slow reactions tractable."""
        self.cnf = cnf
        self.window = window
        self.T, self.lo, self.hi = T, lo, hi
        self.left_phase = left_phase
        self.right_phase = right_phase
        self.cells = {}
        if right_phase is None:
            self.sel = [cnf.new_var() for _ in range(TILE)]
            cnf.exactly_one(self.sel)
            self.rres = []
            for j in range(TILE):
                v = cnf.new_var()
                ones = [self.sel[k] for k in range(TILE)
                        if ETHER_BITS[(j + k) % TILE]]
                cnf.add([-v] + ones)
                for s in ones:
                    cnf.add([v, -s])
                self.rres.append(v)
        else:
            self.sel = None
        init = init or {}
        for x in range(lo, hi):
            self.cells[(0, x)] = init[x] if x in init else cnf.new_var()
        self.bounds = {0: (lo, hi)}
        for t in range(1, T + 1):
            L, R = lo - t, hi + t
            if window is not None:
                wl, wr = window(t)
                L, R = max(L, wl), min(R, wr)
                pl_, pr_ = self.bounds[t - 1]
                if abs(L - pl_) > 1 or abs(R - pr_) > 1 or L >= R:
                    raise ValueError(f"window at t={t} must move <= 1 cell per step")
            self.bounds[t] = (L, R)
            for x in range(L, R):
                self.cells[(t, x)] = cnf.new_var()
        for t in range(1, T + 1):
            L, R = self.bounds[t]
            # border of 2: with a window edge moving by <= 1 per step, every
            # forced-ether cell farther out has only forced-ether parents
            lo_chk, hi_chk = (L - 2, R + 2) if window is not None else (L, R)
            for x in range(lo_chk, hi_chk):
                self._rule(self.lit(t - 1, x - 1), self.lit(t - 1, x),
                           self.lit(t - 1, x + 1), self.lit(t, x))

    # convenience passthroughs (single-spacetime use)
    def new_var(self):
        return self.cnf.new_var()

    def add(self, clause):
        self.cnf.add(clause)

    def equal(self, a, b):
        self.cnf.equal(a, b)

    neg = staticmethod(neg)

    def lit(self, t, x):
        v = self.cells.get((t, x))
        if v is not None:
            return v
        if not 0 <= t <= self.T:
            raise IndexError(f"t={t} outside model")
        L, R = self.bounds[t]
        if x < L:
            return bool(ether_bit(self.left_phase, t, x))
        if x < R:
            raise KeyError((t, x))
        if self.right_phase is not None:
            return bool(ether_bit(self.right_phase, t, x))
        return self.rres[(x + 4 * t) % TILE]

    def _rule(self, l, c, r, n):
        add, N = self.cnf.add, neg
        add([N(n), c, r])
        add([N(n), N(l), N(c), N(r)])
        add([N(c), r, n])
        add([c, N(r), n])
        add([l, N(c), N(r), n])

    # -- constraint helpers ---------------------------------------------
    def fix(self, t, x, val):
        l = self.lit(t, x)
        self.cnf.add([l if val else neg(l)])

    def row_is(self, t, x0, bits):
        for i, b in enumerate(bits):
            self.fix(t, x0 + i, int(b))

    def ether_on(self, t, lo, hi, phase):
        for x in range(lo, hi):
            self.fix(t, x, ether_bit(phase, t, x))

    def match_lits(self, t, x0, bits):
        """Literals that are all true iff row t at x0.. equals bits."""
        out = []
        for i, b in enumerate(bits):
            l = self.lit(t, x0 + i)
            out.append(l if int(b) else neg(l))
        return out

    def indicator_matches(self, t, x0, bits):
        """Fresh var m with m -> (row t at x0.. equals bits)."""
        m = self.cnf.new_var()
        for l in self.match_lits(t, x0, bits):
            self.cnf.add([-m, l])
        return m

    def value_row(self, a, t, lo, hi):
        return np.array([a.val(self.lit(t, x)) for x in range(lo, hi)],
                        dtype=np.uint8)

    def value_right_phase(self, a):
        if self.right_phase is not None:
            return self.right_phase
        return [k for k in range(TILE) if a.val(self.sel[k])][0]


class Model(Spacetime):
    """A Spacetime with its own CNF."""

    def __init__(self, T, lo, hi, left_phase=0, right_phase=0,
                 solver="cadical153"):
        super().__init__(CNF(solver), T, lo, hi, left_phase, right_phase)

    @property
    def clauses(self):
        return self.cnf.clauses

    def solver(self):
        return self.cnf.solver()


# ---------------------------------------------------------------------------
# Forward simulation (independent of the SAT model)

def embed(segment, lo, left_phase, right_phase, pad):
    """Row covering [lo - pad, hi + pad): ether(left) | segment | ether(right).
    Returns (row, x0) with row[i] = cell x0 + i at t = 0."""
    hi = lo + len(segment)
    left = ether_row(left_phase, 0, lo - pad, lo)
    right = ether_row(right_phase, 0, hi, hi + pad)
    return np.concatenate([left, np.asarray(segment, np.uint8), right]), lo - pad


def simulate(row, T):
    """History (T+1, len(row)) by ../../engine.py (cyclic boundary)."""
    from engine import history
    return history(np.asarray(row, np.uint8), T)


def run_embedded(segment, lo, left_phase, right_phase, T, margin=0):
    """Simulate a segment embedded in ether; return (hist, x0). The pads
    are wide enough that debris from the cyclic wrap seam cannot reach
    [lo - margin - T, hi + margin + T) within T steps."""
    pad = 2 * T + margin + 2 * TILE
    row, x0 = embed(segment, lo, left_phase, right_phase, pad)
    return simulate(row, T), x0


# ---------------------------------------------------------------------------
# Higher-level constraints (methods attached to Spacetime)

def _periodic(self, t1, t2, lo, hi, dx=0):
    """row t2 [x + dx] == row t1 [x] for x in [lo, hi)."""
    for x in range(lo, hi):
        self.cnf.equal(self.lit(t2, x + dx), self.lit(t1, x))


def _one_of(self, t, lo, hi, candidates):
    """Row t on [lo, hi) equals one of the candidate cell arrays. Returns
    the indicator vars (indicator i true -> candidate i matches)."""
    inds = []
    for cand in candidates:
        m = self.cnf.new_var()
        for x, b in zip(range(lo, hi), cand):
            l = self.lit(t, x)
            self.cnf.add([-m, l if b else neg(l)])
        inds.append(m)
    self.cnf.add(inds)
    return inds


def _differs(self, t, lo, hi, cells, guard=None):
    """Row t on [lo, hi) differs from `cells` somewhere (if guard true)."""
    cl = [] if guard is None else [neg(guard)]
    for x, b in zip(range(lo, hi), cells):
        l = self.lit(t, x)
        cl.append(neg(l) if b else l)
    self.cnf.add(cl)


Spacetime.periodic = _periodic
Spacetime.one_of = _one_of
Spacetime.differs = _differs


def make_window(T, lo, hi, vL, vR, margin=20):
    """Window function for Spacetime: edges follow lines lo + vL t - margin
    and hi + vR t + margin (vL, vR in cells per step, e.g. -0.5 for B
    speed), never outside the light cone and moving <= 1 cell per step."""
    Ls, Rs = {0: lo}, {0: hi}
    for t in range(1, T + 1):
        tl = int(lo + vL * t - margin)
        tr = int(hi + vR * t + margin) + 1
        L = min(max(tl, Ls[t - 1] - 1), Ls[t - 1] + 1)
        R = max(min(tr, Rs[t - 1] + 1), Rs[t - 1] - 1)
        Ls[t], Rs[t] = max(L, lo - t), min(R, hi + t)
    return lambda t: (Ls[t], Rs[t])
