"""Re-run the unsettled entries of collisions.json with a long budget."""
import json, sys, time
from collide import simulate, describe, meet_time
from catalog import classify
from library import Library

EXTRA_LONG = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
lib = Library.load()
rows = json.load(open("collisions.json"))
for r in rows:
    if r["settled"]:
        continue
    t0 = time.time()
    tm = meet_time(lib, r["X"], r["Y"], r["Y_event"])
    res = simulate(lib, [(r["X"], 0, 0), (r["Y"], *r["Y_event"])],
                   tm + EXTRA_LONG)
    r.update(res)
    r["kind"] = classify(lib, r["X"], r["Y"], r)
    print(describe(r), "T=", r["T"], f"{time.time()-t0:.0f}s", flush=True)
lib.save()
json.dump(rows, open("collisions.json", "w"), indent=0)
