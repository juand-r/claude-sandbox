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
from engine import ETHER, pack, step_packed, unpack

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
        for _ in range(n):
            self.words = step_packed(self.words)
            self.t += 1
            self.since += 1
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
