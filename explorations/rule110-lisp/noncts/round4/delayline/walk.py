"""Window walk: a zero rod E under a rigid right stream of NOPs (GB4).
For each slot-class pattern, print the E's trajectory intercept after each
packet. Glider-level (collider catalog)."""
from dl import *  # noqa
import itertools

def run_prog(ops, classes, T=None):
    items = r1_program(ops, classes)
    sc = r1_scene(0, items)
    T = T or 15 * (sc[-1][2] + 3000)
    sim, err = run(sc, T)
    return sc, sim, err

for cl0 in range(3):
    for n in (1, 2, 3, 4):
        for c in itertools.product(range(3), repeat=n):
            if c[0] != cl0: continue
            sc, sim, err = run_prog("N" * n, list(c))
            st = sim.state()
            print(n, c, err, [(g[0], float(lat(g))) for g in st])
        if n >= 2: break
