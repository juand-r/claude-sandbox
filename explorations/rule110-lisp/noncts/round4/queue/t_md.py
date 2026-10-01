from lscene import *
import numpy as np
for tape in ("YYNN", "NYYN"):
    m = Machine(tape, ["YNNNNN"], 40000, left_periods=3, right_periods=2)
    K0 = [a for n, a, b in m.blocks if n == "K"][0]
    G = [a for n, a, b in m.blocks if n == "G"][0]
    for t, cs in trace(m, m.row, [31500], K0 - 4000, K0 + 100):
        print(tape, t, "G at", G - K0, len(cs), " ".join(f"{k}{a-K0}:{b-a}" for a, b, k in cs))
