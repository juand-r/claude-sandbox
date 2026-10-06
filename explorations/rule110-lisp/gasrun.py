"""Cook's construction on the event engine (gas.py): the t = 0 layout as a
Gas with lazily materialized sides, and a read driver.

The left side (the ossifier train, rigid at (3, 2)) is materialized one
ossifier at a time from the right; the right side (central region and
table, rigid at (30, -8) until reached) in chunks of TABLE_CHUNK cells cut
at clean ether. ReadWatch and census check the reads exactly as for the
HashLife engines (experiments.sample), on windows rendered by the Gas.
"""

import os
import pickle
import time
from fractions import Fraction

import numpy as np

import gas
from casim import TILE, layout
from census import FAMILIES, MAX_DT, ether_phase
from engine import pack, step_packed, unpack
from experiments import ReadWatch, component_regions, sample, sample_rel

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

    def linear(self):
        """bound(t) = b0 + num * t // den (t >= 0), for gasc."""
        i = self.n_all - 1 - self.k
        if i < 0:
            return -(1 << 62), 0, 1
        x, b = self.lay.segments[i]
        return x + len(b) + EDGE_SLACK, TRAIN_SPEED.numerator, TRAIN_SPEED.denominator


class Table:
    """Right side from x on (x a clean cut, c the ether constant there).

    period: (s0, w) when the layout repeats one super-period of w cells
    from s0 on (casim.layout's periodic right side). Chunks are then cut
    at the same offsets in every period, so every period yields the same
    chunks, and the engine splits each distinct chunk only once."""

    def __init__(self, lay, x, c, period=None):
        self.lay, self.x, self.c = lay, x, c
        self.cuts = None
        if period is not None:
            # cuts y0 + i w + o_j: the first clean cut y0 >= s0, then one
            # about every TABLE_CHUNK cells up to y0 + w (the next y0)
            s0, w = period
            cuts = [clean_cut(lay, s0)]
            while True:
                y, cy = clean_cut(lay, cuts[-1][0] + TABLE_CHUNK)
                if y >= cuts[0][0] + w:
                    break
                cuts.append((y, cy))
            self.y0, self.w = cuts[0][0], w
            self.cuts = [(y - self.y0, cy) for y, cy in cuts]   # o_j, constant

    def _next_cut(self):
        x, lay = self.x, self.lay
        if self.cuts is not None:
            first = self.y0
            if x >= first:
                # the next grid point after x (x itself, a clean cut, may be
                # off the grid: the first chunk is cut before the grid is used)
                i, r = divmod(x - self.y0, self.w)
                j = next((j for j, (o, _) in enumerate(self.cuts) if o > r), len(self.cuts))
                if j == len(self.cuts):
                    i, j = i + 1, 0
                o, c = self.cuts[j]
                return self.y0 + i * self.w + o, (c - i * self.w) % TILE
            cut, c = clean_cut(lay, x + TABLE_CHUNK)
            return (cut, c) if cut < first else (first, self.cuts[0][1])
        return clean_cut(lay, x + TABLE_CHUNK)

    def src(self):
        if self.x >= self.lay.hi:
            return None
        cut, c = self._next_cut() if self.x + TABLE_CHUNK < self.lay.hi else (self.lay.hi, None)
        if cut >= self.lay.hi:
            cut, c = self.lay.hi, self.lay.phases[-1]
        row = (self.lay.cells(self.x, cut), self.x, self.c, c)
        self.x, self.c = cut, c
        return row

    def bound(self, t):
        if self.x >= self.lay.hi:
            return 1 << 62
        return self.x - int(TABLE_SPEED * t) - 1 - EDGE_SLACK

    def linear(self):
        """bound(t) = b0 - num * t // den (t >= 0), for gasc."""
        if self.x >= self.lay.hi:
            return 1 << 62, 0, 1
        return self.x - 1 - EDGE_SLACK, TABLE_SPEED.numerator, TABLE_SPEED.denominator


