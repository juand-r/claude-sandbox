"""Long runs of Cook's construction: HashLife in epochs (v0.2).

HashRun (hashlife.py) advances its whole tree at every step. For a large
v that tree holds the whole table and every ossifier, and each advance
moves all of them to new alignments, which HashLife cannot reuse: the cost
per read grows with the table held (NOTES.md, phase 7). Here the tree is
kept small instead, by rebuilding it every few reads (an epoch).

An epoch's universe is the true state truncated to what the next reads
need:
- the active region [A, B): every cell that differs from free evolution
  (tape, moving data, junk, a read in progress), carried over from the
  previous tree as blocks of 2^ALIGN cells on a fixed global grid;
- left of A, the free ossifier train, but only the next few ossifiers;
- right of B, the free table, but only the next few appendants.
Both sides move rigidly (the train by (3, 2), the table by (30, -8)), so
their state at time t is the t = 0 layout translated (Layout.shifted). A
cut in clean ether between gliders evolves exactly like the same cells of
the full row, so truncation is harmless while the excluded gliders cannot
reach the included ones. Every boundary checks this (the old universe's
cut edges must lie outside the active region) and raises otherwise.

At each boundary the memo tables are cleared and the new tree is
re-hash-consed (hashlife.recanonicalize), so memory stays bounded.

Reads are sampled on a local copy of the tree around the watched regions
(local_run), so samples never step the big tree by small amounts.
"""

import os
import pickle
import time

from casim import Layout, TILE, _phase_const, ether_rotation, layout
from census import MAX_DT
from experiments import READS_MARGIN, ReadWatch, component_regions, sample
import hashlife as hl
from hashlife import (LEAF, HashRun, child_a, child_b, join, level,
                      node_from_layout, value)

ALIGN = 16                 # carried blocks: 2^16 cells on a global grid
GRID = 1 << ALIGN
CARRY_MARGIN = GRID        # free cells kept on each side of the active extent
CUT_TILES = 3              # clean ether tiles (one phase) required at a cut
OSS_SPEED = (2, 3)         # ossifier train: (cells, steps)
CLOSING_SPEED = 14 / 15    # ossifiers (2/3) against Ebar-speed matter (-4/15)
APPS_AHEAD = 3             # appendants kept beyond the epoch's last read
OSS_AHEAD = 3              # ossifiers kept beyond the kinematic estimate
HORIZON = 2.0              # truncation must hold for HORIZON x the epoch


def _floor(x):
    return x // GRID * GRID


