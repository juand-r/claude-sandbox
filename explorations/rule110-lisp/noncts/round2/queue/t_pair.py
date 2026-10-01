"""Trace a soft-leader candidate P (two Ebars before the first K)."""
import sys, json
from splice import *
P = json.loads(sys.argv[1]); tape = sys.argv[2]; T = int(sys.argv[3]); dt = int(sys.argv[4])
m = Machine(tape, ["YNNNNN"], T, left_periods=6, right_periods=4)
K = [a for n, a, b in m.blocks if n == "K"]
c = ether_cut(m.row, m.origin + K[0], search=10, tight=True)
for s, D in valid_shifts(600):
    row = insert_exact(m.row, c, [tuple(P[:2]), tuple(P[2:])], s, D)
    if row is not None:
        break
print("shift", s, D, "K", K[:4])
bounds = [1100] + K[:4]
for t, cs in trace(m, row, range(dt, T + 1, dt), 1100, K[3] + 300):
    print(t, [sum(1 for x, y, k in cs if lo <= x < hi and k == "E") for lo, hi in zip(bounds, bounds[1:])],
          " ".join(f"{k}{x}" for x, y, k in cs if k != "E"))
