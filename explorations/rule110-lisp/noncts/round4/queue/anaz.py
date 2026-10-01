import json, sys
from collections import Counter
rs=[json.loads(l) for l in open(sys.argv[1])]
A, B = sys.argv[2], sys.argv[3]   # tape names: s_1 = Y tape, s_1 = N tape
def cls(v):
    if v is None: return "-"
    return "Y" if v[0]==0 else ("N" if v[2]==0 else "x")
c=Counter(); hits=[]
for r in rs:
    key=cls(r.get(A))+cls(r.get(B)) if r.get(A) is not None else "--"
    c[key]+=1
    if key in ("NN","NY","YY"): hits.append((key, r))
print(len(rs), c)
for k, r in sorted(hits, key=lambda h: (h[0], h[1][A][4] + h[1][B][5])):
    print(k, r)
