"""Glider census (census.py) on patterns with known content."""

import numpy as np

from casim import Run, padded_row
from census import MAX_DT, census, clusters
from encoder import assemble
from engine import ether_tape, history


def test_pure_ether_has_no_defects():
    H = history(ether_tape(14 * 40), MAX_DT)
    assert clusters(H[-1]) == []
    assert census(H) == []


def test_assembled_row_types():
    """t=45 of an assembly: each B block holds one A^4 (one A cluster,
    sometimes a zero-width phase slip); every other defect is Ebar
    material; nothing stationary exists yet and nothing is untyped."""
    bits, placed = assemble("YYYYNN", ["YYYYNN"], 1, 1)
    T = 45                      # block C is only defined up to row 51
    H = history(bits, T)
    off = placed[0].gspan(0)[0]
    spans = [(p.block.name, *p.gspan(T)) for p in placed
             if p.block.name != "C"]
    kinds_in = {}
    for a, b, k in census(H):
        mid = off + (a + b) // 2
        name = next((n for n, s, e in spans if s <= mid < e), None)
        if name is not None:
            kinds_in.setdefault(name, []).append(k)
    assert sorted(kinds_in["B"]) == ["A"] * 4
    for name, kinds in kinds_in.items():
        if name not in "AB":
            assert set(kinds) == {"E"}, (name, kinds)


def test_first_ossification_makes_stationary_gliders():
    """The first ossifier sits right next to block C and converts the
    first moving-data character into tape data within a few thousand
    generations: C gliders appear near the initial tape position."""
    row, origin = padded_row("YYYYNN", ["YYYYNN"], left_periods=1,
                             right_periods=4, left_pad=14 * 800,
                             right_pad=14 * 800)
    run = Run(row, origin)
    run.step(4000 - MAX_DT)
    H = run.history(origin - 2000, origin + 3000, MAX_DT)
    cs = [(a + origin - 2000 - origin, k) for a, b, k in census(H)]
    cpos = [x for x, k in cs if k == "C"]
    assert 2 <= len(cpos) <= 6
    assert all(-500 < x < 1000 for x in cpos)
