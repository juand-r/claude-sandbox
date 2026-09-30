import sys
from splice import *
tape, t0, t1, dt, lo, hi = sys.argv[1], *map(int, sys.argv[2:7])
m = Machine(tape, ["YNNNNN"], t1 + 400)
r = Run(m.row, m.origin)
H = 200
t = t0
while t <= t1:
    r.step(t - H - r.t)
    sh = r.ebar_frame(t)
    h = r.history(lo + sh - 300, hi + sh + 300, H)
    objs = rc.objects(h, H, 150, len(h[0]) - 150, merge=4)
    print(t, " ".join(f"{n}@{a + lo - 300}" for a, b, n in objs))
    t += dt
