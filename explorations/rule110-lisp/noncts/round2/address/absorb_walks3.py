"""All closed-walk labels at one start node (absorb graph), to combine into
the four addressing instructions. Usage: python absorb_walks3.py L B"""
import sys, pickle
from absorb_walks import adj, R, walks
L, B = int(sys.argv[1]), int(sys.argv[2])
s = [k for k in adj if (R[k[0]], R[k[1]]) == ((20, 61), (13, 61))][0]
f = walks(s, L, bound=B)
pickle.dump((s, f), open("walks_20_61_13_61.pkl", "wb"))
pos = sorted((k for k in f if k[0] > 0), key=lambda k: (len(f[k]), abs(k[1])))
neg = sorted((k for k in f if k[0] < 0), key=lambda k: (len(f[k]), abs(k[1])))
print("closed labels", len(f), "with k1>0:", len(pos), "k1<0:", len(neg))
print("k1>0 shortest:", [(k, len(f[k])) for k in pos[:30]])
print("k2 values with k1==0:", sorted(k for k in f if k[0] == 0))
