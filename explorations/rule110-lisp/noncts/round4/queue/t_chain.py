"""Direct test of explicit Ebar chains (rej path, t_in=28500): census of the
C's (lab window) at DT and the read.  python t_chain.py TAPE 'k,x;k,x;...'"""
import sys
import numpy as np
import zscreen
zscreen.TIN, zscreen.T, zscreen.RA = 28500, 6000, -1100
from zscreen import *
from census import census, MAX_DT
tape = sys.argv[1]
S = zscreen.setup(); K0, sc = S[tape][:2]; E = ebar_tiles()
def cens(seg, t, lo, hi):
    w = pack(seg); w = step_packed_n(w, t - MAX_DT); rows = []
    for j in range(MAX_DT + 1):
        c = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 + lo, zscreen.TIN + t)
        rows.append(c[i:i + hi - lo]); w = step_packed_n(w, 1)
    return [(a + lo, k) for a, b, k in census(np.array(rows))]
for arg in sys.argv[2:]:
    chain = [tuple(map(int, s.split(","))) for s in arg.split(";")]
    seg = zscreen.build(sc, K0, [(E, k, x) for k, x in chain])
    if seg is None:
        print(arg, "does not fit"); continue
    print(arg, [f"{k}{a}" for a, k in cens(seg, 4300, -1100, 30)], "read", zscreen.score(S, tape, sc.run(seg, zscreen.T)), flush=True)
