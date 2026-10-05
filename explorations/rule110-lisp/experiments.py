"""Long automaton runs whose results are cited in NOTES.md / REPORT.md.

    python experiments.py lblock VARIANT [N] [fill]  # L-block table row
    python experiments.py demol [T]           # De Mol 3x+1, x=3
    python experiments.py reads [N]           # outcomes of the first N reads
    python experiments.py cost                # REPORT.md section 4 table
    python experiments.py collatz [V] [N]     # De Mol 3x+1 on gliders (3.6)
    python experiments.py collatz-hash [V] [N]  # the same on HashLife (5)
    python experiments.py tm-gliders [one|three] [F]  # compiled TM on gliders, F x Cook's v (3.7)

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
from collections import deque

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
    read order; (None, None) for empty appendants. Beyond one super-period
    (encoder.right_super_period) the regions repeat, shifted."""
    from encoder import assemble, right_super_period
    m, w = right_super_period(tape, apps) if right_periods > 2 else (0, 0)
    _, placed = assemble(tape, apps, 0, min(right_periods, m + 1) if m else right_periods)
    names = [p.block.name for p in placed]
    leaders = [i for i, n in enumerate(names) if n in "GKL"]
    regs = [(placed[a + 1].gspan(0)[0], placed[b - 1].gspan(0)[1])
            if b - a > 1 else (None, None)
            for a, b in zip(leaders, leaders[1:])]
    n = right_periods * len(apps)
    per = m * len(apps)
    while len(regs) < n:
        a, b = regs[len(regs) - per]
        regs.append((None, None) if a is None else (a + w, b + w))
    return regs


class ReadWatch:
    """Bookkeeping of the decoder-free read check (see the comment above
    READS_TAPE). regs[j] is read j's component region (global columns at
    t = 0, which in the Ebar frame stay put until the read). state[j]: '.'
    waiting, 'r' reading, then 'Y', 'N' or '!' once settled, '-' for an
    empty appendant (no region)."""

    def __init__(self, regs, apps, lookahead=READS_LOOKAHEAD):
        self.regs, self.apps, self.lookahead = regs, apps, lookahead
        self.before = [None] * len(regs)
        self.state = ["." if a is not None else "-" for a, _ in regs]
        self.read_at = [None] * len(regs)
        self.last = [None] * len(regs)
        self.n_ebar = [None] * len(regs)  # Ebar clusters of a settled region
        self.t_last = None            # time of the latest sample

    def pending(self):
        """Reads happen in order: watch only the next few pending regions."""
        return [j for j, s in enumerate(self.state) if s in ".r"][:self.lookahead]

    def span(self, pending):
        return (min(self.regs[j][0] for j in pending) - READS_MARGIN,
                max(self.regs[j][1] for j in pending) + READS_MARGIN)

    def observe(self, t, pending, rel):
        """rel: census [(x, kind)] at time t, x in Ebar-frame global columns
        (the t = 0 column of a cell moving with Ebar velocity). Samples must
        come in time order (a region seen again before its read started
        would look unread)."""
        if self.t_last is not None and t < self.t_last:
            raise RuntimeError(f"sample at t={t} precedes the previous one ({self.t_last})")
        self.t_last = t
        for j in pending:
            a, b = self.regs[j]
            inside = tuple(c for c in rel if a <= c[0] < b)
            if self.before[j] is None:
                self.before[j] = inside
            elif self.state[j] == "." and inside != self.before[j]:
                self.state[j], self.read_at[j] = "r", t
            elif (self.state[j] == "r" and inside == self.last[j]
                  and not any(k in "CA?" for _, k in inside)):
                # settled: nothing sweeping or crossing, and unchanged since
                # the previous sample (a sweep in progress changes it)
                n_e = sum(1 for _, k in inside if k == "E")
                expect = ACCEPT_CLUSTERS_PER_SYMBOL * len(self.apps[j % len(self.apps)])
                if n_e == 0:
                    self.state[j] = "N"
                elif abs(n_e - expect) <= ACCEPT_TOLERANCE:
                    self.state[j] = "Y"
                else:
                    self.state[j] = "!"
                print(f"read {j}: at t~{self.read_at[j]}, {n_e} Ebar clusters "
                      f"remain: {self.state[j]}", flush=True)
                # a settled region is never watched again: keep its count,
                # drop its censuses (they made long runs' memory grow)
                self.n_ebar[j] = n_e
                self.before[j] = self.last[j] = None
                continue
            self.last[j] = inside

    def forget_settled(self):
        """Drop the censuses of settled regions (for state from before
        observe() did so itself)."""
        for j, st in enumerate(self.state):
            if st in "YN!":
                self.before[j] = self.last[j] = None

    def outcome(self):
        return "".join(s if s in "YN!" else "." for s in self.state)


