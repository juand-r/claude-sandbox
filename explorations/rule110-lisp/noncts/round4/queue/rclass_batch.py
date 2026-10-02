import sys, json
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from rclass import debris_translation, mod_V
from reads import tiles_of
S = zscreen.setup()
# controls
K0, sc = S["NNYY"][:2]
print("control plain N:", debris_translation(S, "NNYY", sc.seg, K0))
seen = set()
for line in open("remnants.txt"):
    if not line.startswith("SAME"):
        continue
    r = json.loads(line[line.index("{"):])
    key = json.dumps(r, sort_keys=True)
    if key in seen: continue
    seen.add(key)
    if "A" in r:
        items = [(tiles_of(r["B"]), r["kb"], r["xb"]), (tiles_of(r["A"]), r["ka"], r["xa"])]
    elif "obj" in r:
        items = [(tiles_of(r["obj"]), r["k"], r["x"])]
    else:
        items = [(tiles_of("Ebar"), r["k2"], r["x2"]), (tiles_of("Ebar"), r["k1"], r["x1"])]
    out = []
    for tape in ("NYYN", "NNYY"):
        K0, sc = S[tape][:2]
        seg = zscreen.build2(sc, K0, items)
        tr = debris_translation(S, tape, seg, K0)
        out.append((tr, mod_V(*tr) if tr else None))
    print(out, key, flush=True)
