# coupler: running log (round 3)

Task (T2): couple counter R1 (E^n at -4/15, right G-speed stream) and R2
(to its left, driven by a left stream) both ways, in the exact automaton.

## 2026-10-01
- Read round3 README/BOARD, round2 SUMMARY, gate README/NOTES, verify THEORY.
- cl.py: thin toolkit importing round-2 gate/collider read-only (bytecode
  writing disabled so nothing is written outside this directory).
- [sim] J at zero reproduced: E(0,0) + J@(-4,454) -> E(13,40) + Bbar(9,1576)
  (glidersim == exact CA product list).
- Catalog facts relevant to coupling [catalog = sim by collider]:
  * E^n + Bbar, 3 classes. n>=4: #0 -> E^(n-1) + A^2 A^2 A,
    #1 -> E^(n+2) + A, #2 -> E^(n-3) + A A A. n=1: #1 -> E^3 + A;
    n=3: #1 -> E^5 + A; n=2: every class gives garbage (C3/F/B...).
  * Every E^n + Bbar class emits right-moving A's: they travel to R1
    (nothing else lies between the counters). So an R1 -> R2 signal
    always echoes back to R1.
  * A + E^2 -> E in ALL three classes (class-free DEC from the left).
    A + E^n for other n: DEC only in one class.
