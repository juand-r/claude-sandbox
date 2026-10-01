import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from vequiv import *
S = zscreen.setup()
K0, sc = S["NNYY"][:2]
print("plain N vs itself:", vclass(S, "NNYY", sc.seg, K0))
K0y, scy = S["NYYN"][:2]
print("plain Y-read left part vs N-read:", vclass(S, "NYYN", scy.seg, K0y))
comp = glider_tiles("Ebar@(0,0)+Ebar@(-1,39)")
for x in (-299, -243, -187, -131, -75):
    for tape in ("NYYN", "NNYY"):
        Kt, sct = S[tape][:2]
        seg = zscreen.build(sct, Kt, [(comp, 19, x)])
        print("compound", x, tape, vclass(S, tape, seg, Kt))
