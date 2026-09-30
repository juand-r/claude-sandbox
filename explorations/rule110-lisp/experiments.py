"""Long automaton runs whose results are cited in NOTES.md / REPORT.md.

    python experiments.py lblock VARIANT     # one row of the L-block table
    python experiments.py demol [T]           # De Mol 3x+1, x=3

Both print decoder reads of the moving data in flight at intervals. Read
the output with REVIEW.md B3 in mind: the decoder sees moving data only,
so these runs show liveness, not verified correctness.
"""

import sys
import time

from casim import Run, padded_row
from decoder import Decoder
from encoder import _left_v

# The L-block table (NOTES.md): the same machinery with and without empty
# appendants. v is 3x the paper's default because these programs have
# rejection runs longer than the default assumes.
LBLOCK_VARIANTS = {
    0: ("YYYYNN", ["YYYYNN"]),
    1: ("YYYYNN", ["YYYYNN", ""]),
    2: ("YYYYNN", ["YYYYNN", "", ""]),
    3: ("YN", ["YNNNNN", ""]),
    4: ("YN", ["YNNNNN", "YNNNNN"]),
}
LBLOCK_T = 250_000
LBLOCK_EVERY = 12_500

# De Mol's tag system {A->CY, C->A, Y->AAA} on tape A^3, compiled to a CTS
# by tag.ts_to_cts (alphabet A, C, Y + 3 dummies; 6-bit unary words).
DEMOL_TAPE = "YNNNNN" * 3
DEMOL_APPS = ["NYNNNNNNYNNN", "YNNNNN", "YNNNNNYNNNNNYNNNNN"] + [""] * 9
DEMOL_EVERY = 2_500


def read_moving_data(decoder, run, lo_off, hi_off):
    c = run.ebar_frame()
    try:
        return "".join(s for _, s in decoder.read(run.window(c + lo_off,
                                                               c + hi_off)))
    except ValueError:
        return "?"


def lblock(variant):
    tape, apps = LBLOCK_VARIANTS[variant]
    v = 3 * _left_v(apps)
    row, origin = padded_row(tape, apps, left_periods=LBLOCK_T // (30 * v) + 3,
                             right_periods=14, left_pad=300_000,
                             right_pad=350_000, v_override=v)
    run, dec = Run(row, origin), Decoder()
    print(f"variant {variant}: tape={tape} apps={apps} v={v} width={run.width}")
    while run.t <= LBLOCK_T:
        print(f"t={run.t}: {read_moving_data(dec, run, -5_000, 40_000)}",
              flush=True)
        run.step(LBLOCK_EVERY)


def demol(T):
    row, origin = padded_row(DEMOL_TAPE, DEMOL_APPS, left_periods=13,
                             right_periods=7, left_pad=700_000,
                             right_pad=1_000_000)
    run, dec = Run(row, origin), Decoder()
    t0 = time.time()
    print(f"De Mol x=3: width={run.width}")
    while run.t <= T:
        print(f"t={run.t} ({time.time() - t0:.0f}s): "
              f"{read_moving_data(dec, run, -30_000, 90_000)}", flush=True)
        run.step(DEMOL_EVERY)


if __name__ == "__main__":
    if sys.argv[1:2] == ["lblock"]:
        lblock(int(sys.argv[2]))
    elif sys.argv[1:2] == ["demol"]:
        demol(int(sys.argv[2]) if len(sys.argv) > 2 else 1_350_000)
    else:
        sys.exit(__doc__)