def _ceil(x):
    return -(-x // GRID) * GRID


def table_cut(x0, bits, x_end):
    """Largest cut x <= x_end such that the CUT_TILES tiles before it are
    ether of one phase (no glider is split). -> (x, phase constant)."""
    for j in range(x_end - x0, CUT_TILES * TILE - 1, -1):
        cs = set()
        for k in range(CUT_TILES):
            a = j - (k + 1) * TILE
            r = ether_rotation(bits[a:a + TILE])
            if r is None:
                break
            cs.add((r - (x0 + a)) % TILE)
        else:
            if len(cs) == 1:
                return x0 + j, cs.pop()
    raise ValueError(f"no clean cut before {x_end}")


class Universe:
    """Truncated free content in t = 0 coordinates: ossifiers 0..n_oss-1
    (ossifier 0 is next to block C) and the right side (central region and
    table, one or more adjacent segments) cut at x_cut. lay is the full
    casim.layout; n_all its number of ossifiers."""

    def __init__(self, lay, n_all, n_oss, x_cut):
        if not 1 <= n_oss <= n_all:
            raise ValueError(f"need 1 <= n_oss <= {n_all}, got {n_oss}")
        segs, ph = lay.segments, lay.phases
        x_last, b_last = segs[n_all - 1]               # ossifier 0
        c_after = _phase_const(b_last[-TILE:], x_last + len(b_last) - TILE)
        self.left = Layout(segs[n_all - n_oss:n_all], ph[n_all - n_oss:n_all] + [c_after])
        right = segs[n_all:]
        x_cut = min(x_cut, lay.hi)
        i = max(k for k, (x, _) in enumerate(right) if x < x_cut)
        xi, bi = right[i]
        cut, c_cut = table_cut(xi, bi, min(x_cut, xi + len(bi)))
        xr, br = right[0]
        self.right = Layout(right[:i] + [(xi, bi[:cut - xi])],
                            [_phase_const(br[:TILE], xr)] + [None] * i + [c_cut])
        self.n_oss, self.x_cut = n_oss, cut

    def at(self, t):
        """(left, right) Layouts of the free sides at time t."""
        if t % 30:
            raise ValueError("free sides are translations only at t = 0 mod 30")
        return (self.left.shifted(OSS_SPEED[0] * t // OSS_SPEED[1]),
                self.right.shifted(-8 * t // 30))


def subnode(run, x, k):
    """Node for cells [x, x + 2^k) of run's current row. Inside the tree x
    must be aligned to 2^k relative to run.x0; outside it, ether."""
    size = 1 << level(run.root)
    if x + (1 << k) <= run.x0 or x >= run.x0 + size:
        c = run.cL if x < run.x0 else run.cR
        return run._ether(k, x, c)
    if not (run.x0 <= x and x + (1 << k) <= run.x0 + size) or (x - run.x0) % (1 << k):
        raise ValueError(f"block [{x}, +2^{k}) is not aligned inside the tree")
    n, pos = run.root, run.x0
    while level(n) > k:
        half = 1 << (level(n) - 1)
        if x < pos + half:
            n = child_a(n)
        else:
            n, pos = child_b(n), pos + half
    return n


def _composite(left, right, split, x, k):
    """Node for [x, x + 2^k) of the free rows: left of split the ossifier
    train, from split on the table."""
    if x + (1 << k) <= split:
        return node_from_layout(left, x, k)
    if x >= split:
        return node_from_layout(right, x, k)
    if k == LEAF:
        import numpy as np
        return hl.from_cells(np.concatenate([left.cells(x, split),
                                             right.cells(split, x + (1 << k))]))
    h = 1 << (k - 1)
    return join(_composite(left, right, split, x, k - 1),
                _composite(left, right, split, x + h, k - 1))


def _leaf_diff(n, f, last):
    d = value(n) ^ value(f)
    return (d.bit_length() - 1) if last else ((d & -d).bit_length() - 1)


def diff_extent(run, left, right, split):
    """(a, b): the first and last cell where run's row differs from the
    free rows (_composite). Nodes are hash-consed, so equal subtrees have
    the same id and are skipped without descending."""
    def search(n, x, last):
        k = level(n)
        f = _composite(left, right, split, x, k)
        if f == n:
            return None
        if k == LEAF:
            return x + _leaf_diff(n, f, last)
        h = 1 << (k - 1)
        a, b = child_a(n), child_b(n)
        order = ((b, x + h), (a, x)) if last else ((a, x), (b, x + h))
        for m, y in order:
            r = search(m, y, last)
            if r is not None:
                return r
        return None
    a = search(run.root, run.x0, False)
    b = search(run.root, run.x0, True)
    if a is None:
        raise RuntimeError(f"t={run.t}: no active region")
    return a, b


def _build(run, A, B, left, right, x, k):
    if x + (1 << k) <= A:
        return node_from_layout(left, x, k)
    if x >= B:
        return node_from_layout(right, x, k)
    if A <= x and x + (1 << k) <= B and k <= ALIGN:
        return subnode(run, x, k)
    h = 1 << (k - 1)
    return join(_build(run, A, B, left, right, x, k - 1),
                _build(run, A, B, left, right, x + h, k - 1))


def rebuild(run, A, B, left, right, collect=True):
    """New HashRun at run.t: run's cells on [A, B) (multiples of GRID),
    the free rows left/right of it. collect: clear the memo tables and
    keep only the new tree's nodes (otherwise every node and memoized
    result survives, and later advances can reuse them)."""
    if A % GRID or B % GRID or run.x0 % GRID:
        raise ValueError("carry bounds and the tree must be on the grid")
    lo, hi = min(left.lo, A), max(right.hi, B)
    k = max(ALIGN + 2, (hi - lo + 2 * GRID).bit_length() + 2)
    x0 = _floor((lo + hi) // 2 - (1 << (k - 1)))
    root = _build(run, A, B, left, right, x0, k)
    if collect:
        root = hl.recanonicalize(root)
    new = HashRun.__new__(HashRun)
    # HashRun's ether constants are t = 0 constants (it adds 4t itself);
    # the shifted layouts' phases are constants at time t
    shift = 4 * run.t
    new._start(root, x0, (left.phases[0] - shift) % TILE,
               (right.phases[-1] - shift) % TILE, 0, run.t)
    return new


def local_run(run, lo, hi):
    """A HashRun on the aligned blocks of run's tree that cover [lo, hi).
    After s steps it is exact on [lo + s, hi - s): garbage enters only
    from the cut edges, at most one cell per step."""
    a, b = _floor(lo), _ceil(hi)
    k = ALIGN
    while (1 << k) < b - a:
        k += 1

    def piece(x, j):
        if j == ALIGN:
            return subnode(run, x, ALIGN)
        h = 1 << (j - 1)
        return join(piece(x, j - 1), piece(x + h, j - 1))
    temp = HashRun.__new__(HashRun)
    temp._start(piece(a, k), a, run.cL, run.cR, 0, run.t)
    return temp


# Between reads nothing is sampled: the next read is due one read interval
# (the last two read starts apart; before that, a fraction of one ossifier
# period, 30v) after the previous one, and sampling resumes JUMP_MARGIN
# samples before that. A read that starts earlier is still caught by the
# next sample (its region differs from its census taken long before), only
# its start time is then late. Watching two regions suffices: region j+1's
# census is taken while read j is under way, long before read j+1.
JUMP_MARGIN = 3
FIRST_GAP = 0.9 * 30       # x v: a safe underestimate of the first interval
LOOKAHEAD = 2
JUMP_GRID_PER_V = 30 / 8   # main-tree jumps land on multiples of 2^b, the
                           # largest power of two <= 30v / 8 (an eighth of a
                           # read interval), so a jump is one or two HashLife
                           # advances; local copies cover the remainder


class EpochReads:
    """read_outcomes for long runs: epochs (module docstring), jumps
    between predicted reads, samples on local copies of the tree.

    Samples are 2^sample_bits steps apart: each is one HashLife advance of
    the local copy plus a census history stepped locally (30-59 steps, so
    that the census lands on t = 0 mod 30). reach: how far a local copy is
    stepped before it is rebuilt from the main tree (default: two jump
    grid units plus 2^20); epoch: reads per epoch."""

    def __init__(self, tape, apps, v, n_reads, sample_bits=17, reach=None,
                 epoch=8, log=print, checkpoint=None, max_nodes=None):
        self.jump_grid = 1 << max(0, int(v * JUMP_GRID_PER_V).bit_length() - 1)
        if reach is None:
            reach = 2 * self.jump_grid + (1 << 20)
        self.key = (tape, tuple(apps), v, n_reads, sample_bits, reach, epoch)
        self.checkpoint = checkpoint
        self.apps, self.v, self.reach, self.epoch = apps, v, reach, epoch
        self.sample_bits = sample_bits
        # memo tables are cleared at a rebuild only past this many nodes
        # (None: at every rebuild)
        self.max_nodes = max_nodes
        self.every = 1 << sample_bits
        self.log = log
        # enough table periods for the reads plus the carry margins
        r2 = component_regions(tape, apps, 2)
        width = r2[len(apps)][0] - r2[0][0]
        rp = n_reads // len(apps) + 3 + -(-4 * GRID // width)
        # ossifiers for the whole run: one per read, at least; at small v reads
        # come further apart than 30v (fixed costs per read), so be generous
        # (the epochs check that the train never runs out)
        self.n_all = 2 * (n_reads + 3) + 10
        self.lay = layout(tape, apps, self.n_all, rp, v_override=v)
        self.regs = component_regions(tape, apps, rp)
        self.watch = ReadWatch(self.regs[:n_reads], apps, lookahead=LOOKAHEAD)
        x_c = self.lay.segments[self.n_all][0]
        self.uni = self._universe(0, x_c, 0)
        left, right = self.uni.at(0)
        # at t = 0 ossifier 0 touches block C: the gap between them is empty
        self.run = HashRun.from_layout(Layout(left.segments + right.segments,
                                              left.phases[:-1] + [None] + right.phases[1:]),
                                       align=GRID)
        self.next_epoch = epoch
        self.t_wall = time.time()
        if checkpoint and os.path.exists(checkpoint):
            self._resume()

    def _save(self):
        """Checkpoint at an epoch boundary, where the tree is smallest."""
        r = self.run
        state = {"key": self.key, "tree": hl.dump(r.root),
                 "run": (r.x0, r.cL, r.cR, r.t),
                 "uni": (self.uni.n_oss, self.uni.x_cut),
                 "watch": {k: getattr(self.watch, k)
                           for k in ("before", "state", "read_at", "last", "t_last")},
                 "next_epoch": self.next_epoch}
        tmp = self.checkpoint + ".tmp"
        with open(tmp, "wb") as fh:
            pickle.dump(state, fh)
        os.replace(tmp, self.checkpoint)

    def _resume(self):
        with open(self.checkpoint, "rb") as fh:
            state = pickle.load(fh)
        # the saved state depends on the program, v and the read count, not
        # on sampling or epoch settings (key[:4])
        if state["key"][:4] != self.key[:4]:
            raise ValueError(f"checkpoint {self.checkpoint} is for another run")
        x0, cL, cR, t = state["run"]
        self.run = HashRun.__new__(HashRun)
        self.run._start(hl.load(state["tree"]), x0, cL, cR, 0, t)
        self.uni = Universe(self.lay, self.n_all, *state["uni"])
        for k, val in state["watch"].items():
            setattr(self.watch, k, val)
        self.next_epoch = state["next_epoch"]
        self.log(f"resumed from {self.checkpoint} at t={t}")

    def _universe(self, t, A, j):
        """Universe for an epoch starting at time t with read j next and
        the active region starting at A (global columns at time t)."""
        # the epoch's reads, plus a local copy's reach beyond the last one
        horizon = HORIZON * (self.epoch * 30 * self.v + self.reach)
        reach_left = A - CLOSING_SPEED * horizon - 3 * GRID
        shift = OSS_SPEED[0] * t // OSS_SPEED[1]
        n = 0
        for k in range(self.n_all):          # ossifier k: segment n_all-1-k
            x = self.lay.segments[self.n_all - 1 - k][0] + shift
            if x < reach_left:
                break
            n = k + 1
        n = min(self.n_all, n + OSS_AHEAD)
        j_end = j + self.epoch + APPS_AHEAD + self.reach // (27 * self.v) + 1
        # the next boundary carries up to ~2 GRID beyond the read point
        x_end = (self.regs[j_end][1] + 3 * GRID if j_end < len(self.regs)
                 else self.lay.hi)
        return Universe(self.lay, self.n_all, n, x_end)

    def _epoch(self, j):
        # the free sides are translations of the t = 0 layout only at
        # t = 0 mod 30
        self.run.step(-self.run.t % 30)
        run, t = self.run, self.run.t
        split = self.regs[j][0] - 8 * t // 30
        left, right = self.uni.at(t)
        a, b = diff_extent(run, left, right, split)
        A, B = _floor(a - CARRY_MARGIN), _ceil(b + CARRY_MARGIN)
        if not (left.lo < A and B < right.hi):
            raise RuntimeError(
                f"t={t}: the active region [{a}, {b}] reached a truncation edge "
                f"(ossifiers from {left.lo}, table to {right.hi}): epoch too long")
        self.uni = self._universe(t, A, j)
        left, right = self.uni.at(t)
        collect = self.max_nodes is None or hl.stats()["nodes"] > self.max_nodes
        self.run = rebuild(run, A, B, left, right, collect)
        st = hl.stats()
        self.log(f"epoch at read {j}, t={t}: active [{a}, {b}] ({b - a} cells), "
                 f"{self.uni.n_oss} ossifiers, table to {self.uni.x_cut}, "
                 f"{st['nodes']} nodes, wall {time.time() - self.t_wall:.0f}s")

    def _due(self, j):
        """Sample time to aim for before read j (None: sample now)."""
        w, starts = self.watch, self.watch.read_at
        if not (w.state[j] == "." and j >= 1 and w.state[j - 1] in "YN!"):
            return None
        if j >= 2 and starts[j - 2] is not None:
            due = 2 * starts[j - 1] - starts[j - 2]
        else:
            due = starts[j - 1] + int(FIRST_GAP * self.v)
        return (due - JUMP_MARGIN * self.every) // 30 * 30

    def run_reads(self):
        w = self.watch
        while w.pending():
            pending = w.pending()
            j = pending[0]
            if j >= self.next_epoch and w.state[j] == ".":
                self._epoch(j)
                self.next_epoch = j + self.epoch
                if self.checkpoint:
                    self._save()
            due = self._due(j)
            # never sample earlier than the last sample: a read that started
            # while the previous one was watched would be seen unread again
            start = max(due or 0, (w.t_last or 0) // 30 * 30)
            # the main tree jumps on the grid; the local copy covers the rest
            grid_t = start // self.jump_grid * self.jump_grid
            if grid_t > self.run.t:
                self.run.step(grid_t - self.run.t)
            # a local copy around the watched regions, valid for `reach` steps
            lo_g, hi_g = w.span(pending)
            sh = -8 * self.run.t // 30
            margin = self.reach + 4 * MAX_DT + 64
            temp = local_run(self.run, lo_g + sh - self.reach * 8 // 30 - margin,
                             hi_g + sh + margin)
            t0 = temp.t
            if start > temp.t:
                temp.step(start - temp.t)       # no samples before the read is due
            while w.pending() == pending and temp.t + self.every - t0 <= self.reach:
                temp.advance(self.sample_bits)
                depth = MAX_DT + (-(temp.t + MAX_DT)) % 30
                sample(temp, w, pending, depth, advance=False)
            if w.pending() == pending:
                # the read outlasted the local copy: move the main tree on
                # (to t = 0 mod 30, where epochs can start)
                self.run.step((temp.t - self.run.t) // 30 * 30)
        return w.outcome()
