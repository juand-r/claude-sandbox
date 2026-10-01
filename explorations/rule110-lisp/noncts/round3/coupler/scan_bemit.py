"""Scan G-speed library packets X of slip s (default 6) for a zero event
that emits a LEFT-moving signal: E + X (every class) -> products.
Records all classes; resumable (appends JSON lines to scan_bemit.jsonl).
Usage: python scan_bemit.py [slip]"""
import json
import os
import sys
from cl import LIB, CHAIN, HERE
from collide import collide_pair

SLIP = int(sys.argv[1]) if len(sys.argv) > 1 else 6
OUT = os.path.join(HERE, f"scan_bemit_s{SLIP}.jsonl")
done = set()
if os.path.exists(OUT):
    done = {json.loads(l)["X"] for l in open(OUT)}
Xs = [n for n, g in LIB.gliders.items() if str(g.velocity) == "-1/3" and g.slip == SLIP]
print(len(Xs), "packets,", len(done), "done", flush=True)
with open(OUT, "a") as f:
    for X in Xs:
        if X in done:
            continue
        try:
            res = collide_pair(LIB, "E", X)
            rec = {"X": X, "E": [(r["cls"], r["settled"], [p[0] for p in r["products"]]) for r in res]}
        except Exception as e:  # recorded loudly, scan continues
            rec = {"X": X, "error": repr(e)}
        f.write(json.dumps(rec) + "\n")
        f.flush()
print("done", flush=True)
