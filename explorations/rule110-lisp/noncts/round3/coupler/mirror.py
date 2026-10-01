"""Ebar 'mirror' idea: catalog Ebar + B (both classes) -> B^3 + Ebar +
A_8_A. Check (1) the Ebar's displacement, (2) what the A_8_A pair does
to R1 = E^n's front (n = 3..10, 15 seed times), exact CA."""
from collections import Counter
from cl import *  # noqa
from collide import collide_pair

for r in collide_pair(LIB, "Ebar", "B"):
    print("Ebar+B #%d" % r["cls"], r["Y_event"], r["products"])
r = collide_pair(LIB, "Ebar", "B")[0]
X = [tuple(p) for p in r["products"] if p[0] == "A_8_A"]
for n in range(3, 11):
    out = Counter()
    for t0 in range(15):
        sc = X + [(CHAIN[n - 1],) + place_right_of(X, CHAIN[n - 1], pos(X[0], 0) + 80, t0)]
        ok, prods = ca(sc, 1500)
        out[tuple(p[0] for p in prods)] += 1
    print("A_8_A + E^%d:" % n, dict(out))
