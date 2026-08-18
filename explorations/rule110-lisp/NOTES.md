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
