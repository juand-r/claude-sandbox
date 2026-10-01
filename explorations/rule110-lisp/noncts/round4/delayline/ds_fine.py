"""Fine sweep of the drift switch around the anomaly found by ds_sweep.py
(gap 1200, tz = 55500 gave W at 78.0, off the walk sequence). Z_L times are
quantised to P_E = 15 steps by the rigid left stream, so step 15 covers
every arrival. Exact CA. Prints each tz with W's final intercept.
Usage: python ds_fine.py GAP TZ0 TZ1"""
import sys
import ds
from ds import *  # noqa
gap, t0, t1 = (int(a) for a in sys.argv[1:4])
ds.GAP = gap
seq = {round(3.33 + w, 2) for w in [0.0, 24.27, 44.8, 69.07, 89.6, 113.87, 134.4, 158.67, 179.2, 203.47, 224.0]}
for tz in range(t0, t1 + 1, 15):
    sc, T = scene(0, tz, c=2)
    ok, prods = ca(sc, T)
    d = describe(prods)
    tag = "" if (len(d) == 2 and d[1][0] == "E" and d[1][1] in seq) else "  <-- off-sequence"
    print(tz, d, tag, flush=True)
