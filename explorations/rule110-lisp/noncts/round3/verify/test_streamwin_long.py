"""Long validation of StreamWindow: E^3 + 100 GB4 (NOP) packets + a sparse
left stream of A^2 trains that arrive late (and wreck the counter), T ~ 3e5.
Compare with one full engine run at the end, cell for cell, and time both."""
import time
import numpy as np
import v3, vlib, engine
from streamwin import from_items, snapshot

N, SP = 100, 210
right = [("GB4", 0, 150 + SP * i) for i in range(N)]
left = [("A^2", 0, -4000 * (k + 1)) for k in range(3)][::-1]
T = 15 * SP * N
t1 = time.time()
sw, placed = from_items(left, [("E^3", 0, 0)], right)
sw.run(T)
t_sw = time.time() - t1
print(f"window: T={T} {t_sw:.1f}s max width {sw.max_width}; objects:",
      [(v3.base(n), x) for n, x in snapshot(sw)][:12])
t1 = time.time()
row, org, placed2 = vlib.build_right(left + [("E^3", 0, 0)] + right, c_right=0, T=T)
assert placed2 == placed
r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
t_full = time.time() - t1
lo, hi = org + T + 50, org + len(row) - T - 50
same = np.array_equal(r[lo - org:hi - org], sw.cells(lo, hi))
print(f"full: {t_full:.1f}s width {len(row)}; equal over [{lo},{hi}): {same}")
assert same
