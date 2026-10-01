"""Spacetime picture of a local scene (Ebar frame, rel K0), with Z items.
    python pic.py MODE k2 x2 k1 x1 T0 T1 XLO XHI out.png   (MODE rej|acc; tape via env)"""
import sys, os
import numpy as np
from zscreen import *
from engine import save_png
mode = sys.argv[1]; k2, x2, k1, x1 = map(int, sys.argv[2:6])
t0, t1, xlo, xhi = map(int, sys.argv[6:10]); outp = sys.argv[10]
tapes = ("NYYN", "NNYY") if mode == "rej" else ("YYNN", "YNYN")
E = ebar_tiles()
panels = []
for tape in tapes:
    m = Machine(tape, ["YNNNNN"], TIN + t1 + 500, left_periods=3, right_periods=2)
    K0 = [a for n, a, b in m.blocks if n == "K"][0]
    sc = Scene(m, m.row, TIN, K0 + xlo, K0 + xhi, t1 + 100)
    for z in (False, True):
        seg = sc.seg if not z else build(sc, K0, [(E, k2, x2), (E, k1, x1)])
        w = pack(seg); rows = []
        w = step_packed_n(w, t0)
        for t in range(t0, t1, 2):
            c = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 + xlo, TIN + t)
            d = c ^ np.roll(c, TILE) | c ^ np.roll(c, -TILE)
            rows.append(1 - d[i:i + xhi - xlo]); w = step_packed_n(w, 2)
        panels.append(np.array(rows))
        panels.append(np.full((len(rows), 6), 1, np.uint8)[:, :0])
sep = np.zeros((panels[0].shape[0], 4), np.uint8)
img = np.concatenate([np.concatenate([p, sep], 1) for p in panels if p.size], 1)
save_png(img, outp)
print(img.shape)
