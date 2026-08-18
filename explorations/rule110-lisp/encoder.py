"""Layer 1: cyclic tag system -> Rule 110 initial row.

Implements the algorithm of Cook, "A Concrete View of Rule 110 Computation"
(arXiv:0906.3248), section "We finally convert it into a Rule 110 state".
The 12 bit-blocks A-L (extracted from the paper's figures into
data/blocks.json by tools/extract_blocks.py) are glued along their zig-zag
seams; the initial row is the horizontal line through the marked t=0 row of
block C.

Geometry (verified in tests): every block except C is periodic with a
drift -- patch row r+p equals row r shifted right by `drift` columns.
A and B have (p, drift) = (3, +2); D through L have (30, -8). C is a
single aperiodic patch whose row 48 carries the t=0 marker. Row order in
blocks.json is time order (increasing row = increasing time).

Block semantics (paper, "Some comments on this algorithm"):
  A ether        B ether+A^4 (ossifier part)      C initial "V"
  D glue between moving data                      E moving data N
  F moving data Y                                 G prepared leader
  H primary component    I,J standard components (II = table Y, IJ = table N)
  K raw leader           L raw short leader

Central region: tape symbol N -> ED, Y -> FD; last D -> G; C in front.
Right side (repeated): appendant Y -> II, N -> IJ; first I -> KH;
empty appendant -> L; the K of the first appendant moves to the end.
Left side (repeated): [A]^v B [A]^13 B [A]^11 B [A]^12 B, where
v = 76*(#Y) + 80*(#N) + 60*(#nonempty) + 43*(#empty) over all appendants.
"""

import json
import os

import numpy as np

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "data", "blocks.json")

PERIODS = {"A": (3, 2), "B": (3, 2), "D": (30, -8), "E": (30, -8),
           "F": (30, -8), "G": (30, -8), "H": (30, -8), "I": (30, -8),
           "J": (30, -8), "K": (30, -8), "L": (30, -8)}
_BASE_LO = {3: 48, 30: 35}  # first row of the canonical band per period


class Block:
    """One bit-block, extendable to any row via its periodicity.

    Patch coordinates: row r, col c as in the extracted figure. A placed
    instance lives at global (r + dy, c + dx). For periodic blocks any
    integer row is defined; for C only rows 0..99.
    """

    def __init__(self, name, rows, period, drift):
        self.name = name
        self.period = period
        self.drift = drift
        self._rows = rows
        self._span = [(len(r) - len(r.lstrip()), len(r.rstrip()))
                      for r in rows]

    def _resolve(self, r):
        """-> (base row index, column shift) for patch row r."""
        if self.period is None:
            if not 0 <= r < len(self._rows):
                raise IndexError(f"row {r} outside aperiodic block {self.name}")
            return r, 0
        lo = _BASE_LO[self.period]
        rb = lo + (r - lo) % self.period
        return rb, (r - rb) // self.period * self.drift

    def span(self, r):
        """Defined column span [start, end) of patch row r."""
        rb, sh = self._resolve(r)
        s, e = self._span[rb]
        return s + sh, e + sh

    def bits(self, r):
        """Defined content of patch row r as a '0'/'1' string."""
        rb, _ = self._resolve(r)
        s, e = self._span[rb]
        return self._rows[rb][s:e]


def load_blocks():
    d = json.load(open(_DATA))
    blocks = {}
    for name, rows in d["blocks"].items():
        p, s = PERIODS.get(name, (None, None))
        blocks[name] = Block(name, rows, p, s)
    return blocks, d["t0_row"]["C"]


class Placed:
    """A block instance at offset (dy, dx): patch (r, c) -> global (r+dy, c+dx)."""

    def __init__(self, block, dy, dx):
        self.block, self.dy, self.dx = block, dy, dx

    def gspan(self, g):
        s, e = self.block.span(g - self.dy)
        return s + self.dx, e + self.dx

    def gbits(self, g):
        return self.block.bits(g - self.dy)

    def rows_defined(self, lo, hi):
        """Global rows in [lo, hi) where this instance is defined."""
        if self.block.period is None:
            return range(max(lo, self.dy), min(hi, self.dy + 100))
        return range(lo, hi)


# rows around the t=0 line used to verify seam fits
_CHECK = 40


