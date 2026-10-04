# Changelog

## Unreleased (after v0.1.1)

Why Cook's spacing can be too small (REPORT 3.8)
- The one-move TM's failure at Cook's v is observed directly: the
  character for read 3,269 is made correctly, then the next ossifier,
  finding no queued symbol in its way, destroys it. Rule: a filled CTS
  breaks at the first transition between consecutively queued appendant
  copies whose spatial gap exceeds c v, 11.05 < c < 11.39; one constant
  fits twelve runs of De Mol's program and the TM, each failing at the
  first transition above it (`experiments.block_gaps`). Prediction
  tested afterwards: at 1.25x Cook's v the TM reads 5,970/5,970
  (data/tm_one_v1.25.log).
- Epoch engine: samples forced into time order (a bug that only small v
  could trigger); ossifier budget enlarged; 55 s -> 38.6 s and 1.64 ->
  1.06 GB on a late benchmark (power-of-two jumps, hash tables to load
  3/4, 12-byte nodes). Ebar-frame HashLife tried and dropped (no gain).

Long runs and a compiled Turing machine on gliders (REPORT 3.7, 5)
- A compiled Turing machine runs on Rule 110 gliders: the smallest
  machine that changes state and moves (tests/machines.py one_move_tm),
  through Cocke-Minsky, the filled CTS and Cook's blocks, at 2x Cook's
  spacing: all 5,970 CTS reads equal the reference over 2.5e11
  generations, and its visit sequence is decoded from the reads alone
  (`experiments.py tm-gliders one 2`, data/tm_one_v2.log; the same at
  4x, data/tm_one_v4.log). At Cook's own
  spacing the construction fails at read 3,269 (a tape character never
  arrives); reproduced with different engine settings, gone at 2x.
- HashLife made practical: casim.layout (the initial row as ossifier
  segments, closed-form ether gaps and a repeated table super-period,
  never materialized), epochrun.EpochReads (tree rebuilt every 8 reads
  from the active region and the next ossifiers and appendants, memory
  bounded, checkpoints), hlc.c (C core via ctypes). De Mol's 556 reads:
  ~40 s and 0.3 GB, against 3.9 h for StreamRun; every read's outcome
  and cluster count identical (data/collatz_v12216_hash.log).
- tag.heads_from_reads: TM visits from a Y/N read sequence alone.
- census(): all clusters typed at once (identical results, ~10x faster).
- data/collatz_v12216.log was ignored by `*.log` and never committed;
  it is now (force-added, like the other cited logs).

- Non-CTS team, round 2 (noncts/round2/SUMMARY.md): a one-counter
  Rule 110 machine that is not a cyclic tag system, driven by a fixed
  glider stream, branches on zero and runs compiled loop programs
  (parity, mod 4, mod 7, saturating subtraction) exactly; cross-verified
  by two agents and spot-checked by the lead. Two independently
  addressable registers in an F-glider lane. Theory: one counter is
  capped at eventually periodic predicates; clean answers give decidable
  machines; universal target = guarded-block machine. Universality not
  reached.
- Non-CTS team, round 3 (noncts/round3/SUMMARY.md): two program streams.
  A left stream increments (I_L, found via slip conservation + SAT),
  decrements and zero-tests its own counter; the two counters couple in
  both directions in one exact run; class-free channel K3. Theory: zero-
  answer coupling is never universal; a shuttle, a right-to-left
  crossing or the gap as a register is required; none found in scope.
- Non-CTS team, round 4 (noncts/round4/SUMMARY.md, ROUTES.md): six
  agents, 23-route map. Verified: gap-drift switches in both directions
  (route 23 half built), MERGE (unbounded transfer), two-way rod
  interiors (right-to-left walls, none glider-launched), C1 stacks,
  single-class head lemma. No universal machine; missing pieces W3/W4
  and a reusable reflector, each searched within stated scopes.

## v0.1.1 (2026-09-30, untagged)

Headline
- Rule 110 gliders compute a whole Collatz trajectory: De Mol's 3x+1
  tag system from x = 3, compiled and assembled with Cook's blocks,
  runs 3 -> 5 -> 8 -> 4 -> 2 -> 1 with all 556 CTS reads observed and
  equal to the reference (2.07e8 generations, Cook's spacing;
  `experiments.py collatz`, REPORT 3.6).

Corrections to v0.1.0
- Withdrawn: "each ossifier converts four characters" and the `fronts`
  table. Both came from the moving-data decoder, which is phase-
  dependent. Measured instead: one ossifier = four C gliders = one tape
  character; one read per ossifier period, ~30v generations.
- The 7.5v-30v cost range is withdrawn; capstone back to ~3.6e20.

Verified
- Decoder-free read check: `{YYYYNN}` 12/12 (3x Cook's v) and 10/10
  (Cook's v), including reads of appended characters.
- Empty appendants: an exact CTS rewrite (cts.fill_empty_appendants)
  removes the failing short-leader block; the minimal program L broke
  reads 12/12.
- Spacing: small programs read correctly at 1/2-1/4 of Cook's v (the
  need grows with appendant length, not table size), but De Mol needs
  more than half of Cook's v (fails at 1,600, 3,200 and 6,400).
- Direct binary clockwise construction (cw.two_way_to_binary_cw): SKI
  machine 119,347 states (old path ~22M, never finished), still
  normalizes SKI terms; capstone 66 states instead of 130, ~7x fewer
  generations.

New tools
- casim.StreamRun: exact streaming-window simulator, checkpointable;
  reference split between the two free rows.
- engine.step_packed_n: numba kernel, 4x, bit-identical.
- hashlife.py: exact 1-D HashLife prototype (~2x StreamRun here).
- experiments.py: `reads`, `lblock [fill]`, `cost`, `collatz`; read
  check flags malformed regions ('!') and resumes from checkpoints.
- encoder: cached seam fits (bit-identical rows, ~5x faster assembly);
  `left_gaps` ossifier schedules.
- noncts/: first team round on non-CTS computers (none found;
  noncts/SUMMARY.md).
- Tests: 52 (fill exactness, edge growth, direct binary tower and SKI,
  engine equivalence).

Known open problems
- Why the short-leader block L fails.
- What spacing a program really needs.
- A compiled Turing machine on gliders (~9e12 generations for the
  smallest case; needs a glider-level simulator).
- A non-destructive zero test and two-counter addressing for a non-CTS
  machine.

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
