# Notes

## Standing rules (read before running anything)

1. Never `pkill -f PATTERN`, and never `kill $(pgrep -f PATTERN)`: the
   pattern is in the calling shell's own command line, so it kills that
   shell (four times now, the last via pgrep). Record PIDs at launch
   (`echo $! > file`) and `kill $(cat file)`.
2. An instrument is a hypothesis until validated. Before trusting a
   decoder or classifier, check it on a known-good run AND make sure it
   rejects a known-bad one (the moving-data decoder and the first read
   classifier both passed broken runs).
3. Before committing, run pytest without piping it (a pipe to tail hides
   the exit status; a failing test was committed once that way).

## Sources

- M. Cook, "Universality in Elementary Cellular Automata", Complex Systems
  15(1), 2004. The original construction.
- M. Cook, "A Concrete View of Rule 110 Computation", EPTCS 1, 2009,
  arXiv:0906.3248. Self-contained explicit algorithm: TM -> tag system ->
  cyclic tag system -> Rule 110 initial state. Layer 1 implements its
  final section verbatim. Its "A Polynomial Time Simulation" section also
  contains an explicit Neary-Woods-style tag system (production tables in
  the LaTeX source) that will drive Layer 2.
- arXiv source tarball fetched from https://arxiv.org/e-print/0906.3248;
  the 12 bit-block figures are Mathematica grayscale rasters, decoded by
  tools/extract_blocks.py into data/blocks.json.

## Block data facts (all verified by tests)

- Pixel values: 0x00 alive, 0xFF dead, 0x80 outside the block's zig-zag
  boundary; 0xB3 marks the t=0 row (block C only).
- EPS prolog applies "1 -1 scale": raster rows are stored bottom-to-top.
  The extractor reverses them so row index = time. This was discovered the
  hard way: with raw ordering, patch row r evolves to row r-1.
- Periodicity as lattice vectors (rows, cols): A, B repeat at (3, +2);
  D..L at (30, -8); C is aperiodic with the t=0 marker at row 48.
- Blocks tile the plane exactly (complementary zig-zag cuts, no overlap,
  no gap). Seam placement is solved geometrically by matching edge
  profiles over ~80 rows; for every seam type this yields a unique
  placement up to lattice equivalence, and the result is rule-valid
  (zero Rule 110 violations across the seam).

## Debugging log

- Symptom: ~50% cell mismatch between evolution and patches. Cause 1:
  time direction (above). Cause 2 (after fixing 1, still ~40% mismatch):
  the comparison script indexed the evolved array by global column
  without subtracting the leftmost block's column origin. The
  construction itself was correct; per-seam rule-validity checks
  localized the problem to the comparison, not the encoder.
  Lesson recorded: when a global differential test fails, first test the
  smallest local property that must also fail (here: single seams) --
  if the local test passes, suspect the test harness.

## Current state

Layer 1 encoder produces a t=0 row for any CTS (nonempty first appendant,
tape of Y/N). Verified: 1.15M patch cells reproduced exactly by the real
CA over the first 45 steps of the NNYN / {YN, NYYN, e, e} example.

Open: long-run validation (glider-level CTS steps take ~O(10^4-10^5)
generations), output decoding (reading appended data / halting signature
01101001101000), and sizing rules for left_periods/right_periods vs
simulation length.

## Long-run findings (first dynamic test, 2026-08-18)

Example {YN, NYYN, e, e}, tape NNYN, 30k generations, decoded every 100:

- Decoded front-of-tape progression NNYN -> NYN -> YN -> N matches the
  reference interpreter exactly.
- Ossifiers arrive every ~390 generations (364-cell spacing / relative
  speed 28/30) and transform the tape front; while one is crossing, reads
  are transiently unreadable (decoder raises on implausible pitch --
  correct behavior, sample later).
- One appendant cycle costs ~22.6k generations, dominated by the A^v
  ether gap (v = 754 here): the CTS "clock" is the ossifier supply.
