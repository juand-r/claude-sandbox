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
