"""Catalog a stationary object X against all Ebar-speed packets that the
F-lane uses (collide_pair, exact simulation). Saves JSON. Usage:
python cat_stat.py X"""
import sys, json, os
import lane  # noqa
from predict import LIB
from collide import collide_pair
import gen
X = sys.argv[1]
packs = sorted({m[0] for m in gen.movers("F")})
out = []
for Y in packs:
    try:
        res = collide_pair(LIB, X, Y)
    except Exception as e:
        print("skip", Y, type(e).__name__, e, flush=True)
        continue
    for r in res:
        out.append(r)
json.dump(out, open(f"cat_{X}.json", "w"))
print(X, "collisions", len(out))
