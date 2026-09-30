import time
from splice import *
T = 60000
for tape in ("YY", "YN", "NY", "NN"):
    m = Machine(tape, ["YNNNNN"], T, left_periods=4, right_periods=3)
    t0 = time.time()
    cs = m.run(m.row, T, 1100, 10000)
    ks = [a for n, a, b in m.blocks if n == "K"]
    print(tape, f"{time.time()-t0:.1f}s", ks[:3], [sum(1 for x, y, k in cs if lo <= x < hi and k == "E") for lo, hi in [(1100, ks[0]), (ks[0], ks[1]), (ks[1], ks[2])]],
          [f"{k}{x}" for x, y, k in cs if k != "E"])
