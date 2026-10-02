"""For the LEFT gate trains of lclass.py (E^2 unmoved in some class, E walks
in some class), test the train against E^4 (= E + B^3, a left window closed
by a K3 shot from R1's zero) in its 3 classes: is it neutral AND unmoved?
Exact CA (lscan.py machinery). Output: lgate4.jsonl."""
import json, os
from lscan import *  # noqa
rs = [json.loads(l) for l in open(os.path.join(HERE, "lscan.jsonl"))]
out = open(os.path.join(HERE, "lgate4.jsonl"), "w")
n = 0
for r in rs:
    if "error" in r:
        continue
    wk = {k: v[1] for k, v in r.items() if k.startswith("E/") and v[0] == ["E"] and abs(v[1]) > 1e-9}
    if not wk:
        continue
    q = (r["bits"], 0, r["pR"], 0)
    res = {}
    for t0 in (0, 1, 2):
        st, seed = right_of("E^4", t0, q)
        ref = Fraction(seed[1]) - VE * seed[0]
        prods = run([q, st], None)
        names = [p[0] for p in prods]
        sh = float(lat(prods[0]) - ref) if len(prods) == 1 and names[0] in CHAIN else None
        res[f"E^4/{t0}"] = [names, sh]
    good = [k for k, v in res.items() if v[0] == ["E^4"] and v[1] is not None and abs(v[1]) < 1e-9]
    rec = {"i": r["i"], "bits": r["bits"], "pR": r["pR"], "walkE": wk, **res, "E4_unmoved": good}
    out.write(json.dumps(rec) + "\n")
    n += 1
    if good:
        print(rec, flush=True)
print("walking trains tested:", n)
