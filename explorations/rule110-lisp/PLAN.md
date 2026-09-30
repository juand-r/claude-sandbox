# Plan

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
      superseded diagnostics to trash/ (E2)
- [ ] 5. SKI-TM gap walking (D1): measure, fix, re-measure
- [ ] 6. NW reachability pruning (D2): re-measure blowup table
- [ ] 7. Glider census (C1): lattice-invariance classifier, tests on
      known gliders; use it to measure real read/ossification cadence
- [ ] 8. Rewrite REPORT.md claims per B1-B4 with the new measurements
- [ ] 9. Tag `rule110-lisp-v0.1.0` with release notes
- [ ] 10. Extension proposal (faster / more direct): write it up, ask
      before starting

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
