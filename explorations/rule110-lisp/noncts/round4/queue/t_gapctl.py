"""Is opening a gap of D cells at Ebar-frame column K0+CUT (everything right
shifted (0, D)) at t_in = 31500 a symmetry of the machine? Full-machine
multi-read check with regions right of the cut shifted by D.
    python t_gapctl.py TAPE NREAD CUT D"""
import sys
from reads import *
tape, nread, cut, D = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
apps = ["YNNNNN"]; t_in = 31500
v = enc._left_v(apps); T = (nread + 3) * 2 * 30 * v
m = Machine(tape, apps, T, v=v, left_periods=T // (30 * v) + 3, right_periods=nread + 3)
K0 = [a for n, a, b in m.blocks if n == "K"][0]
regs = [(a + (D if a >= K0 + cut else 0), b + (D if b > K0 + cut else 0)) for a, b in regions_of(m, nread)]
r = Run(m.row, m.origin); r.step(t_in)
row = r.window(0, r.width).copy()
sh = ebar_shift(m.origin, t_in)
c = K0 + cut + sh
p = phase_at(row, c - TILE)
import numpy as np
new = np.concatenate([row[:c], ETH[(p + np.arange(c, c + D)) % TILE], row[c:len(row) - D]])
r = Run(new, m.origin); r.t = t_in
got, times = outcomes(r, regs, T, [6] * nread)
print(tape, "cut", cut, "D", D, "observed", got, "reference", reference(tape, apps, "K" * nread, nread), times)
