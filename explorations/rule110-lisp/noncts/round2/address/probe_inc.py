"""Apply architect's INC/DEC packet sequences (placed relative to T, with
20 F-periods between movers, as in xcounter.schedule) to a 3-marker
system and report the net changes of D1 and D2 for every D2 residue."""
import lane
from lane import cross_chain, sub
from tworeg import residues, normP, D0
# copied from architect/xcounter.py (importing it drags cwd-dependent modules)
INC = [('Ebar@(0,0)+Ebar@(-26,27)', -1, 45), ('Ebar@(0,0)+Ebar@(-11,37)', -16, 63),
       ('Ebar@(0,0)+Ebar@(-1,25)', -12, 61)]
DEC = [('Ebar@(0,0)+Ebar@(-26,27)', -1, 45), ('Ebar@(0,0)+Ebar@(-4,23)', -15, 59),
       ('Ebar', -14, 55)]

PF = (36, -4)


def apply_seq(markers, seq, gap=20):
    T0 = markers[0]
    delay = 0
    for name, t, x in seq:
        delay += gap
        T = markers[0]
        ev = (T[0] + t + delay * PF[0], T[1] + x + delay * PF[1])
        r = cross_chain(markers, (name,) + ev)
        if r is None:
            return None
        markers = r[0]
    return markers


for opname, seq in (("INC", INC), ("DEC", DEC)):
    for D2 in sorted(residues().values()):
        T, M = (0, 0), (0, -43)
        P = sub(M, D2)
        r = apply_seq([T, M, P], seq)
        if r is None:
            print(opname, D2, "not clean")
            continue
        T2, M2, P2 = r
        n1 = normP(sub(sub(T2, M2), (0, 43)))
        n2 = normP(sub(sub(M2, P2), D2))
        print(opname, "D2", D2, "net1", n1, "net2", n2)
