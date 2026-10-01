"""Inspect a Z placement: typed census over time (Ebar frame, rel K0).
    python t_z.py k2 x2 k1 x1 [times]"""
import sys
import numpy as np
from zscreen import *
from census import census, MAX_DT
k2, x2, k1, x1 = map(int, sys.argv[1:5])
times = list(map(int, sys.argv[5].split(","))) if len(sys.argv) > 5 else [500, 1500, 2000, 2500, 3000]
S = setup()
E = ebar_tiles()
for tape in ("NYYN", "NNYY"):
    K0, sc = S[tape][:2]
    for label, seg in (("plain", sc.seg), ("Z", build(sc, K0, [(E, k2, x2), (E, k1, x1)]))):
        print(tape, label)
        for t in times:
            seg_t = unpack(step_packed_n(pack(seg), t - MAX_DT), len(seg))
            rows = [seg_t]
            w = pack(seg_t)
            for _ in range(MAX_DT):
                w = step_packed_n(w, 1); rows.append(unpack(w, len(seg)))
            i = sc.ebar_to_seg(K0 + WLO, TIN + t)
            h = np.array([r[i:i + (WHI - WLO)] for r in rows])
            cs = census(h)
            print("  ", t, " ".join(f"{k}{a + WLO}" for a, b, k in cs))
