"""Tests for the load-bearing semantics of the ring system.

Run: python3 test_ring_system.py   (prints PASS/FAIL per test)
"""

import numpy as np

import ring_system as rs


def _bits(*vals):
    return np.array(vals, dtype=np.uint8)


# -- 1. elementary-CA core -------------------------------------------------

def test_rule_identity_and_constants():
    x = np.array([1, 0, 1, 1, 0, 0, 1, 0], dtype=np.uint8)
    # rule 204 = output equals center bit -> identity
    assert np.array_equal(rs.apply_rule(204, x), x)
    # rule 0 -> all zeros, rule 255 -> all ones
    assert np.array_equal(rs.apply_rule(0, x), np.zeros_like(x))
    assert np.array_equal(rs.apply_rule(255, x), np.ones_like(x))
    # rule 170 = output equals right neighbour -> left shift (circular)
    assert np.array_equal(rs.apply_rule(170, x), np.roll(x, -1))
    # rule 240 = output equals left neighbour -> right shift (circular)
    assert np.array_equal(rs.apply_rule(240, x), np.roll(x, 1))


def test_rule_30_known_step():
    # Single 1 on a length-9 circular tape, one step of rule 30.
    # neighbourhoods producing 1 for rule 30: 001,010,011,100 (idx 1,2,3,4).
    x = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0], dtype=np.uint8)
    expected = np.array([0, 0, 0, 1, 1, 1, 0, 0, 0], dtype=np.uint8)
    assert np.array_equal(rs.apply_rule(30, x), expected)


# -- 2. edges / composition ------------------------------------------------

def _row_with(rule=0, pull=0, push=0, order=0, spawn=0, death=0, mut=0):
    row = np.zeros(rs.N_BITS, dtype=np.uint8)
    def setf(span, val):
        lo, hi = span
        w = hi - lo
        row[lo:hi] = [(val >> (w - 1 - i)) & 1 for i in range(w)]
    setf(rs.RULE, rule); setf(rs.PULL, pull); setf(rs.PUSH, push)
    setf(rs.ORDER, order); setf(rs.MUT, mut)
    row[rs.SPAWN_BIT] = spawn; row[rs.DEATH_BIT] = death
    return row


def test_field_roundtrip():
    row = _row_with(rule=30, pull=200, push=99, order=123, mut=2)
    b = row[None, :]
    assert int(rs.get_field(b, rs.RULE)[0]) == 30
    assert int(rs.get_field(b, rs.PULL)[0]) == 200
    assert int(rs.get_field(b, rs.PUSH)[0]) == 99
    assert int(rs.get_field(b, rs.ORDER)[0]) == 123
    assert rs.mut_level(row) == 2


def _transform_once(rows: dict[int, np.ndarray], nmax: int) -> np.ndarray:
    """Pure transformation (no mutation/birth/death) on a hand-built universe.

    rows maps slot -> 36-bit row; returns the post-transformation bit array.
    """
    bits = np.zeros((nmax, rs.N_BITS), dtype=np.uint8)
    occ = np.zeros(nmax, dtype=bool)
    for slot, row in rows.items():
        bits[slot] = row
        occ[slot] = True
    targets, rule = rs.build_transformers(bits, occ)
    return rs.compose_apply(bits, targets, rule)


def test_pull_from_empty_is_identity():
    # ring pulls from empty slot 5 and pushes to empty slot 6 -> no edges.
    row = _row_with(rule=255, pull=5, push=6)
    out = _transform_once({0: row}, nmax=8)
    assert np.array_equal(out[0], row)


def test_push_to_empty_is_noop():
    # ring pushes to empty slot 5, pulls from empty slot 6 -> source unchanged.
    row = _row_with(rule=255, push=5, pull=6)
    out = _transform_once({0: row}, nmax=8)
    assert np.array_equal(out[0], row)
    assert np.array_equal(out[5], np.zeros(rs.N_BITS, dtype=np.uint8))


