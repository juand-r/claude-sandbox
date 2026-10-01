"""C1 and F versus every Ebar-speed library object NOT in collider's catalog
(mostly 3-glider compounds), all classes, direct CA (collide_pair).
Output lane_scan.json (resumable): {Y: {"C1": [(cls, settled, prods)], "F": [...]}}"""
import json
from common import HERE, LIB, collide_pair, names

OUT = f"{HERE}/lane_scan.json"
R = json.load(open("collisions.json"))
tested = {r["Y"] for r in R if r["X"] == "C1"}
todo = sorted(n for n, g in LIB.gliders.items()
              if str(g.velocity) == "-4/15" and n not in tested and "^" not in n)
try:
    done = json.load(open(OUT))
except FileNotFoundError:
    done = {}
print(len(todo), "to test;", len(done), "done", flush=True)
for i, Y in enumerate(todo):
    if Y in done:
        continue
    rec = {}
    for X in ("C1", "F"):
        try:
            rec[X] = [(r["cls"], r["settled"], names(r["products"])) for r in collide_pair(LIB, X, Y)]
        except Exception as e:  # report, keep going
            rec[X] = [("ERR", False, [str(e)[:80]])]
    done[Y] = rec
    if i % 5 == 0:
        json.dump(done, open(OUT, "w"))
        print(i, Y, flush=True)
json.dump(done, open(OUT, "w"))
print("done")
