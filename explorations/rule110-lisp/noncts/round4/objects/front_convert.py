"""Can a left-stream packet (library right-mover, every phase) turn the
standard E^n front (type 12) into front type 7 or 13 (the types that absorb
the (1,9) bubble cleanly)? Exact CA.

Reference strings: rods with front type c (fronts_walls.build_scene, no wall)
at all 15 time phases; a product counts if its row contains the reference's
front region (the 40 cells from 10 left of the front into the interior) at
some phase and position, and typing finds a single object.
Usage: python3 front_convert.py N T"""
import json
import sys
import numpy as np
import objlib as O
import fronts_walls as FW

N, T = int(sys.argv[1]), int(sys.argv[2])
FW.N, FW.T = N, T
F = FW.fronts()
L = O.lib()
movers = [n for n, g in L.items() if g["velocity"] in ("2/3", "1/2")]


def front_refs(c):
    sc, x0, fs, _ = FW.build_scene((c, F[c]))
    refs = set()
    for t in range(15):
        a = O.evolve(sc, t)
        i = fs - (4 * t) // 15 - (x0 + t)
        refs.add("".join(map(str, a[i - 12:i + 40])))
    return refs


refs = {c: front_refs(c) for c in F}
b, l, r = O.en_bits(N)
res = []
for name in movers:
    for kg in range(L[name]["p"]):
        row, x_lo, objs, cc = O.build([("g", name, kg, 0), ("raw", b, l, r, 20, "E")], pad=2 * T + 400)
        a = O.evolve(row, T)
        s = "".join(map(str, a))
        hit = [c for c, rs in refs.items() if any(q in s for q in rs)]
        if hit:
            ty = O.types(a, x_lo + T)
            rec = {"g": name, "k": kg, "front_types": hit, "n_objects": len(ty), "types": [t[0] for t in ty]}
            res.append(rec)
            print(json.dumps(rec), flush=True)
print("done", len(movers), "movers")
