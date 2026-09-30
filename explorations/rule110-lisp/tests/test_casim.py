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
        lo, hi = origin - 20_000, origin + 20_000
        assert np.array_equal(full.window(lo, hi), h.window(lo, hi)), target
