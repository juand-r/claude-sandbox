"""Controls for dclass: plain vs plain (all (0,0) with dt=dx=0); known
cases: rej-path E3+Ebar (Y: remnant (0,0) up to V; N: not)."""
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from dclass import debris_classes
from reads import tiles_of
S = zscreen.setup()
for tape in ("NYYN", "NNYY"):
    K0, sc = S[tape][:2]
    ref = S["NNYY"][1].seg
    print(tape, "plain vs plain-N:", debris_classes(sc, K0, sc.seg, ref, zscreen.T))
    for spec in ("Ebar:15:-36;E^3:3:-12", "Ebar@(0,0)+Ebar@(-1,39):19:-243"):
        items = [(tiles_of(n), int(k), int(x)) for n, k, x in (s.rsplit(":", 2) for s in spec.split(";"))]
        seg = zscreen.build2(sc, K0, items)
        print(tape, spec, debris_classes(sc, K0, seg, ref, zscreen.T))
