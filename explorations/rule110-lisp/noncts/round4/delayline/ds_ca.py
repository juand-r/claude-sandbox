"""Exact-CA check of ds.py scenes (gate fastca moving window) + glider sim."""
from ds import *  # noqa
import time
cases = [(c, v2, tz) for c in (2, 0, 1) for v2 in (0, 1) for tz in (20000, 40000, 60000)]
for c, v2, tz in cases:
    t1 = time.time()
    sc, T = scene(v2, tz, c=c)
    sim, err = run(sc, T)
    st = sim.state()
    ok, prods = ca(sc, T)
    print(f"c={c} v2={v2} tz={tz} CA={describe(prods)} ok={ok} glider_err={err is not None} eq={sorted(prods)==sorted(st)} {time.time()-t1:.0f}s", flush=True)