- The endgame misbehaved (Y/YN flicker, no halt signature). Two causes
  suspected, in order of likelihood: (1) this CTS is NOT dynamically
  valid for the construction -- appendant YN has length 2, not a multiple
  of 6, and gets rejected at step 1, which the paper explicitly says the
  construction does not support; (2) cyclic-wrap corruption reaches the
  active zone near t~25k at this width. Both to be fixed: use conforming
  CTSs (lengths multiples of 6, or the paper's expansion transform) and
  larger margins.

Timescale estimate for later blowup accounting: one CTS symbol read
~= one ossifier ~= 390 generations; one appendant cycle ~= 22.6k
generations at this program size (v scales with program).

## Decoder fidelity limit (found with the all-Y grower test)

Observation: with appendant list {YYYYYY} and tape Y -- a program whose
tape can never contain an N -- the full-tape decoder still reports
transient N's behind the front (e.g. reads YYNYN persisting for ~1000
generations between ossifier passes).

Interpretation: a freshly appended symbol is not born as a finished E/F
block. Its gliders reach their final spacing through a sequence of
collisions, and intermediate spacings can exactly alias the other
symbol's core. Core matching is therefore only trustworthy for symbols
that have finished maturing -- in particular the front symbol, which the
machinery itself guarantees is mature by read time.

Consequence: end-to-end validation uses the consumed-symbol sequence
(front symbol at each ossifier consumption, extracted by consumed.py),
which fully determines the CTS computation. Full-tape reads remain as
diagnostics only.

## Program-validity constraints for the periodic left side (collected)

1. Every appendant length must be a multiple of 6 (else only if always
   appended).
2. The first appendant must be nonempty (no prepared-short-leader block).
3. The default v assumes >= 1 nonempty appendant appended per cycle;
   longer bounded rejection runs need larger v (v_override); unbounded
   rejection runs (e.g. the Wolfram p.96 CTS {YYYYYY,e,NNNNNN,e}, whose
   N-runs grow without bound) are impossible with a periodic left side.
   Our first canonical run confirmed this empirically: the machinery
   dismantled itself in a leader-ossifier cascade at t~89k.

## Blowup arithmetic and revised CA-level goals (2026-08-18)

Full-tape content decoding during maturation is unreliable (mixed run
{YYYYNN}: quiescent windows dominated by rejected reads; clean reads are
near-misses consistent with immature Y-symbols aliasing N). Content
decoding is hereby demoted to diagnostics.

Measured/derived scaling for the glider level:
- one CTS symbol read = one ossifier ~ 390 generations + v-gap share
- v =~ 80 * (total CTS appendant content) and one appendant cycle costs
  ~ v*30 generations at ~28*v cells of left-side width per period.
- TM-compiled programs (Cocke-Minsky): |Phi| = 4m+3ms; CTS appendant
  content ~ |Phi|^2 scale. For the 3-state test TM: v ~ 1.9M,
  ~10^10 generations per TM step. Physically out of reach -- the honesty
  clause bites ~10 orders of magnitude before Lisp.

Feasible glider-level deliverables instead:
1. Halting semantics: tiny halting CTS (e.g. {YYYYNN} from tape NN) must
   produce Cook's F-glider signature (spatial 01101001101000, temporal
   110101010111111); its non-halting twin must not. Decisive, no
   maturation issues.
2. De Mol's 3x+1 tag system {A->CY, C->A, Y->AAA} (deletion 2), which
   the paper singles out as directly implementable: its CTS satisfies
   the one-append-per-cycle validity condition with the DEFAULT v
   (~3400). One tag step ~ 310k generations at ~1M cells: real Collatz
   arithmetic by gliders, feasible with a bit-packed engine.
3. Maturation study (zoomed spacetime of an append) to close the decoder
   question honestly.

The Lisp tower above the CTS layer remains exact and differentially
tested at the symbolic layers; physical runs stop where the arithmetic
says they stop, with measured constants in the report.

## Collatz run #1 (De Mol x=3, T=1.35M): two findings

1. Read cadence: front symbols are consumed at t ~ 2.5k, 107k, 210k,
   315k, 417k, 522k -- ONE CTS read per left period (~104k generations),
   not one per ossifier. The four A^4s per period evidently split roles
   (ossify / accept / reject supply). All prior timing estimates were 4x
   optimistic; x=3 -> 5 (4 tag steps = 48 reads) needs ~5M generations
   and ~48 left periods.
