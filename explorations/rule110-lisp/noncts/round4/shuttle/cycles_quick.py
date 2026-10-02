"""Quick cycle search on bounce_table.jsonl (theory owns the full search).
State = (dir, head canon, left wall canon, right wall canon). Deterministic
steps from the canonical-keyed tables; a cycle = perpetual bouncer.
Reports cycles and how chains end (unknown head/wall, non-reflect)."""
import json, sys
from collections import Counter
sys.dont_write_bytecode = True
from bgraph import canon_bits

R, L = {}, {}
hc = {}
for l in open("bounce_table.jsonl"):
    r = json.loads(l)
    h = r["head"]
    k = (h["bits"], h["pR"], h["p"])
    if k not in hc:
        hc[k] = tuple(canon_bits(h["bits"], h["pR"], h["p"]))
    key = (hc[k], tuple(r["wall_canon"]))
    val = (r["kind"], tuple(r.get("wall_out_canon") or ()), tuple(r.get("head_out_canon") or ()),
           (r.get("wall_out") or {}).get("dx"))
    (R if r["side"] == "R" else L)[key] = val
walls = {k[1] for k in R} | {k[1] for k in L}
print("R pairs", len(R), "L pairs", len(L), "walls", len(walls))
Rrefl = {k: v for k, v in R.items() if v[0] == "reflect"}
Lrefl = {k: v for k, v in L.items() if v[0] == "reflect"}
print("R reflect", len(Rrefl), "L reflect", len(Lrefl))
# heads known on each side
Rheads = {k[0] for k in R}
Lheads = {k[0] for k in L}
ends = Counter()
cycles = []
for (h, W), (kind, W2, g, dx) in Rrefl.items():
    if g not in Lheads:
        ends["R-out head not in L list"] += 1
        continue
    for V in walls:
        st = ("R", h, V, W)
        seen = {st: 0}
        path = [st]
        cur = st
        while True:
            d, hh, VV, WW = cur
            if d == "R":
                v = R.get((hh, WW))
                if v is None:
                    ends["unknown R pair"] += 1; break
                if v[0] != "reflect":
                    ends["R " + v[0]] += 1; break
                nxt = ("L", v[2], VV, v[1])
            else:
                v = L.get((hh, VV))
                if v is None:
                    ends["unknown L pair"] += 1; break
                if v[0] != "reflect":
                    ends["L " + v[0]] += 1; break
                nxt = ("R", v[2], v[1], WW)
            if nxt in seen:
                cycles.append(path[seen[nxt]:])
                ends["CYCLE"] += 1
                break
            seen[nxt] = len(path)
            path.append(nxt)
            cur = nxt
print(ends)
print("cycles", len(cycles))
for c in cycles[:5]:
    print(len(c), c[:4])