- Edge invariance [sim, collider collide_pair, every class]:
  * right-stream ops GB3/GB4/GB5 on E^n, n >= 2, leave the LEFT end of the
    counter fixed: the A-probe line that DECs E^n DECs E^(n+-1) too
    (n = 3..16); left edge dL = 0 exactly. Only events at n = 1 move it.
  * left-stream ops (A DEC in its class; leftstream's I_L INC) leave the
    RIGHT end fixed: a Bbar line that gives +2 on E^n gives +2 after
    (n = 3..13; class LABELS rotate at n = 10 but semantics agree).
  So R1's left end changes only at R1 zero events and when R1 absorbs
  signals from the left; R2's right end only at R2 zero events and
  Bbar arrivals.
- Lattice fact [arg]: <P_E,P_A> = <P_E,P_Bbar> = <P_E,P_G> =: M (since
  P_Bbar = P_E - P_A, P_G = 3P_E - P_A), index 3 in the ether lattice.
  So every signal type sees the same Z3 phase of a counter end
  (leftstream's key 2dt-3dx mod 42 is a homomorphism vanishing on M).
- Global slip lemma [arg]: with garbage-free evolution, the ether phase
  in the empty gap between R2 and R1 equals c_L + slip(left stream left)
  + slip(R2) = c_R - slip(R1) - slip(right stream left). Since
  slip(E^n) = 9 + 6(n-1), v1 + v2 (mod 7) is fixed by how much of the two
  streams has been consumed: data-independent. Every coupling op must
  change v1 + v2 by the same amount mod 7 in both branches (check:
  "J I" gives +2 to R2 or to R1; leftstream's Z_L gives -1 to R2 or R1).
- [sim, glider + exact CA] FIRST COUPLING SCENE (two.py; scratch t1ca.py):
  R2 = E^5 (value 4) at place_left_of(target_end=-1500, t0=1); R1 = E(0,0)
  + v GB5's; R1 program J I N N (rafast Program, classes 1,0,0,0).
  v=0: J at zero -> Bbar -> R2 E^5 + Bbar #1 -> E^7 + A; I: R1 -> E^2;
  echo A + E^2 -> E. Final [E, E^7]: R1 0, R2 6. v=1: [E^4, E^5]
  (R1 1 -> 3, R2 untouched). Exact CA product list == glidersim.
  Controls: R2 at t0 = 0 / 2 (other Bbar classes): t0=0 CA gives
  [E^4, E^4] (R2 -1, echo A^2 A^2 A turns R1 E^2 into E^4); t0=2 debris.
  Semantics of "J I": if R1 = 0 then R2 += 2 else R1 += 2.
- J I J I (v=0) [glider]: both J's at zero, both Bbars hit R2 in class
  #1 (E^5 -> E^7 -> E^9), R1 ends E. Open: does a history with NO first
  Bbar meet the second J's Bbar in the same class? (running v=0 vs v=5
  on J I Z^7 J I N N, both zero at J2).
- Board read 06:00: theory (05:49) proves value coupling alone stays
  eventually periodic; asks for a SHUTTLE (glider bouncing between inner
  faces). verify confirmed edge invariance and both couplings compose.
- [sim, collider catalog] reflections at E^n faces in collisions.json:
  right-mover in / only left-movers out: only A^4 + E^7 #1 -> B^2 + E.
  left-mover in / only right-movers out: Bbar (3 classes, n>=1),
  G/GB1/GB2 (+E^n -> E^(n-1) + A^3/A^2/A, class-free), Bhat + E #1,
  GB3/GB6 at E. A + E^n (n<=16) never emits a Bbar: X=A/Y=Bbar shuttle
  impossible.
- [sim, exact CA, echo3.py] Bbar #0/#2 echo trains (A^2 A^2 A; A_8_A A)
  vs R1 = E^1..E^7, 15 R1 phases: no left-mover emitted; notable clean
  results: #0 echo + E^2 -> E^4 (all phases), #2 echo + E^4 -> E.
- [sim, scan_bemit.py, scan_bemit_s6.jsonl] all 319 slip-6 G-speed
  library packets vs E (zero), every class: only 13 GB1 pairs give a
  clean E + left-mover, always Bbar. No single-B emitter (B would have
  been class-free at R2). Scope: library packets only.
- 06:2x verify_scenes.py [sim, glidersim AND exact CA, CA product list ==
  glider prediction in every positive case] (log verify_scenes.log):
  Scene A (R1 zero -> R2 += 2): R1 = E(0,0)+v1 GB5, program J I N N
  (classes 1,0,0,0), R2 = E at seed time 2 (gap 1500) raised by v2 I_L's
  (leftstream's rigid rule, two.left_stream). v1=0: (R2,R1) = (v2+2, 0)
  for v2 = 2..5; v1 = 1,2: (v2, v1+2) for v2 = 0..5. Exceptions (physics):
  v1=0 with v2=0 (needs seed time 1 instead: class differs, as verify
  found) and v2=1 (E^2+Bbar garbage). Controls: R2 seed time 0 or 1 ->
  debris for v2 = 2,3,4 (6/6).
  Scene B (R2 zero -> R1 -= 1): R1 = E(0,0)+v1 GB5's, R2 = E (seed time 0,
  gap 1200), left stream I_L^v2 Z_L arriving after R1 is built.
  15/15 inputs (v1 = 1..5, v2 = 0..2) = model; controls (R2 seed time 1,2)
  6/6 fail (Ebar/B debris).
  Mistake on the way: first Scene A used seed time 1 (taken from the E^5
  scene of t1.py, where R2 was a library E^5); with R2 built from E by
  I_L's the working time is 2 (class labels of E^5 vs E differ). Fixed by
  checking all three before choosing.
- Shuttle SAT batch 1 (sat_shuttle.py, run_shuttle.sh -> run_shuttle.log,
  sat_shuttle_results.jsonl): positive controls first: R2 face alone finds
  Bbar/A (m = 4); R1 face alone finds A^4-like X -> B^2 + E (n = 7).
  Joint shuttle, n = m = 4, X (3,2) width 18, Y width 24: UNSAT for
  Y (12,-6) with (sx,K) = (8,2),(8,1),(8,-1),(2,1),(2,-1), all 9 class
  pairs; Y (4,-2) with (8,1),(8,-1),(6,1), all 3 classes. 54/54 UNSAT.
- 06:4x Batch 2 (joint, widths 30/30) took ~36 s+ per run; stopped after
  1 result (sx 8, K 2, c 0/0: UNSAT) to first map R1-face feasibility
  alone (cheaper; a face that is UNSAT alone prunes the joint search).
  run_r1feas.sh -> run_r1feas.log.
- Board 06:0x: verify finds R2 -> R1 does not repeat (each inner-face DEC
  rotates R1's front class; the emitter does not follow). leftstream took
  the R1-side reflection with Y = Bbar (sat_reflect.py), and warns that
  joint-n SATs at a BACK face are invalid with B-built E^n (I only used
  single n = m = 4, so batch 1 is not affected).
- Catalog note: Ebar + G #3,4,5 -> Ebar + A^4: an Ebar (co-moving with the
  counters, speed -4/15) reflects a G into an A^4. Possible "mirror" in
  the gap; not pursued yet.
- 06:32 G scan died again silently after ~1 min (nohup); the candidate it stopped at runs fine alone. Relaunched via the harness background mechanism.
- 06:43 MISTAKE: the two "silent deaths" of the G scan were not
  deaths. The PID I saved with `echo $!` was not the python process (the
  harness wraps commands in a bash -c), so `ps -p` showed nothing and I
  relaunched twice: three scan processes ran concurrently for ~10 min
  (against the one-heavy-process rule) and appended duplicate lines to
  scan_reflect_M4.jsonl. Killed 11819 and 14271 (found with ps aux),
  kept 14654. Analysis dedupes by Y. Rule for myself: after any launch,
  confirm the PID with `ps aux | grep` before recording it.
- 06:45 Library shuttle scan complete [sim, exact]:
  step 1: all 2523 library left-movers faster than E (186 at -1/2, 2337
  G-speed) vs R2 = E^4, every class (scan_reflect_M4.jsonl, deduped).
  analyze_reflect.py: G-speed packets give many CLASS-FREE back-face
  reflections (e.g. G+GB1@(0,39): +1 & A; GB1+GB1@(-4,48): +2 & A;
  GB2+GB1@(-3,56): +3 & A; G+GB5@(-26,47): +5 & A; GB2+GB1@(-2,52):
  -2 & A^3), but NO crossing (no E^j + left-movers-only outcome) for any
  of the 2523 objects at E^4.
  step 2 (scan_reflect2_N*.log): 368 distinct multi-glider X trains (plus
  single A^k covered by the catalog up to E^9) vs R1 = E^3..E^8, 15 seed
  times: every left-moving return is B-family (B, B^2, B^3, a B compound)
  and is n-specific (R1 dumped to E/E^2/E^8). B-family objects are
  absorbed at R2's back (one class), so no loop closes. Also: some "X"
  were stationary C-pairs left in the gap (my reflect flag counted
  velocity 0 as right-moving); irrelevant for shuttles.
  => No shuttle made of library objects (scope: R2 = E^4, R1 = E^3..8,
  X as emitted, every class/phase).
- Catalog: A^3 + E^n -> E^(n-3) (1 class, n = 7, 8), A^4 + E^n ->
  E^(n-4) (n = 5,6: 2 classes; 8, 9: 2 classes): multi-unit front DECs.
- 06:59 Repeated R1 -> R2 coupling, history dependence [sim,
  glider level; repeat.py]: program J I Z^7 J I N N, R2 = 3 (I_L-built),
  inputs v1 = 0 (couples at J1 and J2) and v1 = 5 (couples at J2 only).
  Greedy per-slot classes (J and the following I chosen jointly, since
  the echo can only be judged after the I) work up to J2; at J2 no class
  works. Diagnosis (diag): (a) R1 side: J2 meets R1 in class 1 at
  different J2 placements for the two inputs (round-2-type conflict); (b)
  R2 side: with J2 in class 1 the Bbar reaches R2's back in class #0
  (v1 = 5, back untouched) or #2 (v1 = 0, back after one coupling): a
  coupling shifts R2's back by a NONZERO Z3 element relative to the
  J-slot frame [sim + class arithmetic].
  Order-3 idea: a logical coupling = three J I in a row (R2 += 6), so the
  back shift is 3*delta = 0. Test J I J I J I Z^7 J I N N, v1 = 0, 1:
  the three Bbars all land in #1 (greedy classes 1,0 / 0,0 / 2,0), and at
  J2 BOTH histories now see the SAME R2 class (#0 for both) - the R2-side
  conflict is gone; left: the common class is #0 (not #1) and the R1-side
  J2 class differs. Both are R1-side phase issues, which N (GB4) at zero
  can correct (class-dependent displacement). Enumerating N correctors
  (run_repeat.sh -> run_repeat.log).
- 07:10 Idea queued: zero-CROSSING scan. If some G-speed packet X
  passes R1 = E (zero) and emerges on the left as a G-speed packet Y
  (R1 kept at E; slip(X) = slip(Y)), then Y acts on R2's back CLASS-FREE
  (G-speed ops on E^m, m >= 2, are class-free; GBk with k >= 3 emit no
  echo). That would be an echo-free, class-free R1 -> R2 coupling and
  would remove the R2-back history conflict found with J's Bbar. Scan:
  scan_reflect.py 1 -1/3 (all 2337 G-speed packets vs E, every class),
  then analyze crossings.
- 07:31 Corrector enumeration (run_repeat.log): J I J I J I N Z^7 N
  J I N N, v1 = 0, 1, R2 = 3, all 9 class pairs of the two N correctors
  (first: after the triple block, acts only on v1 = 0 which is at zero;
  second: after Z^7, both at zero), Z/J/I classes greedy: 7/9 done before
  the 30-min cut, all fail at J2 (no J2 class gives class 1 at R1 AND #1
  at R2 for both inputs); last 2 rerun queued.
  Re-reading the diag numbers: with J2 in class 1, v1 = 0 used cJ = 2 and
  v1 = 1 used cJ = 0, both giving #0 at R2. If R1 correctors aligned the
  two histories on one J2 placement, their R2 classes would differ by 2
  steps (cJ 2 vs 0). In the single-coupling test the difference was 1.
  So the triple block did NOT remove the conflict; my "3 delta = 0"
  reading was wrong. The mismatch is better explained by the INPUT
  ENCODING: inputs v1 from different classes mod 7 get the right program
  x-shifted by different D(v1) (rafast convention), so the right stream's
  frame relative to R2 is input dependent, and R1-side correctors (which
  only move R1) cannot repair R2-side phase.
  [arg] Within ONE input coset (v1 = v1' mod 7, same frames), the slip
  lemma at a pinned zero slot (2b + z = c mod 7; b = couplings so far,
  z = R2 zero answers so far) forces equal b mod 7 when z is equal, so
  "different number of earlier couplings" cannot even arise there unless
  the counts differ by a multiple of 7.
  Conclusion (scoped): one fixed right program serving R1 -> R2 couplings
  for inputs from DIFFERENT mod-7 cosets was not found (2 programs, 7+
  corrector combinations); within one coset the conflict is excluded by
  conservation for count differences < 7. Not a proof of impossibility.
- 07:40 CORRECTION of the entry above: the two rerun combos
  finished and N1 class 2, N2 class 1 WORKS: program
  J I J I J I N Z^7 N J I N N, classes [1,0,0,0,2,0,2,0,0,0,0,0,0,0,1,1,0,0,0],
  inputs v1 = 0 (four couplings: R2 3 -> 11) and v1 = 1 (one coupling:
  R2 3 -> 5), both end with R1 = 0 and nothing else; glider level AND
  exact CA agree with the model [sim]. The other 8 corrector pairs fail
  at J2 (controls). So my "R1 correctors cannot repair it" was wrong
  (premature, written before the run finished). Open: whether the triple
  block matters or correctors alone suffice for the single-coupling
  program (queued: J I N Z^7 N J I N N, v1 = 0, 5).
