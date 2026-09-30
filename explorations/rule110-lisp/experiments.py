"""Long automaton runs whose results are cited in NOTES.md / REPORT.md.

    python experiments.py lblock VARIANT     # one row of the L-block table
    python experiments.py demol [T]           # De Mol 3x+1, x=3
    python experiments.py reads [N]           # outcomes of the first N reads

lblock and demol print decoder reads of the moving data in flight at
intervals: liveness only (the moving-data decoder misreads depending on
glider phase; NOTES.md). reads is the dynamic check of REPORT.md 3.3: it
observes each read's outcome directly (see read_outcomes) and compares
the sequence with the reference CTS.
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


# reads: the dynamic check. Each read's outcome is observed without any
# decoder: when a leader reads a tape character, an acceptor or rejector
# sweeps that appendant's components. A Y turns them into moving data (the
# region keeps Ebars); an N deletes them (the region becomes ether). In the
# Ebar frame every region is static until its read, so its census at a
# fixed phase (t = 0 mod 30) is constant; the first change marks the read.
READS_TAPE, READS_APPS = "YYYYNN", ["YYYYNN"]
READS_EVERY = 600                 # a multiple of 30: same Ebar phase
READS_MARGIN = 3_000


def component_regions(tape, apps, right_periods):
    """Global column ranges (t = 0) of each appendant copy's components, in
    read order; (None, None) for empty appendants."""
    from encoder import assemble
    _, placed = assemble(tape, apps, 1, right_periods)
    names = [p.block.name for p in placed]
    leaders = [i for i, n in enumerate(names) if n in "GKL"]
    return [(placed[a + 1].gspan(0)[0], placed[b - 1].gspan(0)[1])
            if b - a > 1 else (None, None)
            for a, b in zip(leaders, leaders[1:])]


def read_outcomes(tape, apps, v, n_reads, T, row_origin=None):
    """Observed outcome ('Y'/'N') of each of the first n_reads reads, or
    '.' if not completed by generation T. row_origin: optionally a prebuilt
    (row, origin) for a modified assembly with the same right side."""
    rp = n_reads // len(apps) + 3
    if row_origin is None:
        row_origin = padded_row(tape, apps, left_periods=T // (30 * v) + 3,
                                right_periods=rp, left_pad=T + 50_000,
                                right_pad=T + 100_000, v_override=v)
    row, origin = row_origin
    regs = component_regions(tape, apps, rp)[:n_reads]
    run = Run(row, origin)
    before = [None] * len(regs)
    state = ["." if a is not None else "-" for a, _ in regs]
    read_at = [None] * len(regs)
    last = [None] * len(regs)
    lo_g = min(a for a, _ in regs if a is not None) - READS_MARGIN
    hi_g = max(b for _, b in regs if b is not None) + READS_MARGIN
    while run.t + READS_EVERY <= T and any(s in ".r" for s in state):
        run.step(READS_EVERY - MAX_DT)
        shift = run.ebar_frame() - origin
        lo = origin + lo_g + shift
        cs = census(run.history(lo, origin + hi_g + shift, MAX_DT))
        shift = run.ebar_frame() - origin
        rel = [(x0 + lo - origin - shift, k) for x0, _, k in cs]
        for j, (a, b) in enumerate(regs):
            if state[j] not in ".r":
                continue
            inside = tuple(c for c in rel if a <= c[0] < b)
            if before[j] is None:
                before[j] = inside
            elif state[j] == "." and inside != before[j]:
                state[j], read_at[j] = "r", run.t
            elif (state[j] == "r" and inside == last[j]
                  and not any(k in "CA?" for _, k in inside)):
                # settled: nothing sweeping or crossing, and unchanged since
                # the previous sample (a sweep in progress changes it)
                n_e = sum(1 for _, k in inside if k == "E")
                state[j] = "Y" if n_e else "N"
                print(f"read {j}: at t~{read_at[j]}, {n_e} Ebar clusters "
                      f"remain: {state[j]}", flush=True)
            last[j] = inside
    return "".join(s if s in "YN" else "." for s in state)


def reads(n_reads):
    v = 3 * _left_v(READS_APPS)
    T = (n_reads + 2) * 60_000
    got = read_outcomes(READS_TAPE, READS_APPS, v, n_reads, T)
    ref = "".join(t[0] for _, t, _ in cts_run(READS_TAPE, READS_APPS, n_reads)
                  if t)[:n_reads]
    print(f"observed : {got}\nreference: {ref}\n"
          f"{'MATCH' if got == ref else 'DIFFER'} ({sum(g == r for g, r in zip(got, ref))}/{n_reads})")


if __name__ == "__main__":
    if sys.argv[1:2] == ["reads"]:
        reads(int(sys.argv[2]) if len(sys.argv) > 2 else 12)
    elif sys.argv[1:2] == ["lblock"]:
        lblock(int(sys.argv[2]))
    elif sys.argv[1:2] == ["demol"]:
        demol(int(sys.argv[2]) if len(sys.argv) > 2 else 1_350_000)
    else:
        sys.exit(__doc__)
