# Plan

## Phase 7: long exact runs with HashLife; a compiled Turing machine on gliders (started 2026-10-03)

User: "take charge, no more agents". Lead's decision: return to the main
project's first open item (REPORT section 7). Non-CTS work pauses: its open
routes need either a new idea or agent-scale SAT compute.

Starting measurements (scratchpad, 2026-10-03):
- HashRun advanced in 2^20-2^24 jumps runs the whole Collatz configuration
  (v = 12216, 2.1e8 generations) in ~135 s, against 3.9 h for StreamRun.
  The old "~2x StreamRun" figure came from sampling every few hundred steps.
- Cost is independent of v: ~50 reads take 6-7 s at v = 12216, 24432, 48864
  (generations x4). So cost follows events (reads), not generations.
- Target machine: tests/machines.py three_state_tm, short config
  (right = [1, 2]): 5 TM steps, 373 tag steps, 192 CTS appendants (153
  empty, filled), 40,752 table symbols, Cook v = 3.27e6, ~71,600 CTS reads,
  ~7e12 generations. Plain HashRun cannot hold it: the initial row alone
  would be ~6.5e12 cells (left side) plus ~7e9 (table).

Steps:
- [x] 1. Engine: HashLife without a materialized row
  - [x] a. sparse left side: ether plus ossifier chunks, exact positions and
        ether phases computed from the block lattice (no per-A-block work)
  - [x] b. right side: only the next appendants in the tree (epochs);
        long tables as a repeated super-period
  - [x] c. read check with sparse sampling: census history by stepping an
        extracted window locally (exact by light cone), not the root
  - [x] d. bounded memory: memo tables cleared at each epoch rebuild
  - [x] e. validation: Collatz 556/556, every outcome and cluster count
        identical to data/collatz_v12216.log (read times differ only by
        the sampling; an independent full-length cross-check of REPORT 3.6)
  - [x] f. epoch engine (NOTES Phase 7): bounded tree content and memory
  - [x] g. C core (hlc.c): ~4x on the TM runs
- [x] 2. Pilot: TM reads 0-19 correct; ~6 s/read with the table in the
      tree, ~1.6 s with it cut: full run needs the epoch engine (1f).
      Fill triples the reads (212,736 to halt); smaller machines sized
      in NOTES. First target: the 2-state machine (5,760 reads).
- [x] 3. Full TM run: one_move_tm at 2x Cook's v, 5,970/5,970 reads,
      visits decoded; at Cook's v it fails at read 3,269 (NOTES)
  - [x] the 4x run (confirmation): 5,970/5,970, visits decoded
  - [ ] (open) mechanism of the Cook's-v failure
  - [ ] (out of reach for now) three_state_tm right=[2]: 59,136 reads,
        ~100x the cost (junk crossings are quadratic)
- [x] 4. Report: REPORT 3.7 / 5 / 7, README, CHANGELOG, DIRECTIONS

## Phase 6: non-CTS team round 4, every remaining avenue (started 2026-10-01)

User: launch new agents exploring every avenue, orchestrated by the lead.
noncts/round4/ (README with the avenues, BOARD kickoff and rules).
- [x] six agents: delayline (gap/distance memory), shuttle (wide and
      multi-step shuttles), objects (other storage objects, crossings),
      queue (queue machines with finite control), theory (route map,
      no-go loopholes, models), verify (independent checks, integration)
- [x] supervise: board watch, redirect on results, spot-checks, summary
- Outcome: no universal machine; route map and scoped negatives (noncts/round4/SUMMARY.md)

## Phase 5: non-CTS team round 3, two program streams (started 2026-10-01)

User approved the two-stream idea. noncts/round3/ (README with tiers
T1-T3, BOARD kickoff with starting facts).
- [x] agents launched: theory (two-stream abstract machines, minimal
      universal coupling, reaction spec), leftstream (left stream on its
      own counter), coupler (signals between the counters), verify
      (independent verification, integration, instruments)
- [x] supervise, spot-check key claims (round3/lead/), write round-3 summary
- Outcome: T1, T2 reached and verified; T3 not reached (noncts/round3/SUMMARY.md)

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
