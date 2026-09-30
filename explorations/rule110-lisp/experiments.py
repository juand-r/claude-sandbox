"""Long automaton runs whose results are cited in NOTES.md / REPORT.md.

    python experiments.py lblock VARIANT [N] [fill]  # L-block table row
    python experiments.py demol [T]           # De Mol 3x+1, x=3
    python experiments.py reads [N]           # outcomes of the first N reads
    python experiments.py cost                # REPORT.md section 4 table
    python experiments.py collatz [V] [N]     # De Mol 3x+1 on gliders (3.6)

reads and lblock are the dynamic check of REPORT.md 3.3-3.4: they
observe each read's outcome directly (see read_outcomes) and compare the
sequence with the reference CTS. demol prints decoder reads of the
moving data in flight at intervals: liveness only (the moving-data
decoder misreads depending on glider phase; NOTES.md).
"""

import os
import pickle
import sys
import time

from casim import Run, StreamRun, padded_row
from census import MAX_DT, census
from cts import fill_empty_appendants, run as cts_run
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
# Generation budget per read, in ossifier periods (~30v). Measured reads
# come one period apart for {YYYYNN} and two apart for LBLOCK_VARIANTS[4];
# read_outcomes stops as soon as every read has settled, so a generous
# budget only costs padding width.
READ_BUDGET_PERIODS = 2

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


def lblock(variant, n_reads=8, fill=False):
    """fill: replace empty appendants by junk N's (cts.fill_empty_appendants),
    which removes every L block from the construction. With no empty
    appendants the paper's default v is valid, so filled runs use it."""
    tape, apps = LBLOCK_VARIANTS[variant]
    if fill:
        apps = fill_empty_appendants(apps)
    check(tape, apps, (1 if fill else 3) * _left_v(apps), n_reads)


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
# A settled accepted region keeps about 4 Ebar clusters per appendant
# symbol (measured 23-25 for 6 symbols in every run that matched the
# reference); a rejected region keeps none. Any other count means the
# region was disturbed rather than read, and is reported as '!'.
TILE_PAD = 1_400                  # HashRun adds its own ether padding
CHECKPOINT_EVERY = 100            # samples (x READS_EVERY generations)
READS_LOOKAHEAD = 4        # a region must be watched before its read starts
ACCEPT_CLUSTERS_PER_SYMBOL = 4
ACCEPT_TOLERANCE = 2


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