def sample(run, watch, pending, depth=MAX_DT, advance=True):
    """Census of the pending regions at time run.t + depth (which must be
    0 mod 30, the phase the regions' censuses are compared at). With
    advance the run steps there (Run.history's contract); otherwise
    (HashRun only) it stays put."""
    t = run.t + depth
    if t % 30:
        raise ValueError(f"census at t={t}: not 0 mod 30")
    lo_g, hi_g = watch.span(pending)
    shift = run.ebar_frame(run.t) - run.origin
    lo = run.origin + lo_g + shift
    hist = (run.history(lo, run.origin + hi_g + shift, depth) if advance else
            run.history(lo, run.origin + hi_g + shift, depth, advance=False))
    cs = census(hist)
    shift = run.ebar_frame(t) - run.origin
    rel = [(x0 + lo - run.origin - shift, k) for x0, _, k in cs]
    watch.observe(t, pending, rel)


# Why long rejection runs need a larger v (REPORT 3.7). The symbols waiting
# to become tape (moving data) are static in the Ebar frame; tape characters
# drift right through it at 8/30 cell per generation. An ossifier turns the
# next queued symbol into a character only if that symbol has already drifted
# past the newest character, i.e. if the spatial gap from one queued symbol
# to the next is small enough. Within an appendant copy it is one symbol; at
# the boundary between two consecutively queued copies it is the whole width
# of the appendant regions read (and rejected) in between. When the gap is
# too large the ossifier hits the newest character instead and the machine
# breaks. Measured threshold (De Mol, 13 spacings; one-move TM): a gap G
# fails when G > GAP_PER_V * v, GAP_PER_V between 11.05 and 11.39.
GAP_PER_V = 11.2


