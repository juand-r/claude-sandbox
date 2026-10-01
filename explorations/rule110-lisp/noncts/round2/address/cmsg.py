"""C messengers crossing F registers (the other direction of the F lane).

Lab frame: F markers move left (-1/9) over a stationary object C placed to
their left; the LEFTMOST F meets it first. Markers are listed in meeting
order (left to right). A crossing is clean if the F survives and every
other product is stationary (the messenger(s) stay behind and meet the
next F). Catalog-level prediction (collider predict: X = stationary,
Y = F). Node = residues of successive F-F differences mod L_FC =
<P_F, P_C>; label b = coefficient of P_C = (7,0).
Usage: python cmsg.py k   (k markers)"""
import sys, json, os, itertools
from fractions import Fraction
import lane
from predict import predict, LIB
from collide import canonical_reps
from r110lib import class_key
from rx_lite import compatible
from cgraph import analyse

PF, PC = (36, -4), (7, 0)
V = lambda n: LIB.gliders[n].velocity
KEY = lambda D: class_key(D, PF, PC)
DET = PF[0] * PC[1] - PF[1] * PC[0]


def coords(v):
    a = Fraction(v[0] * PC[1] - v[1] * PC[0], DET)
    b = Fraction(PF[0] * v[1] - PF[1] * v[0], DET)
    assert a.denominator == 1 and b.denominator == 1, v
    return int(a), int(b)


def cross(fseed, mover):
    """mover (stationary name, t, x) meets F at fseed."""
    name, t, x = mover
    try:
        # X = mover (left, v=0), Y = F; r = F seed relative to mover
        k, prods = predict(name, "F", (fseed[0] - t, fseed[1] - x), eX=(t, x))
    except (ValueError, KeyError, AssertionError):
        return None
    fs = [p for p in prods if p[0] == "F"]
    rest = [p for p in prods if p[0] != "F"]
    if len(fs) != 1 or not rest or not all(V(p[0]) == 0 for p in rest):
        return None
    return (fs[0][1], fs[0][2]), rest


def chain(seeds, mv):
    """seeds in meeting order (leftmost F first)."""
    outs = [mv]
    new = []
    for s in seeds:
        nxt = []
        # stationary movers: all meet this F; order: rightmost first? The F
        # moves left, so it meets the RIGHTMOST stationary object first.
        for o in sorted(outs, key=lambda p: -p[2]):
            r = cross(s, o)
            if r is None:
                return None
            s = r[0]
            nxt += r[1]
        new.append(s)
        outs = nxt
    return new, outs


def movers():
    rows = json.load(open(os.path.join(lane.COLL, "collisions.json")))
    names = sorted({r["X"] for r in rows if r["Y"] == "F" and V(r["X"]) == 0})
    out = []
    for n in names:
        for rep in canonical_reps(LIB, n, "F"):
            # rep = F seed relative to the mover at (0,0); express mover
            # relative to an F at (0,0)
            out.append((n, -rep[0], -rep[1]))
    return out


def residues():
    out = {}
    for t in range(0, 40):
        for x in range(60, 74):
            # right F at (0,0), left F at (-t,-x); difference right-left
            if compatible("F", (-t, -x), "F", (0, 0)):
                out.setdefault(KEY((t, x)), (t, x))
    return out


def build(k):
    R = residues()
    MV = movers()
    nodes = list(itertools.product(sorted(R), repeat=k - 1))
    edges = []
    for nd in nodes:
        # meeting order: leftmost first. seeds[0] leftmost at (0,0)
        seeds = [(0, 0)]
        for r in nd:
            D = R[r]
            s = seeds[-1]
            seeds.append((s[0] + D[0], s[1] + D[1]))
        for mv in MV:
            res = chain(seeds, mv)
            if res is None:
                continue
            new = res[0]
            lab, nd2 = [], []
            for i in range(k - 1):
                E = (new[i + 1][0] - new[i][0], new[i + 1][1] - new[i][1])
                j = KEY(E)
                if j not in R:
                    break
                lab.append(coords((E[0] - R[j][0], E[1] - R[j][1]))[1])
                nd2.append(j)
            else:
                edges.append((nd, tuple(nd2), tuple(lab), mv))
    return R, nodes, edges


if __name__ == "__main__":
    k = int(sys.argv[1])
    R, nodes, edges = build(k)
    print("C movers", len(movers()), "residues", sorted(R.values()), "nodes", len(nodes), "edges", len(edges))
    for size, red in analyse(nodes, edges):
        print("  SCC", size, "reduced labels", red)
