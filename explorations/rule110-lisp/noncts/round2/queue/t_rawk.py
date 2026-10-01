"""What does a RAW leader K do when it reaches tape data unprepared?
Central region ends with K instead of the prepared leader G."""
import sys
from splice import *
import encoder as enc
central, T, t0, dt, lo, hi = sys.argv[1], *map(int, sys.argv[2:7])
right = enc._right_block_seq(["YNNNNN"]) * 3
left = (enc.OSSIFIER + "A" * 536) * 6
m = Machine(None, None, T, right_names=right, left_names=left, central="C" + central)
print([(n, a) for n, a, b in m.blocks if n not in "AB"][:8])
r = Run(m.row, m.origin)
H = 200
for t in range(t0, T + 1, dt):
    r.step(t - H - r.t)
    sh = r.ebar_frame(t)
    h = r.history(lo + sh - 300, hi + sh + 300, H)
    objs = rc.objects(h, H, 150, len(h[0]) - 150, merge=4)
    print(t, " ".join(f"{n}@{a + lo - 300}" for a, b, n in objs if not n.startswith("E-")))
