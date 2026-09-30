"""Check wrap candidates on E^n for n = 1..9, all classes (direct CA)."""
import sys
from common import CHAIN, LIB, collide_pair, names

for P in sys.argv[1:]:
    print(P)
    for n in range(1, 10):
        print("  n", n, [(r["cls"], names(r["products"])) for r in collide_pair(LIB, CHAIN[n - 1], P)])
