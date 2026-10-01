# theory: running log (round 3)

Task: abstract two-stream machines; which are universal; weakest coupling;
compiler + differential tests; reaction spec for leftstream/coupler.

## Plan (check off as done)
- [x] P1 Models: abstract 2SM (two counters, finite aux state, modes),
      and the physical "local interval machine" (LIM) for E^n counters.
- [x] P2 No-go theorems with proofs (THEORY.md):
      T1 value-only coupling (any reactions, any direction) -> eventually periodic;
      T2 owned modes / one-directional mode coupling -> eventually periodic;
      T3 LIM (E^n intervals, quiescent bounded gap) -> eventually periodic.
- [x] P3 Checks of T1/T2 on random machines + a control that must find
      non-periodic orbits (shared-mode machines).
- [x] P4 Universal model (loop machine, shared mode) + compiler from Minsky
      + differential tests + control.
- [ ] P5 Two-stream realisations: (a) mode copies + cross signals,
      synchronous; controls: one direction cut; value-dependent skew.
      (b) shuttle (gap process) realisation.
      -> (a) DONE (xm.py). (b) NOT done: no construction found; the tie
         constraint (THEORY s.6.3) blocks the obvious per-side-filter
         design; gap-as-register route stated as [hyp]. Left OPEN.
- [x] P6 Reaction spec for leftstream/coupler; post on board early, refine.
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
- 05:49 Posted EARLY claim + spec seeds on the board.
- nogo.py first run: MISTAKE in my periodicity checker. A sequence ending
  in a long quiet stretch (doubling machine: zero events get rarer) was
  accepted as periodic, so both controls "passed" as periodic. Caught by
  the controls themselves. Fix: the periodic part must start within the
  first quarter of the run. Rerun: theorem classes 0/3000 + 0/3000;
  controls flagged; random shuttle class 38/3000 non-periodic.
- lm.py: 502 tests, 0 failures; no-remainder control 96 failures.
- xm.py: first version shared one RNG between programs and delays, so each
  row of the table tested different programs. Fixed (separate RNGs); all
  rows now use the same 150 programs (105 halting). Results in xm.log.
- THEORY.md written. MISTAKE in my first proof draft (Step 2): "long
  passage forces mu2 < 0" was wrong (mu2 = 0 with bounded fluctuation
  is possible). Fixed by classifying passages as far/near by their start
  value, not by length. Verify's review (board 05:57) asked for the
  timing-finite-state argument: added (joint lattice L = L1 ∩ L2, s.2.2).
- Board read 06:2x: coupler ruled out the A/Bbar shuttle (catalog);
  leftstream runs the R1-side reflection SAT; verify: successive A-DECs at
  R1's inner face rotate its class (fixed emitter). In a gap-conserving
  shuttle the emitting face moves too, so the rotation can cancel:
  condition = both faces' displacement per round trip equal mod P_E.
- MISTAKE (THEORY.md s.6.3, first draft): claimed "with per-side filters
  on both sides + a two-type shuttle, the transfer machine can be laid
  out". Wrong: each side's rate is fixed between its own zeros, an
  interval that spans its destination phase AND its next source phase.
  Consecutive transfer ratios share a parameter (tie constraint). Corrected
  to OPEN, with the tie stated. The board post (item 4 B1/B2) says
  "needed", not "sufficient", so it stands; I will say so on the board.
- 06:2x Generalised "owned" (only the owned side's drift must depend on
  its own autonomous mode; the other side may depend on anything incl.
  residues). Proof re-checked: Step 2 uses the joint bulk cycle; Step 3
  needs only that the owned side's mean depends on its own cycle.
  Consequence: a crossing in ONE direction is not enough (THEORY s.3.5,
  posted on board for leftstream's crossing search). nogo.py class
  `residue` added: 0/3000 non-periodic.
- Shuttle + blind streams: total-value law x + y = n0 + (s1+s2) t +
  O(#zero events). All round multipliers on the same side of 1. Shrink
  or flat: decidable [arg]; growth: open (growth-only Conway maps).
- 06:2x Read verify 06:24 (no wide-spacing reflection; rod interior has
  only a front->back "phonon"). Posted: phonons are a one-directional
  channel, so they cannot suffice alone (Theorem 1); listed P1-P3 questions.
- Reflection on process: two overstatements were caught by re-reading
  (Step 2 sign, s.6.3 "can be laid out"); one checker bug was caught by
  its own controls. Rule kept: every positive "sufficient" claim needs a
  construction that runs; otherwise label [hyp]/open.
- 06:26-06:30 verify: walls (I_L/Z_L launch a front->back domain wall; a
  wall at the back switches a Bbar's class). MISTAKE found: my premise (L)
  "no influence either way through a long rod" is false. Restated
  Theorem 2 with the true half: no back->front (right-to-left)
  influence. Conclusion unchanged: Theorem 1 needs only y owned. Wall
  timing makes back-face outcomes depend on y mod m: folded into S [arg].
- Added s.6.5 (wall-driven pump: converter at R2's back) as alternative
  Tier A target; verify 06:32: first scoped test found no converter.
- Final state: Theorems 1-2 with proofs; lm/xm/nogo tests green; spec
  posted; open: shuttle/pump + blind streams universality (tie,
  total-value law), window rod, delay line.
