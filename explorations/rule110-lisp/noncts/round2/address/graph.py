"""Labelled transition graph of the 3-marker F lane (T, M, P).

Node = (residue of D1 = T - M, residue of D2 = M - P) modulo L_FE =
<P_F, P_Ebar>. Edge = one mover (Ebar-speed glider/packet, any class
relative to T) that crosses all three F's cleanly (catalog prediction).
Edge label (b1, b2): with fixed representatives rep(r) of each residue,
D + dD - rep(r') = a P_F + b P_Ebar; b is the integer register change
(a only moves a marker along its own trajectory). A closed walk changes
register i by the sum of b_i. Architect's INC is b = -2, DEC b = +2.

Usage: python graph.py build   (writes graph.pkl)"""
import pickle
import sys
from fractions import Fraction
import os

PF, PE = (36, -4), (30, -8)
HERE = os.path.dirname(os.path.abspath(__file__))
GPATH = os.path.join(HERE, "graph.pkl")


def coords(v):
    det = PF[0] * PE[1] - PF[1] * PE[0]
    a = Fraction(v[0] * PE[1] - v[1] * PE[0], det)
    b = Fraction(PF[0] * v[1] - PF[1] * v[0], det)
    assert a.denominator == 1 and b.denominator == 1, v
    return int(a), int(b)


def build():
    from tworeg import residues, transitions
    from lane import KEY
    R = residues()                  # key -> representative D
    nodes = sorted(R)
    edges = []                      # (u, v, (b1, b2), mover)
    for k1 in nodes:
        for k2 in nodes:
            D1, D2 = R[k1], R[k2]
            for mv, d1, d2 in transitions(D1, D2):
                E1 = (D1[0] + d1[0], D1[1] + d1[1])
                E2 = (D2[0] + d2[0], D2[1] + d2[1])
                j1, j2 = KEY(E1), KEY(E2)
                b1 = coords((E1[0] - R[j1][0], E1[1] - R[j1][1]))[1]
                b2 = coords((E2[0] - R[j2][0], E2[1] - R[j2][1]))[1]
                edges.append(((k1, k2), (j1, j2), (b1, b2), mv))
    pickle.dump({"R": R, "edges": edges}, open(GPATH, "wb"))
    print("nodes", len(nodes) ** 2, "edges", len(edges))


def load():
    return pickle.load(open(GPATH, "rb"))


if __name__ == "__main__" and sys.argv[1:] == ["build"]:
    build()
