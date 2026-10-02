import json, sys
from collections import Counter
def cls(v):
    if v is None: return "-"
    return "Y" if v[0] == 0 else ("N" if v[2] == 0 else "x")
c = Counter()
for l in open(sys.argv[1]):
    r = json.loads(l)
    rk = cls(r.get("NYYN")) + cls(r.get("NNYY")); ak = cls(r.get("YYNN")) + cls(r.get("YNYN"))
    c[(rk, ak)] += 1
    if (rk, ak) != ("xx", "xx") and rk != "x-":
        print(rk, ak, r)
print(c)
