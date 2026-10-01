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
