"""Catalog search with a front plate: mover crosses T and M cleanly (all
outputs), then an output hitting P makes P emit a stationary object while
P survives (F + Y -> F + stationary + Ebar-speed). 144 residue pairs."""
from fractions import Fraction
from collections import Counter
import gen
from gen import LIB, EBAR_SPEED, lateral
from predict import predict
from cgraph import residues, setup
V = lambda n: LIB.gliders[n].velocity
_, key, _ = setup("F")
R = residues("F", key)
MV = gen.movers("F")
hits = []
for D1 in R.values():
    for D2 in R.values():
        T, M = (0, 0), (-D1[0], -D1[1])
        P = (M[0] - D2[0], M[1] - D2[1])
        for mv in MV:
            r = gen.cross_chain(["F", "F"], [T, M], mv)
            if r is None:
                continue
            outs = sorted(r[1], key=lateral)
            if not outs:
                continue
            o = outs[0]
            try:
                _, prods = predict("F", o[0], (o[1] - P[0], o[2] - P[1]), eX=P)
            except (ValueError, KeyError, AssertionError):
                continue
            fs = [p for p in prods if p[0] == "F"]
            st = [p for p in prods if V(p[0]) == 0]
            rest = [p for p in prods if p[0] != "F" and V(p[0]) != 0]
            if st and len(fs) == 1 and all(p[0] in EBAR_SPEED for p in rest):
                hits.append((D1, D2, mv, o[0], tuple(p[0] for p in st), tuple(p[0] for p in rest), len(outs)))
print(len(hits))
print(Counter((h[3], h[4]) for h in hits))
for h in hits[:20]:
    print(h)
