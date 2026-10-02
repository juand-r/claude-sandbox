"""Detail of a clean wall absorption found by fronts_walls.py: show the rod
before and after (front region), its length and the new front."""
import json, sys
import numpy as np
import objlib as O
import fronts_walls as FW   # module-level code is guarded by __main__

c, gw = int(sys.argv[1]), tuple(map(int, sys.argv[2].split(",")))
N, POS, T = FW.N, FW.POS, FW.T
F = FW.fronts()
walls = {}
for l in open("walls_ebg.jsonl"):
    r = json.loads(l)
    if r["found"] and abs(r["v"] + 0.6) < 1e-9:
        g = tuple(r["g"])
        if g not in walls or r["W"] < walls[g]["W"]:
            walls[g] = r
sc0, x0, fs, _ = FW.build_scene((c, F[c]))
sc, x0, fs, wl = FW.build_scene((c, F[c]), walls[gw])
print("front at", fs, "wall at", wl)
for t in (0, 100, 200, 300, 400, 500, 700):
    a = O.evolve(sc, t); b = O.evolve(sc0, t)
    xs = x0 + t
    cf = fs - (4 * t) // 15
    lo, hi = cf - 30, cf + 200
    print(f"{t:4d} wall " + O.show(a, lo - xs, hi - xs))
    print(f"{t:4d} none " + O.show(b, lo - xs, hi - xs))
