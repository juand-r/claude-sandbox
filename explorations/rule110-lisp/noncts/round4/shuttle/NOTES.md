# shuttle: running log (round 4)

Labels: [sim] exact Rule 110 run, [arg], [thm], [hyp].

## 2026-10-01
- 22:48 read BOARD, README, round3 SUMMARY, THEORY (s.2.2, 3.6, 6, 7, 8),
  coupler README/NOTES, synth NOTES.
- 22:55 rod.py: E^n rows (built E + (n-1) B, settled) are PREFIXES of
  each other (fronts identical). [sim] The rod interior is a crystal:
  invariant under (5,2) and (15,-4) (checked on E^12, t = 20..60). One
  unit = u = (5,2): removing K units at the front (or adding K at the
  back) = that boundary moved by K u; leftstream's A_DELTA = (5,2) agrees.
- 23:00 pert.py: perturbation SAT around an exact BACKGROUND spacetime
  (rod alone), cells outside a moving window forced to the background.
  The window's right edge sits 30 cells inside the rod, so solutions are
  wall-free and valid for every larger n (no n-dependence possible).
  Controls [sim, verify.py]: (1) A DEC (K=1, Y allowed empty): SAT, exact
  match for n = 3..13 (n = 2 differs, as expected: A + E^2 -> E in all
  classes, another geometry); (2) G-train moving away (X = (42,-14) train,
  K = 0): SAT only for phiL = 4 (slip 4 = G), verify: Y = G, periodic.
- 23:02 First front grid (A-train X width 24, Y in G family, K = 1, 2, -1,
  all 14 phiL, T 360, depth 30): all UNSAT (0.3 s each). Control at the
  same parameters (A DEC, Y may be empty): SAT.
- MISTAKE 23:03: launched wx 40/60 runs with phiL = 1. A-trains have even
  slips only (trains.py found no odd-pR (3,2) trains), so odd phiL are
  impossible and the solver churned 6+ min. Killed (PIDs 3836 loop, 3837,
  5316). Rule: restrict phiL to the parity allowed by the X family.
- 23:05 trains.py: SAT enumeration of all (3,2) trains of width <= 30
  (start in the first tile, deduped by trimmed bits): 6398 (even pR only).
  frontsim.py: exact simulation of each train vs E^10, E^11 fronts in all
  3 classes; tests rod survival with front shift K and back shift J (wall)
  and names the left products. Control: single A gives K = 1 in exactly one
  class for n = 6, 7, 10, 11; A^2, A^3 give no clean outcome (catalog
  agrees: A^3 is n-dependent).
