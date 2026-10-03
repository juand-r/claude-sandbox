"""Running an encoded cyclic tag system on the automaton.

encoder.assemble() produces a finite row: periodic left side, central tape
region, periodic right side. To simulate it we embed that row in pure
ether padding and run the bit-packed engine on the whole (cyclic) array.
The padding must be phase-matched: the left pad continues the ether
exactly as the row begins, and the right pad continues it exactly as the
row ends (after trimming the ragged right edge back to a clean ether
cut). Debris from the single wrap seam then spreads at speed <= 1 and
must not reach the region of interest within the run; callers size the
pads for that.

Positions: `origin` is the array index of the encoder's global column 0
(the left edge of block C). Moving data and table data travel with the
Ebar velocity, so a window following them is centred at
origin + EBAR_VELOCITY * t.
"""

from fractions import Fraction

import numpy as np

from encoder import assemble
from engine import ETHER, pack, step_packed, step_packed_n, unpack

EBAR_VELOCITY = Fraction(-8, 30)
TILE = len(ETHER)


def ether_rotation(chunk):
    """Rotation r such that chunk == ETHER[r:] + ETHER[:r], else None."""
    s = "".join(map(str, chunk))
    for r in range(TILE):
        if ETHER[r:] + ETHER[:r] == s:
            return r
    return None


def trim_right_to_ether(bits, tiles=3, max_back=4000):
    """Cut the row's ragged right edge back to a point preceded by `tiles`
    consecutive clean ether tiles. Raises if none is found."""
    for back in range(max_back):
        j = len(bits) - back
        if all(ether_rotation(bits[j - (k + 1) * TILE:j - k * TILE]) is not None
               for k in range(tiles)):
            return bits[:j]
    raise ValueError("no clean ether cut near the right edge")


