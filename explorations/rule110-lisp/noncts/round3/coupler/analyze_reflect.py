"""Summarise scan_reflect_M{M}.jsonl: reflections (one E^j + right-movers
only), crossings (one E^j + only left-movers, i.e. the packet passed the
rod, possibly converted), grouped by product pattern.
Usage: python analyze_reflect.py [M] [family]"""
import json
import os
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from cl import LIB, CHAIN, HERE, vel

M = int(sys.argv[1]) if len(sys.argv) > 1 else 4
FAM = sys.argv[2] if len(sys.argv) > 2 else None
VE = Fraction(-4, 15)
refl = defaultdict(list)
cross = defaultdict(list)
n = 0
for l in open(os.path.join(HERE, f"scan_reflect_M{M}.jsonl")):
    r = json.loads(l)
    if "rows" not in r:
        continue
    if FAM and str(LIB.gliders[r["Y"]].velocity) != FAM:
        continue
    n += 1
    for row in r["rows"]:
        ps = row["products"]
        es = [p for p in ps if p[0] in CHAIN]
        oth = [p[0] for p in ps if p[0] not in CHAIN]
        if not row["settled"] or len(es) != 1:
            continue
        j = CHAIN.index(es[0][0]) + 1
        if oth and all(vel(o) > VE for o in oth):
            refl[(j - M, tuple(oth))].append((r["Y"], row["cls"]))
        if oth and all(vel(o) < VE for o in oth):
            cross[(j - M, tuple(oth))].append((r["Y"], row["cls"]))
print(n, "objects")
print("REFLECTIONS (dE, right-movers): count, examples")
for k, v in sorted(refl.items(), key=lambda kv: -len(kv[1])):
    print(" ", k, len(v), v[:3])
print("CROSSINGS / left-moving survivors (dE, left-movers): count, examples")
for k, v in sorted(cross.items(), key=lambda kv: -len(kv[1])):
    print(" ", k, len(v), v[:3])
