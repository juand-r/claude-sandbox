"""Do tape C's cross E^2 / E^4 far in front of the reader, and what is the
net effect of an E^2 + E^4 pair (slips 1 and 13 = -1) on the next read?
Pairs (E^4 left, E^2 right or vice versa) at placements in [-345, -150):
record reads where the C's survive (4 C's at t_in+1300) and the read
score. Rej path tapes."""
import sys
import numpy as np
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from census import census, MAX_DT
from reads import tiles_of
from create import placements as plc
S = zscreen.setup()
def cens(sc, K0, seg, t, lo, hi):
    w = pack(seg); w = step_packed_n(w, t - MAX_DT); rows = []
    for j in range(MAX_DT + 1):
        c = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 + lo, zscreen.TIN + t)
        rows.append(c[i:i + hi - lo]); w = step_packed_n(w, 1)
    return [(a + lo, k) for a, b, k in census(np.array(rows))]
from collections import Counter
for A, B in (("E^2", "E^4"), ("E^4", "E^2")):
    TA_, TB_ = tiles_of(A), tiles_of(B)
    K0, sc = S["NYYN"][:2]
    PL = [a for a, k in cens(sc, K0, sc.seg, 1300, -160, 30) if k == "C"]
    p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + zscreen.RA))
    c = Counter(); ex = []
    for kb, xb, p1 in plc(sc, K0, TB_, -345, -220, p0):
        for ka, xa, _ in plc(sc, K0, TA_, xb + 40, -170, p1):
            seg = zscreen.build2(sc, K0, [(TB_, kb, xb), (TA_, ka, xa)])
            if seg is None: continue
            cs = cens(sc, K0, seg, 1300, -160, 30)
            Cs = [a for a, k in cs if k == "C"]
            if len(Cs) == 4 and all(k in "CE" for a, k in cs):
                sh = tuple(x - y for x, y in zip(Cs, PL))
                sc_ = zscreen.score(S, "NYYN", sc.run(seg, zscreen.T))
                c[(sh, "Y" if sc_[0] == 0 else ("N" if sc_[2] == 0 else "x"))] += 1
                if len(ex) < 3 and sc_[0] == 0: ex.append(((B, kb, xb), (A, ka, xa), sc_))
    print(B, "then", A, c.most_common(8), ex)
