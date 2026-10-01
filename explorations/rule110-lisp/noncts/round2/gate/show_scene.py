"""Print the exact glider placements (name, t0, x0; collider conventions:
seed event, glider phase 0 at (t0, x0)) of a program, plus base-glider parts."""
import sys
from common import LIB
from stream import build
prog = list(sys.argv[1])
for name, t0, x0 in build(prog):
    g = LIB.gliders[name]
    parts = g.parts and [(n, t0 + pt, x0 + px) for n, pt, px in g.parts]
    print(name, t0, x0, "parts:", parts if parts else "-")
