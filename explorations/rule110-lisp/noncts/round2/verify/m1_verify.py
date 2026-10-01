"""Independent re-check of the M1 gadget [GB3 test, G] with the ROUND-1
typer (../../../census.py) instead of mine, plus trajectory snapshots and a
negative control (G shifted by the ether-lattice vector (7,0), which changes
the A x G class)."""
import numpy as np, sys, os
import vlib, libgen
sys.path.insert(0, vlib.ROOT)
import census, engine
libgen.load()
def E(v): return "E" if v == 0 else f"E^{v+1}"

def run(v, gshift=(0, 0), T=1600, snaps=()):
    items = [(E(v), 0, 0), ("GB3", 1, 30), ("G", 36 + gshift[0], 84 + gshift[1])]
    row, org, placed = vlib.build(items, T=T)
    hist = []
    r = row
    out = {}
    for t in range(T + 1):
        if t >= T - census.MAX_DT:
            hist.append(r.copy())
        if t in snaps:
            out[t] = census_types(np.array([r] * (census.MAX_DT + 1)), org, T=t, static=True)
        if t < T:
            r = engine.step(r)
    h = np.array(hist)
    cut = T + 20
    return census.census(h[:, cut:-cut]), placed, org + cut

def census_types(h, org, T, static):
    return None

for shift in ((0, 0), (7, 0)):
    print("G shift", shift)
    for v in range(0, 5):
        objs, placed, off = run(v, shift)
        print(f"  v={v}: ", [(k, b - a) for a, b, k in objs], placed[2])
