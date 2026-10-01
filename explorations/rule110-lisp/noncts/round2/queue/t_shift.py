"""Trace the machine with (K + everything after) shifted by (s, m)."""
import sys
from splice import *
s, mm, tape, T, dt = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
m = Machine(tape, ["YNNNNN"], T, left_periods=6, right_periods=4)
K = [a for n, a, b in m.blocks if n == "K"]
c = ether_cut(m.row, m.origin + K[0], search=10, tight=True)
row, d = shift_remainder(m.row, c, s, mm)
print("d", d)
bounds = [1100] + [k + d for k in K[:4]]
for t, cs in trace(m, row, range(dt, T + 1, dt), 1100, K[3] + 300):
    print(t, [sum(1 for x, y, kk in cs if lo <= x < hi and kk == "E") for lo, hi in zip(bounds, bounds[1:])],
          " ".join(f"{kk}{x}" for x, y, kk in cs if kk != "E"))
