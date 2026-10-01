"""Shortest closed walks in the 3-marker F lane with absorption allowed,
for the four addressing targets. Saves the graph (absorb3.pkl) once.
Usage: python absorb_walks.py [maxlen]"""
import sys, os, pickle
from collections import defaultdict, deque
import gen
gen.ABSORB = True
from cgraph import build

PK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "absorb3.pkl")
if not os.path.exists(PK):
    R, nodes, edges = build("F", 3)
    pickle.dump((R, nodes, edges), open(PK, "wb"))
R, nodes, edges = pickle.load(open(PK, "rb"))
adj = defaultdict(list)
for u, v, lab, mv in edges:
    adj[u].append((v, lab, mv))


def walks(s, L, bound=4):
    """BFS over (node, label); returns {label: walk} for closed walks."""
    start = (s, (0, 0))
    prev = {start: None}
    q = deque([(start, 0)])
    found = {}
    while q:
        (v, lab), d = q.popleft()
        if d >= L:
            continue
        for w, (x, y), mv in adj[v]:
            nl = (lab[0] + x, lab[1] + y)
            if abs(nl[0]) > bound or abs(nl[1]) > bound:
                continue
            st = (w, nl)
            if st in prev:
                continue
            prev[st] = ((v, lab), mv)
            if w == s and nl != (0, 0) and nl not in found:
                seq = []
                cur = st
                while prev[cur] is not None:
                    p, m = prev[cur]
                    seq.append((p[0], m))
                    cur = p
                found[nl] = seq[::-1]
            q.append((st, d + 1))
    return found


if __name__ == "__main__":
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    best = None
    for s in sorted(adj, key=lambda n: -len(adj[n])):
        f = walks(s, L)
        axes = {k: v for k, v in f.items() if (k[0] == 0) != (k[1] == 0)}
        signs = {(k[0] > 0) - (k[0] < 0) + 2 * ((k[1] > 0) - (k[1] < 0)) for k in axes}
        if best is None or len(signs) > best[0]:
            best = (len(signs), s, axes)
        if len(signs) == 4:
            break
    n, s, axes = best
    print("start node", [R[k] for k in s], "axis targets covered", n)
    for k in sorted(axes, key=lambda k: (len(axes[k]), k)):
        print(k, len(axes[k]), [m for _, m in axes[k]])
