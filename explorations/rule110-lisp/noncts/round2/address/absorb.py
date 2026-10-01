"""Lane graphs with absorption allowed (a marker may swallow a mover).
Usage: python absorb.py k"""
import sys
import gen
gen.ABSORB = True
from cgraph import build, analyse
k = int(sys.argv[1])
R, nodes, edges = build("F", k)
print("F k", k, "ABSORB nodes", len(nodes), "edges", len(edges))
for size, red in analyse(nodes, edges):
    if any(any(x) for x in red):
        print("  SCC", size, "reduced labels", red)
