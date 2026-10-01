"""For every forced-N (or other non-normal clean) candidate in a screen
file, test V-equivalence of the debris (vequiv.vclass), both tapes.
    python vfilter.py FILE [FILE...]"""
import sys, json
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from vequiv import vclass
from reads import tiles_of
S = zscreen.setup()
def cls(v):
    if v is None: return "-"
    return "Y" if v[0] == 0 else ("N" if v[2] == 0 else "x")
for f in sys.argv[1:]:
    for line in open(f):
        r = json.loads(line)
        k = cls(r.get("NYYN")) + cls(r.get("NNYY"))
        if k not in ("NN", "NY", "YY", "YN"):
            continue
        if "A" in r:
            items = [(tiles_of(r["B"]), r["kb"], r["xb"]), (tiles_of(r["A"]), r["ka"], r["xa"])]
        elif "obj" in r:
            items = [(tiles_of(r["obj"]), r["k"], r["x"])]
        else:
            items = [(tiles_of("Ebar"), r["k2"], r["x2"]), (tiles_of("Ebar"), r["k1"], r["x1"])]
        out = []
        for tape in ("NYYN", "NNYY"):
            Kt, sct = S[tape][:2]
            seg = zscreen.build2(sct, Kt, items)
            out.append(vclass(S, tape, seg, Kt) if seg is not None else "nofit")
        print(k, out, json.dumps(r), flush=True)
