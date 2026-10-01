"""Catalog search: a mover crosses T cleanly (or is absorbed nowhere), and
one of its outputs makes M EMIT a stationary object while M survives
(F + Y -> F + stationary + Ebar-speed). Residue of D1 = T - M free (12)."""
import json, os
from fractions import Fraction
import gen
from gen import LIB, EBAR_SPEED, lateral
from predict import predict
from cgraph import residues, setup
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
        for o in sorted(r[1], key=lateral):
            try:
                _, prods = predict("F", o[0], (o[1] - M[0], o[2] - M[1]), eX=M)
            except (ValueError, KeyError, AssertionError):
                break
            fs = [p for p in prods if p[0] == "F"]
            st = [p for p in prods if V(p[0]) == 0]
            rest = [p for p in prods if p[0] != "F" and V(p[0]) != 0]
            if len(fs) == 1 and st and all(p[0] in EBAR_SPEED for p in rest):
                hits.append((D, mv, o[0], [p[0] for p in st], [p[0] for p in rest]))
            break   # only the first output (later ones would see an emitted object)
print(len(hits))
for h in hits[:40]:
    print(h)
