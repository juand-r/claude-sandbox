"""Drift switch with the A arriving in each of its 3 classes at the window
(R2 seeded at time r2t0 = 0, 1, 2 shifts the A's lattice class; the left
stream follows R2). Exact CA. A + E^2 -> E is clean in all 3 classes but
leaves the E at shifts 7.0 / 7.0 / 5.13 (lscan.py control), so the walk
sequence may differ per class. Usage: python ds_cls.py"""
from ds import *  # noqa
for r2t0 in (0, 1, 2):
    for tz in (20000, 40000, 60000):
        for v2 in (0, 1):
            sc, T = scene(v2, tz, c=2, r2t0=r2t0)
            ok, prods = ca(sc, T)
            print(f"r2t0={r2t0} tz={tz} v2={v2}: {describe(prods)}", flush=True)
