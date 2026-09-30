"""Check that the collision outcome is a function of the exact collision
class (classes.py), using separations large enough that the gliders start
free. Prints class -> set of outcome types."""
import sys
from collections import defaultdict
import classes as C, r110check as r

def run(xp, yp, seps=(7, 8), T=1500, pad=300):
    xs = [k for k in r.PHASES if k.startswith(xp + "(")]
    ys = [k for k in r.PHASES if k.startswith(yp + "(")]
    table = defaultdict(set); cnt = defaultdict(int)
    for x in xs:
        for y in ys:
            for n in seps:
                c = C.cls(x, n, y)
                e, l, _ = r.outcome(f"{x}-{n}e-{y}", T=T, pad=pad)
                table[c].add(tuple(sorted(l)) + (() if e == l else ("UNSETTLED",)))
                cnt[c] += 1
    ok = all(len(v) == 1 for v in table.values())
    print(xp, yp, "classes:", len(table), "function of class:", ok)
    for c in sorted(table):
        print("   ", c, cnt[c], table[c])

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
