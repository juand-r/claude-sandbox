from dl import *  # noqa
from walk import run_prog
import sys
for c in range(3):
    for n in (1,2,3,4,5,6,8):
        sc, sim, err = run_prog("N"*n, [c]*n)
        print(c, n, err, [(g[0], round(float(lat(g)),2)) for g in sim.state()], flush=True)
