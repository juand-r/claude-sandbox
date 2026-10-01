"""Typed objects (r110check) near the first leader for a tight-pair prefix."""
import sys
from splice import *
name, k, o, tape, t0, t1, dt = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], *map(int, sys.argv[5:8])
lo, hi = (int(sys.argv[8]), int(sys.argv[9])) if len(sys.argv) > 9 else (-300, 500)
m = Machine(tape, ["YNNNNN"], t1 + 400, left_periods=3, right_periods=3)
K = [a for n, a, b in m.blocks if n == "K"]
c = ether_cut(m.row, m.origin + K[0], search=10, tight=True)
row = m.row
if name != "none":
    for s, D in valid_shifts(600):
        row = replace_exact(m.row, c, c, [(glider_tiles(name), k, o)], s, D)
        if row is not None:
            break
r = Run(row, m.origin)
H = 200
for t in range(t0, t1 + 1, dt):
    r.step(t - H - r.t)
    sh = r.ebar_frame(t)
    a, b = K[0] + lo, K[0] + hi
    h = r.history(a + sh - 300, b + sh + 300, H)
    objs = rc.objects(h, H, 150, len(h[0]) - 150, merge=4)
    print(t, " ".join(f"{n}@{x + a - 300 - K[0]}" for x, y, n in objs))
