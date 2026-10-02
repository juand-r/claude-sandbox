"""Find t_in for VMULT=2 at which the scene near P_1 equals the default-v
scene at 31500 (cell-exact Ebar-frame window [K0-600, K0+600])."""
import numpy as np
from lscene import *
import encoder as enc
for tape in ("NYYN", "NNYY"):
    v1 = enc._left_v(["YNNNNN"]); 
    m1 = Machine(tape, ["YNNNNN"], 40000, v=v1, left_periods=3, right_periods=2)
    K0 = [a for n, a, b in m1.blocks if n == "K"][0]
    r = Run(m1.row, m1.origin); r.step(31500); sh = r.ebar_frame()
    w1 = r.window(K0 - 600 + sh, K0 + 600 + sh).copy()
    m2 = Machine(tape, ["YNNNNN"], 60000, v=2 * v1, left_periods=3, right_periods=2)
    K02 = [a for n, a, b in m2.blocks if n == "K"][0]
    r2 = Run(m2.row, m2.origin); r2.step(44000)
    found = None
    for t in range(44000, 52000, 30):
        sh2 = r2.ebar_frame()
        w2 = r2.window(K02 - 600 + sh2, K02 + 600 + sh2)
        if np.array_equal(w1, w2):
            found = t; break
        r2.step(30)
    print(tape, "K0", K0, K02, "t_in for 2v:", found)
