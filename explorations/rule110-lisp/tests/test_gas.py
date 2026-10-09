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
    for ((_, w0, _, pr0), x0), ((_, _, pl1, _), x1) in zip(pieces, pieces[1:]):
        # adjacent pieces agree on the ether between them
        assert (pr0 + x1 - x0 - w0) % 14 == pl1
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
    assert g.n_events > 1_000


def test_c_engine_matches_python_engine_and_hashlife():
    from casim import layout
    from cts import fill_empty_appendants
    from experiments import DEMOL_APPS, DEMOL_TAPE
    from gasc import CGas
    from hashlife import HashRun
    lay = layout(DEMOL_TAPE, fill_empty_appendants(DEMOL_APPS), 20, 3,
                 v_override=12216)
    c, g, h = CGas.from_layout(lay), gas.Gas.from_layout(lay), HashRun.from_layout(lay)
    lo, hi = lay.lo - 20_000, lay.hi + 20_000
    for T in (0, 1_000, 30_000, 300_000, 3_000_000):
        c.advance_to(T)
        g.advance_to(T)
        h.step(T - h.t)
        w = c.window(lo, hi)
        assert np.array_equal(w, h.window(lo, hi)), T
        assert np.array_equal(w, g.window(lo, hi)), T
    assert c.n_events == g.n_events


def test_gas_reads_collatz_first_reads():
    """Lazy sides and the read check: the first 30 Collatz reads, with
    their cluster counts, as in data/collatz_v12216.log."""
    from cts import fill_empty_appendants
    from experiments import DEMOL_APPS, DEMOL_TAPE
    from gasrun import GasReads
    gr = GasReads(DEMOL_TAPE, fill_empty_appendants(DEMOL_APPS), 12216, 30,
                  sample_bits=14, log=lambda *a: None)
    got = gr.run_reads()
    assert got == "YNNNNNYNNNNNYNNNNNNYNNNNNNYNNN"
    counts = gr.watch.n_ebar[:30]
    assert counts[:7] == [48, 0, 0, 0, 0, 0, 48] and counts[26] == 72


def test_periodic_table_chunks_tile_the_table_and_repeat():
    """Table chunks cut on the periodic grid cover the layout exactly, and
    the chunks of one super-period recur in the next (same keys)."""
    from casim import TILE, layout
    from cts import fill_empty_appendants
    from experiments import DEMOL_APPS, DEMOL_TAPE
    from gasrun import Table, clean_cut, table_period
    lay = layout(DEMOL_TAPE, fill_empty_appendants(DEMOL_APPS), 2, 12, v_override=12216)
    period = table_period(lay, 2)
    assert period is not None
    x0 = lay.segments[2][0]
    cut, c = clean_cut(lay, x0 + 1000)
    tab = Table(lay, cut, c, period)
    rows = []
    while True:
        r = tab.src()
        if r is None:
            break
        rows.append(r)
    assert rows[-1][0].size and rows[-1][1] + len(rows[-1][0]) == lay.hi
    for (cells, x, cl, cr), nxt in zip(rows, rows[1:]):
        assert nxt[1] == x + len(cells) and nxt[2] == cr       # contiguous
        assert np.array_equal(cells, lay.cells(x, x + len(cells)))
    keys = [gas.key_of_cells(cells, (cl + x) % TILE, (cr + x + len(cells)) % TILE)[0]
            for cells, x, cl, cr in rows]
    per = len(tab.cuts)
    assert per >= 1 and len(keys) > 3 * per
    assert keys[per:2 * per] == keys[2 * per:3 * per]


def test_gas_checkpoint_resume_matches_uninterrupted_run(tmp_path):
    import pytest
    from cts import fill_empty_appendants
    from experiments import DEMOL_APPS, DEMOL_TAPE
    from gasrun import GasReads
    apps = fill_empty_appendants(DEMOL_APPS)

    class Stop(Exception):
        pass

    def stop_at_100(msg):
        # the checkpoint for read 100 is written just before this line
        if msg.startswith("[gas] read 100:"):
            raise Stop

    def make(ckpt=None, log=lambda *a: None):
        return GasReads(DEMOL_TAPE, apps, 12216, 160, sample_bits=14, log=log,
                        checkpoint=ckpt, ckpt_every=100)

    full = make()
    full.run_reads()
    full_events = full.run.n_events            # the C state is global
    ck = str(tmp_path / "gas.ckpt")
    with pytest.raises(Stop):
        make(ck, stop_at_100).run_reads()
    resumed = make(ck)
    resumed.run_reads()
    assert resumed.watch.outcome() == full.watch.outcome()
    assert resumed.watch.n_ebar == full.watch.n_ebar
    assert resumed.watch.read_at == full.watch.read_at
    assert resumed.run.n_events == full_events


