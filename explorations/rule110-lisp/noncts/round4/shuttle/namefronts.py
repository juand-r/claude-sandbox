"""Name the objects of each enumerated front (rod shortened so it is a
library object): row = ether | D | crystal ... rod E^N back."""
import sys, json
sys.dont_write_bytecode = True
import numpy as np
from rod import ether_bit
from pert import BG
from frontsim import lib
from collide import products_of

fn = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 7
recs = [json.loads(l) for l in open(fn)]
bg = BG(N, 50, -400, 400)
for r in recs:
    ulo = r["c0"] - r["wD"]
    row = [int(c) for c in r["row"]]
    lo, hi = -300, 300
    r0 = np.array([ether_bit(r["phi"], 0, x) if x < ulo else
                   (row[x - ulo] if x < r["c0"] else bg(0, x)) for x in range(lo, hi)], np.uint8)
    ok, prods, _ = products_of(lib(), r0[40:-40], lo + 40, 0)
    print(r["phi"], r["first"], r["row"], [(p[0], p[2]) for p in prods])
