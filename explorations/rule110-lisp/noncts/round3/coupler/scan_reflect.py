"""Library scan for SHUTTLE legs at the inner faces (exact, no SAT).
Step 1 (R2 back): every library glider Y moving left faster than E
(velocity -1/2 or -1/3) against E^M (default M = 4), every class
(collider.collide_pair = full simulation to settlement). A 'reflection'
is: one E^j plus only right-moving products (the X train).
Resumable: appends JSON lines to scan_reflect_M{M}.jsonl.
Usage: python scan_reflect.py [M] [family: -1/2 | -1/3]"""
import json
import os
import sys
from fractions import Fraction
from cl import LIB, CHAIN, HERE
from collide import collide_pair

M = int(sys.argv[1]) if len(sys.argv) > 1 else 4
FAM = sys.argv[2] if len(sys.argv) > 2 else "-1/2"
OUT = os.path.join(HERE, f"scan_reflect_M{M}.jsonl")
VE = Fraction(-4, 15)
done = set()
if os.path.exists(OUT):
    done = {json.loads(l)["Y"] for l in open(OUT)}
Ys = [n for n, g in LIB.gliders.items() if str(g.velocity) == FAM]
print(len(Ys), "candidates,", len(done), "done", flush=True)
with open(OUT, "a") as f:
    for Y in Ys:
        if Y in done:
            continue
        try:
            res = collide_pair(LIB, CHAIN[M - 1], Y)
            rows = []
            for r in res:
                ps = r["products"]
                es = [p for p in ps if p[0] in CHAIN]
                others = [p for p in ps if p[0] not in CHAIN]
                refl = (r["settled"] and len(es) == 1 and others and
                        all(LIB.gliders[p[0]].velocity > VE for p in others))
                rows.append({"cls": r["cls"], "settled": r["settled"],
                             "Y_event": r["Y_event"], "products": ps,
                             "reflect": bool(refl)})
            rec = {"Y": Y, "rows": rows}
        except Exception as e:  # recorded loudly; scan continues
            rec = {"Y": Y, "error": repr(e)}
        f.write(json.dumps(rec) + "\n")
        f.flush()
print("done", flush=True)
