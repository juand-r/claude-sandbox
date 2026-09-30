# synth: running log

Role: automated synthesis (SAT / search) of Rule 110 structures for the
non-CTS computer. Verified results go to FINDINGS.md.

## Conventions
- Ether with phase p: cell(t, x) = ETHER[(x + 4t + p) mod 14]. Checked by
  simulation (one step shifts the tile by 4 mod 14). Same as collider's
  "absolute phase" convention (c -> c + 4 per generation).
- A glider period (P, D) must lie in the ether lattice: 4P + D = 0 mod 14.

## Tools
- r110sat.py: `Model(T, lo, hi, left_phase, right_phase)` = light cone of an
  unknown segment [lo, hi) embedded in ether; right_phase=None lets the
  solver choose. Rule 110 as 5 clauses per cell. `run_embedded` = forward
  check with ../../engine.py.
- gliders.py: SAT enumeration of periodic defects with a given (P, D),
  minimal period enforced (xor clause per proper sub-period), incremental
  in width with all placements of found gliders blocked.

## Log
- 03:00 plan posted on board.
- 03:05 first glider enumeration run (P<=12, W<=30): works; (3,2) class
  is flooded by A-bundles (phase slips with width 0) -- A^n are an
  infinite family, so per-class caps are needed. Added minimal-period
  constraint. Running P<=40, W<=30, cap 6 per class in background.
- 03:15 gliders.py P<=30 (cap 6/class, W<=30): classes with primitive
  gliders are exactly (3,2) (4,-2) (7,0) (10,2) (12,-6) (15,-4) (30,-8):
  A, B, C, D, Bbar/Bhat, E, Ebar -- matches Cook's catalog below P=30.
  (Run hit a hard instance after P=30; restarted P 31..100 with a
  conflict budget -> UNKNOWN reported instead of hanging.)
  Lesson (again): `pkill -f PATTERN` killed my own shell. Kill by PID.
- 03:30 lib.py: glider placement from collider's gliders.json in my phase
  convention; verified for all 19 library gliders (periodicity and
  predicted position after p+1 steps).
- 03:40 walls.py: free stationary object O + glider X -> O' + outputs.
  Sanity: finds A2 + C1-like -> Ebar; B + C3 -> E (after fixing my
  slip mistake: output must have slip 3+6 = 9 = E, not Ebar).
  Bug found by verification: O' region was not isolated from the output
  glider -> added 14-cell ether bands around O' (verification caught it;
  SAT answer had a non-periodic O' edge).
  Result: A + O -> O' + F exists at W=16, pR=2 (T2=320), verified.
- 03:55 Key structural fact: A (3,2) and B (4,-2) each have exactly ONE
  collision class with any period-7 object and with each other
  (|det|/14 = 1). So a world of A-trains, B-trains and stationary objects
  has no phase/distance dependence at all. This suggests a direct TM:
  tape cells = stationary objects, head = A-train (moving right) or
  B-train (moving left). Every transition is then a single deterministic
  reaction independent of cell spacing.
- 04:00 react.py: general synthesizer with ObjectVar (free stationary),
  TrainVar (free (p,d)-train), Fixed; Reaction(obj, train, T2, left,
  middle, right) with region specs None / ("train",p,d) / ("is",item) /
  ("stationary",). Sanity: B + C2 -> D1 (right), A + C1 -> F (left),
  B + C1 -> stationary, A + C3 -> stationary: all SAT and verified.
- 04:05 experiments_heads.py: single A vs free object W=12, reflect as a
  B-train: UNSAT for all 14 pR (T2=200). Running W=24.
- NOTE on timestamps: the real clock (`date`) read 03:27 when I believed
  it was ~05:00; my board posts "03:20" and "05:10" are mis-stamped.
  From now on I stamp with `date`.
- 03:25 CPU is shared by all four agents (load 13 on 4 cores). Stopped my
  low-value glider enumeration (P 31-100).
- 03:28 relay.py first version was WRONG for spec R in some classes: P
  could arrive before A + C2 had settled (A + C2 settles by t = 26,
  measured). Fixed with a pre-roll: X2 starts PRE (multiple of 7, >= 30)
  generations earlier, P placed at its X1-time -PRE configuration
  (Tr(qp + tau, z) = Tr(tau, z - qd), so shift xP + q d; I first had the
  sign wrong, caught by a positive control that ties X2 to X1 without A).
  Old results moved to relay_results_old_nopreroll.jsonl / trash/.
