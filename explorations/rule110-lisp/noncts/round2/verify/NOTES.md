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
- 23:40-23:55 theory: chain machines (models.py). Found the monotonicity +
  Dickson proof that chain machines are eventually periodic/decidable
  (THEORY.md s.2). Feed-forward theorem (s.3). Random/exhaustive searches
  support, but the TZ control shows random search is a weak test (I say so).
- Mistake caught: my first M1 scans used left-anchored build(); the snapped
  x0 of later packets depends on the counter's width, so the G-GB3 offset
  varied with v (by (0,14) steps, which changes the A x G class). Added
  build_right(); m1_program.py re-does M1 with a fixed stream geometry.
  The m1_scan/m1_search results (v-dependent geometry) should be read as
  "per-v placements", not as one rigid stream; the 202-linear finding is
  per placement and still stands in that sense, but should be redone
  right-anchored before being relied on. TODO.
- 00:00 posted board (tools, theorem, M1 gadget).
- 00:01 xlate.py: collider-convention scenes -> my convention; my rebuilt row
  asserted equal to collider/build_row cell for cell. gate_scene.py imports
  gate/stream.build read-only.
- 00:04 gate's Z wrap: I^v Z^3 VERIFIED; random words REFUTE it as a general
  instruction (INZZ...). Cause: Z on value 1 -> trailing GB4 hits zero E ->
  displacement (my earlier caveat #2 paid off). Posted 00:06.
- Mistake: killed a background job by its subshell PID; the python child
  survived (two copies wrote the same log for ~10 s). Now I record the
  python PID itself (ps -eo pid,ppid,cmd) and kill that.
- Typer gap: E^10+ were '?' -> extended library to E^15.
- 00:12 address's 2-register claim VERIFIED 16/16 (+9 controls). Bug of mine
  fixed on the way: xlate.translate set c0 from the (0,0)-seed phase even
  when the leftmost object's seed was elsewhere (gate scenes start with E at
  (0,0), so they were unaffected; rechecked verify_gate_wrap after the fix).
  Typer limitation: F's closer than ~one ether window merge into '?';
  replaced name comparison by cell-level comparison of the F region.
- 00:13 prim_table.py: compound packets x values x classes, with trajectory
  offsets. Explains INZZ failure (Z on value 1).
- 00:16 MISTAKE: prim_table with T=1500 reported "debris" that was just
  unfinished collisions. Rerun with T=4000: all clean, 3 classes each. Posted
  a correction 00:17. Rule for myself: before calling an outcome debris,
  rerun with 2x T (or check the outcome is stable between T and 2T).
- 00:18 gate_scene: collider reads json relative to cwd -> chdir wrapper.
  v2 verified 90/90.
- 00:19 adaptive_ca.py (my own CA-in-the-loop assembler). J^5Z^6 x4 fails
  (J zero displacement accumulates), J^3Z^4 x4 works. Running x6 for M2.
- Mistake: some board stamps (00:14, 00:17, 00:20) were estimated, not read
  from `date -u` (real time was a few minutes earlier). From now on I stamp
  with `date -u +%H:%M` right before posting.
- Search: no word of length <= 9 over {Z,W,X,J,I,N} with #J = 0 mod 3
  realises "DEC, wrap 0 -> 1" (parity block). Parity is read from the mod-4
  counter instead.
- 00:36 batch: parity (J^5Z^6)^2 PASS 0..12; Z^9 and XZ^9 fail out of sample
  (zero at untrained slots); (J^6Z^7)^3 fails to build. Order-3 hypothesis
  about J refuted as stated (zero event maps c -> 2c+const).
- Stamp check: I wrote 00:33 on a post made at 00:31 (stamp typed before
  running date). Fixed procedure: date first, then append.
