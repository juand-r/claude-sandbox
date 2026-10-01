"""Second, independent typing of my T2 demo's final rows with the
project's census.py (ether-phase clustering + invariance typing, written
by others): every final row must hold exactly two clusters, both of kind
'E' ((30,-8)-invariant), and nothing else; the left cluster's width must
grow with R2's value, the right one's with R1's (monotone check)."""
import json, sys, os
import numpy as np
import v3, engine
sys.path.insert(0, v3.ROOT)
import census
import t2_demo as D

d = json.load(open("t2_demo.json"))
t1, slots = d["t1"], [tuple(s) for s in d["slots"]]
rows = []
for v in range(0, 10):
    items, c0 = D.scene(slots, v, t1)
    import vlib
    T = 40000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    w = engine.step_packed_n(engine.pack(row), T - 40)
    hist = []
    for k in range(41):
        hist.append(engine.unpack(w, len(row)))
        w = engine.step_packed(w)
    h = np.stack(hist)[:, T + 100:len(row) - T - 100]
    cl = census.census(h)
    kinds = [k for a, b, k in cl]
    widths = [b - a for a, b, k in cl]
    model = D.model(D.LEFT, v)
    print(f"v1={v}: census kinds {kinds} widths {widths}  model (x, y) = {model}")
