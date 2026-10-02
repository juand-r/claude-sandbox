"""W3 follow-up: the window E^j at (dt, g) against R1 = E^n for many n."""
import sys, json
sys.dont_write_bytecode = True
import w3scan as W
from pert import BG
j, dt, g = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
for n in range(int(sys.argv[4]), int(sys.argv[5])):
    bg = BG(n, W.T + 60, -2 * W.T - 800, 4 * n + 2 * W.T + 400)
    for (dt2, g2), row, span_lo in W.window_rows(j, n, bg):
        if (dt2, g2) == (dt, g):
            r = W.analyse(row, span_lo, bg)
            print(n, r["kind"], r.get("prods"), r.get("front"), r.get("back"),
                  [W.h_of(v) for v in (r.get("back") or [])], flush=True)