def ether_pad(rotation, width):
    tile = np.array([int(c) for c in ETHER[rotation:] + ETHER[:rotation]],
                    dtype=np.uint8)
    return np.tile(tile, width // TILE)


def padded_row(tape, appendants, left_periods, right_periods, left_pad,
               right_pad, v_override=None, left_gaps=None):
    """-> (row, origin): the assembled row embedded in phase-matched ether."""
    bits, placed = assemble(tape, appendants, left_periods, right_periods,
                            v_override=v_override, left_gaps=left_gaps)
    origin = -placed[0].gspan(0)[0]
    bits = trim_right_to_ether(bits)
    rl, rr = ether_rotation(bits[:TILE]), ether_rotation(bits[-TILE:])
    if rl is None:
        raise ValueError("assembled row does not start in clean ether")
    left = ether_pad(rl, left_pad)
    row = np.concatenate([left, bits, ether_pad(rr, right_pad)])
    return row, origin + len(left)


# ---------------------------------------------------------------------------
# Sparse layout (v0.2): the t=0 row without materializing the left side.
#
# The left side is ether except for the ossifiers. Every A block's t=0 row
# is 28 cells of ether (two tiles), and attaching an A to an A keeps the row
# phase dy mod 3 (encoder._FIT_CACHE), so the v A blocks between two
# ossifiers are placed in closed form. A run with Cook's v for a compiled
# Turing machine (v ~ 3e6, ~7e4 ossifiers) has a left side of ~6e12 cells;
# described this way it is ~7e4 short segments.

A_ROW_CELLS = 28              # t=0 width of one A block (checked below)


class Layout:
    """The t=0 row as non-ether segments and the ether between them.

    segments: [(x, bits)] in global columns, left to right, not
    overlapping. phases[i] is the ether phase constant of the gap left of
    segment i (cell x reads ETHER[(phases[i] + x) % 14]); phases[-1] is the
    ether right of the last segment. A gap of length 0 has phase None."""

    def __init__(self, segments, phases):
        if len(phases) != len(segments) + 1:
            raise ValueError("need one phase per gap")
        for (x0, b0), (x1, _), c in zip(segments, segments[1:], phases[1:]):
            if x0 + len(b0) > x1:
                raise ValueError(f"segments overlap at {x1}")
            if (x0 + len(b0) < x1) != (c is not None):
                raise ValueError(f"gap before {x1}: phase given iff nonempty")
        self.segments, self.phases = segments, phases
        self.starts = [x for x, _ in segments]
        self.lo = segments[0][0]
        self.hi = segments[-1][0] + len(segments[-1][1])

    def _first_piece(self, lo):
        """Index k such that lo lies in gap k or in segment k."""
        from bisect import bisect_right
        k = bisect_right(self.starts, lo) - 1     # segment k starts <= lo
        if k >= 0 and lo < self.starts[k] + len(self.segments[k][1]):
            return k
        return k + 1

    def cells(self, lo, hi):
        """uint8 cells [lo, hi) of the t=0 row."""
        out = np.empty(hi - lo, dtype=np.uint8)
        n, k, x = len(self.segments), self._first_piece(lo), lo
        while x < hi:
            e = min(hi, self.starts[k]) if k < n else hi
            if x < e:                                   # gap k
                if self.phases[k] is None:
                    raise AssertionError(f"empty gap {k} has cells")
                out[x - lo:e - lo] = _ether_cells(self.phases[k], x, e)
                x = e
            if k < n and x < hi:                        # segment k
                s, b = self.segments[k]
                e = min(hi, s + len(b))
                out[x - lo:e - lo] = b[x - s:e - s]
                x = e
            k += 1
        return out

    def gap_at(self, lo, hi):
        """Ether phase constant if [lo, hi) lies inside one gap, else None."""
        k = self._first_piece(lo)
        if k < len(self.segments) and hi > self.starts[k]:
            return None
        return self.phases[k]


def _ether_cells(c, lo, hi):
    tile = np.array([int(ch) for ch in ETHER], dtype=np.uint8)
    return tile[(c + np.arange(lo, hi)) % TILE]


def _phase_const(bits, x):
    """Ether phase constant c of cells starting at global column x."""
    r = ether_rotation(bits[:TILE])
    if r is None:
        raise ValueError(f"not ether at column {x}")
    return (r - x) % TILE


def layout(tape, appendants, left_periods, right_periods, v_override=None):
    """Sparse version of assemble(): same t=0 row, as a Layout.

    The central and right sides are one materialized segment (trimmed to a
    clean ether cut, as padded_row does); each ossifier (the OSSIFIER
    blocks, B to B) is a segment; the v A blocks between ossifiers are
    an ether gap whose placement is computed in closed form and checked
    for ether at both ends."""
    from encoder import OSSIFIER, Placed, _attach, _left_v, load_blocks
    bits, placed = assemble(tape, appendants, 0, right_periods)
    x_c = placed[0].gspan(0)[0]
    bits = trim_right_to_ether(bits)
    segs = [(x_c, bits)]
    phases = [_phase_const(bits[-TILE:], x_c + len(bits) - TILE)]
    blocks, _ = load_blocks()
    a_blk = blocks["A"]
    v = v_override if v_override is not None else _left_v(appendants)
    run_step = {}             # row phase -> (ddy, ddx) of A attached to A
    for p in range(3):
        q = _attach(Placed(a_blk, p, 0), a_blk, "L")
        run_step[p] = (q.dy - p, q.dx)
    prev = placed[0]
    gap_hi = None             # right end of the gap being closed
    for _ in range(left_periods):
        group = []
        for name in OSSIFIER:
            prev = _attach(prev, blocks[name], "L")
            group.append(prev)
        x0, x1 = group[-1].gspan(0)[0], group[0].gspan(0)[1]
        if gap_hi is not None and x1 != gap_hi:
            raise AssertionError("ossifier does not meet the A run")
        chunk = "".join(p.gbits(0) for p in reversed(group))
        if len(chunk) != x1 - x0:
            raise AssertionError("non-contiguous ossifier row")
        segs.append((x0, np.frombuffer(chunk.encode(), np.uint8) - ord("0")))
        first = _attach(prev, a_blk, "L")
        ddy, ddx = run_step[first.dy % 3]
        last = Placed(a_blk, first.dy + (v - 1) * ddy, first.dx + (v - 1) * ddx)
        f0, f1 = first.gspan(0)
        l0, l1 = last.gspan(0)
        if f1 != x0 or f1 - f0 != A_ROW_CELLS or l1 - l0 != A_ROW_CELLS:
            raise AssertionError("A block row is not 28 cells")
        if f1 - l0 != A_ROW_CELLS * v:
            raise AssertionError("A run is not 28 cells per block")
        c = _phase_const(np.frombuffer(first.gbits(0).encode(), np.uint8) - ord("0"), f0)
        if _phase_const(np.frombuffer(last.gbits(0).encode(), np.uint8) - ord("0"), l0) != c:
            raise AssertionError("A run changes the ether phase")
        phases.append(c)
        prev, gap_hi = last, l0
    # collected right to left: [right, ossifier 0, 1, ...] with phases
    # [right ether, gap left of ossifier 0, 1, ...]; the gap between
    # ossifier 0 and block C is empty
    segs.reverse()
    if left_periods == 0:
        left = [_phase_const(bits[:TILE], x_c)]
    else:
        left = phases[1:][::-1] + [None]
    return Layout(segs, left + [phases[0]])


class Run:
    """A packed simulation with windowed read-out."""

    def __init__(self, row, origin):
        self.width = len(row)
        self.words = pack(row)
        self.origin = origin
        self.t = 0

    def step(self, n=1):
        for _ in range(n):
            self.words = step_packed(self.words)
        self.t += n

    def window(self, lo, hi):
        """Cells [lo, hi) of the current row (array coordinates)."""
        wlo, whi = lo // 64, -(-hi // 64)
        cells = unpack(self.words[wlo:whi], (whi - wlo) * 64)
        return cells[lo - wlo * 64:hi - wlo * 64]

    def history(self, lo, hi, depth):
        """Advance `depth` steps, recording the window [lo, hi) each step.
        Returns a (depth + 1, hi - lo) array ending at the new current time
        (the input format of census.census)."""
        rows = [self.window(lo, hi)]
        for _ in range(depth):
            self.step()
            rows.append(self.window(lo, hi))
        return np.array(rows)

    def ebar_frame(self, t=None):
        """Array position of global column 0 carried along at Ebar speed."""
        t = self.t if t is None else t
        return self.origin + int(round(EBAR_VELOCITY * t))


def defect_map(cells):
    """Cells that break the ether's spatial period (pure ether -> 0)."""
    return cells ^ np.roll(cells, TILE)


# ---------------------------------------------------------------------------
# Streaming window (v0.1.1)
#
# Far from the collisions the assembled row evolves freely: the left side
# (A and B blocks) translates by (3, 2), the central and right sides (D-L
# blocks) by (30, -8), and the jigsaw assembly already defines every row g
# of that free evolution (Placed.gbits). So only the region where the true
# state differs from the free one needs stepping. StreamRun steps a window
# around that region and re-seats it every RESEAT steps:
#
# - The packed engine is cyclic, so garbage from the window's wrap seam
#   enters from both edges at most one cell per step: after s steps the
#   cells [lo + s, hi - s) are exact.
# - Real activity also spreads at most one cell per step, so cells outside
#   [a - s, b + s], where [a, b] was the active extent (true != free) at
#   the last re-seat, still equal the free evolution.
# - A re-seat checks that a CHECK-cell zone just inside the exact region at
#   each edge equals the free evolution (raises otherwise), finds the new
#   active extent, and rebuilds the window as that extent plus MARGIN on
#   each side, taking cells outside the old exact region from the free
#   evolution. MARGIN >= 2 * RESEAT + CHECK keeps both effects apart.

class _FreeRows:
    """Free evolution of a contiguous run of Placed blocks that share one
    (period, drift): row g is row g mod p shifted by drift * (g div p)."""

    def __init__(self, placed, period, drift):
        self.placed, self.p, self.d = placed, period, drift
        self._rows = {}

    def row(self, g):
        """-> (global column of the first cell, uint8 array) for row g."""
        r = g % self.p
        if r not in self._rows:
            for a, b in zip(self.placed, self.placed[1:]):
                if a.gspan(r)[1] != b.gspan(r)[0]:
                    raise AssertionError(f"non-contiguous free row {r}")
            bits = "".join(pl.gbits(r) for pl in self.placed)
            self._rows[r] = (self.placed[0].gspan(r)[0],
                             np.frombuffer(bits.encode(), np.uint8) - ord("0"))
        start, arr = self._rows[r]
        return start + self.d * ((g - r) // self.p), arr


UNDEFINED = 2   # marks cells with no free-evolution value (the C block's
                # columns once C's patch rows run out, or beyond the row)


class StreamRun:
    """Exact Rule 110 run of an assembled row, stepping only the active
    window (see the comment above). Same read-out API as Run, with
    origin = 0: positions are the encoder's global columns."""

    RESEAT = 256
    CHECK = 64
    MARGIN = 2 * RESEAT + CHECK + 64

    def __init__(self, tape, appendants, left_periods, right_periods,
                 v_override=None, left_gaps=None):
        self._args = (tape, appendants, left_periods, right_periods,
                      v_override, left_gaps)
        bits, placed = assemble(tape, appendants, left_periods, right_periods,
                                v_override=v_override, left_gaps=left_gaps)
        ic = next(i for i, p in enumerate(placed) if p.block.name == "C")
        self.free = [_FreeRows(placed[:ic], 3, 2),
                     _FreeRows(placed[ic + 1:], 30, -8)]
        self.origin = 0
        self.t = 0
        self.since = 0            # steps since the last re-seat
        c_lo, c_hi = placed[ic].gspan(0)
        x0 = placed[0].gspan(0)[0]
        lo = c_lo - self.MARGIN
        hi = c_hi + self.MARGIN
        self.split = (lo + hi) // 2
        self._set_window(lo, np.asarray(bits[lo - x0:hi - x0], dtype=np.uint8))

    # Pickling keeps only the constructor arguments and the live window;
    # the (possibly huge) assembly is rebuilt on load.
    _STATE = ("t", "since", "lo", "width", "words", "split")

    def __getstate__(self):
        return {"args": self._args, **{k: getattr(self, k) for k in self._STATE}}

    def __setstate__(self, d):
        self.__init__(*d["args"][:4], v_override=d["args"][4],
                      left_gaps=d["args"][5])
        for k in self._STATE:
            setattr(self, k, d[k])

    def _set_window(self, lo, cells):
        self.split = lo + len(cells) // 2
        w = -(-len(cells) // 64) * 64
        if w > len(cells):
            cells = np.concatenate([cells, self.free_cells(self.t, lo + len(cells), lo + w)])
        self.lo, self.width = lo, w
        self.words = pack(cells)

    def free_cells(self, g, lo, hi, strict=True):
        """Free-evolution cells [lo, hi) at row g. strict: raise where
        undefined; else mark those cells UNDEFINED.

        The two free rows overlap after a while (the left side moves right,
        the right side left), and only one of them can be true at a given
        place: the left side's to the left of the active region, the right
        side's to its right. So left of self.split (the window centre,
        always inside the active region) the left row takes precedence, and
        right of it the right row. (Before v0.1.1's fix the right row simply
        overwrote the left one, which let the window grow without bound.)
        There is no fallback from one side's row to the other: beyond the
        right side's end, for example, the left side's row (an A-train) is
        not the truth, so such cells stay UNDEFINED and fail loudly."""
        out = np.full(hi - lo, UNDEFINED, dtype=np.uint8)
        left, right = self.free
        for fr, a0, b0 in ((left, lo, self.split), (right, self.split, hi)):
            a0, b0 = max(lo, a0), min(hi, b0)
            if a0 >= b0:
                continue
            start, arr = fr.row(g)
            a, b = max(a0, start), min(b0, start + len(arr))
            if a < b:
                out[a - lo:b - lo] = arr[a - start:b - start]
        if strict and (out == UNDEFINED).any():
            raise ValueError(f"no free evolution for part of [{lo}, {hi}) "
                             f"at t={g}: the run left the assembled row")
        return out

    def step(self, n=1):
        while n:
            k = min(n, self.RESEAT - self.since)
            self.words = step_packed_n(self.words, k)
            self.t += k
            self.since += k
            n -= k
            if self.since == self.RESEAT:
                self._reseat()

    def _reseat(self):
        k, c = self.since, self.CHECK
        cells = unpack(self.words, self.width)
        ref = self.free_cells(self.t, self.lo, self.lo + self.width, strict=False)
        for z0, z1 in ((k, k + c), (self.width - k - c, self.width - k)):
            if not np.array_equal(cells[z0:z1], ref[z0:z1]):
                raise RuntimeError(f"t={self.t}: activity reached the edge of "
                                   f"the streaming window (MARGIN too small)")
        diff = np.nonzero(cells[k:self.width - k] != ref[k:self.width - k])[0]
        if len(diff) == 0:
            raise RuntimeError(f"t={self.t}: no active region left")
        a = self.lo + k + diff[0]
        b = self.lo + k + diff[-1] + 1
        lo, hi = a - self.MARGIN, b + self.MARGIN
        new = self.free_cells(self.t, lo, hi)
        e0, e1 = max(lo, self.lo + k), min(hi, self.lo + self.width - k)
        new[e0 - lo:e1 - lo] = cells[e0 - self.lo:e1 - self.lo]
        self.since = 0
        self._set_window(lo, new)

    def window(self, lo, hi):
        """Cells [lo, hi) of the current row: simulated where exact, free
        evolution elsewhere (exact there too, see above)."""
        out = self.free_cells(self.t, lo, hi, strict=False)
        e0 = max(lo, self.lo + self.since)
        e1 = min(hi, self.lo + self.width - self.since)
        if e0 < e1:
            # unpack only the words covering [e0, e1)
            w0, w1 = (e0 - self.lo) // 64, -(-(e1 - self.lo) // 64)
            cells = unpack(self.words[w0:w1], (w1 - w0) * 64)
            out[e0 - lo:e1 - lo] = cells[e0 - self.lo - 64 * w0:e1 - self.lo - 64 * w0]
        if (out == UNDEFINED).any():
            raise ValueError(f"window [{lo}, {hi}) at t={self.t} not covered")
        return out

    def history(self, lo, hi, depth):
        rows = [self.window(lo, hi)]
        for _ in range(depth):
            self.step()
            rows.append(self.window(lo, hi))
        return np.array(rows)

    def ebar_frame(self, t=None):
        t = self.t if t is None else t
        return self.origin + int(round(EBAR_VELOCITY * t))