2. Death at t ~ 565-592k: the tape erodes from the BACK over ~30k steps
   -- a destruction wave arriving from the right, killing the machinery
   long before wrap corruption could (>1.1M). Under diagnosis with a
   defect video. Prime suspects: the right-edge trim seam, or an error
   in my right-side sizing (appendant supply vs actual consumption
   pattern).

## The L-block (short leader) failure -- localized, parked (2026-08-18)

Controlled experiments, all with v_override = 3x default, T = 250k:

| program                          | empties | outcome            |
|----------------------------------|---------|--------------------|
| {YYYYNN}                         | 0       | healthy at 250k    |
| {YYYYNN, e}                      | 1       | dead by ~160k      |
| {YYYYNN, e, e}                   | 2       | dead by ~200k      |
| {YNNNNN, e} tape YN (minimal)    | 1       | dead by ~180k      |
| {YNNNNN, YNNNNN} tape YN control | 0       | healthy at 250k    |

Empty appendants (L blocks) are the specific killer; the De Mol and
Wolfram-p.96 deaths are both explained by their empties (the p.96 system
is additionally invalid for unbounded rejections).

Side-by-side event renders of the minimal pair localize the failure to
the moment read-1's acceptor reaches the raw short leader to prepare it
(the paper's figSketchesPQR(r) collision), t ~ 54k at the L cluster.
The static properties of my L data all check out: figure extraction
(0x00/0xFF/0x80 clean), (30,-8) periodicity, unique seam fits, zero
rule-110 violations across LL/JL/LK seams, and the 45-generation
evolution match covers L blocks too. The paper's note that raw short
leaders sit "up +3 higher, as measured through the E^n s, than the raw
regular leaders" names exactly the kind of long-range alignment that
pure jigsaw gluing cannot verify; either the L figure in the arXiv
source, my reading of it, or my phase chain is wrong in that measure.

Next steps if resumed: (a) implement the ovd/upd bookkeeping from Cook
2004 and check the L's up-distance mod 6 statically; (b) obtain a known-
good initial condition (e.g. Martinez's published Rule 110 CTS
simulations) and diff block placements.

## Corrected machinery model (replaces earlier note)

The whole assembly B A^13 B A^11 B A^12 B is ONE ossifier (the paper
says so explicitly); its four A^4 packets arrive ~390 steps apart and
perform one CTS read per left period (~30v generations). The earlier
"4 reads per period" and "1-of-4 ossifiers destroyed" readings were
windowing artifacts of the A4 detector (the tight group registers as
one crossing). With one read per period, x=3 Collatz needs ~5M
generations -- attainable once the L bug is fixed (De Mol needs L).

## Takeover review, 2026-09-30: how the machinery actually runs

Two wrong models, then a measured one.

1. The predecessor: "one CTS read per left period (~30v generations)".
2. My first review finding: reads happen at a fixed table rate, because
   table data streams past stationary tape data. Wrong: it assumed the
   tape sits in one place.
3. Measured with the glider census (census.py: ether-phase filtering,
   then typing each defect by the lattice shift that leaves it
   invariant: C (7,0), A (3,2), Ebar (30,-8)):
   - Each A^4 of an ossifier converts one moving-data character into one
     C glider of tape data. The first ossifier makes four C gliders, and
     the moving-data front advances from tape character 0 to character 4
     across it.
   - Tape characters are created at the current front of the Ebar
     stream, a new position each time. In the Ebar rest frame the stream
     (moving data, table data, leaders) is static and tape characters
     travel into it at 4/15 until they meet the next unread leader.
   - Reads are therefore gated by ossification: up to four per left
     period, then idle until the next ossifier. Tape data is absent most
     of the time; that is normal.
   - Reads are visible in typed renders: a short A-glider stroke heading
     right (acceptor or rejector) and, for rejections, a wedge of deleted
     components in the table stream.
   - Dynamic check ({YYYYNN} from YYYYNN, v = 3x default, `python
     experiments.py fronts`): the moving data an ossifier meets on
     arrival matches the "four characters per ossifier" accounting for
     arrivals 0-2 (9 of 9 symbols) and 4, 6; arrivals 3, 5, 7, 8 do not
     (arrival 3 meets what look like characters 15-17 instead of 12-14).
     Unresolved: a machinery fault, or an accounting that is too simple
     (decoder on young appended data, fewer characters per ossifier
     later)? The read cadence is therefore somewhere in 7.5v-30v.

Lesson: I wrote a firm finding from a back-of-envelope argument before
measuring, then retracted it too eagerly on the first confirming
picture. Mark such items "hypothesis" until measured, and measure the
quantity itself (characters per ossifier), not a proxy (a picture).

Tooling lesson (hit twice now): `pkill -f PATTERN` inside a compound
shell command matches that shell's own command line and kills it. Kill
by PID instead.

## Phase 3, item 1: the verification gap, closed (2026-09-30)

The v0.1.0 report said "four characters per ossifier" and showed a
`fronts` table with mismatches from arrival 3 on. Both were artifacts:

1. The moving-data decoder is phase-dependent. After the reads of the
   first cycle, the moving data sits static in the Ebar frame, yet its
   decoded string repeats with the sampling time mod 30: t = 0 mod 30
   gives YYYNN YYYYNN, t = 10 gives NNYNN YYYYN, t = 20 is rejected.
   The cores themselves are unambiguous (60 distinct, none contained in
   the other symbol's rows); the aliasing comes from context (cores span
   parts of neighbouring characters, and acceptor-made moving data sits
   in different surroundings than the initial tape). The "front advanced
   by four characters" observation was one of these misreads.
2. Counting C-glider births per ossifier over 490k generations: every
   ossifier produces one burst of 4 C gliders. With (1), the correct
   reading is: 4 C gliders = ONE tape character (one per A^4 of the
   ossifier), not four characters.
3. Decoder-free check (experiments.py reads): observe each read's
   outcome as what the acceptor/rejector sweep leaves in that appendant's
   component region (Y: Ebars remain, ~55 -> ~24 clusters; N: region
   becomes ether). Reads happen at t ~ 9.0k, 67.2k, 124.8k, 183.0k,
   240.6k, 299.4k, 356.4k: one per ossifier period (48.8k) plus one
   appendant traversal (~9.2k), because each character is delivered at
   about the same place in the Ebar frame and must travel one appendant
   further than the previous one. Outcomes: Y Y Y Y N N Y ... = the
   reference.

So the predecessor's "one read per left period" was right up to the
travel term, and the ~30v generations per read (3.6e20 for the capstone)
stands. My release notes' "four per ossifier" was wrong.

Lesson (third time on this topic): a decoder that has not itself been
validated is a hypothesis, not an instrument. The census-based,
decoder-free observable settled in one run what three decoder-based
analyses had muddled.

Result (experiments.py reads 12, v = 3x default): observed
YYYYNNYYYYNN = reference, 12/12, reads every ~58k generations. Reads
6-11 consume characters appended during the run, so reading, accepting,
rejecting, appending and ossifying are all exercised. A first version of
the check misclassified two reads: a reject sweep takes ~5k generations
and the sweeping rejector is not always typed A or ?, so "nothing moving
inside" fired mid-sweep. The check now also requires the region to be
unchanged between two consecutive samples.

At Cook's default spacing (v = 524) the same program matches 10/10 with
a read every ~26.4k generations (30v + one appendant traversal).

## Phase 3, item 2: the short leader (2026-09-30)

Decoder-free L table (experiments.py lblock, read_outcomes, v = 3x):
- variant 4 (control, {YNNNNN, YNNNNN}, tape YN): YNYNNN = reference
  for all 6 reads that settled by 541k. Note the cadence: ~107k per
  read, i.e. two ossifier periods, not one as for {YYYYNN}. Unexplained.
- variant 3 ({YNNNNN, e}, tape YN): read 0 correct; "read 2" fires at
  121k, only ~10k after the short leader's read, and leaves 3-4 Ebar
  clusters (a real Y read leaves ~24); "read 4" leaves 55 (= untouched
  components, so the region was disturbed, not read). Broken from the
  short-leader read on.
- variant 1 ({YYYYNN, e}): the same signature (read 2 at 124.8k with 3
  clusters, read 4 with 55).

Hypothesis tested: the L block is misplaced (paper: raw short leaders sit
"+3 up" relative to raw regular leaders, which jigsaw gluing cannot see).
- Family A: shift only L's first cluster by ether-lattice vectors
  (7a+3b, 2b), b in -2..1, a in -6..6 (51 shifts, both Z2 classes of
  the Ebar-lattice quotient over the range): none gives the reference
  even reads YYNN; 30 give YYYY, the rest assorted.
- Family B: shift L and everything to its right, cumulatively per L:
  11 of 52 shifts run, none clean. Stopped (below).
Conclusion: a rigid placement error of L is unlikely to be the cause, at
least within small lattice shifts. Other candidates (not tested): the L
figure's content itself (it shares its first ~115-148 cells with K, as
the paper says it should, so a defect would sit in the rest), or the
prepared-leader alignment k after a short leader.

