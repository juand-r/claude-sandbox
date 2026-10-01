"""Single-class consistency check of an exported table: all time-phase
variants of the same physical (head, wall) pair must give the same kind
and the same canonical outputs (and the same displacement up to the
variants' own offsets, not checked here)."""
import sys, json
sys.dont_write_bytecode = True
from collections import defaultdict
from bgraph import canon_bits

fn = sys.argv[1]
rows = [json.loads(l) for l in open(fn)]
hc = {}
groups = defaultdict(set)
for r in rows:
    h = r["head"]
    k = (h["bits"], h["pR"], h["p"])
    if k not in hc:
        hc[k] = canon_bits(h["bits"], h["pR"], h["p"])
    key = (r["side"], hc[k], tuple(r["wall_canon"]))
    out = (r["kind"], tuple(r.get("wall_out_canon") or ()), tuple(r.get("head_out_canon") or ()))
    groups[key].add(out)
n = len(groups)
bad = {k: v for k, v in groups.items() if len(v) > 1}
print("physical pairs", n, "inconsistent", len(bad))
for k, v in list(bad.items())[:10]:
    print(k, v)
