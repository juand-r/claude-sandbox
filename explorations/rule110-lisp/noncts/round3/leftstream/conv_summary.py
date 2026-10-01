"""Summarise conv_scan.jsonl: objects covered, stable placements, flags,
and the non-trivial outcomes (anything other than rod +-1 with the
parked object unchanged)."""
import json, collections
from lsl import LIB, nval
from fractions import Fraction
rs = [json.loads(l) for l in open("conv_scan.jsonl")]
objs = list(dict.fromkeys(r["O"] for r in rs))
allobj = [n for n, g in LIB.gliders.items() if g.velocity == Fraction(-4, 15)]
st = [r for r in rs if "I_L" in r]
print(f"{len(rs)} placements, {len(objs)}/{len(allobj)} objects started, "
      f"{len(st)} stable-alone placements; max width so far "
      f"{max(LIB.gliders[o].width for o in objs)}")
fl = [r for r in st if r.get("I_L_flag") or r.get("Z_L_flag")]
print("FLAGGED:", fl)
odd = collections.Counter()
for r in st:
    for F, exp in (("I_L", "E^5"), ("Z_L", "E^3")):
        if r[F] != [exp, r["O"]]:
            odd[(F, tuple(r[F]))] += 1
print("non-trivial outcomes (top 12):")
for k, c in odd.most_common(12):
    print("  ", c, k)