Workaround adopted instead: remove L from the construction. Replace each
empty appendant by N^m, m = lcm(#appendants, 6) (cts.fill_empty_
appendants). Exact at the CTS level: junk N's are read only as N (never
append), and they delay later symbols by a multiple of the appendant
cycle, so every later symbol meets the same appendant. Tested by
comparing (appendant index, symbol) read traces with junk reads removed
(test_tag.py; a wrong m = 6 for De Mol's p = 12 fails the test). Note
that TS-step boundaries no longer coincide with CTS cycle boundaries
(junk can start mid-cycle), so decoding the tag tape at cycle
boundaries is the wrong check; my first test did that and failed.
Cost: each Y read on a formerly empty appendant adds m N reads; v grows
by ~80m per filled appendant (De Mol: v 3,427 -> ~12,200).

## Phase 3, items 3-4 (2026-09-30)

Item 3, spacing. Uniform-v sweeps with the decoder-free check:
- {YYYYNN} (Cook v 524): 523-528 all 10/10; 262, 196, 160, 131, 30 fail.
  At low v even read 0's region is damaged: 13, 6, 3, 2 clusters at
  v = 262, 196, 160, 131 (24 when correct), i.e. damage grows with
  ossifier density. Render (scratchpad vrender262.png): tape characters
  arrive faster than the table is consumed; some sit stranded in the
  ether gap a rejection leaves. Mechanism not pinned down.
- {YYYYNN, NNNNNN} (Cook v 1,064) at v = 532: 10/10, ~27k per read.
- {YYYYNN, N^6 x3} (Cook v 2,144) at v = 532: 12/12, ~27k per read.
So the needed spacing follows one appendant, not the table. A uniform v
sized for the largest appendant may capture most of the demand-timing
gain; non-uniform schedules matter only for very unequal appendants.
Open: scaling with appendant length (read 0 of De Mol's 12-symbol
appendant left 48 clusters = 4/symbol, so the check generalizes).

Item 4, direct binary clockwise construction (cw.two_way_to_binary_cw).
Measured why binarize() never finished on SKI: its state is (symbolic
state incl. buffered cell, input prefix, pending code of the previous
buffered cell): 345,523 (state, output) pairs x 64 prefixes ~ 22M.
New design: cell = w data bits + mark bit LAST; state = (q, mark_next,
prev_is_E, pending output bits, bits of current cell), with pending +
current = w+1 bits in steady state; insertions at either tape end drain
via 2-bit writes. Mark-last is the key: when the head cell completes,
the previous cell's mark bit is the one pending bit, so a left move can
still set it. Results: capstone 66 states (130 before), SKI 119,347
states in 1.5 s, SKI terms normalize correctly, capstone passes the full
NW + CTS chain. First harness "mismatch" was my de-duplication on
(state, symbol) merging repeated identical visits; the run was right.
Cost table (experiments.py cost) reproduces the v0.1.0 numbers exactly
for the old path; direct path ~5e19 vs 3.6e20 generations.

## Phase 3, item 5 (engine), and more on item 3 (2026-09-30)

Item 3 scaling: {(YYYYNN)^3} (18 symbols, Cook v 1,452): v = 532 gives
1/8, v = 1,000 gives 8/8 (72 clusters per accepted region = 4/symbol,
so the check generalizes to long appendants). Needed v grows with
appendant length: 6 symbols (262, 523], 18 symbols (532, 1000].
Extrapolated to the capstone (direct construction): v <= 1.7e6 instead
of 2.9e9, total ~2.9e16 instead of 5e19. Computed, not guessed: my first
draft used rule length 3; the real longest tag rule is 7.

Item 5: casim.StreamRun instead of HashLife first (DIRECTIONS 2.3 lists
it as the simpler alternative). Exactness argument: wrap garbage and
real activity each spread <= 1 cell/step; re-seat every 256 steps with
margin 2*256+64+64; check zones must equal the free evolution or it
raises. Verified: 30 checkpoints to t = 60k plus +-3,000 cells of the
free fill, cell for cell (scratchpad stream_check.py), and tests/
test_casim.py. Speed work found two hotspots by profiling: assemble()
re-solved identical seam fits (now cached per (blocks, side, phase),
rows bit-identical on three assemblies) and np.roll overhead in
step_packed (23 us/step on small arrays, was ~93). The read check now
watches only the next 4 pending regions (reads are sequential).
De Mol filled, v = 1600: reads 0-9 in ~80 s on StreamRun vs ~1 h on the
full array, with identical read times on both (independent cross-check).

De Mol x=3, filled, v = 1,600 (Cook 12,216), StreamRun: reads 0-28 all
correct (29/29), including the first 18-symbol accept (read 26, 72
clusters) and junk accepts (48). Then read 29 comes 169k generations
after read 28 (normal ~70k), read 30 settles with 112 clusters ('!'),
and everything after is broken. The reference has 16 consecutive N reads
at 27-42. Hypothesis "moving data runs dry" is refuted: the reference
queue holds ~55 characters there. Discriminating runs: same program at
v = 12,216 (Cook) and v = 3,200, 48 reads each (scratchpad
demol_v12216.out, demol_v3200.out).
HashLife (item 5): exact vs full run and vs StreamRun (1M generations,
94k cells); ~2x faster than StreamRun on {YYYYNN}, memo grows ~0.85
results per generation (little repetition when the tape grows). My
first HashLife test compared inside the cyclic Run's seam light cone at
t=6000 and failed; the reference was wrong there. I also committed that
failing test because `pytest | tail` hid the exit code: run pytest
without a pipe before committing (standing rule 3).

De Mol at v = 3,200 (StreamRun, ~11 min for 9.3M generations): reads
0-82 all match the reference (checked from the log against cts.run), so
the tag tape passed AAAAA (Collatz 5, read 72). Read 83 (5th of a 17-N
run) settles with 114 clusters ('!') after a 1.5M-generation delay. The
earlier 16-N run (27-42) passed at this v, so rejection-run length alone
does not explain it; accumulating drift is a candidate, untested. Now
running v = 6,400 to 560 reads.
scholar finished (report on BOARD.md and noncts/scholar/NOTES.md; the
harness would not let it create FINDINGS.md, and its findings F1-F20 are
in its NOTES.md).

v = 6,400: reads 0-82 correct again, read 83 malformed again with 114
clusters (113 at 3,200). The read-83 failure is independent of spacing;
my "accumulating drift" and "spacing too small" guesses for it are
refuted. A HashLife-driven check (engine="hash", an independent engine)
was too slow and memory-hungry (7 reads in 10 min, 3.2 GB: one-step
census sampling defeats memoization) and was stopped. Running Cook's
v = 12,216 to read 85 on StreamRun to see if the construction itself
fails there.

Cook's v = 12,216: 86/86 correct, read 83 included (1,916 s). So the
read-83 failure IS a spacing failure, with a threshold between 6,400 and
12,216. Lesson: two spacings giving the same failure do not show that
spacing is irrelevant; I retracted too fast. Running Cook's v to read
556 (Collatz 1 at 552).

De Mol at Cook's v = 12,216, run 1: reads 0-204 all correct (205/205,
through Collatz 8 at read 204, 7.7e7 generations, ~2 h), then the
container was reclaimed while the session was idle and the process died
without error. Log kept as scratchpad demol_cook_full_run1.out. Run 2
restarted 09:45 UTC with 30-minute check-ins so the session stays active.
Lesson: long runs need either an active session or checkpoints.

