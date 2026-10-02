import json, sys
from collections import Counter
def cls(v):
    if not isinstance(v, list): return "?"
    return "Y" if v[0] == 0 else ("N" if v[2] == 0 else "x")
c = Counter(); hits = []
for l in open(sys.argv[1]):
    r = json.loads(l)
    key = ["rejA0" if r.get("rejA") == 0 else "rejA!"]
    if "rejB" in r:
        key.append("rej:" + cls(r["rejB"].get("NYYN")) + cls(r["rejB"].get("NNYY")))
        key.append("accA0" if r.get("accA") == 0 else "accA!")
    if "accB" in r:
        key.append("acc:" + cls(r["accB"].get("YYNN")) + cls(r["accB"].get("YNYN")))
    c[tuple(key)] += 1
    if "accB" in r: hits.append(r)
for k, v in c.most_common(): print(v, k)
for h in hits[:20]: print(h)
