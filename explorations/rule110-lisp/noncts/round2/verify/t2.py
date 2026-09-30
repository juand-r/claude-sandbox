import numpy as np, vlib
vlib.init_martinez()
prev = "E"
for n in range(2, 7):
    row, org, placed = vlib.build([(prev, 0, 0), ("B", 0, 80)], T=400)
    r = vlib.evolve(row, 400)
    g = vlib.harvest(f"E^{n}", r, 400)
    print(g.name, g.P, g.D, g.w, g.hi - g.lo)
    prev = g.name
# check E^n + B in all 4 B phases gives E^(n+1)
for n in range(1, 6):
    nm = "E" if n == 1 else f"E^{n}"
    outs = set()
    for t0 in range(4):
        row, org, placed = vlib.build([(nm, 0, 0), ("B", t0, 80)], T=400)
        r = vlib.evolve(row, 400)
        outs.add(tuple(vlib.names(r[416:-416])))
    print(nm, "+ B ->", outs)
