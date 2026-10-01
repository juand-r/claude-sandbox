"""Analyse zt.jsonl: per mover, outcome signature per gap index k
(number of F's after splitting F compounds, multiset of other products).
Report movers whose k=8 (smallest gap) signature differs from the k=4,0,-4
signatures while those three agree, and both are 'well formed' (no '?')."""
import json
from collections import defaultdict
from fractions import Fraction
import lane  # noqa
from predict import LIB


def sig(prods):
    nF, other = 0, []
    for n, t, x in prods:
        if n.startswith("ERR") or n == "?":
            return None
        g = LIB.gliders.get(n)
        if g is None:
            return None
        if n == "F":
            nF += 1
        elif n.startswith("F_") and g.parts and all(p[0] == "F" for p in g.parts):
            nF += len(g.parts)
        else:
            other.append(n)
    return nF, tuple(sorted(other))


by = defaultdict(dict)
for line in open("zt.jsonl"):
    r = json.loads(line)
    by[tuple(r["mv"])][r["k"]] = sig(r["prods"])
cnt = 0
for mv, d in by.items():
    if len(d) < 4:
        continue
    big = {d[4], d[0], d[-4]}
    if len(big) == 1 and None not in big and d[8] is not None and d[8] != d[4]:
        cnt += 1
        print(mv, "\n   large:", d[4], "\n   zero :", d[8])
print("candidates", cnt, "of", len(by))
