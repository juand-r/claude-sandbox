"""Do the next symbol's C's reach the reader in the same class in the
acceptor path (YYNN, after crossing E0) and the rejector path (NYYN)?
Lab-frame C positions relative to K0's Ebar-frame origin, sampled every
210 steps (lcm of 7 and 30) as they approach P."""
import numpy as np
from lscene import *
from census import census, MAX_DT
for tape in ("YYNN", "NYYN"):
    m = Machine(tape, ["YNNNNN"], 34000, left_periods=3, right_periods=2)
    K0 = [a for n, a, b in m.blocks if n == "K"][0]
    r = Run(m.row, m.origin)
    out = []
    for t in range(31920, 33600, 210):
        r.step(t - MAX_DT - r.t)
        sh = r.ebar_frame(t)
        lo = K0 - 400 + sh
        h = r.history(lo, lo + 460, MAX_DT)       # lab-fixed window
        cs = [(a - 400, k) for a, b, k in census(h) if k == "C"]
        out.append((t, cs))
    print(tape, out)
