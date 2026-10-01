"""run_packed vs full engine (and vs the per-cell window) on the two
validation scenes; same controls as test_streamwin.py."""
import time, sys
import numpy as np
import v3, vlib, engine
import streamwin as S
import test_streamwin as TS

# scene 1 (short, garbage-rich), compare at several times
row, org, ex = TS.scene(TS.LEFT)
ref = TS.full(row, org, [500, 2000, 4000, TS.T])
xa, xb = S.auto_cuts(row, org, len(TS.LEFT), len(TS.RIGHT))
sw = S.StreamWindow(row, org, xa, xb, (3, 2), (42, -14))
for tt in [500, 2000, 4000, TS.T]:
    S.run_packed(sw, tt, K=300)
    lo, hi = org + TS.T + 50, org + len(row) - TS.T - 50
    ok = np.array_equal(ref[tt][lo - org:hi - org], sw.cells(lo, hi))
    print("scene1 t", tt, "equal", ok, "width", sw.hi - sw.lo)
    assert ok
# control: different left stream must disagree
alt = list(TS.LEFT); alt[2] = ("A", 2, -728)
row2, org2, ex2 = TS.scene(alt)
sw2 = S.StreamWindow(row2, org, xa, xb, (3, 2), (42, -14))
S.run_packed(sw2, TS.T, K=300)
assert not np.array_equal(ref[TS.T][lo - org:hi - org], sw2.cells(lo, hi))
print("control (different left stream) disagrees, as required")

# scene 2 (long)
N, SP = 100, 210
right = [("GB4", 0, 150 + SP * i) for i in range(N)]
left = [("A^2", 0, -4000 * (k + 1)) for k in range(3)][::-1]
T = 15 * SP * N
t1 = time.time()
sw, placed = S.from_items(left, [("E^3", 0, 0)], right)
S.run_packed(sw, T)
print(f"scene2 packed window: {time.time() - t1:.1f}s, max width {sw.max_width}")
row, org, placed2 = vlib.build_right(left + [("E^3", 0, 0)] + right, c_right=0, T=T)
r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
lo, hi = org + T + 50, org + len(row) - T - 50
ok = np.array_equal(r[lo - org:hi - org], sw.cells(lo, hi))
print("scene2 equal", ok)
assert ok
print("ALL OK")