def test_random_patches_both_engines_match_hashlife():
    """Arbitrary collisions, not just Cook's: random patches in ether
    make debris, unknown gliders, slips and stationary groups."""
    from census import ether_phase
    from gasc import CGas
    from hashlife import HashRun
    rng = np.random.default_rng(3)
    reg = gas.Registry()
    for _ in range(8):
        n = 14 * 300
        c = int(rng.integers(14))
        row = _E[(c + np.arange(n)) % 14].copy()
        x = 300
        while x < n - 400:
            w = int(rng.integers(1, 25))
            row[x:x + w] = rng.integers(0, 2, w)
            x += w + int(rng.integers(40, 400))
        cr = (int(ether_phase(row[-14:])[0]) - (n - 14)) % 14
        T = int(rng.integers(300, 1500))
        py, cg, h = gas.Gas(reg=reg), CGas(reg=reg), HashRun(row, 0)
        for g in (py, cg):
            g.append_row(row, 0, c, cr)
            g.start()
            g.advance_to(T)
        h.step(T)
        lo, hi = -T - 50, n + T + 50
        w = cg.window(lo, hi)
        assert np.array_equal(w, h.window(lo, hi))
        assert np.array_equal(w, py.window(lo, hi))
        assert cg.n_events == py.n_events
    assert len(reg.orbits) > 30


def test_particle_census_equals_cell_census():
    """census="both" computes the read check's census from the particles
    and by rendering the span, and raises at the first difference inside
    a watched region; the reads must equal the reference too."""
    from cts import fill_empty_appendants
    from experiments import DEMOL_APPS, DEMOL_TAPE
    from gasrun import GasReads
    gr = GasReads(DEMOL_TAPE, fill_empty_appendants(DEMOL_APPS), 12216, 120,
                  sample_bits=14, log=lambda *a: None, census="both")
    got = gr.run_reads()
    assert got[:30] == "YNNNNNYNNNNNYNNNNNNYNNNNNNYNNN"
    assert "." not in got and "!" not in got
    assert gr.pc.stats["memo"] > 10 * gr.pc.stats["rendered"]


def test_stop_on_fail():
    """Below half of Cook's v De Mol's program breaks (REPORT 3.6): the run
    stops at the first read that settles as '!'."""
    from cts import fill_empty_appendants
    from experiments import DEMOL_APPS, DEMOL_TAPE
    from gasrun import GasReads
    gr = GasReads(DEMOL_TAPE, fill_empty_appendants(DEMOL_APPS), 4000, 556,
                  sample_bits=13, log=lambda *a: None)
    out = gr.run_reads()
    assert gr.failed is not None and out[gr.failed] == "!"
    assert "!" not in out[:gr.failed]
    assert set(out[gr.failed + 1:]) <= {".", "Y", "N", "!"} and out.count(".") > 300


def test_rope_equals_plain():
    """The debris rope (gasc: ossifiers swept through absorbed debris by
    memoized crossings), with and without stretch jumps, gives the plain
    engine's reads, census counts and final gas, item for item, on a
    compiled Lisp program."""
    import gasc
    from gasrun import GasReads
    from lisp_bus import LispBus
    lb = LispBus("(car (quote (a b)))")
    comp = lb.compile_bus()
    tape = comp.pm.encode(comp.initial_tape(lb.values))
    apps = comp.pm.appendants()
    got = {}
    for mode in ("plain", "slow", "jumps"):
        er = GasReads(tape, apps, 99303, 600, log=lambda *a: None,
                      rope=(mode != "plain"), rope_jumps=(mode == "jumps"))
        out = er.run_reads()
        g = er.run
        kind, ids, ph, left, _, _, _ = g.list_items(-gasc.FAR, gasc.FAR)
        items = [(int(k), int(i), int(p), int(x)) for k, i, p, x in zip(kind, ids, ph, left)
                 if k in (gasc.PART, gasc.COMP)]
        got[mode] = (out, list(er.watch.n_ebar), g.t, items)
        if mode == "slow":
            info = g.rope_info()
            assert info["crossings"] > 10_000 and info["units"] > 100 and info["jumps"] == 0, info
        if mode == "jumps":
            # each unit crossed one by one about once, the rest by jumps
            info = g.rope_info()
            assert info["jumps"] > 100 and info["jumped"] > 10_000, info
            assert info["crossings"] < 2 * info["units"], info
    o1, n1, t1, i1 = got["plain"]
    for mode in ("slow", "jumps"):
        o2, n2, t2, i2 = got[mode]
        assert o1 == o2 and n1 == n2 and t1 == t2, mode
        assert i2 == [x for x in i1 if x[3] >= i2[0][3]], mode