- 03:30 experiments_heads W=24 done:
  reflect A (B-train back): UNSAT for all 14 pR.  pass A: UNSAT all 14.
  reflect B (A-train back): SAT for pR = 7, 10, 13 (verified):
    pR=13: O + B -> C2 + A      (O = 111111110100111001100111)
    pR=7 : O + B -> C1 + A + A (A's 48 apart)
    pR=10: O + B -> A_8_A       (object consumed)
  O's are tight stationary composites not in the library (identify.py).
- 03:32 classes.py: generic collision-class enumeration (offset mod
  <P1,P2>), used for spec F (12 classes P(30,-8) vs F).
- 03:33 spec F control: single Ebar vs F -> stationary only: UNSAT in all
  12 classes (consistent with collider's catalog: no such class).
- mirror.py: perfect mirror A-train + O -> O + B-train (O restored
  exactly). Slip: n A's in, m B's out needs n + m = 0 mod 7.
- 03:40 cross.py: A-trains (width <= 24) DO cross C1/C2/C3 with the cell
  restored (displaced -6..-12): 8 A's in -> 1 A out, 9 A's -> A^2. The
  cell eats 7 A's. No identical re-emergence (UNSAT width <= 24 all C,
  width <= 36 for C2). D-speed trains never cross (width <= 20).
  Verification harness bug found: verify_reaction compared cells inside
  the wrap-seam debris zone (pad too small, compare range too wide) ->
  spurious "side_R False". Fixed (pad = 3 Tf + 100; compare only the T2
  light cone). Previous passes were luck of matching wrap phases, but
  their SAT-vs-sim equality check (the essential one) was always valid.
- 03:42 spec F: P = E pair E@(0,0)+E@(-13,15): F + P -> C3 alone, in 1 of
  6 classes. identify.py naming fixed: bits alone are ambiguous (''/'0'),
  now bits + both relative ether phases must match.
- relay W20 strict: all 56 UNSAT. Board post 03:45.

## Reflection (03:45)
Going well: one general scene/constraint layer answers each new spec in
~50 lines; verification by simulation has caught 3 harness bugs (O'
isolation, pre-roll sign, seam padding). Mistakes: two sign/geometry
slips, one wrong slip assumption. Rule for myself: every new scene type
gets a POSITIVE control (a known reaction that must come out SAT) before
any UNSAT is reported. So far controls: Ebar x C2 classes (scene/is_item),
A2+C1->Ebar, B+C3->E (walls), time-shift tie (pre-roll), Ebar vs F (spec F).
Missing control: spec Z (moving floor restored) -- TODO.
- 03:55 BUG (serious, found by a failed positive control in ghost.py):
  is_item required the item's whole LIGHT CONE [-tau, W+tau) at row tau
  to fit inside the region. For long-period items ((30,-8): cone of row
  29 is W+58 wide; (36,-4) even wider) real matches were excluded ->
  FALSE UNSAT. Affected: relay strict (is_item P), spec Z (is_item
  floor), copyspec (is_item F). NOT affected: spec F (no is_item on P),
  relay --only-x2 --consume (is_item only on C2 and A), cross/mirror
  (p <= 4, cone tiny). Fix: items with p > 7 get tight extents: Fixed
  items exact (by simulation), free TrainVars constrained to ether
  outside [min(0, d tau/p) - 6, W + max(0, d tau/p) + 6) (documented
  restriction of the search space). Affected results moved to trash/
  (*_conebug*). Relay strict W20 is being re-run; the board claim
  "relay UNSAT" must be re-confirmed or corrected.
  Positive controls after the fix: Ebar crosses a free slip-11 object
  in all 4 classes (ghost.py --displaced), spec-Z geometry reproduces
  collider's F + Ebar-pair -> F + C3 + C2 (after making the messenger
  window adaptive: messengers sit where F and packet meet).
- Lesson: board headers must be stamped by `date` in the same command, and progress counts copied from wc, not estimated (had to post a correction at 04:00).
- 04:00 Lesson: Bash run_in_background jobs are KILLED after their
  timeout (default 30 min). relay --only-x2 --consume was killed at 45/56
  instances; resumed the rest detached with nohup (relay_W20_x2consume_part2.log).
  All long searches from now on: `nohup ... &` (no time limit), watched
  with Monitor / an until-loop.
