# Plan

## Phase 3: extension (started 2026-09-30)

User chose: pursue DIRECTIONS.md in order, and run a 4-agent team on a
non-CTS Rule 110 computer (noncts/, board in noncts/BOARD.md).

- [x] 1. Close the dynamic-verification gap: decoder was phase-dependent; decoder-free read check matches 12/12 (NOTES)

- [ ] 2. L-block (short leader) defect
  - [x] decoder-free L table (experiments.py lblock uses read_outcomes)
  - [x] family A: shift only the first L cluster by ether-lattice vectors
        (51 shifts): none reads correctly
  - [ ] family B: shift L and everything right of it, cumulatively
  - [ ] if B fails: census render of the short-leader read (debris source)
- [x] 2b. Correct v0.1.0 docs to 1 char per ossifier / 30v (REPORT, REVIEW, DIRECTIONS, CHANGELOG)
- [ ] 3. Demand-timed ossifiers (encoder option + scheduler + verification)
- [ ] 4. Direct binary clockwise SKI machine (skip conversion/binarization)
- [ ] 5. 1-D HashLife engine, measured on the above
- [ ] 6. Team results: review, verify, integrate, report

## Phase 2: takeover, cleanup, release v0.1.0 (started 2026-09-30)

Request: review, refactor and document; build on it; tag a release when in
good shape; then extend toward faster / more direct constructions.
Findings and their status live in REVIEW.md (ids referenced below).

Order of work (each step committed separately):
- [x] 1. Repo hygiene: untrack pyc/out (E1); trash `consumed.py` (E4)
- [x] 2. Semantic bugs A1-A3 with new edge-case tests
- [x] 3. Refactor: single tag runner (E3), CWTM into cw.py (E9), dead code
      and docstrings (E5, E6), magic numbers (E7), shared test machine (E8)
- [x] 4. Experiments: shared CA-run helper, scripts to experiments/,
      experiments.py + casim.py; superseded scripts to trash/ (E2)
- [x] 5. SKI-TM gap walking (D1): 4-7x fewer steps, same results
- [x] 6. NW reachability pruning (D2): refuted by measurement (0 symbols removed); real lever is binarization, deferred
- [x] 7. Glider census (C1): census.py + tests; measured the mechanism; dynamic check partial (REPORT 3.3)
- [x] 8. Rewrite REPORT.md claims per B1-B4 with the new measurements
- [x] 9. Tag `rule110-lisp-v0.1.0` with release notes
- [x] 10. Extension proposal (faster / more direct): DIRECTIONS.md

---

# Phase 1 plan (original, completed 2026-08-18)
Agreed scope (2026-08-18): full Cook-style construction, Lisp front end,
Python, Neary-Woods polynomial route. Honesty clause: if full Lisp eval
at glider level exceeds available compute, the deliverable is the
complete verified pipeline + real glider-level runs of cyclic tag
programs + measured blowup factors per layer.

Status: tower complete and tested end-to-end (see REPORT.md).

## Layer 0 - Rule 110 engine
- [x] Vectorized simulator (numpy), cyclic boundary
- [x] Bit-packed uint64 engine, 39x faster, cross-checked
- [x] Ether background verified; spacetime rendering

## Layer 1 - CTS -> gliders (Cook 2009)
- [x] Block catalog extracted from the paper's figures
- [x] Seam-matching assembly; local exactness verified (1.15M cells)
- [x] Decoder (mature-symbol core matching, block-extent aliasing fix)
- [x] Dynamic validation on empty-appendant-free programs
- [ ] BLOCKED: short-leader (L) block self-destroys at its preparation
      collision -> all TS-compiled programs unrunnable physically.
      Localized (see NOTES.md); fix would unlock De Mol 3x+1 on gliders.

## Layer 2 - machines -> CTS
- [x] CTS reference interpreter
- [x] Tag-system layer; TS -> CTS (Chapman + De Mol 3x+1 verified)
- [x] TM -> TS (Cocke-Minsky, exponential; test path only)
- [x] Two-way TM -> clockwise TM -> binary clockwise TM
- [x] Neary-Woods 2-tag from clockwise binary TM (stage tables)
- [x] Capstone: full tower on a 3-state TM, exact at every level

## Layer 3 - Lisp
- [x] Mini-Lisp spec + reference interpreter
- [x] Lisp -> SKI compiler; SKI string engine (spec) + graph engine
- [x] SKI Turing machine (255 states): Lisp runs on a TM
      ((car (quote (a b))) -> a, 5.9e8 steps)

## Reporting
- [x] REPORT.md with measured blowup table and defect analysis
