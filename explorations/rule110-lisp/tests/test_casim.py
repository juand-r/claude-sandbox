"""The streaming window must reproduce the full cyclic run exactly."""

import numpy as np

from casim import Run, StreamRun, padded_row


def test_stream_run_matches_full_run():
    tape, apps, v, T = "YYYYNN", ["YYYYNN"], 524, 6_000
    full = Run(*padded_row(tape, apps, left_periods=3, right_periods=3,
                           left_pad=T + 5_000, right_pad=T + 5_000,
                           v_override=v))
    s = StreamRun(tape, apps, 3, 3, v_override=v)
    for target in range(500, T + 1, 500):
        full.step(target - full.t)
        s.step(target - s.t)
        # the simulated window plus 2,000 free-evolution cells each side
        lo, hi = s.lo - 2_000, s.lo + s.width + 2_000
        assert np.array_equal(full.window(full.origin + lo, full.origin + hi),
                              s.window(lo, hi)), target
    assert s.width < full.width / 10


def test_hashlife_matches_full_run():
    from hashlife import HashRun
    tape, apps, v, T = "YYYYNN", ["YYYYNN"], 524, 6_000
    row, origin = padded_row(tape, apps, left_periods=3, right_periods=3,
                             left_pad=T + 5_000, right_pad=T + 5_000,
                             v_override=v)
    full, h = Run(row, origin), HashRun(row, origin)
    for target in (1, 7, 100, 1_000, 4_096, T):
        full.step(target - full.t)
        h.step(target - h.t)
        # the cyclic run is exact only beyond its wrap seam's light cone
        lo, hi = full.t, len(row) - full.t
        assert np.array_equal(full.window(lo, hi), h.window(lo, hi)), target


def test_layout_matches_padded_row():
    """The sparse layout (ossifiers as segments, A runs as ether gaps placed
    in closed form) is the assembled row, cell for cell."""
    from casim import TILE, layout
    from cts import fill_empty_appendants
    from experiments import DEMOL_APPS, DEMOL_TAPE
    for tape, apps, lp, rp, v in ((DEMOL_TAPE, fill_empty_appendants(DEMOL_APPS), 3, 2, 12_216),
                                  ("YN", ["YNNNNN", ""], 4, 3, 7),
                                  ("YYYYNN", ["YYYYNN"], 0, 2, None)):
        row, origin = padded_row(tape, apps, lp, rp, TILE * 5, TILE * 5, v_override=v)
        lay = layout(tape, apps, lp, rp, v_override=v)
        assert np.array_equal(lay.cells(-origin, len(row) - origin), row)
        assert len(lay.segments) == lp + 1


def test_hashlife_from_layout_and_local_history():
    """HashRun built from a layout equals the full run, and its locally
    stepped history equals the full run's history."""
    from casim import layout
    from census import MAX_DT
    from hashlife import HashRun
    tape, apps, v, T = "YYYYNN", ["YYYYNN"], 524, 6_000
    row, origin = padded_row(tape, apps, left_periods=3, right_periods=3,
                             left_pad=T + 5_000, right_pad=T + 5_000,
                             v_override=v)
    full = Run(row, origin)
    h = HashRun.from_layout(layout(tape, apps, 3, 3, v_override=v))
    for target in (1, 100, 4_096, T - MAX_DT):
        full.step(target - full.t)
        h.step(target - h.t)
        lo, hi = full.t - origin, len(row) - full.t - origin
        assert np.array_equal(full.window(lo + origin, hi + origin), h.window(lo, hi))
    a, b = -3_000, 4_000
    assert np.array_equal(full.history(a + origin, b + origin, MAX_DT),
                          h.history(a, b, MAX_DT))


def test_hashlife_read_check():
    """The HashLife read check (sparse layout, jumps between reads) sees the
    reference read sequence of the small {YYYYNN} program."""
    from encoder import _left_v
    from experiments import READS_APPS, READS_TAPE, read_outcomes_hash
    v = 3 * _left_v(READS_APPS)
    assert read_outcomes_hash(READS_TAPE, READS_APPS, v, 6, 8 * 32 * v, 600) == "YYYYNN"


def test_epoch_run_is_exact():
    """After several epochs (each a rebuilt, truncated tree), the epoch
    engine's row equals the full run's row over the active region and a
    margin around it, and the read sequence is the reference."""
    from casim import layout
    from encoder import _left_v
    from epochrun import GRID, EpochReads, diff_extent
    from experiments import READS_APPS, READS_TAPE
    from hashlife import HashRun
    v = 3 * _left_v(READS_APPS)
    er = EpochReads(READS_TAPE, READS_APPS, v, 12, sample_bits=9, epoch=3,
                    log=lambda *a: None)
    assert er.run_reads() == "YYYYNNYYYYNN"
    run = er.run
    full = HashRun.from_layout(layout(READS_TAPE, READS_APPS, er.n_all,
                                      len(er.regs) // len(READS_APPS), v_override=v))
    full.step(run.t)
    left, right = er.uni.at(run.t)
    a, b = diff_extent(run, left, right, er.regs[11][0] - 8 * run.t // 30)
    lo, hi = a - 2 * GRID, b + 2 * GRID
    assert np.array_equal(run.window(lo, hi), full.window(lo, hi))


def test_periodic_right_side():
    """Beyond one super-period the layout tiles the right side with shared
    copies (encoder.right_super_period); cells and read regions equal the
    direct assembly's."""
    from casim import TILE, layout, trim_right_to_ether
    from encoder import assemble, right_super_period
    from experiments import component_regions
    tape, apps, rp = "YYYYNN", ["YYYYNN"], 40
    assert right_super_period(tape, apps)[0] == 15
    bits, placed = assemble(tape, apps, 2, rp)
    row, origin = padded_row(tape, apps, 2, rp, TILE * 5, TILE * 5)
    end = len(trim_right_to_ether(bits)) + placed[0].gspan(0)[0]
    lay = layout(tape, apps, 2, rp)
    assert len(lay.segments) > 4 and lay.hi >= end
    assert np.array_equal(lay.cells(-origin, end), row[:end + origin])
    _, placed = assemble(tape, apps, 0, rp)
    lead = [i for i, p in enumerate(placed) if p.block.name in "GKL"]
    direct = [(placed[a + 1].gspan(0)[0], placed[b - 1].gspan(0)[1])
              for a, b in zip(lead, lead[1:])]
    assert component_regions(tape, apps, rp) == direct
