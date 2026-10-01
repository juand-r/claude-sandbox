from lscene import *
for tape in ("YYNN", "YNYN"):
    m = Machine(tape, ["YNNNNN"], 40000, left_periods=3, right_periods=2)
    K0 = [a for n, a, b in m.blocks if n == "K"][0]
    for t, cs in trace(m, m.row, [28000, 30000, 31500, 33000], K0 - 1500, K0 + 200):
        print(tape, t, " ".join(f"{k}{a-K0}" for a, b, k in cs))