def read_outcomes(tape, apps, v, n_reads, T, row_origin=None, stream=True,
                  engine=None, checkpoint=None):
    """Observed outcome ('Y'/'N') of each of the first n_reads reads, '!'
    if the region settled in a state that is neither, or '.' if not
    completed by generation T. row_origin: optionally a prebuilt
    (row, origin) for a modified assembly with the same right side.
    stream: use casim.StreamRun (exact, steps only the active window).
    engine="hash": use hashlife.HashRun instead (an independent check)."""
    rp = n_reads // len(apps) + 3
    if engine == "hash":
        from hashlife import HashRun
        run = HashRun(*padded_row(tape, apps, left_periods=T // (30 * v) + 3,
                                  right_periods=rp, left_pad=TILE_PAD,
                                  right_pad=TILE_PAD, v_override=v))
    elif row_origin is not None:
        run = Run(*row_origin)
    elif stream:
        run = StreamRun(tape, apps, T // (30 * v) + 3, rp, v_override=v)
    else:
        run = Run(*padded_row(tape, apps, left_periods=T // (30 * v) + 3,
                              right_periods=rp, left_pad=T + 50_000,
                              right_pad=T + 100_000, v_override=v))
    regs = component_regions(tape, apps, rp)[:n_reads]
    before = [None] * len(regs)
    state = ["." if a is not None else "-" for a, _ in regs]
    read_at = [None] * len(regs)
    last = [None] * len(regs)
    key = (tape, tuple(apps), v, n_reads, T)
    if checkpoint and os.path.exists(checkpoint):
        with open(checkpoint, "rb") as fh:
            saved = pickle.load(fh)
        if saved["key"] != key:
            raise ValueError(f"checkpoint {checkpoint} is for another run")
        run, before, state, read_at, last = (saved[k] for k in
                                             ("run", "before", "state", "read_at", "last"))
        print(f"resumed from checkpoint at t={run.t}", flush=True)
    origin = run.origin
    samples = 0
    while run.t + READS_EVERY <= T and any(s in ".r" for s in state):
        # reads happen in order: watch only the next few pending regions
        pending = [j for j, s in enumerate(state) if s in ".r"][:READS_LOOKAHEAD]
        lo_g = min(regs[j][0] for j in pending) - READS_MARGIN
        hi_g = max(regs[j][1] for j in pending) + READS_MARGIN
        run.step(READS_EVERY - MAX_DT)
        shift = run.ebar_frame() - origin
        lo = origin + lo_g + shift
        cs = census(run.history(lo, origin + hi_g + shift, MAX_DT))
        shift = run.ebar_frame() - origin
        rel = [(x0 + lo - origin - shift, k) for x0, _, k in cs]
        for j in pending:
            a, b = regs[j]
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
                expect = ACCEPT_CLUSTERS_PER_SYMBOL * len(apps[j % len(apps)])
                if n_e == 0:
                    state[j] = "N"
                elif abs(n_e - expect) <= ACCEPT_TOLERANCE:
                    state[j] = "Y"
                else:
                    state[j] = "!"
                print(f"read {j}: at t~{read_at[j]}, {n_e} Ebar clusters "
                      f"remain: {state[j]}", flush=True)
            last[j] = inside
        samples += 1
        if checkpoint and samples % CHECKPOINT_EVERY == 0:
            tmp = checkpoint + ".tmp"
            with open(tmp, "wb") as fh:
                pickle.dump({"key": key, "run": run, "before": before,
                             "state": state, "read_at": read_at, "last": last}, fh)
            os.replace(tmp, checkpoint)
    if checkpoint and os.path.exists(checkpoint):
        os.remove(checkpoint)          # finished: a rerun starts fresh
    return "".join(s if s in "YN!" else "." for s in state)


def check(tape, apps, v, n_reads):
    """Observed read outcomes vs the reference CTS. Reads of empty
    appendants have no component region and show as '.' in both."""
    T = (n_reads + 2) * READ_BUDGET_PERIODS * 30 * v
    got = read_outcomes(tape, apps, v, n_reads, T)
    ref = "".join(t[0] if apps[i % len(apps)] else "."
                  for i, (_, t, _) in enumerate(cts_run(tape, apps, n_reads))
                  if t)[:n_reads]
    same = sum(g == r for g, r in zip(got, ref))
    print(f"observed : {got}\nreference: {ref}\n"
          f"{'MATCH' if got == ref else 'DIFFER'} ({same}/{n_reads})")


def reads(n_reads):
    check(READS_TAPE, READS_APPS, 3 * _left_v(READS_APPS), n_reads)


def collatz(v, n_reads, per_read):
    """De Mol's 3x+1 tag system from x = 3, filled (no L blocks), on
    gliders: the first n_reads CTS reads against the reference. Collatz
    5, 8, 4, 2, 1 are reached at reads 72, 204, 372, 492, 552. Checkpoints
    to collatz_v{v}_n{n_reads}.ckpt, so an interrupted run resumes."""
    apps = fill_empty_appendants(DEMOL_APPS)
    got = read_outcomes(DEMOL_TAPE, apps, v, n_reads, n_reads * per_read + 30_000,
                        checkpoint=f"collatz_v{v}_n{n_reads}.ckpt")
    ref = "".join(t[0] for _, t, _ in cts_run(DEMOL_TAPE, apps, n_reads) if t)[:n_reads]
    same = sum(g == r for g, r in zip(got, ref))
    print(f"{'MATCH' if got == ref else 'DIFFER'} ({same}/{n_reads})")


def tower_cost(direct):
    """Sizes and step counts of the capstone machine (tests/machines.py
    three_state_tm on CAPSTONE_CFG) at every level of the tower, and the
    Rule 110 estimate at ~30v generations per read (REPORT.md 3.3).
    direct: build the binary clockwise machine with two_way_to_binary_cw
    instead of two_way_to_cw + binarize."""
    sys.path.insert(0, "tests")
    from machines import three_state_tm
    from cw import binarize, two_way_to_binary_cw, two_way_to_cw, CWTM
    from nw import build_rules, initial_tape
    from tag import run as tag_run, ts_to_cts
    tm2 = three_state_tm()
    if direct:
        bdelta, bword, bst0, _ = two_way_to_binary_cw(tm2, *CAPSTONE_CFG)
    else:
        bdelta, bword, bst0, _ = binarize(*two_way_to_cw(tm2, *CAPSTONE_CFG))
    bstates = {q for q, _ in bdelta} | {n for _, n in bdelta.values()}
    bsteps = sum(1 for _ in CWTM(bdelta).run(bst0, bword, 10**6)) - 1
    rules = build_rules(CWTM(bdelta), sorted(bstates, key=repr))
    tape0 = initial_tape(bst0, list(bword), 16)
    tag_steps, empty_hits = 0, 0
    for n, t in tag_run(rules, tape0, 2, 10**7):
        tag_steps = n
        if len(t) >= 2 and not rules[t[0]]:
            empty_hits += 1
    _, apps, order = ts_to_cts(rules, tape0, 2, order=sorted(rules, key=repr))
    reads = tag_steps * len(apps)
    v = _left_v(apps)
    # fill_empty_appendants: each Y read on an empty appendant (one skipped
    # word per tag step, plus reads of halting symbols) adds m junk reads
    filled = fill_empty_appendants(apps)
    m = len(apps)
    reads_f = reads + (tag_steps + empty_hits) * m
    v_f = _left_v(filled)
    print(f"{'direct' if direct else 'binarize'}: binary cw {len(bstates)} states,"
          f" {bsteps} steps; NW {len(rules)} rules, {tag_steps} tag steps;"
          f" CTS {len(apps)} appendants, {sum(map(len, apps)):.3g} symbols,"
          f" {reads:.3g} reads; v = {v:.3g} -> {30 * v * reads:.2g} generations;"
          f" filled: {reads_f:.3g} reads, v = {v_f:.3g} ->"
          f" {30 * v_f * reads_f:.2g} generations")


CAPSTONE_CFG = (1, [1], 1, [1, 1, 2])     # as in tests/test_tower.py


if __name__ == "__main__":
    if sys.argv[1:2] == ["collatz"]:
        # Cook's v = 12,216 and 556 reads reproduce REPORT.md 3.6 (~4 h)
        collatz(int(sys.argv[2]) if len(sys.argv) > 2 else 12_216,
                int(sys.argv[3]) if len(sys.argv) > 3 else 556, 430_000)
    elif sys.argv[1:2] == ["cost"]:
        tower_cost(direct=False)
        tower_cost(direct=True)
    elif sys.argv[1:2] == ["reads"]:
        reads(int(sys.argv[2]) if len(sys.argv) > 2 else 12)
    elif sys.argv[1:2] == ["lblock"]:
        args = [a for a in sys.argv[2:] if a != "fill"]
        lblock(int(args[0]), int(args[1]) if len(args) > 1 else 8,
               fill="fill" in sys.argv)
    elif sys.argv[1:2] == ["demol"]:
        demol(int(sys.argv[2]) if len(sys.argv) > 2 else 1_350_000)
    else:
        sys.exit(__doc__)
