"""Chains of n Ebars far in front of P (tile starts in [-345, -150)) that the
Y symbol's four C's cross intact (lab census at t_in + 1300: 4 C's only).
Then the read: right part vs standard Y/N windows (zscreen.score).
    python cross4.py TAPE N"""
import sys
import numpy as np
from zscreen import *
from census import census, MAX_DT
tape, N = sys.argv[1], int(sys.argv[2])
S = setup(); K0, sc = S[tape][:2]; E = ebar_tiles()
def cens(seg, t, lo, hi):
    w = pack(seg); w = step_packed_n(w, t - MAX_DT); rows = []
    for j in range(MAX_DT + 1):
        c = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 + lo, TIN + t)
        rows.append(c[i:i + hi - lo]); w = step_packed_n(w, 1)
    return [(a + lo, k) for a, b, k in census(np.array(rows))]
PL = [a for a, k in cens(sc.seg, 1300, -140, 30) if k == 'C']
print('plain C', PL)
p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + RA))
def extend(chain, p):
    last = chain[-1][1] if chain else RA - 20
    for k, x, p1 in placements(sc, K0, E, last + 20, -150, p):
        yield chain + [(k, x)], p1
found = 0
def rec(chain, p):
    global found
    if found >= 6: return
    if len(chain) == N:
        if N % 2: return
        seg = build(sc, K0, [(E, k, x) for k, x in chain])
        if seg is None: return
        cs = cens(seg, 1300, -140, 30)
        Cs = [a for a, k in cs if k == "C"]
        if len(Cs) == 4 and all(k in "CE" for a, k in cs) and len({c - p for c, p in zip(Cs, PL)}) == 1:
            sc_ = score(S, tape, sc.run(seg, T))
            print(chain, cs, "read", sc_, flush=True); found += 1
        return
    for ch, p1 in extend(chain, p):
        if found >= 6: return
        rec(ch, p1)
rec([], p0)
