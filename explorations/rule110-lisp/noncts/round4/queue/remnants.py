"""For every forced-N candidate: the left-part census (lab frame, at the end
of the scene) for the Y and N tapes, and whether they coincide."""
import sys, json
import numpy as np
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from vequiv import vclass, lab_window
from reads import tiles_of
from census import census, MAX_DT
S = zscreen.setup()
def cls(v):
    if v is None: return "-"
    return "Y" if v[0] == 0 else ("N" if v[2] == 0 else "x")
def left_census(tape, seg):
    K0, sc = S[tape][:2]
    T = zscreen.T
    rows = []
    w = pack(seg); w = step_packed_n(w, T - MAX_DT)
    for j in range(MAX_DT + 1):
        c = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 + zscreen.WLO, zscreen.TIN + T)
        rows.append(c[i:i + zscreen.SPLIT - zscreen.WLO]); w = step_packed_n(w, 1)
    return [(a + zscreen.WLO, k) for a, b, k in census(np.array(rows))]
print("plain N", left_census("NNYY", S["NNYY"][1].seg), "plain Y", left_census("NYYN", S["NYYN"][1].seg))
for f in sys.argv[1:]:
    for line in open(f):
        r = json.loads(line)
        if cls(r.get("NYYN")) + cls(r.get("NNYY")) != "NN":
            continue
        if "A" in r:
            items = [(tiles_of(r["B"]), r["kb"], r["xb"]), (tiles_of(r["A"]), r["ka"], r["xa"])]
        elif "obj" in r:
            items = [(tiles_of(r["obj"]), r["k"], r["x"])]
        else:
            items = [(tiles_of("Ebar"), r["k2"], r["x2"]), (tiles_of("Ebar"), r["k1"], r["x1"])]
        cy = left_census("NYYN", zscreen.build2(S["NYYN"][1], S["NYYN"][0], items))
        cn = left_census("NNYY", zscreen.build2(S["NNYY"][1], S["NNYY"][0], items))
        same = zscreen.build2(S["NYYN"][1], S["NYYN"][0], items) is not None
        print("SAME" if cy == cn else "diff", cy, cn, json.dumps({k: v for k, v in r.items() if k not in ("NYYN", "NNYY")}), flush=True)
