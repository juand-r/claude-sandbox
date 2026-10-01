"""Read of the bare rejector-prepared reader P_1 versus the number c of Ebars
the symbol crosses first (class test). Chain: Ebars (0, -1053 + 63 i),
i < c, in front; if c is odd, one compensating Ebar at (0, CX) LEFT of the
symbol (the symbol never meets it). Rej path, t_in = 28500.
    python t_class.py TAPE CX"""
import sys
import numpy as np
import zscreen
zscreen.TIN, zscreen.T, zscreen.RA = 28500, 6000, -1700
zscreen.JS = range(-12, 13)
from zscreen import *
tape, CX = sys.argv[1], int(sys.argv[2])
S = zscreen.setup(); K0, sc = S[tape][:2]; E = ebar_tiles()
print("control", zscreen.score(S, tape, sc.run(sc.seg, zscreen.T)))
for c in range(0, 10):
    items = [(E, 0, -1053 + 63 * i) for i in range(c)]
    if c % 2:
        # compensator: first placement at or right of CX with matching phase
        p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + zscreen.RA))
        k, x, _ = placements(sc, K0, E, CX, CX + 14, p0)[0]
        items = [(E, k, x)] + items
    seg = zscreen.build(sc, K0, items)
    if seg is None:
        print(c, "does not fit"); continue
    print(c, zscreen.score(S, tape, sc.run(seg, zscreen.T)), flush=True)