StreamRun window growth (De Mol, Cook's v): 519k cells at t=34M. Two
causes. (1) An artifact: the right side's free row overwrote the left
side's where they overlap, and beyond the table's end the left row was
used where neither is true. Fixed with a split at the window centre
(left row to the left, right row to the right, no fallback); validated
cell for cell against the full run to 200k generations, and the rerun
reproduces run 1's read times and cluster counts exactly. (2) Real: the
census of the window's leftmost 200k cells at t=28M finds 100 Ebar
clusters among the ossifier train's A's. Cook's machine leaves a
permanent stream of left-moving Ebars that later ossifiers must cross,
so the active region really grows ~linearly with t and run time
~quadratically. Keeping it exact means simulating them; HashLife would
compress that regular region but is too slow with census sampling.
Run 3 (killed for the fix): 94 reads correct before the restart.

DONE: De Mol x=3 at Cook's v = 12,216, 556/556 reads correct, Collatz
3 -> 5 -> 8 -> 4 -> 2 -> 1 (1 at read 552, generation ~2.07e8), 13,919 s
of compute across one checkpoint resume. Reads 0-204 agree with the
earlier run 1 in time and cluster count. Moved the driver into
experiments.py (collatz subcommand, checkpointed).

## Phase 7: HashLife for long runs (2026-10-03)

Measurements (scripts in the session scratchpad, numbers here):

- HashRun advanced in 2^20-2^24 jumps runs the whole Collatz configuration
  (v = 12,216, 2.1e8 generations, no sampling) in ~135 s; nodes grow about
  linearly in t (1.4e7 at the end). The old "~2x StreamRun" figure in
  REPORT 5 came from sampling every 600 generations.
- Cost follows events, not generations: ~50 Collatz reads cost 6-7 s at
  v = 12,216, 24,432 and 48,864 alike (generations x4).
- Sparse layout (casim.layout): the left side is ether plus ossifier
  segments; A runs are placed in closed form (A attached to A keeps
  dy mod 3; each A row is 28 cells of ether). Equal to padded_row cell for
  cell on five configurations (tests/test_casim.py).
- read_outcomes_hash (since superseded by epochrun.EpochReads, which
  keeps its sampling rule): samples only near reads, jumps in between (the next
  read is predicted from the previous two starts). Full Collatz 556/556,
  every read's outcome and Ebar-cluster count identical to
  data/collatz_v12216.log, in 340 s (StreamRun: 13,919 s); the committed
  version (watching 2 regions) took 441 s. Peak memory 11 GB (2.9e7
  nodes at ~380 bytes): memory, not time, was then the limit. With the
  epoch engine and the C core (below), `python experiments.py
  collatz-hash` takes ~40 s at 0.3 GB; log in data/collatz_v12216_hash.log.
- Read start times differ from the StreamRun log by up to ~3 samples:
  when the prediction is late the read is caught already under way.
  Outcomes and counts do not depend on this.

Compiled Turing machines (Cocke-Minsky, filled CTS), measured sizes:

| TM (tests/machines.py) | visits | table symbols | Cook v | filled CTS reads to halt |
|---|---|---|---|---|
| three_state, right=[1,2] | 5 | 40,752 | 3.27e6 | 212,736 |
| three_state, right=[2] | 4 | 40,752 | 3.27e6 | 59,136 |
| 2 states, 2 symbols, one R move | 2 | 21,888 | 1.76e6 | 16,704 |
| 2 states, 1 symbol, one R move | 2 | 8,700 | 7.0e5 | 5,760 |

The fill rewrite roughly triples the reads (REPORT 4's 9.6e4 was the
unfilled count).

TM pilot (three_state, right=[1,2], v = 3,270,732): the first 20 reads
match the reference CTS (YNNN...). Cost per read in steady state:
- whole table in the tree (3 periods, 5.7e7 cells): ~6 s per read;
  9 periods: ~10 s. Per-read cost grows with the table held in the tree,
  because each advance moves the whole table to a new alignment and
  HashLife cannot reuse those nodes.
- table cut after the next 14 appendants: ~1.6 s per read, ~1.8e5 new
  nodes per read (so ~70 MB per read without collection).
- of a sample's cost, the census was 60% before vectorizing (census() now
  types all clusters with prefix sums; identical output, test added) and
  stepping the whole root for the sample's small steps most of the rest.

