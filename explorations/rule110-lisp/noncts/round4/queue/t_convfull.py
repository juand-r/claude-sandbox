"""Full-machine multi-read check of an answer converter Z placed in a gap of
D cells opened at Ebar-frame K0+CUT (surgery at t_in = 31500; regions right
of the cut shifted by D).  python t_convfull.py TAPE NREAD CUT D ITEMS [KINDS]
ITEMS = 'name:k:x;...' with x rel K0 (inside the gap)."""
import sys
import numpy as np
from reads import *
tape, nread, cut, D, spec = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
kinds = sys.argv[6] if len(sys.argv) > 6 else "KF"
items = [(tiles_of(n), int(k), int(x)) for n, k, x in (s.split(":") for s in spec.split(";"))] if spec != "-" else []
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
new = np.concatenate([row[:c], ETH[(p + np.arange(c, c + D)) % TILE], row[c:len(row) - D]])
if items:
    new = rewrite2(new, m.origin, t_in, K0 + cut + 5, K0 + cut + D - 5, [(t, k, K0 + x) for t, k, x in items])
    assert new is not None
r = Run(new, m.origin); r.t = t_in
got, times = outcomes(r, regs, T, [6] * nread)
ref = reference(tape, apps, kinds + "K" * nread, nread)
print(tape, spec, "observed", got, "reference", ref, "MATCH(reads>=1)" if got[1:] == ref[1:] else "DIFFER", times, flush=True)
