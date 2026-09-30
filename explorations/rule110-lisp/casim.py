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
