"""Closed walks covering all four addressing directions (absorb graph).
Usage: python absorb_walks2.py L bound nstarts"""
import sys
from absorb_walks import adj, R, walks
L, B, NS = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
starts = sorted(adj, key=lambda n: -len(adj[n]))[:NS]
for s in starts:
    f = walks(s, L, bound=B)
    pick = {}
    for k, w in f.items():
        if (k[0] == 0) == (k[1] == 0):
            continue
        d = ("R1+" if k[0] > 0 else "R1-") if k[1] == 0 else ("R2+" if k[1] > 0 else "R2-")
        if d not in pick or len(w) < len(pick[d][1]) or (len(w) == len(pick[d][1]) and abs(sum(k)) < abs(sum(pick[d][0]))):
            pick[d] = (k, w)
    print("start", [R[k] for k in s], "deg", len(adj[s]), "directions", sorted(pick), flush=True)
    for d in sorted(pick):
        k, w = pick[d]
        print("  ", d, k, len(w), [m for _, m in w], flush=True)
