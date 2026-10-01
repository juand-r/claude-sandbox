"""hrun vs engine on one scene for 30,000 steps (cell for cell), + wrong-time control."""
import numpy as np
import hrun
from test_hrun import scene, compare
vlib = hrun.vlib
rng = np.random.default_rng(11)
T = 30000
while True:                  # rejection sampling of non-overlapping placements
    items = scene(rng, 60, 40)
    try:
        row, org, _ = vlib.build(items, T=T)
        break
    except ValueError:
        continue
hr = hrun.HRun(row, org)
for t in (7777, T):
    a, b = compare(row, org, t, hr)
    assert np.array_equal(a, b), t
    print(t, "equal over", len(a), "cells; defects:", len(vlib.defects(b)))
a, _ = compare(row, org, T - 1, hrun.HRun(row, org))
assert not np.array_equal(a, b), "control passed?!"
print("test_hrun_long ok")
