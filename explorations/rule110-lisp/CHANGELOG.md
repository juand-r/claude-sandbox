# Changelog

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