def test_push_and_pull_double_apply():
    # A.push = B and B.pull = A  =>  B' = A(A(B)). Point A's own edges at an
    # empty slot so A does not self-transform and confuse the snapshot.
    A = _row_with(rule=170, push=1, pull=7)        # slot 0, rule 170 = right nbr
    B = _row_with(rule=204, pull=0, push=7, order=5)  # slot 1, identity rule
    out = _transform_once({0: A, 1: B}, nmax=8)
    expected = rs.apply_rule(170, rs.apply_rule(170, B))
    assert np.array_equal(out[1], expected), (out[1], expected)


def test_order_composition():
    # Three pushers onto target 0 with orders 1,2,3: innermost = lowest order.
    # Each pusher points its pull at an empty slot to avoid self-edges.
    target = _row_with(rule=204, pull=7, push=7)          # slot 0
    C = _row_with(rule=170, push=0, pull=7, order=3)      # right-nbr, outermost
    B = _row_with(rule=240, push=0, pull=7, order=1)      # left-nbr, innermost
    D = _row_with(rule=204, push=0, pull=7, order=2)      # identity, middle
    out = _transform_once({0: target, 1: C, 2: B, 3: D}, nmax=8)
    # order asc: B(o1) then D(o2) then C(o3) => C(D(B(target)))
    expected = rs.apply_rule(170, rs.apply_rule(204, rs.apply_rule(240, target)))
    assert np.array_equal(out[0], expected), (out[0], expected)


# -- 3. tick cycle: latency, birth-before-death, placement -----------------

def test_death_latency_one_tick():
    # A ring whose death bit is already set dies, but only on resolution of
    # the tick (latency is about transformations setting it -- here we just
    # confirm a set death bit removes the ring).
    u = rs.Universe(nmax=4, seed=1, record_history=False)
    u.place(0, _row_with(rule=204, death=1))
    u.step()
    assert not u.occupied[0]


def test_death_set_by_transformation_is_delayed():
    # Slot 0 starts with death=0. A transformation flips its death bit this
    # tick, but because resolution reads the snapshot, it must SURVIVE this
    # tick and die next tick.
    u = rs.Universe(nmax=4, seed=1, record_history=False)
    # rule 255 makes every bit 1, including the death bit.
    u.place(0, _row_with(rule=255, pull=0))  # self-transform to all ones
    u.step()
    assert u.occupied[0], "should survive the tick its death bit gets set"
    assert u.bits[0][rs.DEATH_BIT] == 1
    u.step()
    assert not u.occupied[0], "should die the following tick"


def test_birth_before_death():
    # A ring with BOTH spawn and death set: it must produce a child, then die.
    u = rs.Universe(nmax=8, seed=3, record_history=False)
    u.place(0, _row_with(rule=204, spawn=1, death=1))
    u.step()
    assert not u.occupied[0], "parent should die"
    assert u.occupied.sum() == 1, "exactly one child should exist"


def test_birth_uses_empty_slot_only():
    u = rs.Universe(nmax=2, seed=1, record_history=False)
    # both slots occupied -> spawn cannot place a child (no empty slot)
    u.place(0, _row_with(rule=204, spawn=1))
    u.place(1, _row_with(rule=204))
    u.step()
    assert u.occupied.sum() == 2  # unchanged, no room


# -- 4. mutation statistics ------------------------------------------------

def test_ambient_mutation_rate_statistical():
    # Many independent high-mutation rings; observed per-bit flip frequency
    # should be near AMBIENT_P[3]. Use identity rule so only mutation changes
    # bits, and avoid spawn/death bits being set.
    nmax = 4000
    u = rs.Universe(nmax=nmax, seed=7, record_history=False)
    base = _row_with(rule=204, mut=3)  # high; identity transform
    for i in range(nmax):
        u.place(i, base)
    before = u.bits.copy()
    u.step()
    flips = np.sum(u.bits != before)
    expected = rs.AMBIENT_P[3] * nmax * rs.N_BITS
    # within 15% of expectation
    assert 0.85 * expected < flips < 1.15 * expected, (flips, expected)


def _run_all():
    tests = [v for k, v in globals().items()
             if k.startswith("test_") and callable(v)]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
        except Exception as e:  # noqa
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    return passed == len(tests)


if __name__ == "__main__":
    import sys
    sys.exit(0 if _run_all() else 1)
