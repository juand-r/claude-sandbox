import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
S = zscreen.setup(); E = ebar_tiles()
K0, sc = S["NYYN"][:2]
comp = glider_tiles("Ebar@(0,0)+Ebar@(-1,39)")
ref = zscreen.build(sc, K0, [(comp, 19, -243)])
# find a two-tile build2 equal to ref
p0 = phase_at(sc.seg, sc.ebar_to_seg(K0 + zscreen.RA))
hits = []
for k2, x2, p1 in placements(sc, K0, E, -260, -230, p0):
    for k1, x1, _ in placements(sc, K0, E, x2, x2 + 60, p1):
        s = zscreen.build2(sc, K0, [(E, k2, x2), (E, k1, x1)])
        if s is not None and (s == ref).all():
            hits.append((k2, x2, k1, x1))
print("two-tile equivalents of the compound:", hits)
