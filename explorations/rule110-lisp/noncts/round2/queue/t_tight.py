"""Trace a tight-pair prefix (glider name, phase k, offset o) before K[0]."""
import sys
from splice import *
name, k, o, tape, T, dt = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
m = Machine(tape, ["YNNNNN"], T, left_periods=T // 16000 + 2, right_periods=T // 30000 + 3)
K = [a for n, a, b in m.blocks if n == "K"]
c = ether_cut(m.row, m.origin + K[0], search=10, tight=True)
for s, D in valid_shifts(600):
    row = replace_exact(m.row, c, c, [(glider_tiles(name), k, o)], s, D)
    if row is not None:
        break
print("shift", s, D, "K", K[:5])
bounds = [1100] + [x + (D if i > 0 or True else 0) for i, x in enumerate(K[:5])]
bounds = [1100, K[0]] + [x + D for x in K[1:5]]
for t, cs in trace(m, row, range(dt, T + 1, dt), 1100, K[4] + 300):
    print(t, [sum(1 for x, y, kk in cs if lo <= x < hi and kk == "E") for lo, hi in zip(bounds, bounds[1:])],
          " ".join(f"{kk}{x}" for x, y, kk in cs if kk != "E"))
