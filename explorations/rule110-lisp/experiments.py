"""Long automaton runs whose results are cited in NOTES.md / REPORT.md.

    python experiments.py lblock VARIANT     # one row of the L-block table
    python experiments.py demol [T]           # De Mol 3x+1, x=3
    python experiments.py fronts [N]          # moving data met by ossifiers

lblock and demol print decoder reads of the moving data in flight at
intervals: liveness, not verified correctness (REVIEW.md B3). fronts is
the dynamic check of REPORT.md section 3.3: at each ossifier's arrival it
prints the first moving-data symbols it will meet, next to the symbols
the reference CTS predicts if each A^4 converts one character.
"""

import sys
import time

from casim import Run, padded_row
from census import MAX_DT, census
from cts import run as cts_run
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


# fronts: {YYYYNN} from YYYYNN, whose read sequence is YYYYNN repeated
FRONTS_TAPE, FRONTS_APPS = "YYYYNN", ["YYYYNN"]
FRONTS_EVERY = 250
A4_PER_OSSIFIER = 4


def ossifier_fronts(n_arrivals):
    """At each ossifier arrival, the first three moving-data symbols it
    will meet. An ossifier is A material entering the Ebar-frame window
    from outside the Ebar stream (acceptors and rejectors are A material
    too, but are born inside the stream)."""
    v = 3 * _left_v(FRONTS_APPS)
    T = (n_arrivals + 2) * 32 * v
    row, origin = padded_row(FRONTS_TAPE, FRONTS_APPS, left_periods=n_arrivals + 3,
                             right_periods=T // 30_000 + 4, left_pad=T + 50_000,
                             right_pad=T + 100_000, v_override=v)
    run, dec = Run(row, origin), Decoder()
    out, approaching = [], False
    while len(out) < n_arrivals and run.t < T:
        run.step(FRONTS_EVERY - MAX_DT)
        f = run.ebar_frame()
        H = run.history(f - 3_000, f + 12_000, MAX_DT)
        cs = census(H)
        stream_left = min((a for a, b, k in cs if k == "E"), default=H.shape[1])
        n_a = sum(1 for a, b, k in cs if k == "A" and b < stream_left)
        if n_a and not approaching:
            try:
                front = "".join(s for _, s in dec.read(H[-1])[:3])
            except ValueError:
                front = "?"
            out.append((run.t, front))
        approaching = bool(n_a)
    return out


def fronts(n_arrivals):
    reads = [t[0] for _, t, _ in cts_run(FRONTS_TAPE, FRONTS_APPS,
                                         A4_PER_OSSIFIER * n_arrivals + 3) if t]
    for k, (t, front) in enumerate(ossifier_fronts(n_arrivals)):
        i = A4_PER_OSSIFIER * k
        want = "".join(reads[i:i + 3])
        print(f"arrival {k} t={t:7d}: meets {front}  predicted {want}  "
              f"{'ok' if front == want else 'MISMATCH'}", flush=True)


if __name__ == "__main__":
    if sys.argv[1:2] == ["fronts"]:
        fronts(int(sys.argv[2]) if len(sys.argv) > 2 else 9)
    elif sys.argv[1:2] == ["lblock"]:
        lblock(int(sys.argv[2]))
    elif sys.argv[1:2] == ["demol"]:
        demol(int(sys.argv[2]) if len(sys.argv) > 2 else 1_350_000)
    else:
        sys.exit(__doc__)
