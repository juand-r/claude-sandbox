"""Layer 1 tests: block data integrity and the CTS -> Rule 110 encoder.

Ground truth throughout is Rule 110 dynamics itself: the glued blocks are
claimed pieces of a single valid spacetime diagram, so we verify (a) each
patch is internally a valid evolution, (b) every seam in a real assembly is
locally rule-valid, and (c) the actual CA run from the assembled t=0 row
reproduces every defined patch cell.
"""

import numpy as np

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from encoder import PERIODS, Placed, _right_block_seq, assemble, load_blocks
from engine import history, step

TAPE, APPS = "NNYN", ["YN", "NYYN", "", ""]


def test_right_block_seq_paper_example():
    # worked example from the paper
    assert _right_block_seq(["YN", "NYYN", "", ""]) == "HIIJKHJIIIIIJLLK"


def test_block_periodicity():
    blocks, _ = load_blocks()
    for name, blk in blocks.items():
        if name == "C":
            continue
        p, d = PERIODS[name]
        for r in range(35, 60):
            s1, e1 = blk.span(r)
            s2, e2 = blk.span(r + p)
            assert (s2, e2) == (s1 + d, e1 + d)
            assert blk.bits(r) == blk.bits(r + p)


def test_patch_rows_step_downward():
    # patch row r must evolve to patch row r+1 (time increases with row)
    blocks, _ = load_blocks()
    for name, blk in blocks.items():
        for r in (40, 50):
            s, e = blk.span(r)
            tape = np.zeros(e - s + 20, dtype=np.uint8)
            tape[10:10 + e - s] = np.frombuffer(
                blk.bits(r).encode(), dtype=np.uint8) - ord("0")
            nxt = step(tape)
            s2, e2 = blk.span(r + 1)
            row2 = np.frombuffer(blk.bits(r + 1).encode(), dtype=np.uint8) - ord("0")
            lo, hi = max(s, s2) + 2, min(e, e2) - 2
            assert np.array_equal(nxt[10 + lo - s:10 + hi - s],
                                  row2[lo - s2:hi - s2]), (name, r)


def _seam_violations(p1, p2, glo=-25, ghi=25):
    rows = {}
    for g in range(glo, ghi + 1):
        cells = {}
        for p in (p1, p2):
            try:
                s, e = p.gspan(g)
            except IndexError:
                continue
            for c, ch in zip(range(s, e), p.gbits(g)):
                if c in cells and cells[c] != int(ch):
                    return -1  # overlap disagreement
                cells[c] = int(ch)
        rows[g] = cells
    bad = 0
    for g in range(glo, ghi):
        cur, nxt = rows[g], rows[g + 1]
        for c in nxt:
            if all(x in cur for x in (c - 1, c, c + 1)):
                trip = 4 * cur[c - 1] + 2 * cur[c] + cur[c + 1]
                if ((110 >> trip) & 1) != nxt[c]:
                    bad += 1
    return bad


def test_all_seams_rule_valid():
    _, placed = assemble(TAPE, APPS)
    seen = set()
    for a, b in zip(placed, placed[1:]):
        key = a.block.name + b.block.name
        if key in seen:
            continue
        seen.add(key)
        assert _seam_violations(a, b) == 0, f"seam {key}"
    # the assembly must exercise a good variety of seam types
    assert len(seen) >= 20


def test_evolution_matches_patches():
    bits, placed = assemble(TAPE, APPS)
    off = placed[0].gspan(0)[0]
    T = 45
    h = history(bits, T)
    W = len(bits)
    total = 0
    for p in placed:
        for g in range(1, T + 1):
            try:
                s0, e0 = p.gspan(g)
            except IndexError:
                continue
            s, e = max(s0, off + g), min(e0, off + W - g)
            if s >= e:
                continue
            expect = np.frombuffer(
                p.gbits(g)[s - s0:e - s0].encode(), dtype=np.uint8) - ord("0")
            assert np.array_equal(expect, h[g, s - off:e - off]), \
                (p.block.name, g)
            total += e - s
    assert total > 1_000_000
