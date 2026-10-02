"""Earliest T at which the Ebar-frame window [K-250, K+240) is static
(equal to itself 300 steps later) after the answer reaches K."""
import numpy as np
from lscene import *
for tape, tin in (("YYNN", 14010), ("NYYN", 11010)):
    m = Machine(tape, ["YNNNNN"], tin + 3000, left_periods=4, right_periods=3)
    K = [a for n, a, b in m.blocks if n == "K"][0]
    r = Run(m.row, m.origin); r.step(tin)
    ws = {}
    for T in range(0, 2101, 30):
        sh = r.ebar_frame(); ws[T] = r.window(K - 250 + sh, K + 240 + sh).copy(); r.step(30)
    st = [T for T in ws if T + 300 in ws and np.array_equal(ws[T], ws[T + 300])]
    print(tape, tin, "static from T =", min(st) if st else None)
    for t, cs in trace(m, m.row, [tin, tin + 300, tin + 600, tin + 900], K - 250, K + 240):
        print("  ", t, " ".join(f"{k}{a-K}" for a, b, k in cs))
