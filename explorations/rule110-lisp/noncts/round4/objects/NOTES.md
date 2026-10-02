# objects NOTES (running log)

## 2026-10-01 22:48 UTC start
Read README, BOARD, round3 SUMMARY + THEORY, round1/2 summaries, synth/r110sat.py,
synth/encross.py, round3/verify ebg_* (E-bg = tile 1101011100, period 5, shift -8).

Idea: rather than search for crossings, compute the exact INFLUENCE CONE of a
rod's interior background. A right-to-left crossing (any width, any fuel) is a
perturbation of the interior whose left edge must travel faster than the rod.
If the cone's left edge in the E-bg is no faster than -4/15, no crossing exists
at all.

22:52 Naive edge bound (left edge moves unless bg pair (l,c) = 01) is useless:
speed -0.89 (ether) and -0.93 (E-bg). Need the exact cone (SAT).

23:05 cone.py (exact influence cone by SAT, witness re-simulated).
- Bug found and fixed: witness check padding was T+2 (needs 2T); a negative
  index silently wrapped. Now asserts index range.
- Positive control, ether: left edge speed >= -0.571 at T=56 (B at -1/2
  inside), right <= +0.679 (A at 2/3 inside). Converging as expected.
- E-bg (tile 1101011100, tper 5, shift +2): T=90 left D=-58 (speed >= -0.644),
  right <= +0.411. The LEFT cone is far faster than the rod (-4/15)!
- look.py on the T=90 witness: an expanding domain of E-bg at another phase;
  its left wall moves at exactly -3/5 (lab), i.e. -1/3 relative to the rod.
  wall_id.py: left domain phase (0,0), right domain (tg,sg) = (3,5).
  So Theorem 2's premise (L) is false in principle: E-bg carries
  right-to-left domain walls. verify's 16-cell search missed them because it
  measured deviation from ONE best-matching phase (a wall leaves a
  different-phase domain behind = non-localized deviation).
- plant_wall.py: planted the (3,5) wall in E^60, 125 cells behind the front.
  It reaches the front at t~360; the rod then disintegrates from the front
  (debris B, Ebar, Ebar, A, A, A, ?). Destructive for this wall type.
- wallsat.py: SAT for periodic walls between phases g of a background.
  Controls in ether: finds A (3,2), B family (4,-2) as ether-phase walls,
  C's (7,0), F (36,-4), E family (30,-8). E-bg scan running
  (P <= 30, W <= 40, all 50 phases): many -3/5 walls (g=(0,3),(0,6),(1,2),
  (1,3) W=12,(1,9),...), +2/5 phonons, co-moving (15,-4) cuts.

23:11 Posted first board note; I headed it 23:28 by guessing (wrong) - corrected on board. Rule: run date -u immediately before writing a header.

23:20 MISTAKE: scan_back.py PADL=T+40 let the front leave the shrinking sim window after t~742 (needs PADL > 19T/15). First run (0/99170 hits) moved to trash/; rerun with PADL=2T+100, T=1200. Spot check (pad 2000) confirms collisions do happen (E^24 -> E^25 with B etc.).

23:12-23:25
- wallsat scan of E-bg finished (1050 records): velocities only -3/5 (15 phase
  kinds), -4/15 (45), +2/5 (18, all even h). Phase group Z/50, h = 2t - 5s.
- plant.py: all 15 left-wall kinds destroy (or mostly destroy) E^45 at the
  front (T=1000). Fixed an R' coverage bug (extended source row by 30 cells).
- scan_back.py rerun (fixed padding): 2523 library left-movers (v=-1/2: 1016
  scenes, v=-1/3: 98154 scenes), every phase, vs back of E^24, T=1200:
  0 front hits. Positive control E^2: hits (Bbar, Bhat, G, GB3...), B none.
- launch_sat.py (synth Scene) free control was UNSAT -> could not serve as a
  control (free cells far from the rod + window). Rewrote as launch2.py
  (own model on r110sat.Spacetime). Controls: --overlap 10 30 (free cells
  overlapping the rod back): SAT, sim ok (88 s). Train mode, target
  'extend': SAT for even slips, solutions type as E^12 + B-train -> E^13/15/17.
- launch2 wall target, B-lattice trains WY 24/32/40, n=12, T2=160, depth 5:
  42/42 UNSAT (odd slips trivially). Scope caveat: T2=160 only lets the
  first part of a wide train act. Rerunning n=36, T2=400, WY 24/40/56.

23:50 launch2 wall target, B-lattice trains, n=36, T2=400, depth 5:
  W=24: 8/8 UNSAT (even slips + 13), W=40: 8/8 UNSAT (51-250 s each).
  W=56 started by the script, killed by PID (15960) to free the CPU.
  Controls: --overlap (SAT), --target extend (SAT, B-trains extend rod).
