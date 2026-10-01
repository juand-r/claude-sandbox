"""Catalog search: mover crosses T cleanly; its first output, hitting M,
leaves a stationary object (M kept or destroyed) plus Ebar-speed debris.
All 12 residues of D1. Reports (D1, mover, output name, M kept?, stationary, debris)."""
from fractions import Fraction
import gen
from gen import LIB, EBAR_SPEED, lateral
from predict import predict
from cgraph import residues, setup
from collections import Counter
V = lambda n: LIB.gliders[n].velocity
_, key, _ = setup("F")
R = residues("F", key)
MV = gen.movers("F")
hits = []
for k, D in R.items():
    T, M = (0, 0), (-D[0], -D[1])
    for mv in MV:
        r = gen.cross("F", T, mv)
        if r is None:
            continue
        o = sorted(r[1], key=lateral)[0]
        try:
            _, prods = predict("F", o[0], (o[1] - M[0], o[2] - M[1]), eX=M)
        except (ValueError, KeyError, AssertionError):
            continue
        fs = [p for p in prods if p[0] == "F"]
        st = [p for p in prods if V(p[0]) == 0]
        rest = [p for p in prods if p[0] != "F" and V(p[0]) != 0]
        if st and all(p[0] in EBAR_SPEED for p in rest):
            hits.append((D, mv, o[0], len(fs), tuple(p[0] for p in st), tuple(p[0] for p in rest), len(r[1])))
print(len(hits))
print(Counter((h[3], h[4], h[5]) for h in hits))
for h in hits[:30]:
    print(h)
