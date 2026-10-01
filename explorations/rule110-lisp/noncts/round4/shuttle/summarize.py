"""Summarize frontsim output: per (K, J, empty, left products) the trains
that give that clean outcome for EVERY n tested in some class k."""
import sys, json
from collections import defaultdict
fn = sys.argv[1]
agg = defaultdict(list)
for l in open(fn):
    r = json.loads(l)
    byk = defaultdict(dict)
    for item in r["res"]:
        k, n = item[0], item[1]
        byk[k][n] = None if item[2] is None else tuple(map(str, item[2:4])) + (str(item[4]),) + (tuple(item[5]) if len(item) > 5 else ())
    for k, d in byk.items():
        vals = set(d.values())
        if len(vals) == 1 and None not in vals:
            agg[vals.pop()].append((r["i"], r["bits"], r["pR"], k))
        elif any(v is not None for v in vals):
            agg[("n-dependent",) + tuple(sorted(str(v) for v in vals))].append((r["i"], r["bits"], r["pR"], k))
for key in sorted(agg, key=str):
    print(len(agg[key]), key, agg[key][:3])
