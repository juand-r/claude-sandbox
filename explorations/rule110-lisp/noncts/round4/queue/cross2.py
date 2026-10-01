"""Ebar pairs far in front of P (tile starts in [-345, -170)); do s_1's four
C's cross both intact?  Census at t_in + 1300 over [K0-160, K0+30): exactly
4 C's and nothing untyped/A.  Also record C positions (displacement vs plain).
    python cross2.py TAPE"""
import sys
import numpy as np
from zscreen import *
from census import census, MAX_DT
tape = sys.argv[1]
S = setup(); K0, sc = S[tape][:2]; E = ebar_tiles()
def cens(seg, t, lo, hi):
    w = pack(seg); w = step_packed_n(w, t - MAX_DT); rows = []
    for j in range(MAX_DT + 1):
        c = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 + lo, TIN + t)
        rows.append(c[i:i + hi - lo]); w = step_packed_n(w, 1)
    return [(a + lo, k) for a, b, k in census(np.array(rows))]
print("plain", cens(sc.seg, 1300, -160, 30))
p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + RA))
for k2, x2, p1 in placements(sc, K0, E, RA, -190, p0):
    for k1, x1, _ in placements(sc, K0, E, x2 + 20, -170, p1):
        seg = build(sc, K0, [(E, k2, x2), (E, k1, x1)])
        if seg is None: continue
        cs = cens(seg, 1300, -160, 30)
        if sum(1 for a, k in cs if k == "C") == 4 and all(k in "CE" for a, k in cs):
            print(k2, x2, k1, x1, cs, flush=True)
