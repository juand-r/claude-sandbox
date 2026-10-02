"""Follow one phonon x cut collision for a long time (wallchem.py builder)."""
import sys, json
import numpy as np
sys.argv = [sys.argv[0], "400", "/dev/null"] + sys.argv[1:]
exec(open("wallchem.py").read().split("if __name__")[0])
gp = tuple(map(int, sys.argv[3].split(","))); gc = tuple(map(int, sys.argv[4].split(",")))
Tmax = int(sys.argv[5])
ph = best(0.4); cuts = best(-4 / 15)
W = 2 * Tmax + 800
lo, hi = -W // 2, W // 2
A = wall_scene(ph[gp], lo, 0, 0, -60)
B = wall_scene(cuts[gc], 0, hi, gp[0], 120 + gp[1])
row = np.concatenate([A, B])
prev = None
for t in range(0, Tmax + 1, 100):
    a = O.evolve(row, t)
    w = walls_of(phase_map(a, lo + t, t))
    # keep only walls within the region of interest
    w = [x for x in w if -400 < x[0] < 400]
    print(t, [(x1, tuple(l), tuple(r)) for x1, x2, l, r in w])
