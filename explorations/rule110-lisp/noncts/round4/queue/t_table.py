from lscene import *
for tape in ("YYNN", "NYYN"):
    m = Machine(tape, ["YNNNNN"], 20000, left_periods=3, right_periods=2)
    K0 = [a for n, a, b in m.blocks if n == "K"][0]
    print([(n, a - K0, b - K0) for n, a, b in m.blocks if -800 < a - K0 < 800])
    for t, cs in trace(m, m.row, [600, 6000, 7000, 8000, 8500, 9000, 10000, 11000, 12000, 13000], K0 - 700, K0 + 200):
        print(tape, t, " ".join(f"{k}{a-K0}" for a, b, k in cs))
