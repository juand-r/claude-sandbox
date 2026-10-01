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
- 23:12 frontsim results (exact sim, E^10 and E^11, every class, T 700,
  rod check = exact equality with the background shifted by K units at
  the front and J at the back; left/right products named):
  * A-trains w <= 30 (6398): only K in {-1,0,1,2,3} with NOTHING emitted
    (22 INC trains, 68 "eaters" with K = 0, 47 DEC, 22 DEC2, 1 DEC3);
    no wall survivors (J != 0 never clean), no emission.
  * D-trains (10,2) w <= 30 (1071), stationary (7,0) w <= 34 (4877): no
    clean outcome at all (every one destroys/dumps the rod).
  * Library right-movers (libscan.py, 368 objects incl. compounds, n = 8..11,
    all classes): no X with "rod + left-movers only" for all n. 21 (X, cls)
    DUMP the whole rod into a left-moving B-train (D1 x3 classes, D2, C2,
    C3, C-compounds, F).
  * SAT (pert.py, wall-free, all n >= ~10 at once): A-trains w <= 32 all
    UNSAT for G output, K = 1, 2, -1, all phiL (w 24); w 40 K=-1 phiL 6
    UNSAT (57 s). Cost grows fast with w.
- 23:15 [sim] MERGE: D1 + R1 (E^n, from the gap side) in 3 of 5 classes
  turns R1 into a left-moving B-train of n+1 B's, which fuses into R2's
  back: E^m | D1 | E^n -> E^(m+n+1), i.e. y := y + x + 2 (values), R1
  destroyed. dump2.py: n = 3..12, m = 1, 2, 3, 6, gaps 150/200/207, all
  exact; D1 classes 2 and 4 give debris (controls). Costs a counter (the
  right stream then acts on the merged rod), so not a shuttle; noted for
  theory (bulk transfer is outside Theorem 1's bounded-change premise).
- 23:16 fronts.py: all (15,-4)-periodic front terminations of the rod
  crystal. Within 12 cells: only the standard front. Within 24 cells:
  41 rows, 36 NEW tight terminations (stdfront.py). Sweep of A-trains
  (w <= 22) against each new front running (run_fs2.sh).
- 23:21 backscan.py (library left-movers vs E^n BACK, every class; Y
  placed right of the rod). BUG found by its positive control: BG.phi_right
  was (pr - W) instead of pr (wrong for W not = 0 mod 14); fixed in
  pert.py. Not used by frontsim/pert before (they only use phi_left and
  bg cells), so earlier results are unaffected. Also the right span was
  too short for right-moving products (A's left the valid region); fixed.
  Control now matches the catalog: B -> +1; Bbar 3 classes (+2 & A,
  -1 & A^2A^2A, -3 & A A A, labels rotate with n); G/GB1/GB2 -> -1 &
  A^3/A^2/A class-free.
- 23:23 decorated fronts (first 12 of 36): A-trains w <= 22 give only
  K = 0 "eaters" (nothing emitted, rod unchanged); not even a DEC.
- IDEA (gap-collision pump): R2's back emits a fast + slow right-mover
  pair; they collide mid-gap at a fixed distance from R2's back, emitting
  Y back to R2 (a self-clocked loop attached to R2's back) and an A that
  DECs R1. Needs no front emission. Catalog has many right-mover pair
  collisions that emit left-movers (e.g. A^4 + H #14 -> G + D1,
  D1 + H #12 -> G + A + A, D2 + C3 #0 -> B^3 + A). Needs the back table.
