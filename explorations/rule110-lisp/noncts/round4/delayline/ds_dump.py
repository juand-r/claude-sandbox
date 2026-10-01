"""Dump the seeds (collider conventions: (name, t0, x0)) of the ds.py
drift-switch scenes used in the exact-CA check, for independent rebuild.
Writes ds_scenes.json: list of {c, v2, tz, T, seeds, result_CA}."""
import json, os
from ds import *  # noqa
out = []
for c in (2, 0, 1):
    for v2 in (0, 1):
        for tz in (20000, 40000, 60000):
            sc, T = scene(v2, tz, c=c)
            ok, prods = ca(sc, T)
            out.append({"c": c, "v2": v2, "tz": tz, "T": int(T), "seeds": [[n, int(t), int(x)] for n, t, x in sc],
                        "result_CA": [[p[0], int(p[1]), int(p[2])] for p in prods]})
json.dump(out, open(os.path.join(HERE, "ds_scenes.json"), "w"))
print(len(out), "scenes written")
