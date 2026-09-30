"""Closed-walk labels in the 3-marker graph: strongly connected
components, and for each start node the set of (b1, b2) labels of closed
walks up to length L (DP over (node, label))."""
import sys
from collections import defaultdict, Counter
from graph import load

G = load()
E = G["edges"]
adj = defaultdict(list)
for u, v, lab, mv in E:
    adj[u].append((v, lab, mv))
nodes = sorted({u for u, *_ in E} | {v for _, v, *_ in E})


def sccs():
    # Tarjan (iterative-safe enough for 144 nodes)
    sys.setrecursionlimit(10000)
    idx, low, on, st, out = {}, {}, set(), [], []
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
            out.append(comp)
    for v in nodes:
        if v not in idx:
            dfs(v)
    return out


def closed_labels(s, L, bound=12):
    """labels of closed walks at s of length 1..L -> shortest length."""
    cur = {(s, (0, 0))}
    found = {}
    for n in range(1, L + 1):
        nxt = set()
        for v, (a, b) in cur:
            for w, (x, y), _ in adj[v]:
                lab = (a + x, b + y)
                if abs(lab[0]) > bound or abs(lab[1]) > bound:
                    continue
                if w == s and lab not in found:
                    found[lab] = n
                nxt.add((w, lab))
        cur = nxt
    return found


if __name__ == "__main__":
    comps = sccs()
    big = [c for c in comps if len(c) > 1 or any(w == c[0] for w, _, _ in adj[c[0]])]
    print("SCCs with cycles:", [len(c) for c in big])
    labs = Counter(lab for _, _, lab, _ in E)
    print("single-edge labels:", labs.most_common(20))
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    for comp in big:
        s = comp[0]
        f = closed_labels(s, L)
        axis = {k: v for k, v in f.items() if (k[0] == 0) != (k[1] == 0)}
        print("comp size", len(comp), "start", s, "closed labels", len(f),
              "axis labels", sorted(axis.items()))
        print("   all:", sorted(f.items())[:60])


def cycle_basis_labels(comp):
    """Labels of fundamental cycles (potential differences) inside an SCC:
    they generate all closed-walk labels as a group."""
    cs = set(comp)
    pot = {comp[0]: (0, 0)}
    st = [comp[0]]
    while st:
        v = st.pop()
        for w, lab, _ in adj[v]:
            if w in cs and w not in pot:
                pot[w] = (pot[v][0] + lab[0], pot[v][1] + lab[1])
                st.append(w)
    out = set()
    for v in comp:
        for w, lab, mv in adj[v]:
            if w in cs:
                out.add((pot[v][0] + lab[0] - pot[w][0], pot[v][1] + lab[1] - pot[w][1]))
    return out
