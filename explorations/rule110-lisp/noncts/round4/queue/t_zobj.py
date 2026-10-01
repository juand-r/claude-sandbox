"""Inspect a single-object Z (library name) in the rej path: census over time.
    python t_zobj.py NAME k x [times]"""
import sys
import numpy as np
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from census import census, MAX_DT
name, k, x = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
times = list(map(int, sys.argv[4].split(","))) if len(sys.argv) > 4 else [500, 1500, 2000, 2500, 3000]
S = zscreen.setup(); tiles = glider_tiles(name)
for tape in ("NYYN", "NNYY"):
    K0, sc = S[tape][:2]
    for label, seg in (("plain", sc.seg), ("Z", zscreen.build(sc, K0, [(tiles, k, x)]))):
        print(tape, label)
        for t in times:
            w = pack(seg); w = step_packed_n(w, t - MAX_DT); rows = []
            for j in range(MAX_DT + 1):
                c = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 + WLO, TIN + t - MAX_DT + j)
                rows.append(c[i:i + WHI - WLO]); w = step_packed_n(w, 1)
            print("  ", t, " ".join(f"{kk}{a + WLO}" for a, b, kk in census(np.array(rows))))
