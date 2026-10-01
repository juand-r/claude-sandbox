"""Wide census after the forced-N Z insertion (full machine)."""
import sys
from reads import *
k2, x2, k1, x1 = map(int, sys.argv[1:5]); tape = sys.argv[5]
times = list(map(int, sys.argv[6].split(",")))
lo, hi = int(sys.argv[7]), int(sys.argv[8])
apps = ["YNNNNN"]; E = ebar_tiles(); t_in = 31500
m = Machine(tape, apps, max(times) + 500, left_periods=4, right_periods=3)
K0 = [a for n, a, b in m.blocks if n == "K"][0]
for z in (False, True):
    r = Run(m.row, m.origin); r.step(t_in)
    if z:
        row = rewrite(r.window(0, r.width), m.origin, t_in, K0 - 345, K0 + 37,
                      [(E, k2, K0 + x2), (E, k1, K0 + x1)])
        r = Run(row, m.origin); r.t = t_in
    print("Z" if z else "plain")
    for t in times:
        r.step(t - MAX_DT - r.t)
        sh = r.ebar_frame(t)
        cs = census(r.history(K0 + lo + sh, K0 + hi + sh, MAX_DT))
        print(" ", t, " ".join(f"{k}{a + lo}" for a, b, k in cs))
