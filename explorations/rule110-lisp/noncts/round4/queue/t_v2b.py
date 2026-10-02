from lscene import *
import encoder as enc
v1 = enc._left_v(["YNNNNN"])
for tape in ("NYYN",):
    for vm, ts in ((1, [31500]), (2, [47040, 47250, 47460, 47670])):
        m = Machine(tape, ["YNNNNN"], max(ts) + 500, v=vm * v1, left_periods=3, right_periods=2)
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        for t, cs in trace(m, m.row, ts, K0 - 1500, K0 + 200):
            print(vm, t, " ".join(f"{k}{a-K0}" for a, b, k in cs))