class RunInterface:
    """The HashRun interface that experiments.sample uses, for a Gas."""

    origin = 0

    def ebar_frame(self, t=None):
        t = self.t if t is None else t
        return int(round(Fraction(-8, 30) * t))

    def history(self, lo, hi, depth, advance=False):
        """Rows t..t+depth of [lo, hi), stepped locally (exact on [lo, hi)
        by the light cone, as HashRun.history); the Gas stays at t. Only
        the rows census reads (the last, and the last minus each family's
        period) are unpacked; asking for another raises."""
        if advance:
            raise ValueError("GasRun.history does not advance")
        width = hi - lo + 2 * depth
        need = {depth} | {depth - dt for dt, _ in FAMILIES.values()}
        words = pack(self.window(lo - depth, hi + depth))
        rows = {}
        for k in range(depth + 1):
            if k:
                words = step_packed(words)
            if k in need:
                rows[k] = unpack(words, width)[depth:width - depth]
        return _Rows(rows, depth + 1, hi - lo)


class _Rows:
    """Some rows of a history (row k = time t + k), indexed like an array
    of all of them."""

    def __init__(self, rows, n, width):
        self.rows, self.n, self.shape = rows, n, (n, width)

    def __len__(self):
        return self.n

    def __getitem__(self, i):
        k = i + self.n if i < 0 else i
        if k not in self.rows:
            raise KeyError(f"history row {i} was not kept")
        return self.rows[k]


class GasRun(RunInterface, gas.Gas):
    pass


def _cgas_run():
    from gasc import CGas

    class CGasRun(RunInterface, CGas):
        pass
    return CGasRun


def table_period(lay, n_all):
    """(s0, w) if the layout's right side repeats one shared super-period
    (casim.layout), else None."""
    right = lay.segments[n_all:]
    if len(right) >= 4 and right[2][1] is right[1][1]:
        return right[1][0], right[2][0] - right[1][0]
    return None


def build(lay, n_all, engine="c"):
    """Gas for a casim.layout with n_all ossifiers: ossifier 0 (adjacent
    to block C) and the first table chunk materialized, the rest lazy.
    engine: "c" (gasc.CGas) or "py" (gas.Gas, the reference)."""
    x0 = lay.segments[n_all - 1][0]
    x_c = lay.segments[n_all][0]
    cut, c = clean_cut(lay, x_c + TABLE_CHUNK)
    g = GasRun() if engine == "py" else _cgas_run()()
    g.append_row(lay.cells(x0, cut), x0, lay.phases[n_all - 1], c)
    g.add_sides(_side("L", Train(lay, n_all), TRAIN_SPEED),
                _side("R", Table(lay, cut, c, table_period(lay, n_all)), TABLE_SPEED))
    g.start()
    return g


def _side(name, s, speed):
    side = gas.Side(name, s.src, s.bound, speed)
    side.linear = s.linear
    return side


FIRST_GAP = 0.9 * 30           # as epochrun: a safe underestimate (x v)
JUMP_MARGIN = 3


