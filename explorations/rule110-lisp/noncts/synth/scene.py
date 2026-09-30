"""Scenes: several items (fixed gliders, free objects, free trains) placed
at explicit spacetime positions in one row, evolved in one CNF, with
region constraints at chosen times. Several scenes may share items and
be tied together (e.g. "the same cell after a crossing, with and without
a relayed signal").

Item placement (item from react.py, canonical frame: cells [0, W) at
t = 0, my-phase 0 on the left, pR on the right): a piece (item, tau, x)
puts the item's row `tau` (0 <= tau < p) at t = 0 with canonical column
x' at global column x' + x. As a t = 0 row, its left ether then has
my-phase 4 tau - x and its right ether 4 tau + pR - x (mod 14).
Consecutive pieces must agree on the ether between them (checked).

Region constraints (method names):
  ether(t, lo, hi, phase)       fixed phase; phase=None -> some phase
                                (returns 14 indicators)
  invariant(t, lo, hi, p, d)    row t+p [x+d] == row t [x] on [lo, hi)
  is_item(t, lo, hi, item, far_left=None, far_right=None, window=None)
                                row t on [lo, hi) == item at some (tau,
                                delta); prunes by a known far phase
  nonempty(t, lo, hi, phase)    differs somewhere from ether(phase)
  tie(other, t, lo, hi, t2=None, shift=0)  cellwise equality across scenes
"""

import numpy as np

from r110sat import Spacetime, TILE, ether_bit, neg, simulate

BAND = 14


class Scene:
    def __init__(self, cnf, T, pieces, name="S", window=None):
        self.cnf, self.T, self.name = cnf, T, name
        pieces = sorted(pieces, key=lambda q: q[2])
        init = {}
        prev_right = None
        prev_end = None
        self.pieces = pieces
        for item, tau, x in pieces:
            lph = (4 * tau - x) % TILE
            rph = (4 * tau + item.pR - x) % TILE
            a, b = x - tau, x + item.W + tau
            if prev_right is not None:
                if prev_right != lph:
                    raise ValueError(f"ether phase mismatch before {item.name}"
                                     f" ({prev_right} vs {lph})")
                if a < prev_end:
                    raise ValueError(f"pieces overlap at {item.name}")
                for xx in range(prev_end, a):
                    init[xx] = bool(ether_bit(prev_right, 0, xx))
            else:
                self.p_left = lph
            for xx in range(a, b):
                init[xx] = item.st.lit(tau, xx - x)
            prev_right, prev_end = rph, b
        self.p_right = prev_right
        self.lo = pieces[0][2] - pieces[0][1]
        self.hi = prev_end
        self.st = Spacetime(cnf, T, self.lo, self.hi, self.p_left,
                            self.p_right, init=init, window=window)

    def lit(self, t, x):
        return self.st.lit(t, x)

    # -- constraints -----------------------------------------------------
    def ether(self, t, lo, hi, phase=None):
        if phase is not None:
            for x in range(lo, hi):
                self.st.fix(t, x, ether_bit(phase, t, x))
            return None
        inds = []
        for ph in range(TILE):
            m = self.cnf.new_var()
            for x in range(lo, hi):
                l = self.lit(t, x)
                self.cnf.add([-m, l if ether_bit(ph, t, x) else neg(l)])
            inds.append(m)
        self.cnf.add(inds)
        return inds

    def invariant(self, t, lo, hi, p, d):
        if t + p > self.T:
            raise ValueError("scene too short for invariance check")
        for x in range(lo, hi):
            self.cnf.equal(self.lit(t + p, x + d), self.lit(t, x))

    def nonempty(self, t, lo, hi, phase, guard=None):
        cl = [] if guard is None else [neg(guard)]
        for x in range(lo, hi):
            l = self.lit(t, x)
            cl.append(neg(l) if ether_bit(phase, t, x) else l)
        self.cnf.add(cl)

    def is_item(self, t, lo, hi, item, far_left=None, far_right=None,
                window=None, only=None):
        """Row t on [lo, hi) == item (row tau, shifted by delta), with
        ether continuing on both sides. Returns [((tau, delta), var)]."""
        cnf = self.cnf
        p = item.period[0]
        opts = []
        for tau in range(p):
            elo, ehi = item.extent(tau)
            for delta in range(lo - elo, hi - ehi + 1):
                if window and not window[0] <= delta <= window[1]:
                    continue
                if only is not None and (tau, delta) != tuple(only):
                    continue
                if far_left is not None and \
                        (4 * tau - delta - 4 * t - far_left) % TILE:
                    continue
                if far_right is not None and \
                        (4 * tau + item.pR - delta - 4 * t - far_right) % TILE:
                    continue
                m = cnf.new_var()
                for x in range(lo, hi):
                    a = self.lit(t, x)
                    b = item.st.lit(tau, x - delta)
                    if isinstance(b, bool):
                        cnf.add([-m, a if b else neg(a)])
                    else:
                        cnf.add([-m, neg(a), b])
                        cnf.add([-m, a, neg(b)])
                opts.append(((tau, delta), m))
        if not opts:
            raise ValueError(f"is_item({item.name}): no placement fits")
        cnf.add([m for _, m in opts])
        return opts

    @staticmethod
    def undisturbed(item, tau, x, t):
        """(tau', delta') of an item placed as piece (tau, x) at time 0,
        observed at time t if nothing touched it."""
        p, d = item.period
        q, tau2 = divmod(tau + t, p)
        return tau2, x + q * d

    def tie(self, other, t, lo, hi, t2=None, shift=0):
        t2 = t if t2 is None else t2
        for x in range(lo, hi):
            self.cnf.equal(self.lit(t, x), other.lit(t2, x + shift))

    # -- decoding / verification ------------------------------------------
    def row(self, sol, t, lo=None, hi=None):
        lo = self.lo - t if lo is None else lo
        hi = self.hi + t if hi is None else hi
        return np.array([sol.val(self.lit(t, x)) for x in range(lo, hi)],
                        np.uint8)

    def simulate(self, sol, T, margin=0):
        """Forward simulation of the decoded t=0 row with ../../engine.py.
        Returns (hist, off): hist[t, x + off] = cell (t, x)."""
        pad = 2 * T + margin + 60
        row0 = self.row(sol, 0)
        left = np.array([ether_bit(self.p_left, 0, x)
                         for x in range(self.lo - pad, self.lo)], np.uint8)
        right = np.array([ether_bit(self.p_right, 0, x)
                          for x in range(self.hi, self.hi + pad)], np.uint8)
        h = simulate(np.concatenate([left, row0, right]), T)
        return h, pad - self.lo

    def check_sat_vs_sim(self, sol):
        """Every modelled row (whole light cone; outside a window the SAT
        values are the forced ether) equals the forward simulation."""
        h, off = self.simulate(sol, self.T)
        for t in range(0, self.T + 1):
            if not np.array_equal(h[t, self.lo - t + off:self.hi + t + off],
                                  self.row(sol, t)):
                return False
        return True
