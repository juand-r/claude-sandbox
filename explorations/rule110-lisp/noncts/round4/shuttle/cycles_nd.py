"""Nondeterministic cycle search: like cycles_quick.py, but multi-class
rows (frontier_*.jsonl) give one transition per class; a cycle in this
graph is a CANDIDATE perpetual bouncer (classes must then be realised by
one box geometry: check by direct simulation). Reports reachable cycles
via DFS from every clean R-reflection start."""
import json, sys
from collections import defaultdict, Counter
sys.dont_write_bytecode = True
from bgraph import canon_bits

trans = {"R": defaultdict(set), "L": defaultdict(set)}
kinds = Counter()
hc = {}


def add(r, head_canon):
    key = (head_canon, tuple(r["wall_canon"]))
    if r["kind"] == "reflect":
        trans[r["side"]][key].add((tuple(r["wall_out_canon"]), tuple(r["head_out_canon"])))
    else:
        trans[r["side"]][key].add(("STOP", r["kind"]))


for l in open("bounce_table.jsonl"):
    r = json.loads(l)
    h = r["head"]
    k = (h["bits"], h["pR"], h["p"])
    if k not in hc:
        hc[k] = tuple(canon_bits(h["bits"], h["pR"], h["p"]))
    add(r, hc[k])
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l)
        add(r, tuple(r["head_canon"]))
walls = {k[1] for s in "RL" for k in trans[s]}
print("R keys", len(trans["R"]), "L keys", len(trans["L"]), "walls", len(walls))
# graph on states (dir, head, V, W); DFS with depth limit
sys.setrecursionlimit(100000)
found = []
ends = Counter()
starts = [(h, W) for (h, W), outs in trans["R"].items() if any(o[0] != "STOP" for o in outs)]
visited_global = set()
for (h, W) in starts:
    for V in walls:
        stack = [(("R", h, V, W), [])]
        while stack:
            st, path = stack.pop()
            if st in path:
                found.append(path[path.index(st):] + [st])
                continue
            if len(path) > 40:
                ends["depth"] += 1
                continue
            if st in visited_global:
                continue
            visited_global.add(st)
            d, hh, VV, WW = st
            key = (hh, WW) if d == "R" else (hh, VV)
            outs = trans[d].get(key)
            if not outs:
                ends["unknown " + d] += 1
                continue
            for o in outs:
                if o[0] == "STOP":
                    ends[d + " " + o[1]] += 1
                    continue
                w2, h2 = o
                nxt = ("L", h2, VV, w2) if d == "R" else ("R", h2, w2, WW)
                stack.append((nxt, path + [st]))
print(ends)
print("cycles", len(found))
for c in found[:5]:
    print(len(c) - 1, [x[0] for x in c])
