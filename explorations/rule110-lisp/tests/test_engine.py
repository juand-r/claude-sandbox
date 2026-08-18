"""Layer 0 tests: rule table, differential check, ether periodicity."""

import numpy as np
import pytest

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import ETHER, ether_tape, history, parse, run, show, step


def slow_step(cells):
    """Naive pure-Python Rule 110, cyclic boundary. Reference for testing."""
    truth = {
        (1, 1, 1): 0, (1, 1, 0): 1, (1, 0, 1): 1, (1, 0, 0): 0,
        (0, 1, 1): 1, (0, 1, 0): 1, (0, 0, 1): 1, (0, 0, 0): 0,
    }
    w = len(cells)
    return np.array(
        [truth[(cells[(i - 1) % w], cells[i], cells[(i + 1) % w])]
         for i in range(w)],
        dtype=np.uint8,
    )


def test_rule_table_all_neighborhoods():
    # Width-3 cyclic tapes exercise every neighborhood; compare to truth table.
    for n in range(8):
        tape = parse(f"{n:03b}")
        assert np.array_equal(step(tape), slow_step(tape))


def test_differential_random():
    rng = np.random.default_rng(0)
    tape = rng.integers(0, 2, size=257, dtype=np.uint8)
    for _ in range(100):
        fast = step(tape)
        assert np.array_equal(fast, slow_step(tape))
        tape = fast


def test_ether_periodicity():
    # On a tape tiled with the period-14 ether cell, the background returns
    # exactly to itself after 7 steps (zero net drift mod 14), and 7 is the
    # minimal temporal period.
    tape = ether_tape(14 * 10)
    cur = tape.copy()
    periods = []
    for t in range(1, 8):
        cur = step(cur)
        if np.array_equal(cur, tape):
            periods.append(t)
    assert periods == [7], f"ether temporal periods found: {periods}"


def test_ether_width_check():
    with pytest.raises(ValueError):
        ether_tape(15)


def test_show_parse_roundtrip():
    s = "1011001"
    assert show(parse(s)) == "X.XX..X"
    assert np.array_equal(parse(show(parse(s))), parse(s))


def test_history_shape():
    h = history(ether_tape(28), 10)
    assert h.shape == (11, 28)
    assert np.array_equal(h[10], run(ether_tape(28), 10))
