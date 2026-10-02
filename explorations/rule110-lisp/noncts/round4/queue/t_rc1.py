import sys
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from rclass import debris_translation, mod_V
from reads import tiles_of
S = zscreen.setup()
for spec in sys.argv[1:]:
    items = [(tiles_of(n), int(k), int(x)) for n, k, x in (s.rsplit(":", 2) for s in spec.split(";"))]
    out = []
    for tape in ("NYYN", "NNYY"):
        K0, sc = S[tape][:2]
        seg = zscreen.build2(sc, K0, items)
        tr = debris_translation(S, tape, seg, K0)
        out.append((tr, mod_V(*tr) if tr else None, zscreen.score(S, tape, sc.run(seg, zscreen.T))))
    print(spec, out)
