# Notes

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
