# gate (round 2): making zero answers act on the program stream

What: branch on data in the Rule 110 E^n counter driven by a rigid G-speed
packet stream (round-1 GB3 = DEC, GB4 = NOP, GB5 = INC), with no cyclic tag
system. Running log, including mistakes: NOTES.md. Plan: PLAN.md.

Results (details in NOTES.md and ../BOARD.md):
- Slip lemma [arg]: the E^n counter's net change is fixed mod 7 by the
  stream and the leftover objects. A garbage-free branch can change the
  counter only by multiples of 7 relative to the other branch, and every
  clean answer conversion satisfies e(Y) = e(X) - 1 (mod 7).
- Wrap packet Z6 = GB3@(0,0)+GB4@(-25,46) [sim]: a DEC whose zero answer
  shatters the trailing GB4 into 6 B's, so 0 -> 6. Garbage-free and
  non-monotone (M1).
- Left garbage J = GB1@(0,0)+GB1@(-1,36) [sim]: INC, but at zero a Bbar
  leaves to the left and the counter stays 0. Zk = J^(6-k) Z6^(7-k) is
  "DEC with wrap to k". J at zero displaces the counter; L = GB1+GB1@(-4,34)
  undoes four J's, and a GB4 that meets zero can correct phases.
- Fixed programs (same text for every input) [sim, exact CA]:
  (Z6 N)^10 computes (v-10) mod 7 for v = 0..9; (J^4 L Z6^6)^8 computes
  v mod 2 for v = 0..8 (M2).

How to run (from this directory; imports ../../collider read-only):
- python rafast.py PROGRAM VMAX --dfs     search per-slot classes (glider level)
- python verify_ra.py PROGRAM CLASSES VMIN VMAX [--control S:C]   exact CA check
  e.g. python verify_ra.py ZNZNZNZNZNZNZNZNZNZN 0,1,0,1,0,0,1,0,2,0,0,0,1,0,2,0,0,0,1,0 0 9
- python wrapcheck.py 'GB3@(0,0)+GB4@(-25,46)'   counter action, n = 1..9
- python test_fastca.py ; python test_cacheck.py   checks of the exact CA window
Op letters: I = GB5, N = GB4, D = GB3, Z = Z6, W = GB3+GB5@(-14,40),
X = GB5+GB4@(-4,56), J/K/L/M/P = GB1+GB1 pairs (stream.ALIAS).

Older tools (per-input compilation, see the NOTES correction at 01:3x):
stream.build/build2, adaptive.py, fastsearch.py, test_wrap.py, diff_test.py.
Scans: scan_counter.py (counter_scan.json), list_clean.py (clean_list.txt),
units.py, analyze_scan.py, semantic_search.py.
