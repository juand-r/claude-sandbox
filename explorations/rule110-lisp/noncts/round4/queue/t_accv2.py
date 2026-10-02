from lscene import *
import encoder as enc
from reads import rewrite2
v2 = 2 * enc._left_v(["YNNNNN"])
for tape in ("YYNN", "YNYN"):
    m = Machine(tape, ["YNNNNN"], 48000, v=v2, left_periods=3, right_periods=2)
    K0 = [a for n, a, b in m.blocks if n == "K"][0]
    for t, cs in trace(m, m.row, [47460], K0 - 600, K0 + 100):
        print(tape, t, " ".join(f"{k}{a-K0}" for a, b, k in cs))
    r = Run(m.row, m.origin); r.step(47460)
    row = r.window(0, r.width)
    new = rewrite2(row, m.origin, 47460, K0 - 104, K0 - 2, [])
    print("identity rewrite equal:", new is not None and (new == row).all())
