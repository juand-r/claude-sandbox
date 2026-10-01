"""Check shuttle 23:24 MERGE: E^m | D1 | E^n -> E^(m+n+1) (D1 hits R1's front,
R1 becomes n+1 left-moving B's that fuse into R2's back), in 3 of the 5
D1-vs-E^n classes; the other 2 give debris.

My construction: my builder, my library E^k (round-2 libgen), D1 from the
Martinez string; R2 = E^m at x = 0, D1 ~gap cells right of R2, R1 = E^n
~150 cells further. D1's time phase t0 runs over 0..9 and its x over a
14-cell window, so all 5 classes are hit (class = relative lattice position
of D1 and R1; det((10,2),(15,-4))/14 = 5). Outcome after T steps (hrun), read
by rodval.value (any length). Control that can fail: the classes that do
not merge must give something other than one clean rod."""
import sys
from collections import Counter

import hrun
import rodval

vlib = hrun.vlib
T = 3000


def outcome(m, n, t0, dx, gap=200):
    nm = lambda k: "E" if k == 1 else f"E^{k}"
    items = [(nm(m), 0, 0), ("D1", t0, gap + dx), (nm(n), 0, gap + 150)]
    row, org, placed = vlib.build(items, pad=400)
    # class of D1 vs R1: relative lattice position mod <(10,2),(15,-4)>, via the placed seeds
    return rodval.value(row, org, T), placed


def main(ms=(1, 2, 3, 6), ns=range(3, 13)):
    tot = Counter()
    for m in ms:
        for n in ns:
            # class of D1 vs R1 = t0 mod 5: f(t, x) = t mod 5 kills (10,2) and
            # (15,-4) and is onto Z/5 on the ether lattice ((1,-4) -> 1)
            cls = {}
            seen = set()
            for t0 in range(10):
                for dx in (0, 5, 9):
                    k, placed = outcome(m, n, t0, dx)
                    key = (placed[1][1], placed[1][2])
                    if key in seen:
                        continue
                    seen.add(key)
                    o = "merge" if k == m + n + 1 else ("rod %s" % k if k else "debris")
                    cls.setdefault(t0 % 5, set()).add(o)
            assert all(len(v) == 1 for v in cls.values()), cls      # single outcome per class
            res = {c: v.pop() for c, v in sorted(cls.items())}
            tot.update(res.values())
            print(m, n, res, flush=True)
    print("total", dict(tot))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main([int(sys.argv[1])], [int(sys.argv[2])])
    else:
        main()
