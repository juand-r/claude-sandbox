import sys
from common import LIB
from glidersim import GliderSim
from stream import build, horizon
prog = list(sys.argv[1])
sc = build(prog)
print(sc)
sim = GliderSim(LIB, sc)
try:
    sim.run(horizon(sc))
except Exception as e:
    print("EXC", e)
for l in sim.log:
    print(l)