def test_readwatch_pending_cursor():
    """ReadWatch.pending skips the settled prefix; it must equal the plain
    definition (first `lookahead` regions in state '.' or 'r') while states
    move forward ('.' -> 'r' -> Y/N/!) in any order."""
    import random
    from experiments import ReadWatch
    rng = random.Random(1)
    regs = [(None, None) if rng.random() < 0.1 else (i, i + 1) for i in range(300)]
    w = ReadWatch(regs, apps=None, lookahead=4)
    nxt = {".": "r", "r": "YN!"}
    for _ in range(2000):
        live = [j for j, s in enumerate(w.state) if s in ".r"]
        assert w.pending() == live[:w.lookahead]
        if not live:
            break
        j = rng.choice(live[:8])
        w.state[j] = rng.choice(nxt[w.state[j]])


def test_census_missing_keys_beyond_table():
    """A key index past the end of the census's single-particle table is
    missing even when the table's last entry is filled (this broke the
    resume of a long plain run: a key new since the checkpoint was never
    rendered)."""
    import numpy as np
    from gascensus import ParticleCensus
    pc = ParticleCensus.__new__(ParticleCensus)
    pc._k_start = np.array([0, -1, 5], np.int64)
    kid = np.array([0, 1, 2, 3, 7])
    assert pc._missing(kid).tolist() == [False, True, False, True, True]


def _demol_reads(v, n, census, **kw):
    from cts import fill_empty_appendants
    from experiments import DEMOL_APPS, DEMOL_TAPE
    from gasrun import GasReads
    gr = GasReads(DEMOL_TAPE, fill_empty_appendants(DEMOL_APPS), v, n, sample_bits=14,
                  log=lambda *a: None, census=census, **kw)
    return gr, gr.run_reads()


def test_light_check_equals_full_check():
    """census="light" (particles, no rendering) gives the full check's
    read outcomes and Ebar counts, on De Mol's program and on a compiled
    Lisp program with the rope; its spot checks ran and agreed."""
    full, out_f = _demol_reads(12216, 120, "particles")
    light, out_l = _demol_reads(12216, 120, "light", spot_every=8)
    assert out_l == out_f and "." not in out_l and "!" not in out_l
    assert light.watch.n_ebar == full.watch.n_ebar
    assert light.spot_stats["checked"] >= 14 and light.spot_stats["count_differs"] == 0
    from gasrun import GasReads
    from lisp_bus import LispBus
    lb = LispBus("(car (quote (a b)))")
    comp = lb.compile_bus()
    tape, apps = comp.pm.encode(comp.initial_tape(lb.values)), comp.pm.appendants()
    got = {}
    for census in ("particles", "light"):
        gr = GasReads(tape, apps, 99303, 600, log=lambda *a: None, rope=True,
                      census=census, spot_every=16)
        got[census] = (gr.run_reads(), gr.watch.n_ebar)
    assert got["light"] == got["particles"] and "Y" in got["light"][0]


def test_light_check_stops_on_fail():
    """The light check stops a failing construction at the same read as
    the full check (De Mol below half of Cook's v, as test_stop_on_fail)."""
    full, out_f = _demol_reads(4000, 556, "particles")
    light, out_l = _demol_reads(4000, 556, "light")
    assert full.failed is not None and light.failed == full.failed
    assert out_l[:light.failed + 1] == out_f[:full.failed + 1]


def test_spot_check_catches_a_wrong_light_census(monkeypatch):
    """Negative control: a light census that loses every other Ebar makes
    an accepted read come out wrong; the spot check must raise."""
    import pytest
    import gascensus
    rel = gascensus.LightCensus.rel

    def lossy(self, watch, pending, depth):
        T, out = rel(self, watch, pending, depth)
        es = [e for e in out if e[1] == "E"]
        drop = set(es[1::2])
        return T, [e for e in out if e not in drop]
    monkeypatch.setattr(gascensus.LightCensus, "rel", lossy)
    with pytest.raises(AssertionError, match="spot check"):
        _demol_reads(12216, 40, "light", spot_every=1, stop_on_fail=False)