def block_gaps(tape, apps, n_reads):
    """[(read R, copy a, copy b, gap)]: the reads after which the queue moves
    from the appendant copy appended at read a to the one appended at read
    b, with the t = 0 spatial gap between their component regions. The
    first predicted failure at spacing v is the first R with
    gap > GAP_PER_V * v."""
    regs = component_regions(tape, apps, n_reads // len(apps) + 3)
    q = deque((-1, ch) for ch in tape)
    origin = []
    for r in range(n_reads):
        if not q:
            break
        a, ch = q.popleft()
        origin.append(a)
        if ch == "Y":
            q.extend((r, x) for x in apps[r % len(apps)])
    return [(R, a, b, regs[b][0] - regs[a][1])
            for R, (a, b) in enumerate(zip(origin, origin[1:])) if a != b and a >= 0]


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
    watch = ReadWatch(component_regions(tape, apps, rp)[:n_reads], apps)
    key = (tape, tuple(apps), v, n_reads, T)
    if checkpoint and os.path.exists(checkpoint):
        with open(checkpoint, "rb") as fh:
            saved = pickle.load(fh)
        if saved["key"] != key:
            raise ValueError(f"checkpoint {checkpoint} is for another run")
        run, watch = saved["run"], saved["watch"]
        print(f"resumed from checkpoint at t={run.t}", flush=True)
    samples = 0
    while run.t + READS_EVERY <= T and watch.pending():
        run.step(READS_EVERY - MAX_DT)
        sample(run, watch, watch.pending())
        samples += 1
        if checkpoint and samples % CHECKPOINT_EVERY == 0:
            tmp = checkpoint + ".tmp"
            with open(tmp, "wb") as fh:
                pickle.dump({"key": key, "run": run, "watch": watch}, fh)
            os.replace(tmp, checkpoint)
    if checkpoint and os.path.exists(checkpoint):
        os.remove(checkpoint)          # finished: a rerun starts fresh
    return watch.outcome()


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


def collatz_hash(v, n_reads):
    """collatz() on the HashLife epoch engine (epochrun.EpochReads): the
    same 556 reads in under a minute instead of hours, an independent
    check of the StreamRun run."""
    from epochrun import EpochReads
    apps = fill_empty_appendants(DEMOL_APPS)
    t0 = time.time()
    got = EpochReads(DEMOL_TAPE, apps, v, n_reads, sample_bits=14).run_reads()
    ref = "".join(t[0] for _, t, _ in cts_run(DEMOL_TAPE, apps, n_reads) if t)[:n_reads]
    same = sum(g == r for g, r in zip(got, ref))
    print(f"{'MATCH' if got == ref else 'DIFFER'} ({same}/{n_reads}) "
          f"(v={v}, {time.time() - t0:.0f}s)")


def collatz_gas(v, n_reads):
    """collatz() on the event engine (gasrun.GasReads)."""
    from gasrun import GasReads
    apps = fill_empty_appendants(DEMOL_APPS)
    t0 = time.time()
    got = GasReads(DEMOL_TAPE, apps, v, n_reads, sample_bits=14).run_reads()
    ref = "".join(t[0] for _, t, _ in cts_run(DEMOL_TAPE, apps, n_reads) if t)[:n_reads]
    same = sum(g == r for g, r in zip(got, ref))
    print(f"{'MATCH' if got == ref else 'DIFFER'} ({same}/{n_reads}) "
          f"(v={v}, {time.time() - t0:.0f}s)")


def gas_vs_hash(checkpoint):
    """Cell-exact check of the event engine against HashLife: load an
    EpochReads checkpoint of the one-move TM at Cook's v (tm-gliders one
    1), run the event engine from t = 0 to its time, and compare every
    cell of the active region."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests"))
    import numpy as np
    import machines
    import gasrun
    from epochrun import EpochReads, diff_extent
    from tag import ts_to_cts
    from tm import tm_to_ts
    make, cfg = TM_RUNS["one"]
    rules, ts_tape, s = tm_to_ts(getattr(machines, make)(), *cfg)
    tape, apps, _ = ts_to_cts(rules, ts_tape, s)
    apps = fill_empty_appendants(apps)
    t0 = time.time()
    er = EpochReads(tape, apps, _left_v(apps), 5970, 17, checkpoint=checkpoint)
    er.checkpoint = None                     # read only
    T = er.run.t
    g = gasrun.build(er.lay, er.n_all)
    g.advance_to(T)
    print(f"event engine at t={T}: {g.n_events} events, {time.time() - t0:.0f}s", flush=True)
    left, right = er.uni.at(T)
    j = next(j for j, st in enumerate(er.watch.state) if st in ".r")
    a, b = diff_extent(er.run, left, right, er.regs[j][0] - 8 * T // 30)
    lo, hi, chunk, bad = a - (1 << 16), b + (1 << 16), 1 << 22, 0
    for x in range(lo, hi, chunk):
        y = min(hi, x + chunk)
        bad += int(np.count_nonzero(g.window(x, y) != er.run.window(x, y)))
    print(f"{'MATCH' if bad == 0 else 'DIFFER'}: {hi - lo} cells compared "
          f"(active region [{a}, {b}]), {bad} differ, {time.time() - t0:.0f}s")


# Compiled Turing machines on gliders (REPORT.md 3.7): tests/machines.py
# machine and start configuration (state, left_bg, left, cur, right,
# right_bg), compiled TM -> tag (Cocke-Minsky) -> CTS -> filled CTS.
TM_RUNS = {"one": ("one_move_tm", (1, [1], [1], 1, [1], [1])),
           "three": ("three_state_tm", (1, [1], [1], 1, [2], [1]))}


def tm_visits(heads, t):
    """Genuine (state, symbol) visits among tag heads H_i_j (j <= t)."""
    out = []
    for h in heads:
        if h.startswith("H_") and h.count("_") == 2:
            i, j = map(int, h.split("_")[1:])
            if j <= t:
                out.append((i, j))
    return out


def tm_gliders(name, v_factor=1, sample_bits=17, epoch=8, engine="hash"):
    """Run a compiled TM on gliders (at v_factor times Cook's v) up to the
    read that completes its halting visit, then decode the TM's visit
    sequence from the observed reads alone and compare it with the TM.
    engine: "hash" (epochrun.EpochReads) or "gas" (gasrun.GasReads, the
    event engine). Checkpoints to tm_{name}_v{v_factor}[_gas].ckpt (rerun
    the same command to resume)."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests"))
    import machines
    from epochrun import EpochReads
    from tag import heads_from_reads, ts_to_cts
    from tm import tm_to_ts
    make, cfg = TM_RUNS[name]
    tm = getattr(machines, make)()
    ref = list(tm.run(*cfg, max_steps=1000))
    rules, ts_tape, s = tm_to_ts(tm, *cfg)
    tape, apps, order = ts_to_cts(rules, ts_tape, s)
    apps = fill_empty_appendants(apps)
    v = v_factor * _left_v(apps)
    if v == int(v):
        v = int(v)
    # reference reads, long enough to contain the halting visit's word
    q, ref_reads, n = deque(tape), [], 0
    while True:
        c = q.popleft()
        ref_reads.append(c)
        if c == "Y":
            q.extend(apps[n % len(apps)])
        n += 1
        if n % (s * len(order)) == 0:
            heads, stops = heads_from_reads("".join(ref_reads), order, s, ends=True)
            if len(tm_visits(heads, tm.t)) >= len(ref):
                break
    n_reads = max(e for h, e in zip(heads, stops) if h == f"H_{ref[-1][0]}_{ref[-1][1]}")
    ref_reads = "".join(ref_reads[:n_reads])
    print(f"{make} {cfg}: visits {ref}; CTS {len(apps)} appendants, "
          f"{sum(map(len, apps))} symbols, v = {v}; {n_reads} reads", flush=True)
    t0 = time.time()
    if engine == "gas":
        from gasrun import GasReads
        ckpt = f"tm_{name}_v{v_factor}_gas.ckpt"
        er = GasReads(tape, apps, v, n_reads, sample_bits=sample_bits, checkpoint=ckpt)
    else:
        ckpt = f"tm_{name}_v{v_factor}.ckpt"
        er = EpochReads(tape, apps, v, n_reads, sample_bits=sample_bits, epoch=epoch,
                        checkpoint=ckpt)
    got = er.run_reads()
    same = sum(g == r for g, r in zip(got, ref_reads))
    print(f"reads: {'MATCH' if got == ref_reads else 'DIFFER'} ({same}/{n_reads}), "
          f"t = {er.run.t}, {time.time() - t0:.0f}s")
    visits = tm_visits(heads_from_reads(got, order, s), tm.t)
    print(f"TM visits decoded from the glider reads: {visits}\n"
          f"TM visits (reference):                   {ref}\n"
          f"{'MATCH' if visits == ref else 'DIFFER'}")
    if os.path.exists(ckpt):
        os.remove(ckpt)


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
    elif sys.argv[1:2] == ["collatz-hash"]:
        # the same run on the HashLife epoch engine (~1 min)
        collatz_hash(int(sys.argv[2]) if len(sys.argv) > 2 else 12_216,
                     int(sys.argv[3]) if len(sys.argv) > 3 else 556)
    elif sys.argv[1:2] == ["tm-gliders"]:
        # tm-gliders [one|three] [F] [gas]
        f = sys.argv[3] if len(sys.argv) > 3 else "1"
        tm_gliders(sys.argv[2] if len(sys.argv) > 2 else "one",
                   float(f) if "." in f else int(f),
                   engine="gas" if "gas" in sys.argv[4:] else "hash")
    elif sys.argv[1:2] == ["collatz-gas"]:
        # the same run on the event engine (gasrun.GasReads, ~15 s)
        collatz_gas(int(sys.argv[2]) if len(sys.argv) > 2 else 12_216,
                    int(sys.argv[3]) if len(sys.argv) > 3 else 556)
    elif sys.argv[1:2] == ["gas-vs-hash"]:
        gas_vs_hash(sys.argv[2])
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
