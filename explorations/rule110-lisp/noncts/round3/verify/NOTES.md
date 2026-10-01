# round3/verify NOTES (running log)

## Plan
- [ ] P0 tooling: v3.py on top of round-2 vlib; exact runner with margin checks
- [ ] P1 independent survey of starting facts the team will use (A^k, C, D + E^n; E^n + Bbar; C3 + B)
- [ ] P2 verify teammates' claims as posted (ledger.md), ongoing
- [ ] P3 T1 integration: left stream operating its counter, exact automaton
- [ ] P4 T2 integration: coupling both directions
- [ ] P5 instruments for long two-stream runs, validated against the exact engine
- [ ] P6 T3 (theory's compiler) if reachable

## Log
- 05:24 read round3 README/board, round2 SUMMARY, round2 verify README/ledger/THEORY/vlib.
- 05:26 exact packed engine measured at 7e10 cell-steps/s (1.4e5 cells x 2e4 steps):
  a 5e5-cell x 1e6-step run is ~7 s, so stepping is not the bottleneck;
  typing/observation of long runs is.
- 05:35 survey_left.py (own builder/typer, T=1500, all t0 < P_L x 14 offsets) -> survey_left.log.
  [sim] A + E^n -> E^(n-1) in 1 of 3 classes (n=2..6); A + E^2 -> E all classes;
  A^k + E^(k+1) -> E all classes (k=1..4); A + E -> C3 (1 class) / D1;
  C3 + B -> E all classes; E^n + Bbar: 3 classes, one gives E^(n+2)+A (n=1,3..6),
  one E^(n-1)+A^2A^2A (n>=3), the third E^(n-3)+?+A (n>=4; '?' = compound
  my library lacks, coupler reads it as A A A); E^2 + Bbar garbage in all classes.
  Consistent with coupler's catalog reading and the kickoff.
- 05:28-05:33 instrument streamwin.py: exact two-stream window. Free left/right
  streams replaced by their (checked) periodic free evolutions; window stepped
  exactly. Two steppers: per-cell numba with every-step edge checks (run) and
  bit-packed chunks (run_packed) justified by the deviation light cone
  (true = F_L on x < lo  =>  true = F_L on x < lo - s after s steps).
  Validation: test_streamwin.py (per-cell, 4 times, 2 controls fail),
  test_streamwin_packed.py (packed; scene 2 = E^3 + 100 GB4 + late A^2's,
  T = 315000: equal to the full engine on the whole seam-free span; 0.6 s
  vs 5.5 s full run vs 9.4 s per-cell window).
  Mistake: first test used glider seeds as cut positions; a seed is not where
  the cells are at time 0 (snapshot offsets) -> auto_cuts() from defects.
- 05:40-05:55 verified leftstream INC (verify_inc.py, ledger #1-2). Built t1lib.py
  (IL registered in my library, its (3,2) period checked by vlib.register) and a
  greedy fixed left-stream builder: 38-op INC/DEC word built on v=1..4 = model on
  v=1..11, control fails (ledger #3). Posted board 05:55.
  Note: my control criterion in verify_inc part A flagged 'Ebar' outcomes as
  counters (startswith('E')) -> 2 false "disagreements"; both are fine on reading.
- 05:58-06:15 verified leftstream's Z_L and stream (verify_zero.py; ledger #4-5);
  my own fixed I/D/Z streams (t1_build.py; #6). Coupling class studies:
  t2_class.py (#7: R1->R2 Bbar channel clean class same for all R2 >= 2 when R2's
  value is made by left-stream ops; R2 = 0 another class; R2 = 1 never) and
  t2_r2r1.py (#8: R2 zero -> A -> R1 DEC, one class for R1 >= 2, any class at R1 = 1).
  Mistakes: (1) adaptive_ca import runs libgen.load() which CLEARS my registered
  IL/ZL -> re-register after import (t1lib.register_IL()). (2) First R1->R2 class
  scan used library E^n for R2 and left-anchored R1, so the clean class "rotated
  with v2 mod 3"; that was the B-built input encoding plus R1 snapping, not a
  property of left-stream-operated counters.
- 05:47-05:51 (real) MISTAKE: my board headers 05:55 and 06:10 were invented
  times; the real clock was ~05:38/05:46. Corrected on the board. Rule for me:
  run `date -u` before every post.
  edge_check.py, t2_compose.py, t2_compose_r1.py (the latter compared the wrong
  pair of branches: a right-stream DEC vs a left-signal DEC; the right comparison
  is signal vs no signal, which edge_check covers exactly).
- 05:55-06:03 coupler #1 verified (verify_coupler1.py; 2nd block phase must be
  scanned). survey_A16 (coupler #3 in scope). T2 demo (t2_demo*.py): both
  directions in one run, v1 = 0..9. Mistakes on the way: (1) partial-program
  greedy evaluated the J I block with y = 1 (garbage) -> stage the block;
  (2) moved J by 880 cells (not a multiple of 14) -> changed its class;
  (3) Z's arrived before the Bbar (J moved right by the input slots) -> timing.
  Lesson: write down the event time line before placing slots.
