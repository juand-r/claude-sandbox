"""Drift balancing for a FIXED stream (two-register F lane, absorption).
For each instruction: T's drift vector mod L_FE. NOP padding = closed
walks with label (0,0) at the start node; BFS over (node, drift class)."""
import pickle
from collections import deque
import gen
gen.ABSORB = True
from gen import cross_chain
from lane import KEY
from absorb_walks import adj, R
import tworeg_abs as T2

PF = (36, -4)
import sys
LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 3


def drift(seq, markers=None):
    m = markers or T2.start_markers()
    T0 = m[0]
    delay = 0
    for name, t, x in seq:
        delay += T2.GAP
        T = m[0]
        r = cross_chain(["F"] * 3, m, (name, T[0] + t + delay * PF[0], T[1] + x + delay * PF[1]))
        m = r[0]
    # remove the free motion: drift measured as seed change (seeds are events)
    return (m[0][0] - T0[0], m[0][1] - T0[1])


s = [k for k in adj if (R[k[0]], R[k[1]]) == ((20, 61), (13, 61))][0]
for op, seq in T2.OPS.items():
    d = drift(seq)
    print(op, "T drift", d, "key", KEY(d))

# zero-label closed walks: edges carry movers relative to T at origin; T's
# drift per edge = predicted T displacement. Recompute per edge.
edrift = {}
for u in adj:
    for v, lab, mv in adj[u]:
        pass
start = (s, (0, 0), KEY((0, 0)))
q = deque([(s, (0, 0), (0, 0), ())])
seen = {(s, (0, 0), KEY((0, 0)))}
found = {}
D1, D2 = R[s[0]], R[s[1]]
while q:
    v, lab, dr, seq = q.popleft()
    if len(seq) >= LMAX:
        continue
    for w, (x, y), mv in adj[v]:
        nl = (lab[0] + x, lab[1] + y)
        if abs(nl[0]) > 12 or abs(nl[1]) > 12:
            continue
        # T displacement of this mover at node v (T at origin)
        Dv1, Dv2 = R[v[0]], R[v[1]]
        M = (-Dv1[0], -Dv1[1]); P = (M[0] - Dv2[0], M[1] - Dv2[1])
        r = cross_chain(["F"] * 3, [(0, 0), M, P], mv)
        td = r[0][0]
        nd = (dr[0] + td[0], dr[1] + td[1])
        st = (w, nl, KEY(nd))
        if st in seen:
            continue
        seen.add(st)
        s2 = seq + (mv,)
        if w == s and nl == (0, 0):
            k = KEY(nd)
            if k not in found or len(s2) < len(found[k][1]):
                found[k] = (nd, s2)
        q.append((w, nl, nd, s2))
print("NOP drift classes reachable (len<=3):", len(found))
for k, (nd, s2) in sorted(found.items(), key=lambda z: len(z[1][1])):
    print("  ", nd, k, len(s2), s2)
pickle.dump(found, open("nops.pkl", "wb"))