Consequence (design of the next engine step, PLAN 7.1): rebuild the tree
in epochs. Each epoch carries the active region over from the old tree
(aligned subtrees, found by comparing against free evolution), adds only
the next few appendants and ossifiers from the sparse layout (shifted to
the epoch's time: left by (3,2), right by (30,-8); every ether phase
constant becomes c + 4t), and clears the memo tables. Samples step a small
local subtree (exact by light cone), never the root.

### Epoch engine and C core (2026-10-03, later)

- epochrun.EpochReads: the tree is rebuilt every 8 reads from (a) the
  active region, carried as 2^16-cell blocks on a global grid, (b) the
  next ossifiers and (c) the next appendants, both from the sparse layout
  translated to the epoch's time. Memo tables are cleared at each
  rebuild: ~15k nodes after a rebuild, 0.5 GB peak for the TM pilot.
  Exactness: tests/test_casim.py compares the epoch run's row with a full
  run on the active region after three rebuilds; Collatz reads 0-119
  match data/collatz_v12216.log outcome for outcome and cluster count for
  cluster count.
- Mistake found while building it: HashRun's ether constants are t = 0
  constants, but the rebuilt tree was first given the shifted layouts'
  time-t constants, so the ether added on expansion had the wrong phase;
  the next epoch's active region then spanned the whole tree (16M
  cells). Fixed (rebuild subtracts 4t).
