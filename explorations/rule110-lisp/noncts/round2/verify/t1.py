import numpy as np, vlib
vlib.init_martinez()
for t0 in range(0, 4):
  for dx in range(0, 28, 14):
    row, org, placed = vlib.build([("E", 0, 0), ("B", t0, 60+dx)], T=300)
    r = vlib.evolve(row, 300)
    print(t0, dx, placed[1], [(n, x+org) for n, x, w, k in vlib.identify(r, T=300)])
