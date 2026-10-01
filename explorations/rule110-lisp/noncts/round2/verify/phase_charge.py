"""Test a positional conservation law: for a counter in class c (seed t mod 3)
hit by packet P with seed phase p (my convention), is the output counter's
class always c + p + k(P, value, outcome) (mod 3)? If yes, the class is an
additive 'phase charge' that no single packet can erase, and inputs whose
histories differ only by escaped garbage keep different classes."""
from collections import defaultdict
import sync_search as S

for P, m in (("Z", 1), ("N", 0), ("I", 0), ("Z", 0), ("J", 0), ("W", 1), ("X", 0), ("W", 0),
             ("D", 1), ("I", 2), ("Z", 2), ("N", 2)):
    ks = defaultdict(set)
    for p in range(0, 42):
        for c in range(3):
            o = S.out(m, c, P, p)
            if o == "snap" or o[0] == "bad":
                continue
            nm, cls, other = o
            ks[(nm, other)].add((cls - c - p) % 3)
    print(f"{P} on {m}: " + "; ".join(f"{nm}{'+' + '+'.join(ot) if ot else ''}: k in {sorted(k)}"
                                     for (nm, ot), k in ks.items()), flush=True)
