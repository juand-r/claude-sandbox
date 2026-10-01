"""E-shift at zero: for packet P and zero class k, the event of the E-chain
product relative to the input E at (0,0), and its class mod <P_E, P_G>
(class 0 = same trajectory class as the reference E, so later zero-meetings
keep their designated classes)."""
import sys
from common import LIB, CHAIN, collide_pair, class_key

PE, PG = (15, -4), (42, -14)
for P in sys.argv[1:]:
    for r in collide_pair(LIB, "E", P):
        es = [p for p in r["products"] if p[0] in CHAIN]
        out = [(p[0], p[1], p[2], class_key((p[1], p[2]), PE, PG)) for p in es]
        print(P, r["cls"], [p[0] for p in r["products"]], out)
