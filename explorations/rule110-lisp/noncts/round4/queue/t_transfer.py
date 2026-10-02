"""Do the 1v forced-N / normal results transfer to the 2v machine?
Run listed Z's in both and print scores."""
import os, sys
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from vequiv import vclass
from reads import tiles_of
S = zscreen.setup()
print("VMULT", zscreen.VMULT, "TIN", zscreen.TIN)
for tape in S:
    K0, sc = S[tape][:2]
    print("control", tape, zscreen.score(S, tape, sc.run(sc.seg, zscreen.T)))
Z = [("pair forcedN", "Ebar:0:-73;Ebar:14:-4"), ("compound -243", "Ebar@(0,0)+Ebar@(-1,39):19:-243"),
     ("E3+Ebar", "Ebar:15:-36;E^3:3:-12"), ("normal exact", "Ebar_8_Ebar:5:-28"), ("normal pair", "Ebar:21:-50;Ebar:7:-11")]
for label, spec in Z:
    items = [(tiles_of(n), int(k), int(x)) for n, k, x in (s.rsplit(":", 2) for s in spec.split(";"))]
    out = []
    for tape in ("NYYN", "NNYY"):
        K0, sc = S[tape][:2]
        seg = zscreen.build2(sc, K0, items)
        out.append((zscreen.score(S, tape, sc.run(seg, zscreen.T)), vclass(S, tape, seg, K0)) if seg is not None else "nofit")
    print(label, out, flush=True)
