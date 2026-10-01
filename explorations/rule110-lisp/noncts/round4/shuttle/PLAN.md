# shuttle (round 4) plan

Avenue (a): a shuttle between R2 (left, back faces the gap) and R1
(right, front faces the gap). Needed: a right-mover X and a left-mover Y
(faster than E: B family (4,-2)/(12,-6) or G family (42,-14)) with
  R1 front:  X + E^n -> E^(n-K) + Y   (for all large n, no wall)
  R2 back :  E^m + Y -> E^(m+K) + X   (for all large m)
plus d1 = d2 mod P_E and a cycle of valid classes (THEORY s.6.1).

Steps
- [ ] 1. Physics of the rod front: catalog + simulation; locality of
      left-moving emissions (no back -> front influence).
- [ ] 2. Perturbation SAT around a BACKGROUND spacetime (long rod), moving
      window, cells outside forced to background: no walls, valid for all
      n >= n_min automatically. Positive controls: A DEC, I_L-like INC,
      known catalog emissions.
- [ ] 3. Front-face searches: X in A (3,2), D (10,2), C (7,0) families,
      Y in B and G families, K in {-2..3}; widths well beyond 30.
- [ ] 4. Back-face table: library G packets that reflect class-free at
      R2's back (+k, emit A^j) -> what X the front must turn into Y.
- [ ] 5. Close loops; multi-step (helpers, two-speed signals); simulate
      several round trips exactly; then stop/reversal and start.
