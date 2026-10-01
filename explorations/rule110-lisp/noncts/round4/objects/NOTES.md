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
