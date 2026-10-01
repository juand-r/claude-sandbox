"""Which Ebar placements do the tape symbol's C's cross cleanly, after n prior
crossings? Rej-path scene (lscene, exact), s_1's C's at K0-488..-359 at
t_in = 31500 (tapes NYYN: Y symbol, NNYY: N symbol). Prior crossings: a
fixed chain of Ebars; candidate Ebar at (k, x) between the chain and P
(x in [XLO, XHI)), total slip fixed by an extra crossing-free partner?  No:
we test candidate PAIRS (chain + candidate) only when the chain has odd
length, so slip is 0. Criterion: at t = t_in + TT the census of
[K0-400, K0+30) shows exactly the chain + candidate as 'E' objects and no
C/A/?, and 4 C's have reached [K0-60, K0+30)?  Simpler: compare with the
plain scene: the C's must arrive at P region (K0+30) with the 4 C's intact.
We record the C positions (census) at the time the first C reaches K0-40.
    python cross_sets.py TAPE 'k,x;k,x;...' XLO XHI"""
import sys, json
import numpy as np
from zscreen import *
from census import census, MAX_DT
tape = sys.argv[1]
chain = [tuple(map(int, s.split(","))) for s in sys.argv[2].split(";") if s]
xlo, xhi = int(sys.argv[3]), int(sys.argv[4])
S = setup()
K0, sc = S[tape][:2]
E = ebar_tiles()
def cens(seg, t, lo, hi):
    w = pack(seg); w = step_packed_n(w, t - MAX_DT); rows = []
    for _ in range(MAX_DT + 1):
        c = unpack(w, len(seg)); i = sc.ebar_to_seg(K0 + lo, TIN + t - MAX_DT + len(rows))
        rows.append(c[i:i + hi - lo]); w = step_packed_n(w, 1)
    return [(a + lo, k) for a, b, k in census(np.array(rows))]
p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + RA))
# phase after chain
items = [(E, k, x) for k, x in chain]
last = max([x for k, x in chain], default=RA - 30)
pin = p0
for k, x in chain:
    arr, cl, cr = E[k]
    pin = (cr - sc.ebar_to_seg(K0 + x)) % TILE
out = []
for k, x, _ in placements(sc, K0, E, max(xlo, last + 20), xhi, pin):
    seg = build(sc, K0, items + [(E, k, x)])
    if seg is None:
        continue
    cs = cens(seg, 1400, -400, 30)   # C's still left of P's Ebar (plain: C-83,-38,7 at 1500)
    nC = sum(1 for a, kk in cs if kk == "C")
    junk = [f"{kk}{a}" for a, kk in cs if kk not in "CE"]
    Cs = [a for a, kk in cs if kk == "C"]
    out.append((k, x, nC, Cs, junk))
    print(k, x, nC, Cs, junk, flush=True)
