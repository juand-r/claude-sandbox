"""Inspect an answer converter (gap at K0+310, D): census over time.
    python t_conv.py D kb xb ka xa [times]"""
import sys
import numpy as np
import zconv
from zconv import *
from census import census, MAX_DT
D, kb, xb, ka, xa = map(int, sys.argv[1:6])
times = list(map(int, sys.argv[6].split(","))) if len(sys.argv) > 6 else [2500, 3000, 3500, 4000, 4800]
tapes = ("NYYN", "NNYY")
S = setup(D, tapes); E = ebar_tiles()
for t in tapes:
    K0, sc, g, _ = S[t]
    for label, seg in (("gap-plain", g), ("Z", build_tight(g, sc, K0, [(E, kb, xb), (E, ka, xa)], CUT + 5, CUT + D - 5))):
        print(t, label)
        for tt in times:
            w = pack(seg); w = step_packed_n(w, tt - MAX_DT); rows = []
            for j in range(MAX_DT + 1):
                c = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 - 100, TIN + tt)
                rows.append(c[i:i + 1100]); w = step_packed_n(w, 1)
            print("  ", tt, " ".join(f"{kk}{a - 100}" for a, b, kk in census(np.array(rows))))