- What the active region holds (one-move TM, read 96): 3,691 Ebar
  clusters and 4 C (tape) gliders over 4.5e6 cells; most of the Ebars are
  junk at its left end. Junk is permanent in Cook's machine and every
  later ossifier crosses all of it, so the cost per read grows with the
  number of reads so far (quadratic total). Python core: 1.6 s/read at
  read 96, 2.1 s at 192.
- hlc.c: the HashLife core in C (ctypes), same algorithm and API, node
  ids instead of objects. With census labels vectorized, 200 TM reads
  take 41 s (Python core: ~255 s). The remaining time is census and
  local history (numpy) as much as HashLife itself.
- Right side beyond one super-period: placing a period changes the
  blocks' row phase dy by a fixed amount mod 30, so the t=0 row repeats
  after m = 30 / gcd periods (m = 15 for {YYYYNN}, 1 for De Mol); the
  layout tiles shared copies of one super-period (checked cell for cell
  against the direct assembly, and the read regions likewise).

### One-move TM at Cook's v: a construction failure at read 3,269

Run: `experiments.py tm-gliders one` (one_move_tm, Cook's v = 701,044,
5,970 reads planned). Reads 0-3,268 equal the reference: 3,269 reads,
including all 55 accepts, each accept leaving 4 Ebar clusters per symbol
within +-1, and the TM's first visit (read 720). Then:
- read 3,269 came ~6e7 generations late (three read intervals) and
  reads 3,269-3,272 all within 3.4e6 generations; 3,270 and 3,272 came
  out '!'.
