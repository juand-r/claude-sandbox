"""Exact Rule 110 evolution of an ether-background configuration on a
moving, self-extending window (rigorous; no glider-level assumptions).

State: cells on [x0, x0 + W) at time t; everything outside is ether with
absolute phase cL(t) = cL0 + 4t (left) and cR(t) = cR0 + 4t (right), mod 14
(collider/r110lib conventions: ether cell x at phase c is ETHER[(c+x) % 14]).
Invariant (checked every step, fails loudly): the MARGIN outermost cells on
each side equal the ether. Then cells just outside the window evolve as
ether, so the invariant "outside = ether" is preserved exactly. The window
grows when a defect comes within MARGIN of an edge and is trimmed when more
than 2*MARGIN ether cells sit at an edge.
"""
import numpy as np
from numba import njit

ETHER = np.array([int(c) for c in "11111000100110"], np.uint8)
TILE = 14
MARGIN = 32


def ether(c, lo, hi):
    return ETHER[(c + np.arange(lo, hi)) % TILE]


@njit(cache=True)
def _step(row, a0, a1, b0, b1):
    """New row (same length) from row with ether neighbours: a0 = cell left
    of row[0] two steps out? we pass the two cells left (a0, a1) and two
    right (b0, b1) at time t; only the immediate ones matter."""
    n = row.shape[0]
    out = np.empty(n, np.uint8)
    for i in range(n):
        l = row[i - 1] if i > 0 else a1
        c = row[i]
        r = row[i + 1] if i < n - 1 else b0
        v = (l << 2) | (c << 1) | r
        out[i] = (110 >> v) & 1
    return out


@njit(cache=True)
def _run(row, x0, cL0, cR0, t0, nsteps, eth, margin):
    """Run nsteps; returns (row, x0, t, status). status 0 = done,
    1 = needs extension (defect within margin)."""
    t = t0
    for _ in range(nsteps):
        n = row.shape[0]
        cL = (cL0 + 4 * t) % 14
        cR = (cR0 + 4 * t) % 14
        a1 = eth[(cL + x0 - 1) % 14]
        b0 = eth[(cR + x0 + n) % 14]
        row = _step(row, 0, a1, b0, 0)
        t += 1
        cL = (cL0 + 4 * t) % 14
        cR = (cR0 + 4 * t) % 14
        for i in range(margin):
            if row[i] != eth[(cL + x0 + i) % 14]:
                return row, x0, t, 1
            j = n - 1 - i
            if row[j] != eth[(cR + x0 + j) % 14]:
                return row, x0, t, 1
    return row, x0, t, 0


class Window:
    def __init__(self, row, x0, cL0, cR0):
        self.row, self.x0, self.cL0, self.cR0, self.t = row.copy(), x0, cL0, cR0, 0
        self._check()

    def _check(self):
        n = len(self.row)
        cL = (self.cL0 + 4 * self.t) % 14
        cR = (self.cR0 + 4 * self.t) % 14
        okL = np.array_equal(self.row[:MARGIN], ether(cL, self.x0, self.x0 + MARGIN))
        okR = np.array_equal(self.row[n - MARGIN:], ether(cR, self.x0 + n - MARGIN, self.x0 + n))
        return okL, okR

    def _extend(self):
        okL, okR = self._check()
        cL = (self.cL0 + 4 * self.t) % 14
        cR = (self.cR0 + 4 * self.t) % 14
        ext = 4 * MARGIN
        if not okL:
            self.row = np.concatenate([ether(cL, self.x0 - ext, self.x0), self.row])
            self.x0 -= ext
        if not okR:
            n = len(self.row)
            self.row = np.concatenate([self.row, ether(cR, self.x0 + n, self.x0 + n + ext)])

    def _trim(self):
        cL = (self.cL0 + 4 * self.t) % 14
        cR = (self.cR0 + 4 * self.t) % 14
        n = len(self.row)
        e = ether(cL, self.x0, self.x0 + n)
        diff = np.nonzero(self.row != e)[0]
        if len(diff) and diff[0] > 3 * MARGIN:
            k = diff[0] - 2 * MARGIN
            self.row = self.row[k:]
            self.x0 += k
        n = len(self.row)
        e = ether(cR, self.x0, self.x0 + n)
        diff = np.nonzero(self.row != e)[0]
        if len(diff) and n - 1 - diff[-1] > 3 * MARGIN:
            k = n - 1 - diff[-1] - 2 * MARGIN
            self.row = self.row[:n - k]

    def run(self, T, chunk=2000):
        while self.t < T:
            k = min(chunk, T - self.t)
            row, x0, t, st = _run(self.row, self.x0, self.cL0, self.cR0, self.t, k, ETHER, MARGIN)
            self.row, self.x0, self.t = row, x0, t
            if st == 1:
                self._extend()
            else:
                self._trim()
        return self

    def cells(self, lo, hi):
        """Cells [lo, hi) at the current time (ether outside the window)."""
        cL = (self.cL0 + 4 * self.t) % 14
        cR = (self.cR0 + 4 * self.t) % 14
        out = np.empty(hi - lo, np.uint8)
        for x in range(lo, hi):
            if x < self.x0:
                out[x - lo] = ETHER[(cL + x) % 14]
            elif x >= self.x0 + len(self.row):
                out[x - lo] = ETHER[(cR + x) % 14]
            else:
                out[x - lo] = self.row[x - self.x0]
        return out
