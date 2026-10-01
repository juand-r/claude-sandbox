"""Typed objects (Ebar frame) around the first K during its read, with the
E9 variant vs plain K."""
import sys
from splice import *
tape, which, t0, t1, dt, lo, hi = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:8])
m = Machine(tape, ["YNNNNN"], t1 + 400, left_periods=t1 // 16000 + 2, right_periods=3)
K = [a for n, a, b in m.blocks if n == "K"][0]
row = m.row if which == "plain" else replace_exact(m.row, m.origin + K + 41, m.origin + K + 72, [(en_tiles(9), 14, 9)], 0, 0)
r = Run(row, m.origin)
H = 200
import re
for t in range(t0, t1 + 1, dt):
    r.step(t - H - r.t)
    sh = r.ebar_frame(t - H)      # window fixed in the Ebar frame of time t-H
    a, b = K + lo, K + hi
    h = r.history(a + sh - 300, b + sh + 300, H)
    objs = rc.objects(h, H, 150, len(h[0]) - 150, merge=4)
    shift_t = r.ebar_frame(t) - sh
    print(t, " ".join(f"{n}@{x + a - 300 - K - shift_t}" for x, y, n in objs
                      if not re.match(r'E-(\^2)?$|\?\(2[24],(17|23),w7\)$', n)))