- interfaces at E speed (wallsat.InterfaceModel, W<=24): ether|E-bg 36 front
  types (matches shuttle's 36 tight fronts), E-bg|ether 13 backs; p12 bg
  000001110011 has fronts but no back and no successor; p20 bg has backs
  but no predecessor. So E^n is the only uniform-interior rod at E speed in
  this scope.
- p12 and p20 backgrounds: cones also two-way (left >= -0.79/-0.73, right
  <= 0.375/0.42 at T=48/45).
Started rods_scan.py (all backgrounds p<=20 x library speeds: ether
interfaces on both sides, W<=24).

00:00-00:20
- rods_scan.py (backgrounds p<=20 x library speeds, ether interfaces both
  sides, W<=24): rods with non-ether interiors: p4 0111, p6 000111, p10,
  p12, ... at A speed; p8 00010011 and p16, p18 at B speed; p9 000000111 and
  p11 00000010011 STATIONARY; p11 00001011111 at D speed; E-bg at E speed.
  (p17/p19/p20 entries are glider gases in ether.)
- rodsat.py: face-free stationary rods tile^k for p9 and p11 (6 variants
  each), stable for k + 1, 2, 5, 10 extra tiles. p9 variant 100000110 has
  slip 5 per tile: a tight C1 stack (a "C-stack").
- walls in p9 and p11 (P<=28, W<=30): ONLY stationary walls (59 / 71 phase
  kinds). Lattice forces |D| multiple of 9 (11), so moving walls need
  longer periods; cones are two-way (p9 left >= -0.98, right <= 0.34).
- srod.py reaction table, C-stack S9 (100000110)^k, k=6, every phase:
  from the LEFT A, A^2, A^4: one tile removed at the left face (+ F, Ebar,
  E emitted back to the left); D1, D2: two tiles removed. Single class (as
  for any A/B/D-lattice vs stationary pair). From the RIGHT, B, B^2, B^3:
  the WHOLE stack is destroyed (right-to-left destruction cascade), debris
  varies with k (k=2: S^1 and nothing else).
  MISTAKE: first measure overcounted tiles by 1 (face cells continue the
  pattern); now normalized by the rod-alone baseline at the same T.
- S1 (s1_pass.py): first run gave one SAT (sc=2, sh=8) that was a FALSE
  POSITIVE: the head (a single A at its window edge) was absorbed into c',
  and synth's Reaction 'is h' matched h as the phase jump at c' 's right
  edge (the 'is' region includes the band next to the middle); verify_
  reaction passes because the far side is pure ether. Caught by typing the
  witness (no A ever emerges; ether phases right of the cell never change).
  Fix: the band between c' and the far region must be ether of the phase
  on the head's near side. Control for the fix: far side = one library A
  (--outA): SAT for C2/C1/C3 slips with an 8-A head (the known fuel
  crossing). Old file in trash/. Rerunning S1.

00:25 S11 stack table: from the left A is absorbed (stack shifted 2, face
change), A^2 -1 + F, A^3/A^4 -1 + Ebar, D1/D2 -1; from the right B family
and Bbar destroy it. C-stacks: clean DEC from the left with a backward
answer glider; fragile from the right.
S1 A_24_12 running ~30 s per even-slip instance (odd slips trivially UNSAT:
A-lattice trains carry slip 8k = even).
Queue (run_queue.sh, PID file run_queue.pid): S1 B_24_12 -> bouncer prune
(scene R alone, scene L alone; W 22/22, walls 16, T2 180) -> S1 30/16 ->
long-period walls in p9/p11 (P 29..63).
[arg] Layout reasoning: with both rods moving the same way, Theorem 1 needs
clean in-rod signalling left->right in R1 AND right->left in R2. E^n gives
only left->right (phonons). So R2 needs a different rod type with a clean,
glider-launched right->left channel (or R2 is not a rod).

00:25-00:32 (header corrected: I first wrote a guessed 00:40-01:00)
- fronts_walls.py: 7 front types (left ether phase c = 2,4,7,8,10,12,13;
  c=12 W=12 is the standard one). 105 (front, left-wall) pairs: 2 clean
  (c=7 and 13 with wall (1,9), W=38 compound wall containing an ether pocket).
- MISTAKE 1: first "clean" criterion compared T and T+15 only; I then
  worried the product shrinks (show() lengths 143/141/139 at 700/900/1100)
  - that was the time-phase dependence of the displayed length; rows at 700
  and 1000 are identical shifted by -80. Criterion now T vs T+300 (D=-80).
- MISTAKE 2 (posted, corrected on board): I called the product's interior a
  new background X (0000100011) from its look at one time; it is the E-bg at
  phase (3,9). Window-by-window phase map now part of the check.
- Result: E^n (front type 7) + bubble wall (1,9) -> clean E-rod, phase
  (3,9), 27 cells shorter (~8 units), front type 4; n = 30..60 (11 values).

00:40 backs_scan.py: MISTAKE: stability check indexed b2 with negative indices (wrap) near the window edge -> false 'unstable'; margins fixed (420).

00:33-00:45
- launch2 K=0 (40 free cells entirely right of the back, T2 160): SAT, but the
  witness destroys the back (A, A^2, C1, Ebar debris). The phase-domain target
  is too weak for arbitrary content; K=2..8 skipped (records marked skipped).
- backs_scan.py: 11 back types (c = 1,2,3,4,5,7,9,10,11,12,13), all stable
  rods; B family x all phases: 0 front hits (E^24, T=1200). No positive
  control specific to this script (E^9 too short for the construction, E^12
  gives no hits); detection code = scan_back.py's.
- srod_all.py: all 12 face-free stacks x 7 left + 9 right gliders. Several
  "clean-looking" outcomes (p9 v3 + A: +1 tile; p11 + F: -1; p11 + Ebar: -3;
  p11 v0 + G: -1 + A^3), BUT srod_check.py (product == canonical stack of k+dk
  tiles, single object) fails for all phases: the faces change type. So my
  run-length measure is only a coarse indicator; C-stack op algebra not
  established.
- S1 A_24_12: 0/196 SAT.
- bouncer L (B head 30, wall 28 restored, A head out 30, T2 200): ~73 s per
  slip combo (98 combos). L-scene control (bL_ctrl.py, wall may change, out =
  free A-lattice slip 8 + separation): running.
