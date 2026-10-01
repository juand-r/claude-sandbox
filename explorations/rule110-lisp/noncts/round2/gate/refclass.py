"""Assembler rule v2 (see stream.build2): a packet's class is designated
relative to the REFERENCE E^k of its slot, k - 1 = value mod 7 forced by
slip in a garbage-free stream: val = 5 * (slip / 2) mod 7.
Here: find the class c of Z at value-1 slots (relative to reference E^2 =
chain_events()[2]) for which I Z_c leaves E exactly on the reference (0,0)
class, so that later zero meetings keep their designated classes."""
from common import LIB
from glidersim import GliderSim
from r110lib import class_key
from stream import build2, horizon

for c in range(3):
    sc = build2(["I", "Z"], {("Z", 1): c})
    sim = GliderSim(LIB, sc)
    sim.run(horizon(sc))
    st = sim.state()
    print(c, st, [class_key((g[1], g[2]), (15, -4), (42, -14)) for g in st])
