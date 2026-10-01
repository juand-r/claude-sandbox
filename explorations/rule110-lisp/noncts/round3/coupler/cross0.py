"""Zero-crossing packets (from scan_reflect_M1.jsonl): a G-speed packet X
that, at R1's zero (E), leaves E (or E^2) and sends only LEFT-movers
(B-family trains or G-speed packets) toward R2. For each candidate, show
E^n + X for n = 1..NMAX in every class (collider collide_pair = full
simulation) to see whether X is also clean at n >= 2.
Usage: python cross0.py [NMAX] [X ...]"""
import json
import sys
from fractions import Fraction
from cl import *  # noqa
from collide import collide_pair

VE = Fraction(-4, 15)
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
cands = sys.argv[2:]
if not cands:
    for l in open(os.path.join(HERE, "scan_reflect_M1.jsonl")):
        r = json.loads(l)
        for row in r.get("rows", []):
            ps = row["products"]
            es = [p for p in ps if p[0] in CHAIN]
            oth = [p[0] for p in ps if p[0] not in CHAIN]
            if row["settled"] and len(es) == 1 and oth and all(vel(o) < VE for o in oth):
                cands.append(r["Y"])
    cands = sorted(set(cands))
for X in cands:
    print("==", X, "slip", LIB.gliders[X].slip)
    for n in range(1, NMAX + 1):
        res = collide_pair(LIB, CHAIN[n - 1], X)
        print("   E^%d:" % n, [(r["cls"], [(("E^%d" % (CHAIN.index(p[0]) + 1)) if p[0] in CHAIN else p[0]) for p in r["products"]]) for r in res], flush=True)
