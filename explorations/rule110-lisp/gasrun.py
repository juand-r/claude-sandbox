"""Cook's construction on the event engine (gas.py): the t = 0 layout as a
Gas with lazily materialized sides, and a read driver.

The left side (the ossifier train, rigid at (3, 2)) is materialized one
ossifier at a time from the right; the right side (central region and
table, rigid at (30, -8) until reached) in chunks of TABLE_CHUNK cells cut
at clean ether. ReadWatch and census check the reads exactly as for the
HashLife engines (experiments.sample), on windows rendered by the Gas.
"""

import time
from fractions import Fraction

import numpy as np

import gas
from casim import TILE, layout
from census import MAX_DT, ether_phase
from engine import pack, step_packed, unpack
from experiments import ReadWatch, component_regions, sample

TABLE_CHUNK = 1 << 16          # cells per lazily materialized table chunk
CUT_CELLS = 2 * TILE           # clean ether of one phase at a chunk cut
CUT_SEARCH = 1 << 14           # cells searched beyond a chunk for a cut
TRAIN_SPEED = Fraction(2, 3)
TABLE_SPEED = Fraction(8, 30)
EDGE_SLACK = 64                # cells a moving glider's patch may stray
                               # from its rigid t = 0 translate (checked)


def clean_cut(lay, x):
    """First cut c >= x with CUT_CELLS clean ether of one phase before it
    -> (c, phase constant there)."""
    hi = min(lay.hi, x + CUT_SEARCH)
    lo = x - CUT_CELLS
    ph = ether_phase(lay.cells(lo, hi))         # constant c in row coordinates
    need = CUT_CELLS - TILE + 1                 # windows covering CUT_CELLS cells
    for i in range(len(ph) - need + 1):
        if ph[i] >= 0 and np.all(ph[i:i + need] == ph[i]):
            return lo + i + CUT_CELLS, int(ph[i] - lo) % TILE
    raise ValueError(f"no clean ether cut in [{x}, {hi})")


class Train:
    """Left side: ossifiers k = 1, 2, ... (layout segment n_all - 1 - k)."""

    def __init__(self, lay, n_all):
        self.lay, self.k, self.n_all = lay, 1, n_all

    def src(self):
        i = self.n_all - 1 - self.k
        if i < 0:
            return None
        x, b = self.lay.segments[i]
        self.k += 1
        return b, x, self.lay.phases[i], self.lay.phases[i + 1]

    def bound(self, t):
        i = self.n_all - 1 - self.k
        if i < 0:
            return -(1 << 62)
        x, b = self.lay.segments[i]
        return x + len(b) - 1 + int(TRAIN_SPEED * t) + 1 + EDGE_SLACK


class Table:
    """Right side from x on (x a clean cut, c the ether constant there)."""

    def __init__(self, lay, x, c):
        self.lay, self.x, self.c = lay, x, c

    def src(self):
        if self.x >= self.lay.hi:
            return None
        if self.x + TABLE_CHUNK >= self.lay.hi:
            cut, c = self.lay.hi, self.lay.phases[-1]
        else:
            cut, c = clean_cut(self.lay, self.x + TABLE_CHUNK)
        row = (self.lay.cells(self.x, cut), self.x, self.c, c)
        self.x, self.c = cut, c
        return row

    def bound(self, t):
        if self.x >= self.lay.hi:
            return 1 << 62
        return self.x - int(TABLE_SPEED * t) - 1 - EDGE_SLACK


class GasRun(gas.Gas):
    """A Gas with the HashRun interface that experiments.sample uses."""

    origin = 0

    def ebar_frame(self, t=None):
        t = self.t if t is None else t
        return int(round(Fraction(-8, 30) * t))

    def history(self, lo, hi, depth, advance=False):
        """Rows t..t+depth of [lo, hi), stepped locally (exact on [lo, hi)
        by the light cone, as HashRun.history); the Gas stays at t."""
        if advance:
            raise ValueError("GasRun.history does not advance")
        width = hi - lo + 2 * depth
        words = pack(self.window(lo - depth, hi + depth))
        rows = [unpack(words, width)[depth:width - depth]]
        for _ in range(depth):
            words = step_packed(words)
            rows.append(unpack(words, width)[depth:width - depth])
        return np.array(rows)


def build(lay, n_all, reg=None):
    """GasRun for a casim.layout with n_all ossifiers: ossifier 0 (adjacent
    to block C) and the first table chunk materialized, the rest lazy."""
    x0 = lay.segments[n_all - 1][0]
    x_c = lay.segments[n_all][0]
    cut, c = clean_cut(lay, x_c + TABLE_CHUNK)
    g = GasRun(reg)
    g.append_row(lay.cells(x0, cut), x0, lay.phases[n_all - 1], c)
    g.add_sides(gas.Side("L", *_side(Train(lay, n_all)), float(TRAIN_SPEED)),
                gas.Side("R", *_side(Table(lay, cut, c)), float(TABLE_SPEED)))
    g.start()
    return g


def _side(s):
    return s.src, s.bound


FIRST_GAP = 0.9 * 30           # as epochrun: a safe underestimate (x v)
JUMP_MARGIN = 3


class GasReads:
    """Read outcomes of a CTS program at spacing v on the event engine;
    samples every 2^sample_bits steps around the predicted read times
    (the sampling scheme of epochrun.EpochReads)."""

    def __init__(self, tape, apps, v, n_reads, sample_bits=17, log=print):
        self.apps, self.v, self.log = apps, v, log
        self.every = 1 << sample_bits
        rp = n_reads // len(apps) + 3
        self.n_all = 2 * (n_reads + 3) + 10
        self.lay = layout(tape, apps, self.n_all, rp, v_override=v)
        self.regs = component_regions(tape, apps, rp)
        self.watch = ReadWatch(self.regs[:n_reads], apps, lookahead=2)
        self.run = build(self.lay, self.n_all)
        self.t_wall = time.time()

    def _due(self, j):
        w, starts = self.watch, self.watch.read_at
        if not (w.state[j] == "." and j >= 1 and w.state[j - 1] in "YN!"):
            return None
        if j >= 2 and starts[j - 2] is not None:
            due = 2 * starts[j - 1] - starts[j - 2]
        else:
            due = starts[j - 1] + int(FIRST_GAP * self.v)
        return (due - JUMP_MARGIN * self.every) // 30 * 30

    def run_reads(self):
        w, g = self.watch, self.run
        logged = -1
        while w.pending():
            pending = w.pending()
            if pending[0] // 100 > logged:
                logged = pending[0] // 100
                n_items = sum(1 for _ in g.items())
                self.log(f"[gas] read {pending[0]}: t={g.t}, {g.n_events} events, "
                         f"{n_items} items, {len(g.memo)} collisions, "
                         f"{len(g.reg.orbits)} orbits, wall {time.time() - self.t_wall:.0f}s")
            t = max(g.t, self._due(pending[0]) or 0, (w.t_last or 0) // 30 * 30)
            while w.pending() == pending:
                g.advance_to(t)
                depth = MAX_DT + (-(t + MAX_DT)) % 30
                sample(g, w, pending, depth, advance=False)
                t += self.every
        return w.outcome()
