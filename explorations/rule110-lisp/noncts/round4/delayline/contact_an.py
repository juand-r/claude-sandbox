"""Strict re-classification of contact_<train>_<t0>.jsonl: EMIT only if all
non-rod products move right (velocity > 0). Usage: python contact_an.py FILE"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collections import Counter
from dl import LIB, CHAIN, HERE
from cl import vel
rs = [json.loads(l) for l in open(os.path.join(HERE, sys.argv[1]))]
EF = set(CHAIN) | {"Ebar"}


def strict(r):
    ns = [p[0] for p in r["products"]]
    rods = [n for n in ns if n in EF]
    oth = [n for n in ns if n not in EF]
    try:
        vs = [vel(n) for n in oth]
    except Exception:
        return "DEB"
    if rods and oth and all(v > 0 for v in vs):
        return "EMIT"
    if len(rods) == 1 and not oth:
        return "STOP"
    if len(rods) == 2 and not oth:
        return "KEEP"
    return "DEB"


print(Counter((r["X"], strict(r)) for r in rs))
for r in rs:
    if strict(r) != "DEB":
        print(r["X"], r["t0"], r["dist"], strict(r), r["products"])
