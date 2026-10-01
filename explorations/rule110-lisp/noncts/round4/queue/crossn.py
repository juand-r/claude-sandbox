"""Order of the crossing shift: chains of 2m Ebars far in front of P that the
Y symbol's C's all cross with a uniform shift of +7 per Ebar (lab census at
t_in + 1300); then P_1's read. Greedy: add one pair at a time.
Ebars are placed from the left end of [K0-345, ...), 2m <= 8; the region
left of P must be wide enough: we move t_in earlier? No: we keep t_in and
pack Ebars with minimum tile spacing SP.
    python crossn.py TAPE MMAX SP"""
import sys
import numpy as np
from zscreen import *
from census import census, MAX_DT
tape, MMAX, SP = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
import zscreen
zscreen.TIN, zscreen.T, zscreen.RA = 28500, 6000, -1100
TIN, T, RA = zscreen.TIN, zscreen.T, zscreen.RA
DT = 1300 + 3000          # census time (C's just left of P)
S = zscreen.setup(); K0, sc = S[tape][:2]; E = ebar_tiles()
def cens(seg, t, lo, hi):
    w = pack(seg); w = step_packed_n(w, t - MAX_DT); rows = []
    for j in range(MAX_DT + 1):
        c = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 + lo, TIN + t)
        rows.append(c[i:i + hi - lo]); w = step_packed_n(w, 1)
    return [(a + lo, k) for a, b, k in census(np.array(rows))]
PL = [a for a, k in cens(sc.seg, DT, -160, 30) if k == "C"]
print("plain C", PL, "plain read", zscreen.score(S, tape, sc.run(sc.seg, T)), flush=True)
p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + RA))
chain, p = [], p0
DBG = {}
for m in range(1, MMAX + 1):
    last = chain[-1][1] if chain else RA - SP
    ok = False
    for ka, xa, pa in placements(sc, K0, E, last + SP, last + SP + 120, p):
        for kb, xb, pb in placements(sc, K0, E, xa + SP, xa + SP + 120, pa):
            c2 = chain + [(ka, xa), (kb, xb)]
            if xb > -110: continue
            seg = zscreen.build(sc, K0, [(E, k, x) for k, x in c2])
            if seg is None: continue
            cs = cens(seg, DT, -160, 30)
            Cs = [a for a, k in cs if k == "C"]
            if m == 2 and len(Cs) == 4 and all(k in "CE" for a, k in cs):
                DBG[tuple(c - q for c, q in zip(Cs, PL))] = DBG.get(tuple(c - q for c, q in zip(Cs, PL)), 0) + 1
            if len(Cs) == 4 and all(k in "CE" for a, k in cs) and {c - q for c, q in zip(Cs, PL)} == {14 * m}:
                chain, p, ok = c2, pb, True
                print(2 * m, "Ebars", chain, "C", Cs, "read", zscreen.score(S, tape, sc.run(seg, T)), flush=True)
                break
        if ok: break
    if not ok:
        print("no extension at m =", m, DBG); break
