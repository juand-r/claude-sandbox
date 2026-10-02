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