class GasReads:
    """Read outcomes of a CTS program at spacing v on the event engine;
    samples every 2^sample_bits steps around the predicted read times
    (the sampling scheme of epochrun.EpochReads)."""

    def __init__(self, tape, apps, v, n_reads, sample_bits=17, log=print, engine="c",
                 checkpoint=None, ckpt_every=500, census="particles", stop_on_fail=True,
                 rope=False, rope_every=25):
        """census: "cells" (experiments.sample: census() of the rendered
        span), "particles" (gascensus: the same clusters from the
        particles, C engine only), or "both" (raise on any difference in
        the watched regions). stop_on_fail: stop at the first read that
        settles as '!' (the construction has failed; what follows is
        debris), keeping the last checkpoint."""
        if census not in ("cells", "particles", "both"):
            raise ValueError(f"census must be cells, particles or both, not {census!r}")
        if census != "cells" and engine != "c":
            raise ValueError("the particle census needs the C engine")
        self.census, self.stop_on_fail = census, stop_on_fail
        if rope and (engine != "c" or checkpoint):
            raise ValueError("the rope needs the C engine and no checkpoints (not saved yet)")
        self.rope, self.rope_every = rope, rope_every
        self.failed = None
        self.apps, self.v, self.log = apps, v, log
        self.every = 1 << sample_bits
        self.key = (tape, tuple(apps), v, n_reads)
        self.checkpoint, self.ckpt_every = checkpoint, ckpt_every
        rp = n_reads // len(apps) + 3
        self.n_all = 2 * (n_reads + 3) + 10
        self.lay = layout(tape, apps, self.n_all, rp, v_override=v)
        self.regs = component_regions(tape, apps, rp)
        self.watch = ReadWatch(self.regs[:n_reads], apps, lookahead=2)
        if checkpoint and os.path.exists(checkpoint):
            self._resume()
        else:
            self.run = build(self.lay, self.n_all, engine)
        self.t_wall = time.time()
        if census != "cells":
            from gascensus import ParticleCensus
            self.pc = ParticleCensus(self.run)

    _WATCH = ("before", "state", "read_at", "last", "t_last", "n_ebar")

    def _save(self):
        """Checkpoint (C engine only): the gas, the sides' positions, the
        read check."""
        g = self.run
        sides = [s.linear.__self__ for s in g.sides]
        state = {"key": self.key, "gas": g.state(),
                 "train_k": sides[0].k, "table": (sides[1].x, sides[1].c),
                 "watch": {k: getattr(self.watch, k) for k in self._WATCH}}
        tmp = self.checkpoint + ".tmp"
        with open(tmp, "wb") as fh:
            pickle.dump(state, fh)
        os.replace(tmp, self.checkpoint)

    def _resume(self):
        with open(self.checkpoint, "rb") as fh:
            state = pickle.load(fh)
        if state["key"] != self.key:
            raise ValueError(f"checkpoint {self.checkpoint} is for another run")
        train = Train(self.lay, self.n_all)
        train.k = state["train_k"]
        table = Table(self.lay, *state["table"], table_period(self.lay, self.n_all))
        sides = [_side("L", train, TRAIN_SPEED), _side("R", table, TABLE_SPEED)]
        self.run = _cgas_run().from_state(state["gas"], sides)
        for k, val in state["watch"].items():
            setattr(self.watch, k, val)
        self.watch.forget_settled()
        self.log(f"resumed from {self.checkpoint} at t={self.run.t}")

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
                if self.checkpoint and logged >= 0 and pending[0] % self.ckpt_every < 100:
                    self._save()
                logged = pending[0] // 100
                self.log(f"[gas] read {pending[0]}: t={g.t}, {g.n_events} events, "
                         f"{g.count()} items, {len(g.memo)} collisions, "
                         f"{len(g.reg.orbits)} orbits, wall {time.time() - self.t_wall:.0f}s")
            if self.rope and pending[0] % self.rope_every == 0 and pending[0] != getattr(self, "_roped", -1):
                self._roped = pending[0]
                g.rope_absorb()
            t = max(g.t, self._due(pending[0]) or 0, (w.t_last or 0) // 30 * 30)
            while w.pending() == pending:
                g.advance_to(t)
                depth = MAX_DT + (-(t + MAX_DT)) % 30
                self._sample(pending, depth)
                t += self.every
            bad = [j for j in pending if w.state[j] == "!"]
            if bad and self.stop_on_fail:
                self.failed = bad[0]
                self.log(f"[gas] read {bad[0]} settled as '!': the construction failed; "
                         f"stopping at t={g.t} (last checkpoint kept)")
                return w.outcome()
        return w.outcome()

    def _sample(self, pending, depth):
        w, g = self.watch, self.run
        if self.census == "cells":
            sample(g, w, pending, depth, advance=False)
            return
        T, rel = self.pc.rel(w, pending, depth)
        if self.census == "both":
            Tc, rel_c = sample_rel(g, w, pending, depth, advance=False)

            def inside(r):
                return [c for c in r if any(w.regs[j][0] <= c[0] < w.regs[j][1] for j in pending)]
            if Tc != T or inside(rel) != inside(rel_c):
                a, b = inside(rel), inside(rel_c)
                diff = sorted(set(a) ^ set(b))[:10]
                raise AssertionError(f"t={T}: particle census differs from the cell census "
                                     f"({len(a)} vs {len(b)} clusters; first differences {diff})")
        w.observe(T, pending, rel)
