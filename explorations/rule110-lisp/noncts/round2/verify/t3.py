import numpy as np, vlib
vlib.init_martinez()
prev = "E"
for n in range(2, 8):
    row, org, placed = vlib.build([(prev, 0, 0), ("B", 0, 80)], T=400)
    r = vlib.evolve(row, 400); vlib.harvest(f"E^{n}", r, 400); prev = f"E^{n}"
prev = "G"
for k in range(1, 7):
    outs = set()
    for t0 in range(4):
        row, org, placed = vlib.build([(prev, 0, 0), ("B", t0, 90)], T=600)
        r = vlib.evolve(row, 600)
        outs.add(tuple(n for n, x, w, kk in vlib.identify(r, T=600)))
    print(prev, "+ B:", outs)
    row, org, placed = vlib.build([(prev, 0, 0), ("B", 0, 90)], T=600)
    r = vlib.evolve(row, 600)
    g = vlib.harvest(f"GB{k}", r, 600, which="all")
    print(g.name, g.P, g.D, g.w)
    prev = g.name
import pickle
pickle.dump({n: (g.base, (g.P, g.D)) for n, g in vlib.LIB.items()}, open("lib_v1.pkl", "wb"))
