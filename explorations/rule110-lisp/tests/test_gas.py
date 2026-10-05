"""The event engine (gas.py) against the plain engines."""

import numpy as np

import gas
from engine import ETHER, step as engine_step

_E = np.array([int(c) for c in ETHER], dtype=np.uint8)


def _render(pieces, lo, hi):
    """Cells [lo, hi) of patches [(key, left edge)] (left to right) in ether."""
    a = min(lo, pieces[0][1])
    b = max(hi, pieces[-1][1] + pieces[-1][0][1])
    return _render_all(pieces, a, b)[lo - a:hi - a]


def _render_all(pieces, lo, hi):
    ys = np.arange(lo, hi)
    out = np.empty(hi - lo, dtype=np.uint8)
    x = lo
    for (bits, w, pl, _), xp in pieces:
        out[x - lo:xp - lo] = _E[(pl + ys[x - lo:xp - lo] - xp) % 14]
        out[xp - lo:xp - lo + w] = gas.cells_of(bits, w)
        x = xp + w
    (_, w, _, pr), xp = pieces[-1]
    out[x - lo:] = _E[(pr + ys[x - lo:] - xp - w) % 14]
    return out


def _random_row(rng):
    """Ether of random phases with random blobs between."""
    c = rng.integers(14)
    row = list(_E[(c + np.arange(30)) % 14])
    for _ in range(rng.integers(1, 4)):
        row += list(rng.integers(2, size=rng.integers(0, 12)))
        c, n = rng.integers(14), len(row)
        row += list(_E[(c + np.arange(n, n + rng.integers(5, 40))) % 14])
    row += list(_E[(c + np.arange(len(row), len(row) + 30)) % 14])
    return np.array(row, dtype=np.uint8), int(row_phase(row[:14], 0)), c


def row_phase(chunk, x):
    s = "".join(map(str, chunk))
    for r in range(14):
        if ETHER[r:] + ETHER[:r] == s:
            return (r - x) % 14
    raise ValueError("not ether")


def test_patch_step_matches_engine():
    rng = np.random.default_rng(1)
    for _ in range(100):
        row, cl, cr = _random_row(rng)
        n = len(row)
        width = 14 * 60
        full = np.concatenate([row, _E[(cr + np.arange(n, width)) % 14]])
        key, x = gas.key_of_cells(row, cl % 14, (cr + n) % 14)
        for _ in range(60):
            full = engine_step(full)
            b, w, pl, pr, dx = gas.step(*key)
            key, x = (b, w, pl, pr), x + dx
            # cells far from the cyclic seam
            assert np.array_equal(_render([(key, x)], 100, width - 200),
                                  full[100:width - 200])


def test_split_reproduces_cells():
    rng = np.random.default_rng(5)
    for _ in range(1000):
        row, cl, cr = _random_row(rng)
        key, _ = gas.key_of_cells(row, cl % 14, (cr + len(row)) % 14)
        for _ in range(rng.integers(0, 20)):
            key = gas.step(*key)[:4]
        pieces = gas.split(key)
        if not pieces:
            assert gas._empty(key)
            continue
        assert np.array_equal(_render([(key, 0)], -60, key[1] + 60),
                              _render(pieces, -60, key[1] + 60))


def test_gas_matches_hashlife_on_collatz_layout():
    from casim import layout
    from cts import fill_empty_appendants
    from experiments import DEMOL_APPS, DEMOL_TAPE
    from hashlife import HashRun
    lay = layout(DEMOL_TAPE, fill_empty_appendants(DEMOL_APPS), 20, 3,
                 v_override=12216)
    g = gas.Gas.from_layout(lay)
    h = HashRun.from_layout(lay)
    lo, hi = lay.lo - 20_000, lay.hi + 20_000
    for T in (0, 1_000, 30_000, 300_000, 3_000_000):
        g.advance_to(T)
        h.step(T - h.t)
        assert np.array_equal(g.window(lo, hi), h.window(lo, hi)), T
    assert g.n_events > 10_000
