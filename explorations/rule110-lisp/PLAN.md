# Plan

## Phase 4: documentation pass, non-CTS team round 2 (started 2026-09-30)

User: make sure documentation is complete, push, then supervise another
round of agents on a non-CTS machine.
- [x] Documentation pass: README (modules, commands, status), REPORT
      (engines section 5, non-CTS section 6, next steps 7, summary),
      DIRECTIONS (status per option), CHANGELOG, PLAN
- [x] Push
- [x] Round 2: brief from round-1 results (noncts/SUMMARY.md), agents
      launched, board supervised, results verified and summarized
  - [x] noncts/round2/ (README with milestones M1-M3, BOARD kickoff with
        the verified frontier and round-1 rules)
  - [x] agents launched: gate (zero answers act on the stream), address
        (two registers), queue (queue automaton with finite control),
        verify (independent verification, theory, integration)
  - [x] supervise, verify key claims myself (lead/), write round-2 summary
  - Outcome: M1, M2 reached and cross-verified; M3 not reached (noncts/round2/SUMMARY.md)

## Phase 3: extension (started 2026-09-30)

User chose: pursue DIRECTIONS.md in order, and run a 4-agent team on a
non-CTS Rule 110 computer (noncts/, board in noncts/BOARD.md).

- [x] 1. Close the dynamic-verification gap: decoder was phase-dependent; decoder-free read check matches 12/12 (NOTES)

- [x] 2. L-block (short leader) defect: sidestepped by exact rewrite (fill); L itself unexplained
  - [x] decoder-free L table (experiments.py lblock uses read_outcomes)
  - [x] family A: shift only the first L cluster by ether-lattice vectors
        (51 shifts): none reads correctly
  - [x] family B: shift L and everything right of it (11/52 run, none clean; stopped)
  - [x] workaround: cts.fill_empty_appendants; filled variants 3 and 1 read 12/12 at default v
  - [ ] (open) cause of the L failure
- [x] 2b. Correct v0.1.0 docs to 1 char per ossifier / 30v (REPORT, REVIEW, DIRECTIONS, CHANGELOG)
- [ ] 3. Demand-timed ossifiers (encoder option + scheduler + verification)
  - [x] uniform-v sweeps: 1-app min in (262, 523]; 2-app at v/2 10/10; 4-app at v/4 12/12
  - [x] De Mol filled at v=1600 (7.6x below default): reads 0-11 correct (full-width run)
  - [x] scaling: 18-symbol appendant needs 532 < v <= 1000; 6-symbol 262 < v <= 523
  - [x] De Mol x=3: 83/83 through Collatz 3 -> 5 at v=3200; fails at read 83
  - [x] De Mol to Collatz 1: 556/556 at Cook's v (v=6400 fails at read 83)
- [x] 4. Direct binary clockwise SKI machine (skip conversion/binarization)
  - measured: SKI clockwise machine 10,897 states / 43 symbols / 395,550
    transitions; binarize() carries (new state, written symbol) = 345,523
    pairs x 2^6 input prefixes ~ 22M states. That is why it never finishes.
  - design: binary cells [mark bit][w data bits]; the one-cell delay needed
    for left moves becomes a (w+1)-bit shift register in the state:
    (q, last w+1 bits, phase) <= 256 x 2^6 x 6 ~ 98k states, no symbolic
    buffer. Build directly from the two-way TM; verify against tm.TM.
  - [x] done: cw.two_way_to_binary_cw; SKI 119,347 states (1.5 s); capstone 66 vs 130
- [ ] 5. 1-D HashLife engine, measured on the above
  - [x] first: streaming window (casim.StreamRun), exact, verified vs full run; ~40x on De Mol
  - [ ] HashLife: decide after measuring where StreamRun's time goes
- [x] 6. Team results: all four agents finished; no non-CTS computer; building blocks and missing gadgets in noncts/SUMMARY.md

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
