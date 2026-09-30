# Changelog

## v0.1.1 (unreleased)

Corrections to v0.1.0
- Withdrawn: "each ossifier converts four characters" and the `fronts`
  table with its 4-of-6 mismatches. Both came from the moving-data
  decoder, which is phase-dependent (its output changes with t mod 30
  on static data). Measured instead: one ossifier = one burst of four C
  gliders = one tape character; one read per ossifier period.
- Cost estimate back to ~30v generations per read (capstone ~3.6e20);
  the 7.5v-30v range is withdrawn.

Verified
- Dynamic correctness on gliders for `{YYYYNN}`: a decoder-free check
  (experiments.py reads) matches the reference CTS 12/12 at 3x Cook's
  ossifier spacing and 10/10 at the default spacing, including reads of
  characters appended during the run.
- Uniform ossifier spacing: for `{YYYYNN}` v = 523-528 correct, v <= 262
  fails; for 2- and 4-appendant programs 1/2 and 1/4 of Cook's v read
  correctly (10/10, 12/12), at the one-appendant cadence.
- Empty appendants: cts.fill_empty_appendants rewrites them exactly as
  junk N-words one appendant-cycle long, so the failing short-leader
  block L is never used. The minimal program that L broke reads 12/12.
- cw.two_way_to_binary_cw: direct binary clockwise construction. SKI
  machine 119,347 states in 1.5 s (old path: ~22M states, never
  finished) and still normalizes SKI terms; capstone 66 states instead
  of 130, ~7x fewer generations (experiments.py cost).

- Needed spacing grows with appendant length (6 symbols: 262-523; 18
  symbols: 532-1,000), not with table size.
- casim.StreamRun: exact streaming-window simulator (steps only where the
  state differs from the assembly's free evolution); matches the full
  run cell for cell. With faster seam fitting and stepping, De Mol's
  first 10 reads take ~80 s instead of ~1 h.

- De Mol's 3x+1 system, x = 3, on gliders: 83/83 reads correct through
  the first Collatz step 3 -> 5 at v = 3,200 and 6,400 (Cook: 12,216).
  Read 83 fails identically at both, so that failure is not spacing;
  cause open. At v = 1,600 it fails at read 29, a spacing failure during
  a 16-rejection run.
- hashlife.py: exact 1-D HashLife; ~2x StreamRun on growing-tape runs.

Changes
- encoder.assemble(left_gaps=...): explicit ossifier schedule.
- experiments.py: `reads`, `cost`; `lblock` decoder-free, with `fill`.
- read check flags regions that settle with an unexpected Ebar count
  ('!') instead of calling them Y.
- Tests: fill exactness, edge growth, direct binary tower and SKI (49).

## v0.1.0 (2026-09-30)

Tag: `rule110-lisp-v0.1.0`

A Lisp whose execution bottoms out in Rule 110:
mini-Lisp -> SKI -> Turing machine -> clockwise binary TM -> 2-tag
(Neary-Woods) -> cyclic tag system -> Rule 110 (Cook's glider blocks).
Details and evidence: explorations/rule110-lisp/REPORT.md.

Verified
- Every layer against its reference interpreter; composition tested on
  a 3-state TM down to the CTS, and on the Lisp-running SKI machine
  through the clockwise conversion (10,897 states).
- Lisp on a 256-state TM: (car (quote (a b))) -> a in 85.9M steps.
- Cook's initial conditions exact: 1,152,891 cells over 45 generations.

Changes since the phase-1 state
- Fixed: compiled atom? was false for nil; reference eq? was structural
  on lists (both now McCarthy LISP 1.5).
- SKI TM: counter kept beside the live term, 4-7x fewer steps.
- New: glider census (census.py) typing gliders by lattice invariance;
  used to measure the ossifier/read mechanism.
- Refactor: one tag-system runner, shared experiment helper (casim.py,
  experiments.py), dead code and junk files removed. 44 tests.
- Report rewritten; overclaims about long-run dynamics withdrawn.

Known open problems
- Long-run correctness on gliders unverified: 9 of 9 checked symbols
  match for the first three ossifier arrivals, 4 of the next 6 arrivals
  do not match the simple accounting.
- Empty appendants (Cook's short-leader block L) lose the moving data;
  no tag-compiled program runs on gliders yet.
- Binarizing the SKI machine's clockwise form does not finish.

Next: DIRECTIONS.md (demand-timed ossifiers, smaller tag alphabets,
1-D HashLife).
