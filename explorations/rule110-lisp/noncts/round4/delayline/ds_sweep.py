"""Delay-insensitivity sweep of the drift switch (exact CA, gate fastca).
For gaps 600/1200/2400 and Z_L times tz = 15000..75000 (step 1500):
v2 = 0 must give R2 = E and W = E at 3.33 + (sum of the first k walks of the
alternating sequence 24.27/20.53 starting with the class-2 step 20.53 ...),
i.e. one of a fixed set of positions, non-increasing in tz; v2 = 1 must give
W = E^2 unmoved. Any other product list counts as a failure.
Usage: python ds_sweep.py"""
import ds
from ds import *  # noqa

walks = [0.0]
seq = [20.53, 24.27] * 10        # from walk2.py, class 2: 20.53, 44.8, 65.33, ...
for w in seq:
    walks.append(round(walks[-1] + w, 2))
allowed = {round(3.33 + w, 2) for w in walks}
fails = 0
for gap in (600, 1200, 2400):
    ds.GAP = gap
    prev = None
    seen = []
    for tz in range(15000, 75001, 1500):
        sc, T = scene(0, tz, c=2)
        ok, prods = ca(sc, T)
        d = describe(prods)
        good = ok and len(d) == 2 and d[0][0] == "E" and d[1][0] == "E" and \
            any(abs(d[1][1] - a) < 0.02 for a in allowed) and (prev is None or d[1][1] <= prev + 1e-9)
        if good:
            prev = d[1][1]
        fails += not good
        seen.append(d[1][1] if len(d) == 2 else None)
        if not good:
            print("FAIL", gap, tz, d, flush=True)
    sc, T = scene(1, 40000, c=2)
    ok, prods = ca(sc, T)
    d = describe(prods)
    ctrl = len(d) == 2 and d[1] == ("E^2", -1.8)
    fails += not ctrl
    print(f"gap={gap}: W positions over tz: {seen}; control v2=1: {d} {'ok' if ctrl else 'FAIL'}", flush=True)
print("FAILURES:", fails)
