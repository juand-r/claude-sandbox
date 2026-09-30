"""Tests for the collision machinery (run: pytest -q test_collider.py)."""

import numpy as np
import pytest

from r110lib import (ETHER, build_row, class_key, evolve_batch, evolve_hist,
                     in_ether_lattice, n_classes, objects, step_rows,
                     verify_glider, window_phase)
from library import Library, key_of_string
from martinez_strings import STRINGS, EXPECTED
from collide import canonical_reps, simulate, meet_time, EXTRA

LIB = Library.load()


def norm(lib, name, t, x):
    g = lib.gliders[name]
    t2 = t % g.p
    return name, t2, x - (t - t2) // g.p * g.d


def test_ether_phase_advance():
    from r110lib import ether_cells
    r = ether_cells(3, 0, 140)
    assert set(window_phase(step_rows(r)).tolist()) == {7}
    assert in_ether_lattice(7, 0) and in_ether_lattice(3, 2)
    assert in_ether_lattice(1, 10) and not in_ether_lattice(1, 0)


def test_batch_engine_matches_scalar():
    rng = np.random.default_rng(1)
    rows = rng.integers(0, 2, (70, 97)).astype(np.uint8)
    fin, _ = evolve_batch(rows, 33)
    for i in range(70):
        assert np.array_equal(evolve_hist(rows[i], 33)[-1], fin[i])


@pytest.mark.parametrize("name", list(LIB.gliders))
def test_library_gliders_periodic(name):
    verify_glider(LIB.gliders[name], periods=3)


@pytest.mark.parametrize("name", list(EXPECTED))
def test_literature_period_vectors(name):
    if name == "gun":
        pytest.skip("gun emits gliders")
    g = LIB.gliders[name]
    assert (g.p, g.d) == EXPECTED[name]


def test_build_row_clean_wrap():
    # a lone A in a cyclic row: the width is chosen so the wrap is clean,
    # hence exactly one object at all times
    g = LIB.gliders["A"]
    row, x0 = build_row([g.state_at(0, 0, 0)], pad=200)
    h = evolve_hist(row, 60)
    for t in range(61):
        rolled = np.roll(h[t], len(row) // 3)   # move the wrap into view
        assert len(objects(rolled)) == 1


@pytest.mark.parametrize("X,Y", [("A", "Ebar"), ("C2", "Ebar"), ("A", "B"),
                                 ("A", "G"), ("D1", "B"), ("C3", "F")])
def test_class_count(X, Y):
    reps = canonical_reps(LIB, X, Y)
    PX = (LIB.gliders[X].p, LIB.gliders[X].d)
    PY = (LIB.gliders[Y].p, LIB.gliders[Y].d)
    assert len(reps) == n_classes(PX, PY)


@pytest.mark.parametrize("X,Y", [("A", "Ebar"), ("C2", "Ebar"), ("D1", "B"),
                                 ("A", "G")])
def test_translation_equivariance(X, Y):
    """Moving Y by X's period vector P_X must translate every product by
    P_X; moving it by P_Y must change nothing."""
    gx, gy = LIB.gliders[X], LIB.gliders[Y]
    for rep in canonical_reps(LIB, X, Y):
        tm = meet_time(LIB, X, Y, rep)
        base = simulate(LIB, [(X, 0, 0), (Y, *rep)], tm + EXTRA)
        assert base["settled"]
        exp = sorted(norm(LIB, n, t + 2 * gx.p, x + 2 * gx.d)
                     for n, t, x in base["products"])
        r2 = (rep[0] + 2 * gx.p, rep[1] + 2 * gx.d)
        res = simulate(LIB, [(X, 0, 0), (Y, *r2)], tm + EXTRA + 100)
        assert sorted(norm(LIB, *p) for p in res["products"]) == exp
        r3 = (rep[0] - gy.p, rep[1] - gy.d)
        res = simulate(LIB, [(X, 0, 0), (Y, *r3)], tm + EXTRA)
        assert sorted(norm(LIB, *p) for p in res["products"]) == \
            sorted(norm(LIB, *p) for p in base["products"])


def test_predict_matches_simulation():
    """predict() (catalog + lattice translation) equals direct simulation
    for non-canonical relative events."""
    from predict import predict
    import random
    rnd = random.Random(3)
    for X, Y in [("C1", "F"), ("A", "Ebar"), ("C2", "G"), ("D1", "B")]:
        gx, gy = LIB.gliders[X], LIB.gliders[Y]
        for rep in canonical_reps(LIB, X, Y):
            a, b = rnd.randint(0, 6), rnd.randint(-3, 3)
            r = (rep[0] + a * gx.p + b * gy.p, rep[1] + a * gx.d + b * gy.d)
            # keep Y to the right of X with a gap: only accept if Y starts
            # right of X at time 0
            ys = gy.state_at(*r, 0)[3]
            if ys < 40:
                continue
            k, pred = predict(X, Y, r)
            tm = meet_time(LIB, X, Y, r)
            res = simulate(LIB, [(X, 0, 0), (Y, *r)], tm + EXTRA + 300)
            assert res["settled"]
            assert sorted(norm(LIB, *p) for p in res["products"]) == pred


def test_glidersim_matches_automaton():
    """The catalog-driven glider simulator reproduces the automaton cell
    for cell on random multi-glider scenes (three-body cases are refused)."""
    from glidersim import validate
    stats = validate(15, seed=5, n_gliders=5, T=1500)
    assert stats["DISAGREE"] == 0
    assert stats["agree"] >= 5
