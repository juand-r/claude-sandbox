"""Window behaviour table, part 2: every library G-speed packet (the 2,337
of round-3 coupler's scan_reflect_M1.jsonl, which has them against E)
against E^M (default M = 2, i.e. a window of value 1), every class
(collider collide_pair = full exact simulation to settlement).
Resumable: appends JSON lines to scan_e{M}.jsonl (in this directory).
Usage: python scan_e2.py [M]"""
import json, os, sys
from dl import LIB, CHAIN, HERE, COUP
from collide import collide_pair

M = int(sys.argv[1]) if len(sys.argv) > 1 else 2
OUT = os.path.join(HERE, f"scan_e{M}.jsonl")
Ys = [json.loads(l)["Y"] for l in open(os.path.join(COUP, "scan_reflect_M1.jsonl"))]
done = set()
if os.path.exists(OUT):
    done = {json.loads(l)["Y"] for l in open(OUT)}
print(len(Ys), "packets,", len(done), "done", flush=True)
with open(OUT, "a") as f:
    for Y in Ys:
        if Y in done:
            continue
        try:
            res = collide_pair(LIB, CHAIN[M - 1], Y)
            rec = {"Y": Y, "rows": [{"cls": r["cls"], "settled": r["settled"],
                                     "Y_event": r["Y_event"], "products": r["products"]}
                                    for r in res]}
        except Exception as e:  # recorded loudly, scan continues
            rec = {"Y": Y, "error": repr(e)}
        f.write(json.dumps(rec) + "\n")
        f.flush()
print("done", flush=True)
