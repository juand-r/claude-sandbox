# verify/ NOTES (running log)

Agent: verify (round 2). Role: independent verification, theory (abstract
models with differential tests), integration (M1 -> M2 -> M3).

## Plan
- [ ] P1 own tooling: vlib.py (independent row builder from Martinez strings,
      own glider typer by exact phase-snapshot matching, own compound
      gliders E^n, GBk, A^k derived by my own collisions)
- [ ] P2 re-derive round-1 frontier facts needed for integration:
      GB3/GB4/GB5 on E^n, GB3 at zero -> E + A, A + GB4#4 -> A,
      A + (GB3,GB5) -> GB3, A + (G,GB2) -> GB4
- [ ] P3 theory: weakest primitive sets; executable models (models.py) with
      differential tests
- [ ] P4 verify teammates' claims as posted (ledger.md)
- [ ] P5 M1 integration: a stored value changes later program behaviour
- [ ] P6 M2, M3 if reachable

## Log
- 23:25 read round-1 SUMMARY, THEORY, csm.py, round-1 board (GB stream, hard gate).
- 23:30 wrote vlib.py: own row builder (Martinez strings, event placement with
  ether-phase constraint x0 + 4 t0 + c = 0 mod 14), own typer (canonical
  defect keys, exact lookup over all phases), own compounds harvested from my
  own collisions (E^2..E^9, GB1..GB8, A^2..A^4) -> libgen.py, lib_v1.pkl.
  Mistakes on the way: (1) snapshot edge contamination from my finite stepper
  (fixed by trimming s cells per side); (2) identify() looked at seam-
  contaminated edges (added T+16 cut); (3) pad T+100 too small once gliders
  move 2/3 T (now 2T+100).
- 23:35 [sim, own code] reproduced round-1 GB instruction set: E^n + GB3/4/5
  -> E^(n-1)/E^n/E^(n+1) in all 42 G phases, n=2..5, product at the same
  position; zero: E + GB3 -> E + A in 14/42 phases (one class), C3 or debris
  otherwise; E + GB4 -> E in all classes BUT displaced in 2 of 3 classes
  (E@4:-128, E@3:-131 vs untouched E@5:-153); E + GB5 -> E^2 in 3 positions.
  E^n + GBk (k<3) -> E^(n-1) + A^(3-k) (round-1 text "E^(n+k-4)" is only
  right for k >= 3).
  Anomalies: E^3+GB4 1/42 and E^6 + G/GB1/GB2 1-2/42 gave debris - probably
  a too-close initial placement; not chased (irrelevant to claims so far).
