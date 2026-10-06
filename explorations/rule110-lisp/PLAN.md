# Plan

## Phase 9: next improvements (started 2026-10-05)

To-do (user asked for these to be recorded, then #1 planned and done):
- [x] 1. Crossings as single events (done as an event engine; Phase B below)
- [ ] 2. Fix Cook's short-leader block, so no fill rewrite (fewer reads,
        less junk, smaller gaps)
- [ ] 3. Finish the spacing model: derive c ~ 11.2 from geometry; explain
        the small-program constraint (REPORT 3.5)
- [ ] 4. Stronger verification: decode the tape itself; independent engine
        check of a stretch near read 3,269 (Python core from a checkpoint)
- [ ] 5. Small engine wins: memo kept across epochs under a memory budget

### Plan for #1: junk crossings as events

Why: late in a run ~87% of the time is HashLife evolving glider
interactions, and the active region grows ~43k cells per read, mostly
junk that every later ossifier must cross. Cost per read grows linearly,
total quadratically. If an ossifier's passage through the junk can be
computed as a sequence of table lookups (exact outcomes memoized from
real simulation), the junk can leave the HashLife tree.

Phase A: feasibility (measure before building; go/no-go at the end)
- [ ] A1. Map the active region in the Ebar frame at a late checkpoint:
      where the pure junk zone is (left of the ossification point, with
      nothing but junk and ossifiers in transit), how many objects, of
      which kinds, how far apart (are crossings pairwise?).
- [ ] A2. Upper bound on the gain: HashLife cost of the full active region
      vs the region without the pure junk zone, over one read interval.
- [ ] A3. Crossing physics: an ossifier (and a single A^4) crossing each
      junk kind at every relative phase in clean ether: clean? which
      displacements? how many phase classes? Then: does a real ossifier's
      passage through a real stretch of junk equal the composition of
      pairwise outcomes (cell-exact against HashLife)?
- Gate: go only if (A2) the zone is most of the cost and (A3) crossings
  are clean, pairwise and phase-determined.
- Result (NOTES, phase 9): A1 and A2 done; the junk zone is only ~16% of
  the cost, so the gate fails for it. 83% is the queue zone, where tape
  characters cross queued matter; A3 there: 14 crossings all clean
  (character +14 cells; object shifted by one of 4 amounts = the 4
  relative phase classes). Target moved to the queue zone; Phase B
  below is rewritten for it (pending the user's go-ahead, since it is a
  multi-day build).

Phase B (rewritten 2026-10-05 after the go-ahead): an event engine
("gas engine", gas.py) instead of the HashLife/list hybrid.

Why not the hybrid: the queue zone's two ends (ossification, read point)
move, and matter crosses them both ways (characters out of the
ossification zone, data into the queue). Exact handover between a tree
and a list at moving boundaries is the hardest part of the hybrid and the
most likely to be subtly wrong. A pure event engine has no handover; its
correctness rests on one lemma, and HashLife becomes the oracle it is
checked against.

