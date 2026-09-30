"""Hard-gate search: A vs 2-object G-speed packets (G, GB1..GB5 pairs,
gaps <= 40). Reports outcomes consisting only of G-speed objects."""
import json
from fractions import Fraction
from library import Library
from packets import enumerate_pairs
from catalog import run_pairs, merge_save

lib = Library.load()
parts = ["G", "GB1", "GB2", "GB3", "GB4", "GB5"]
pk = []
for a in parts:
    for b in parts:
        if (a, b) == ("G", "G"):
            continue
        pk += enumerate_pairs(lib, a, b, 40)[0]
pk = list(dict.fromkeys(pk))
print(len(pk), "packets", flush=True)
done = {(r["X"], r["Y"]) for r in json.load(open("collisions.json"))}
rows = run_pairs(lib, [("A", p) for p in pk if ("A", p) not in done])
lib.save()
merge_save(rows)
V = Fraction(-1, 3)
for r in rows:
    ps = [p[0] for p in r["products"]]
    if r["settled"] and ps and all(lib.gliders[p].velocity == V for p in ps):
        print("G-SPEED ONLY:", r["X"], r["Y"], r["cls"], ps, flush=True)
