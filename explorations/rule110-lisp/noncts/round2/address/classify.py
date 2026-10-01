"""Classify outcomes of X + Ebar-speed packet collisions (cat_X.json)."""
import sys, json
from fractions import Fraction
from collections import defaultdict
import lane  # noqa
from predict import LIB
V = lambda n: LIB.gliders[n].velocity if n in LIB.gliders else None
EB = Fraction(-4, 15)
X = sys.argv[1]
rows = json.load(open(f"cat_{X}.json"))
cat = defaultdict(list)
for r in rows:
    pr = [p[0] for p in r["products"]]
    if not r["settled"] or any(V(p) is None for p in pr):
        cat["unsettled/unknown"].append((r["Y"], r["cls"]))
        continue
    st = sorted(p for p in pr if V(p) == 0)
    other = [p for p in pr if V(p) != 0]
    if any(V(p) != EB for p in other):
        k = ("dirty", tuple(st))
    else:
        k = ("clean", tuple(st))
    cat[k].append((r["Y"], r["cls"], tuple(other)))
for k in sorted(cat, key=str):
    if k[0] != "dirty":
        print(k, len(cat[k]), cat[k][:8])
print("dirty kinds:", {k[1]: len(v) for k, v in cat.items() if k[0] == "dirty"})