Lemma (superposition). Let a row be ether with two non-ether patches P
and Q, and let the cells between them be ether of one phase constant.
If at every step the two patches, each evolved alone in ether, stay at
least 3 cells apart (no cell's neighbourhood touches both), the row
evolves as the union of the two isolated evolutions. (Induction on t:
rule 110 has radius 1.) So particles far apart can be moved in closed
form, and only patches that come within 3 cells must be simulated
together.

Design:
- Item = particle or composite. A particle is a periodic patch: an orbit
  (period p, displacement d, its p patches) plus an anchor and the
  ether phase constant on its left. Recognized automatically: an
  isolated patch is simulated until its canonical key (cells + local
  ether phases on both sides, translation invariant) recurs.
- Composite: patches that came within 3 cells; its cells are simulated
  exactly (big-int bit rows, ether re-padded each step). Outcome
  memoized by the canonical key at merge time: duration, envelope, and
  the particles it splits into (pieces at least 14 cells of one-phase
  ether apart, each a recognized particle).
- Items in a doubly linked list, left to right; the next collision of
  each adjacent pair in a heap (lazy invalidation). A composite hit by a
  neighbour before it splits is re-simulated to that time and merged.
- Sides from the t = 0 Layout, materialized lazily (the ossifier train
  from the left, the table from the right).
- Interface like HashRun (t, window, history, step), so ReadWatch and
  census sample it unchanged.

Steps:
- [x] B1. Decomposition and period detection; the t = 0 rows of Collatz
      and the one-move TM must split into periodic particles.
- [x] B2. Engine core; tests against the packed engine on small rows.
- [x] B3. Lazy sides and a read driver; Collatz 556 reads identical to
      data/collatz_v12216.log (outcomes and cluster counts).
- [x] B4. One-move TM: windows cell-exact against EpochReads at several
      times; identical read outcomes; then the full run at 1.25x.
  - [x] read 3152 at Cook's v: 137,190,722 cells identical
  - [x] read 3256 at Cook's v: 141,909,284 identical; the failure at 3269
        reproduced read for read (then debris: 13.5 GB, as HashLife)
  - [x] full run at 1.25x: 5970/5970 identical to HashLife
- [x] Bound groups (tape characters cross as one particle): events 4-5x
      fewer; all checks repeated and identical.
- [x] Python too slow per event (37 us): event loop ported to C (gasc.c,
      0.2-0.3 us per event after pair tables); Python engine kept as the
      reference (identical reads and event counts).
- [x] Checkpoints (gasrun.GasReads checkpoint=..., tested by kill/resume).

Phase C: use it
- [x] C1. Benchmark against the current engine: Collatz 45 s -> 9 s;
      one-move TM 1.25x 9151 s -> 524 s (REPORT 5).
- [x] C2. The 3-state TM that moves both ways (59,184 reads; the gap rule
      needs v > 1.69x Cook's, run at 2x): 59,184/59,184 reads, visits
      decoded and equal; first 3,072 reads identical on HashLife (REPORT 3.9).
- [x] C3. Write up (REPORT 5, 3.7, 3.9, summary, 7; NOTES; CHANGELOG).

## Phase 8: the Cook's-v failure; engine efficiency (started 2026-10-04)

User: find why the one-move TM fails at Cook's v (read 3,269), then make
the engine faster and smaller.

- [x] 1. Mechanism of the failure (REPORT 3.8, NOTES phase 8)
  - [x] a. tape characters traced through checkpoints: 3,269's is made
        correctly, then destroyed by the next ossifier
  - [x] b. queue-gap rule: break at the first transition between queued
        copies with gap > c v, 11.05 < c < 11.39 (12 runs, 2 programs)
  - [x] c. fresh test: one-move TM at 1.25x Cook's v (critical gaps
        10.78v and 10.92v: predicted to pass): 5,970/5,970
  - [ ] (open) c from geometry; the small-program constraint of 3.5
- [x] 2. Efficiency (REPORT 5, NOTES phase 8)
  - [x] a. profiles: main-tree advances dominate; cost linear in time
  - [x] b. kept: power-of-two jumps, skip-ahead local copies, tables to
        load 3/4, 12-byte nodes: 55 s -> 38.6 s, 1.64 -> 1.06 GB (late)
  - [x] dropped: Ebar-frame HashLife, interleaved tables, bigger direct
        blocks (all measured)
  - [x] bug found and fixed: samples out of time order at small v
  - [ ] (open) collision-level stepping of junk crossings

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

# Phase 10b: the debris sweep ("rope") in the event engine (2026-10-06)

User: "Do 1 first then start 3 and monitor it": build the engine-level
fix for the debris cost, then run `last` of (a b c) on gliders.

Facts (car run, read 1500; scratchpad rope/map.py):
- Left of the newest tape character (C) the gas holds only E-family
  debris (2,767 items, gaps >= 64 since closer ones are bound) and
  ossifiers; an ossifier is 4 separate A gliders (orbit 0, p 3, d 2),
  338-399 cells apart; ossifiers ~2.2e6 cells apart.
- Debris is not repetitive (138 distinct item states, all 32-blocks
  distinct), so a HashLife-style memo of stretches would not hit.
- Each A x E crossing is a memoized merge + split (2 events, ~500 ns).

Design: the left side becomes train + rope.
- Rope: debris items absorbed from the left end of the C gas, kept in C
  arrays outside the event list, plus in-transit gliders (each with the
  index of the next rope item). The front glider is swept item by item
  with the existing machinery (periodic collision time, merge table,
  composite pieces), no heap or list work; unknown merges/pieces go to
  Python as now. It is emitted into the gas right after the left
  sentinel at its last split time (a sentinel wake time).
- Checks (fail loudly): every crossing yields exactly [E', A'] (both
  particles); the composite does not reach the neighbouring items before
  it splits; a glider reaches an item only after the previous glider's
  crossing of it has split; debris items stay >= BOUND_GAP apart.
- Absorption (Python, every few reads): items right of the sentinel up
  to a cut that is (a) left of where the front was when the newest tape
  character was made (Ebar frame), minus a margin, (b) at a gap >= 256,
  (c) with whole ossifiers only, all items particles.
- Validation: car with and without the rope: every read and every
  census count equal; value equal. Then speed on car/cond.

- [ ] C: rope arrays, sweep, wake/emission, absorb API
- [ ] Python: RopeSide (train draws), absorption, GasReads option
- [ ] Exactness: car, rope vs no rope
- [ ] Speed: car, cond
- [ ] Run last (a b c) on gliders, monitored
