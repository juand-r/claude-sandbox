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
- 23:33 verify re-ran MERGE independently (120/120). theory: MERGE + blind
  streams = one multiplier; needs a switchable second rate.
- 23:35 [sim] the D1 dump is a traveling wave: it reaches the rod's back
  5 steps later per extra unit (n = 8..20), i.e. a dissolution boundary
  with period V = u = (5,2) (lab velocity +2/5, the phonon speed objects
  found), eating one unit and emitting one B per 5 steps. So the dump is
  a "front gun" with j = 0 in V = u + j(15,-4).
- backscan_all.jsonl done (2523 library left-movers x classes, n 8..11):
  'spawn' reactions exist (G pairs -> rod - 1 + Ebar_8_Ebar class-free;
  GB1+GB2@(-41,38) -> rod + E-pair compound), none spawns a clean single E.
  2721 entries unsettled at T = 900 (G-speed packets placed 40 cells
  away need ~600 steps to arrive): rerun those with a closer start later.
- NEXT: gun SAT (gun.py): periodic structure at a rod face with period
  V = K u + j P_E emitting a B-train (front gun) or A-train (back gun).
  Positive control: the dump wave (front, K = 1, j = 0).
- 23:38-23:46 gun.py: SAT for face structures periodic under
  V = K u + j P_E emitting one glider per cycle. Controls: front j = 0
  (B out) 6 SAT, all verified 8 cycles by exact sim (the dump wave);
  back face with an INCOMING B-train j = 1, 2: SAT, verified. A first
  version built the glider train from seeds far from the window (the
  "train" next to the window was plain ether): verify_gun caught it
  (periodicity failed 7/7); fixed (train_seeds picks seeds near the
  window). Results: front guns (B out, K = 1) j = 1, 2, 3 (window 16+16):
  UNSAT for every train placement; back guns (A out, K = 1) j = 0
  (impossible, A's overlap), 1, 2: UNSAT (window 20+20). Batch stopped by
  me during back j = 3 to free the CPU for the bouncer tables. MISTAKE:
  killing the python child before the shell let the shell start j = 4;
  killed that orphan (15690) too. Rule: kill the parent shell FIRST.
- 23:45 bouncer tables started (run_bounce.sh: L-table 391 B-trains x 193
  walls, then R-table 1863 A/D-trains x 193 walls; T = 500).
- 00:01-00:11 bouncer tables (lead 23:46: shuttle owns them). bounce.py
  raw tables done; export.py -> bounce_table.jsonl (435,022 rows; format
  in its docstring). First export treated 2 stationary products as dirty;
  the typer names C2+C1 at distance 21 either as C2_18_C1 or as two
  objects depending on the copy -> 1,131 spurious inconsistencies;
  fixed by taking all stationary products as the new wall. After the fix
  consist.py: 278 inconsistencies, all "settled vs unsettled at T=500";
  no physics contradiction (single class holds on 73,500 physical pairs).
  The cached exporter was checked identical to the uncached one on the
  L-table before use. cycles_quick.py: no perpetual bouncer in the tables.
  frontier.py running (heads produced but not listed, all classes);
  control: list heads through frontier's scene give the table outcome
  (8/8).
- 00:27 MISTAKE: ran the pert.py B/Bbar-output SAT loop next to frontier.py
  (two heavy processes; lead asked to serialise). Killed the loop (shell
  25364 first, then 29928/29929). Partial results in front_B.jsonl.
  frontier_L.jsonl complete (heads produced by R-reflections, all classes).
  run_ext.sh running: physical heads x 291 produced walls (walls_frontier).
- 00:2x front SAT with B (4,-2) and Bbar (12,-6) outputs (A-trains w <= 30,
  T 220, wall-free, all even phiL): UNSAT for K = -2, -1, 1, 2, 3 (B) and
  K = 1, 2 (Bbar) [partial: loop killed, 47 of 70 runs; K=-1 B 6/7,
  Bbar K=2 6/7]. Control in the same code: a B-train moving away (K = 0)
  is SAT for phiL 2, 4, 10, 12 and verify.py confirms Y = B (n = 5..7).
- 00:28-00:52 extension tables (run_ext.sh): 193 physical B-trains (L) and
  857 physical A/D-trains (R) x the 291 wall types that reflections
  produce but the 20-cell list lacks (walls_frontier.jsonl): ext_table.jsonl
  305,550 rows (L reflect 2,503; R reflect 105,867). cycles_nd.py over
  bounce_table + frontier_L + ext_table (361 physical walls, multi-class
  heads treated nondeterministically): 0 cycles.
- Hybrid check (R2 = E^n back, R1 side = stationary wall) [sim, tables]:
  the trains R2's back returns for G, GB1, GB2 (A^3, A^2, A) reflect at
  walls only into Ebar or F (559 + 301 + 171 + 171 + 114 rows), never into
  a G-family packet; Ebar (E speed) and F (slower) never reach R2's back.
  So no hybrid loop at this level.
- bounce_table_L.jsonl (intermediate, old classification) moved to trash/.

## Reflection (00:52)
- Went well: the background-spacetime SAT (pert.py) and exhaustive
  simulation (frontsim.py) gave a clean, two-method answer for the E^n
  front; the gun SAT recovered the dump as a positive control; the
  bouncer tables were reusable by theory/verify within minutes because
  the format was agreed first.
- Mistakes (all logged above): odd-phase SAT jobs (impossible parity);
  BG.phi_right bug (caught by the backscan control); vacuous compare
  ranges in frontsim (caught by an assertion); far-away glider train in
  gun.py (caught by verify_gun); typer compound naming split
  (consistency check); two heavy processes twice (gun child before
  parent; pert loop next to frontier); several guessed timestamps
  corrected. Rule kept: positive control first, parent shell killed
  first, date -u for every stamp.
- 01:09 route 23 (lead): W4 = w4.py (joint three-class back SAT, pinned
  background, A-family outputs, Delta via w4_delta.py). Bugs on the way:
  X region must start right of all three shifted backs (gap was inside
  the k = 2 rod); X region must be >= ~27 wide (leading ether offset of
  the train's time phase); window right edge must allow A's emitted from
  t = 0 (generous line); depth 56 exceeded E^16 (whole rod shifted ->
  every d rejected; first batch killed and restarted with N = 30).
  Control passes (Bbar-type, Delta -6/+1/-6 at E^30 and E^23).
  W3 = w3scan.py windows: no clean n-independent back-changing contact.
