"""Which enumerated fronts are the STANDARD E^n front (up to translation /
time phase)? Compare the decorated rod's first 40 cells (from its first
non-ether cell) with the standard rod E^20 at every time phase."""
import sys, json
sys.dont_write_bytecode = True
import numpy as np
from rod import ether_bit
from pert import BG

fn = sys.argv[1]
recs = [json.loads(l) for l in open(fn)]
std = BG(20, 20, -200, 200)
L = 40
cands = set()
for tau in range(15):
    f = std.front(tau)
    cands.add(tuple(std(tau, x) for x in range(f - 14, f + L)))
for i, r in enumerate(recs):
    bg = BG(16, 20, -200, 200, decor=(r["phi"], r["row"], r["c0"]))
    f = bg.front(0)
    sig = tuple(bg(0, x) for x in range(f - 14, f + L))
    print(i, "standard" if sig in cands else "NEW", r["phi"], r["first"], r["row"])
