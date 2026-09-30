"""Same-type marker lanes (k markers of type X) crossed by Ebar-speed
catalog movers: residue graph with integer labels, SCC reduced labels.
Usage: python cgraph.py X k"""
import sys
from collections import defaultdict
from fractions import Fraction
import gen
from gen import LIB
from r110lib import class_key

PE = (30, -8)


def setup(X):
    g = LIB.gliders[X]
    PX = (g.p, g.d)
    det = PX[0] * PE[1] - PX[1] * PE[0]
    key = lambda D: class_key(D, PX, PE)

    def coords(v):
        a = Fraction(v[0] * PE[1] - v[1] * PE[0], det)
        b = Fraction(PX[0] * v[1] - PX[1] * v[0], det)
        assert a.denominator == 1 and b.denominator == 1, v
        return int(a), int(b)
    return PX, key, coords


def residues(X, key, base_gap=60):
    """Ether-compatible seed differences D (front minus back) between two
    X gliders, one representative per residue; found by building the pair."""
    from rx_lite import compatible
    out = {}
    for t in range(0, 40):
        for x in range(base_gap, base_gap + 14):
            if compatible(X, (-t, -x), X, (0, 0)):
                k = key((t, x))
                out.setdefault(k, (t, x))
    return out


def build(X, k):
    PX, key, coords = setup(X)
    R = residues(X, key)
    MV = gen.movers(X)
    import itertools
    nodes = list(itertools.product(sorted(R), repeat=k - 1))
    edges = []
    for nd in nodes:
        seeds = [(0, 0)]
        for r in nd:
            D = R[r]
            s = seeds[-1]
            seeds.append((s[0] - D[0], s[1] - D[1]))
        for mv in MV:
            res = gen.cross_chain([X] * k, seeds, mv)
            if res is None:
                continue
            new = res[0]
            lab, nd2 = [], []
            for i in range(k - 1):
                E = (new[i][0] - new[i + 1][0], new[i][1] - new[i + 1][1])
                j = key(E)
                if j not in R:
                    break
                lab.append(coords((E[0] - R[j][0], E[1] - R[j][1]))[1])
                nd2.append(j)
            else:
                edges.append((nd, tuple(nd2), tuple(lab), mv))
    return R, nodes, edges


def analyse(nodes, edges):
    adj = defaultdict(list)
    for u, v, lab, mv in edges:
        adj[u].append((v, lab, mv))
    sys.setrecursionlimit(100000)
    idx, low, on, st, comps = {}, {}, set(), [], []
    c = [0]

    def dfs(v):
        idx[v] = low[v] = c[0]; c[0] += 1
        st.append(v); on.add(v)
        for w, _, _ in adj[v]:
            if w not in idx:
                dfs(w); low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = st.pop(); on.discard(w); comp.append(w)
                if w == v:
                    break
            comps.append(comp)
    for v in nodes:
        if v not in idx:
            dfs(v)
    out = []
    for comp in comps:
        cs = set(comp)
        pot = {comp[0]: (0,) * len(comp[0])}
        stack = [comp[0]]
        while stack:
            v = stack.pop()
            for w, lab, _ in adj[v]:
                if w in cs and w not in pot:
                    pot[w] = tuple(a + b for a, b in zip(pot[v], lab))
                    stack.append(w)
        red = set()
        for v in comp:
            for w, lab, mv in adj[v]:
                if w in cs:
                    red.add(tuple(p + l - q for p, l, q in zip(pot[v], lab, pot[w])))
        if red:
            out.append((len(comp), sorted(red)))
    return out


if __name__ == "__main__":
    X, k = sys.argv[1], int(sys.argv[2])
    R, nodes, edges = build(X, k)
    print(X, "k", k, "residues", len(R), sorted(R.values()), "nodes", len(nodes), "edges", len(edges))
    for size, red in analyse(nodes, edges):
        print("  SCC", size, "reduced labels", red)
