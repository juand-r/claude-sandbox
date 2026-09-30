"""Step 2: action of candidate G-speed packets on the counter E^n.

For every G-speed object P that absorbs an A cleanly (catalog: A + P -> only
G-speed products or nothing, in some class), simulate E^n + P for n = 1..NMAX
in every class (direct CA simulation via collider.collide_pair) and record
products. Output: counter_scan.json (in this directory).
"""
import json
import sys
from collections import defaultdict

from common import HERE, CHAIN, LIB, collide_pair, isG, names

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 4
OUT = f"{HERE}/counter_scan.json"

R = json.load(open("collisions.json"))
cands = defaultdict(list)
for r in R:
    if r["X"] == "A" and isG(r["Y"]):
        ps = names(r["products"])
        if all(isG(p) for p in ps):
            cands[r["Y"]].append((r["cls"], ps))
try:
    done = json.load(open(OUT))
except FileNotFoundError:
    done = {}
print(len(cands), "candidates;", len(done), "done", flush=True)
for i, P in enumerate(sorted(cands)):
    if P in done:
        continue
    rec = {"A": cands[P], "E": {}}
    for n in range(1, NMAX + 1):
        res = collide_pair(LIB, CHAIN[n - 1], P)
        rec["E"][n] = [(r["cls"], r["settled"], names(r["products"])) for r in res]
    done[P] = rec
    if i % 10 == 0:
        json.dump(done, open(OUT, "w"))
        print(i, P, rec["E"][1], rec["E"][2], flush=True)
json.dump(done, open(OUT, "w"))
print("done")
