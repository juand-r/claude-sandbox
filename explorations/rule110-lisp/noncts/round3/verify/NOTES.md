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
