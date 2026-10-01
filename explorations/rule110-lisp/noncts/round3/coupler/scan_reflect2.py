"""Step 2 of the shuttle leg scan: for every R2-back reflection found by
scan_reflect.py (E^M + Y -> E^j + right-movers X), send the X train, as
emitted (exact relative seeds), against R1 = E^N (default N = 4) at all 15
seed times (covering the 3 classes), exact CA (fastca window). A
'return leg' is: one E^k plus only left-moving products. A SHUTTLE needs
the left-movers to reproduce Y (checked: same names; positions are
reported for the drift analysis).
Usage: python scan_reflect2.py M N [T]"""
import json
import os
import sys
from fractions import Fraction
from cl import *  # noqa

M = int(sys.argv[1]) if len(sys.argv) > 1 else 4
N = int(sys.argv[2]) if len(sys.argv) > 2 else 4
T = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
VE = Fraction(-4, 15)
IN = os.path.join(HERE, f"scan_reflect_M{M}.jsonl")
OUT = os.path.join(HERE, f"scan_reflect2_M{M}_N{N}.jsonl")
done = set()
if os.path.exists(OUT):
    done = {(json.loads(l)["Y"], json.loads(l)["cls"]) for l in open(OUT)}
with open(OUT, "a") as f:
    for l in open(IN):
        rec = json.loads(l)
        for row in rec.get("rows", []):
            if not row["reflect"] or (rec["Y"], row["cls"]) in done:
                continue
            X = [tuple(p) for p in row["products"] if p[0] not in CHAIN]
            j = [CHAIN.index(p[0]) + 1 for p in row["products"] if p[0] in CHAIN][0]
            outs = []
            for t0 in range(15):
                try:
                    sc = X + [(CHAIN[N - 1],) + place_right_of(X, CHAIN[N - 1],
                              max(pos(g, 0) for g in X) + 60, t0)]
                    ok, prods = ca(sc, T)
                    es = [p for p in prods if p[0] in CHAIN]
                    oth = [p for p in prods if p[0] not in CHAIN]
                    ret = ok and len(es) == 1 and oth and all(
                        LIB.gliders[p[0]].velocity < VE for p in oth)
                    outs.append({"t0": t0, "names": [p[0] for p in prods],
                                 "ret": bool(ret)})
                except Exception as e:  # recorded loudly
                    outs.append({"t0": t0, "error": repr(e)[:200]})
            r = {"Y": rec["Y"], "cls": row["cls"], "j": j, "X": [p[0] for p in X],
                 "outs": outs}
            f.write(json.dumps(r) + "\n")
            f.flush()
            hits = [o for o in outs if o.get("ret")]
            print(rec["Y"], row["cls"], "E^%d" % j, r["X"], "returns:",
                  [(o["t0"], o["names"]) for o in hits], flush=True)
print("done", flush=True)
