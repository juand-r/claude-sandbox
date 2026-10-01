"""F versus the conversion products of the neutral eaters (direct CA)."""
import sys
from common import LIB, collide_pair, names
for Y in sys.argv[1:]:
    print(Y, Y in LIB.gliders)
    for r in collide_pair(LIB, "F", Y):
        print("  ", r["cls"], names(r["products"]))
