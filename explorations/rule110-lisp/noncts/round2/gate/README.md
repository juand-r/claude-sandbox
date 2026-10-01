# gate (round 2): making zero answers act on the program stream

What: branch on data in the Rule 110 E^n counter driven by a rigid G-speed
packet stream (round-1 GB3 = DEC, GB4 = NOP, GB5 = INC), without a cyclic
tag system. Log of everything (including mistakes): NOTES.md. Plan: PLAN.md.

Main results (details in NOTES.md and on ../BOARD.md):
- Slip lemma [arg]: the E^n counter's net change is fixed mod 7 by the stream
  and the leftover objects, so a garbage-free branch can only change the
  counter by multiples of 7 relative to the other branch.
- Wrap packets [sim]: Z6 = GB3@(0,0)+GB4@(-25,46) is a DEC whose zero answer
  shatters the trailing GB4 into 6 B's: 0 -> 6. Garbage-free, non-monotone.
- Left garbage [sim]: J = GB1@(0,0)+GB1@(-1,36): INC, but at zero a Bbar
  leaves to the left and the counter stays 0.
- Zk = J^(6-k) Z6^(7-k) = "DEC with wrap to k"; k = 1 is a parity counter.

Scripts (run from this directory; they import ../../collider read-only):
- scan_counter.py: E^n + every A-absorbing G-speed packet (counter_scan.json)
- analyze_scan.py, list_clean.py (clean_list.txt), units.py: tables
- wrapcheck.py P...: E^n + P, n = 1..9, all classes (direct CA)
- stream.py: build fixed streams (designated classes), run with glidersim +
  exact CA (full engine row, or fastca moving window)
- fastca.py (+ test_fastca.py, test_cacheck.py): exact windowed Rule 110
- test_wrap.py M [--ca]: input v (v GB5's) then Z6^M, v = 0..8
- adaptive.py PROGRAM VMAX: per-slot class search for a fixed program
- semantic_search.py: which op words compute parity (no physics)
