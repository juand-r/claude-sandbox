"""Enumerate X + Y (X left) over all phases, grouping by exact class;
report class -> outcome types. Usage: python class_check2.py X Y [T]"""
import sys
from collections import defaultdict
import classes as C, r110check as r

def run(xp, yp, T=2000, seps=(8,)):
    xs = [k for k in r.PHASES if k.startswith(xp + "(") and k != "B(A,f4_1)"]
    ys = [k for k in r.PHASES if k.startswith(yp + "(") and k != "B(A,f4_1)"]
    table = defaultdict(set)
    for x in xs:
        for y in ys:
            for n in seps:
                c = C.cls(x, n, y)
                e, l, _ = r.outcome(f"{x}-{n}e-{y}", T=T, pad=T // 14 + 120)
                table[c].add(tuple(sorted(l)) + (() if e == l else ("UNSETTLED",)))
    print(xp, "+", yp, "classes:", len(table))
    for c in sorted(table):
        print("   ", c, table[c])

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 2000)
