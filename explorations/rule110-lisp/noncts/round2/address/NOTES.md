# address: running log (round 2)

Task: two independently addressable registers in Rule 110 (or universality
without addressing), without emulating a cyclic tag system.

## Plan
- [x] 1. Read round-1 material (SUMMARY, architect ARCHITECTURE s.4/s.9, notes of all agents). 
- [x] 2. Two F-pair registers in the Ebar lane, addressed by collision class:
      3 markers T (front), M (middle), P (back); reg1 = T-M, reg2 = M-P.
      Catalog-level BFS (architect's winding3.cross/apply generalized) for
      mover sequences with net (dD1, dD2) = (+-U, 0) and (0, +-U).
      RESULT: impossible with crossings only; possible with absorption.
- [x] 3. Verify candidates by full Rule 110 simulation, with a negative control.
- [x] 4. Fixed-stream version (balanced drift for all instruction types).
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
- 00:40 KEY: allowing absorption (F + Ebar pair -> F) makes the 3-F graph one
  SCC (144 nodes) with all directions. tworeg_abs.py: DN2/UP2/DN1/UP1 verified
  by full simulation 6/6 exact, no junk; controls control_abs.py 6/6 fail.
  Mechanism: pairs pass some F's and are swallowed by one F (kick).
  Mistake: first gap formula had the wrong sign (x0 - t0/9); fixed to x0 + t0/9
  (position at t=0 for v=-1/9); caught by the arithmetic mismatch.
- 01:00 killed balance.py 5 (PID 7535): superseded by fixed_stream.find_pads (NOP = DN2+UP2 / DN1+UP1 combos).
- 01:05 fixed_stream.py: NOP padding = DN2+UP2 / DN1+UP1 combos; pads
  UP2 0, DN2 +NOP_A, DN1 +NOP_B, UP1 +2 NOP_B (all drift keys equal mod L_FE).
  MISTAKE: first build overlapped movers at t=0: kicks move T by up to ~1000
  cells per slot, so the drift DIFFERENCE between instructions (a lattice
  vector with a large P_Ebar part) reorders slots unless the stream has idle
  space; added EXTRA = 150 idle F periods per slot. UP1 UP1 DN2 -> OK [sim].
  Batch run_fixed.py (5 random length-5 programs + 2 unbalanced controls)
  running, PID in run_fixed.pid.
- 01:10 verify re-ran tworeg_abs independently: 16/16, controls 9/9 fail.
- 01:15 zero_probe.py [sim]: driving a register down: at gap ~26 (DN^5 from
  119) the catalog still predicts clean but the CA forms a compound
  (F_15_F#4 for reg1, F_18_F#5 for reg2) = multi-body regime. DN2^6: reg2's
  two F's become ONE stationary C2 (+Ebar debris), T intact: a destructive
  zero answer that is a stationary messenger. Not developed further.
- 01:40 run_fixed.py: 4/5 random fixed-stream programs OK; #5 (DN2^4 UP1,
  reg2 at -4 units = 43.8 cells) FAILED (debris, one F). Diagnosis
  (range_check.py, diag_fixed.py, dips.py): DN2^4 prefix is exact; relative
  DN2^5 UP2^5 (25.1 cells) exact, DN2^6 fails; instructions have internal
  dips up to 38.9 cells (padded DN1), so UP1 at 43.8 dips to 23.6 < ~25-cell
  multi-body threshold. => working range: values >= -2 units from the
  start (gap >= 81). Program #5 was outside the range; not a design flaw of
  addressing, but the register "zero" must sit >= ~64 cells.
  CORRECTION of my 01:15 note: "F_15_F#4 / F_18_F#5 compounds form at DN^5"
  was a NAMING artifact: collider's typer names two F's ~25 cells apart as a
  compound; split into parts they are exactly where predicted.
- run_fixed2.py: programs restricted to >= -2, + controls (PID file).