- In the checkpoint at read 3,272, an unread appendant region holds ~846
  Ebar clusters; region 3,270's "843 clusters" is such an unread region
  after a brief disturbance (the check took it for a read). Tape C
  gliders sit inside the regions being read: the table has slid over
  tape characters without reading them.
- Afterwards the tree grew to 12.8 GB and the run died (out of memory):
  debris spreading.
- Reference CTS there: tape ~3,300 symbols (not dry); read 3,269 is the
  197th of a 209-read rejection run; earlier runs of 215 and 216 passed.
- Read times show no slow drift before it: residuals of a linear fit
  stay within +-1e7 and are near 0 around read 3,100; the jump is abrupt.

Engine or construction? Two variants:
- same v, epoch 5 instead of 8, samples 2^16 instead of 2^17: the same
  failure at the same generation (read 3,270 settles at
  t~69,236,293,080 with 843 clusters in both). Truncation and sampling
  choices differ, the result does not: not an epoch artifact.
- 2 x Cook's v: reads 3,269-3,282 correct (3,282 an accept with 360
  clusters).
So it is the construction at Cook's spacing, as with De Mol below half
of Cook's v (REPORT 3.6), and consistent with the encoder's caveat that
Cook's formula assumes a nonempty append in every appendant cycle; the
filled program's rejection runs are ~200 reads. The mechanism is not
identified yet (diagnosis run stopped at read 3,265 to render it).
Full runs at 2x and 4x Cook's v are going.