def _attach(prev, block, side):
    """Place `block` against `prev` on the given side ('R' or 'L').

    The seam must fit exactly: on 'R', prev's right edge + 1 == block's left
    edge at every checked global row; mirrored for 'L'. Returns the unique
    Placed instance; raises if the fit is not unique.
    """
    period = block.period or 1
    solutions = []
    for dy in range(-_CHECK, -_CHECK + (100 - 2 * _CHECK if block.period is None
                                        else period)):
        cand = Placed(block, dy, 0)
        rows = [g for g in prev.rows_defined(-_CHECK, _CHECK)
                if g in cand.rows_defined(-_CHECK, _CHECK)]
        if len(rows) < 2 * period:
            continue
        g0 = rows[0]
        if side == "R":
            dx = prev.gspan(g0)[1] - cand.gspan(g0)[0]
        else:
            dx = prev.gspan(g0)[0] - cand.gspan(g0)[1]
        cand.dx = dx
        if side == "R":
            ok = all(prev.gspan(g)[1] == cand.gspan(g)[0] for g in rows)
        else:
            ok = all(cand.gspan(g)[1] == prev.gspan(g)[0] for g in rows)
        if ok:
            solutions.append(cand)
    if len(solutions) != 1:
        raise ValueError(
            f"seam {prev.block.name}-{block.name} ({side}): "
            f"{len(solutions)} fits, expected 1")
    return solutions[0]


def _right_block_seq(appendants):
    """Appendant list -> block-name string for one period of the right side."""
    seqs = []
    for app in appendants:
        if not app:
            seqs.append("L")
            continue
        s = "".join("II" if c == "Y" else "IJ" for c in app)
        seqs.append("KH" + s[1:])
    joined = "".join(seqs)
    if not joined.startswith("KH"):
        raise ValueError("first appendant must be nonempty (no prepared "
                         "short leader block available)")
    return joined[1:] + "K"  # move the initial K to the very end


def _left_v(appendants):
    """Paper's ossifier-spacing estimate. Valid only if at least one
    nonempty appendant is appended per appendant cycle; programs with
    longer rejection runs need a larger v (pass v_override to assemble)."""
    ys = sum(a.count("Y") for a in appendants)
    ns = sum(a.count("N") for a in appendants)
    nonempty = sum(1 for a in appendants if a)
    empty = len(appendants) - nonempty
    return 76 * ys + 80 * ns + 60 * nonempty + 43 * empty


def _left_block_seq(appendants, v_override=None):
    """One period of the left side, listed right-to-left starting from C."""
    v = v_override if v_override is not None else _left_v(appendants)
    return "B" + "A" * 12 + "B" + "A" * 11 + "B" + "A" * 13 + "B" + "A" * v


def assemble(tape, appendants, left_periods=1, right_periods=1,
             v_override=None):
    """Build the Rule 110 initial row for a cyclic tag system.

    tape: string of 'Y'/'N' (the CTS initial tape, must be nonempty).
    appendants: list of 'Y'/'N' strings (empty string = empty appendant).
    left_periods / right_periods: how many copies of the periodic side
    sequences to lay down (bounds the simulatable time).

    Returns (bits, placed): bits is a numpy uint8 row (the t=0 line through
    all placed blocks), placed is the list of Placed instances left-to-right
    for inspection and testing.
    """
    if not tape or any(c not in "YN" for c in tape):
        raise ValueError(f"bad tape {tape!r}")
    for a in appendants:
        if any(c not in "YN" for c in a):
            raise ValueError(f"bad appendant {a!r}")

    blocks, t0 = load_blocks()

    # central region: N -> ED, Y -> FD, last D -> G, C in front
    central = "".join("FD" if c == "Y" else "ED" for c in tape)
    central = "C" + central[:-1] + "G"

    c = Placed(blocks["C"], -t0, 0)  # global row 0 is the t=0 line
    placed = [c]
    for name in central[1:]:
        placed.append(_attach(placed[-1], blocks[name], "R"))
    right_seq = _right_block_seq(appendants)
    for _ in range(right_periods):
        for name in right_seq:
            placed.append(_attach(placed[-1], blocks[name], "R"))

    left = [c]
    left_seq = _left_block_seq(appendants, v_override)
    for _ in range(left_periods):
        for name in left_seq:
            left.append(_attach(left[-1], blocks[name], "L"))
    placed = left[:0:-1] + placed

    bits = "".join(p.gbits(0) for p in placed)
    # seam sanity: contributions must be contiguous
    for a, b in zip(placed, placed[1:]):
        if a.gspan(0)[1] != b.gspan(0)[0]:
            raise AssertionError("non-contiguous t=0 row")
    return np.array([int(ch) for ch in bits], dtype=np.uint8), placed
