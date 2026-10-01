# address: running log (round 2)

Task: two independently addressable registers in Rule 110 (or universality
without addressing), without emulating a cyclic tag system.

## Plan
- [ ] 1. Read round-1 material (SUMMARY, architect ARCHITECTURE s.4/s.9, notes of all agents). 
- [ ] 2. Two F-pair registers in the Ebar lane, addressed by collision class:
      3 markers T (front), M (middle), P (back); reg1 = T-M, reg2 = M-P.
      Catalog-level BFS (architect's winding3.cross/apply generalized) for
      mover sequences with net (dD1, dD2) = (+-U, 0) and (0, +-U).
- [ ] 3. Verify candidates by full Rule 110 simulation, with a negative control.
- [ ] 4. Fixed-stream version (balanced drift for all instruction types).
- [ ] 5. Zero test / combination with gate's work (M3 direction).
- [ ] 6. Final board post + report.

## Log
- 23:30 Read round-1 material. Key constraints: G packets cross only A;
  G reflects off Ebar (mirror); nothing crosses E^n; Ebar-speed packets
  never meet E^n (same speed).
- 23:45 [arg] Consequence (right-only program): the frontmost E^n seals
  everything to its left; everything upstream (right) of it must be
  G-transparent, and only A's are. So E^n technology gives exactly one
  register unless the program has a second source (left stream) or
  messengers. Hybrid E^n + F lane fails for speed reasons (architect s.9).
- 23:50 tworeg.py/graph.py/cycles.py: 3-marker F lane (T, M, P), all 1488
  catalog movers (Ebar-speed gliders/2-packets x classes), catalog-level
  prediction (architect's cross()). 144 residue-pair nodes, 3606 clean
  edges. SCCs with cycles: sizes 16,2,2,1,... Reduced edge labels per
  SCC are only {(0,0)}, {(0,0),(-1,1)}, {(0,0),(-2,0)}, {(0,0),(1,0)}.
  => [sim-catalog, exhaustive over catalog movers] no F-pair register
  can be both INC'ed and DEC'ed when any third F follows it in the lane,
  and register 2 can never change alone. Architect's INC/DEC destroy a
  third F in all 12 residues (probe_inc.py). The F counter is a
  "last in lane" object.
- 00:05 simcheck.py [sim]: architect INC on a lone pair MATCH (control);
  same INC with a third F behind (3 residues): third F destroyed, B/G/A
  debris, as predicted. Graph self-loop mover Ebar@(0,0)+Ebar@(-11,37)
  @(-16,63) on 3 F's at (35,43)/(35,43): reg2 gap constant (47.11),
  reg1 grows per application; MATCH with prediction for x1, x3. (One
  direction only: no DEC1 exists in that SCC.)
- cmsg.py: C messengers (stationary, met by the F's) wind ONE F pair
  (labels -20,-2,2,6), but with 3 F's only (0,0)/(2,0): also last-in-lane.
- F compounds as control: F_19_F + Ebar is clean in 1/12 classes only
  (and splits into F,F); 0.25 s/collision; full compound catalog ~3h: not run.
- 00:20 cgraph F 4 (two separate pairs, 1728 nodes, 16626 edges): every SCC
  has reduced labels in {(0,0,0)}, {(-2,0,0)}, {(1,0,0)}. Same verdict as
  3 markers: no reg2-only change, no bidirectional reg1. [catalog-exhaustive]
- Idea: F-world needs ABSORBERS (debris sinks). Catalog: F + Ebar-pair -> F
  alone exists (Ebar@(0,0)+Ebar@(-26,27)#4, Ebar@(0,0)+Ebar@(-9,29)#4).
  Test: allow absorption (empty output) at markers in the graph.
