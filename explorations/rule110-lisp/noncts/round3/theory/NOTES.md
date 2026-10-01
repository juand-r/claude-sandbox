# theory: running log (round 3)

Task: abstract two-stream machines; which are universal; weakest coupling;
compiler + differential tests; reaction spec for leftstream/coupler.

## Plan (check off as done)
- [ ] P1 Models: abstract 2SM (two counters, finite aux state, modes),
      and the physical "local interval machine" (LIM) for E^n counters.
- [ ] P2 No-go theorems with proofs (THEORY.md):
      T1 value-only coupling (any reactions, any direction) -> eventually periodic;
      T2 owned modes / one-directional mode coupling -> eventually periodic;
      T3 LIM (E^n intervals, quiescent bounded gap) -> eventually periodic.
- [ ] P3 Checks of T1/T2 on random machines + a control that must find
      non-periodic orbits (shared-mode machines).
- [ ] P4 Universal model (loop machine, shared mode) + compiler from Minsky
      + differential tests + control.
- [ ] P5 Two-stream realisations: (a) mode copies + cross signals,
      synchronous; controls: one direction cut; value-dependent skew.
      (b) shuttle (gap process) realisation.
- [ ] P6 Reaction spec for leftstream/coupler; post on board early, refine.
- [ ] P7 README.md, final board summary, report.

## Log
- 05:2x-05:48 Read BOARD, README, round2 SUMMARY, THEORY.md, models.py,
  gbm.py, csm.py, ledger; teammates' notes.
- Key idea (to prove): with two counters, the per-period map in the "bulk"
  (both counters large) is a translation unless some PERSISTENT finite
  state changes the drift. Zero events happen only near the axes. Then an
  orbit cannot ping-pong between the axes (that needs drifts pointing both
  ways), so it is eventually periodic. Value kicks, deletions in bounded
  windows, non-monotone wraps: all irrelevant. Needed: a persistent mode
  that both counters' zero events can change (shared or cross-coupled).
- For E^n counters: ops act at outer faces, answers at inner faces, and by
  locality (coupler 05:4x confirmed by sim: outer ops leave the inner end
  fixed) an outer-face mode can only change at its own counter's zero.
  So the only shared persistent state can live in the gap, and it must be
  a process that keeps changing the counters while both are large: a
  "shuttle" bouncing between the inner faces.
- Physical timing fact: R1's outer face moves when x changes, so stream-1
  packets reach R1 earlier/later by ~15*alpha per unit (value-dependent
  skew between the two streams). Lockstep designs break; a shuttle is a
  physical handshake (each bounce moves one unit), which survives skew.
