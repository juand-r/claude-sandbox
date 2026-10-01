"""Census over time for Z items 'name:k:x;...' (rej path scene, build2).
    python t_zitems.py ITEMS [times]"""
import sys
import numpy as np
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from census import census, MAX_DT
from reads import tiles_of
items = [(tiles_of(n), int(k), int(x)) for n, k, x in (s.split(":") for s in sys.argv[1].split(";"))]
times = list(map(int, sys.argv[2].split(","))) if len(sys.argv) > 2 else [500, 1500, 2000, 2500, 3000]
S = zscreen.setup()
for tape in ("NYYN", "NNYY"):
    K0, sc = S[tape][:2]
    for label, seg in (("plain", sc.seg), ("Z", zscreen.build2(sc, K0, items))):
        print(tape, label)
        for t in times:
            w = pack(seg); w = step_packed_n(w, t - MAX_DT); rows = []
            for j in range(MAX_DT + 1):
                c = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 + WLO, TIN + t)
                rows.append(c[i:i + WHI - WLO]); w = step_packed_n(w, 1)
            print("  ", t, " ".join(f"{kk}{a + WLO}" for a, b, kk in census(np.array(rows))))
