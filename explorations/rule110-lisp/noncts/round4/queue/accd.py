"""Debris classes of acceptor-path forced-N candidates (zaccpair.jsonl).
Reference: standard acc-path N read (tape YNYN)."""
import json, sys
from accZ_common import *
from dclass import debris_classes
def cls(v):
    if v is None: return "-"
    return "Y" if v[0] == 0 else ("N" if v[2] == 0 else "x")
ref = S["YNYN"][1].seg
K0, sc = S["YNYN"][:2]
print("control", debris_classes(sc, K0, sc.seg, ref, T))
for l in open(sys.argv[1]):
    r = json.loads(l)
    if cls(r.get("YYNN")) + cls(r.get("YNYN")) != "NN": continue
    items = [(tiles_of(r["B"]), r["kb"], r["xb"]), (tiles_of(r["A"]), r["ka"], r["xa"])]
    res = []
    for t in ("YYNN", "YNYN"):
        K0t, sct = S[t][:2]
        seg = build_tight(sct.seg, sct, K0t, items, -104, -2)
        d, refpos = debris_classes(sct, K0t, seg, S["YNYN"][1].seg if t == "YNYN" else ref, T)
        bad = [o for o in d if o[1] is None or o[1][3] != (0, 0)]
        res.append((len(d), len(refpos), len(bad), bad[:3]))
    print(json.dumps({k: r[k] for k in ("A", "ka", "xa", "B", "kb", "xb")}), res, flush=True)
