"""Semantic search (no physics): which words over the verified/candidate
one-counter ops compute parity when iterated?
Ops (value v >= 0):
  I: v+1          (GB5)
  Z: v-1, 0 -> 6  (GB3,GB4)@(-25,46), zero class 0      [wrap]
  W: v,   0 -> 7  (GB3,GB5)@(-14,40), zero class 0      [wrap]
  X: v+1, 0 -> 8  (GB5,GB4)@(-4,56),  zero class 2      [wrap]
  J: v+1, 0 -> 0 + Bbar left   (GB1,GB1)@(-1,36), zero class 1  [garbage]
"""
import itertools
import sys

OPS = {
    "I": lambda v: v + 1,
    "Z": lambda v: v - 1 if v else 6,
    "W": lambda v: v if v else 7,
    "X": lambda v: v + 1 if v else 8,
    "J": lambda v: v + 1 if v else 0,
}


def apply(w, v):
    for c in w:
        v = OPS[c](v)
    return v


alph = sys.argv[1] if len(sys.argv) > 1 else "IZWXJ"
maxL = int(sys.argv[2]) if len(sys.argv) > 2 else 6
V = range(0, 15)
hits = []
for L in range(1, maxL + 1):
    for w in map("".join, itertools.product(alph, repeat=L)):
        for m in (20, 21):
            r = [apply(w * m, v) for v in V]
            # parity-like: result depends only on v mod 2 and differs
            a = {r[v] for v in V if v % 2 == 0}
            b = {r[v] for v in V if v % 2 == 1}
            if len(a) == 1 and len(b) == 1 and a != b:
                hits.append((w, m, r))
                break
print(len(hits))
for h in hits[:20]:
    print(h)
