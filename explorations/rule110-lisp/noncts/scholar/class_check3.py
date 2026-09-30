"""Like class_check2 but with X restricted to a few phases (faster).
Usage: python class_check3.py X Y T xphase1,xphase2 ..."""
import sys
from collections import defaultdict
import classes as C, r110check as r

def run(xs, yp, T=2000, seps=(8, 9)):
    ys = [k for k in r.PHASES if k.startswith(yp + "(") and k != "B(A,f4_1)"]
    table = defaultdict(set)
    for x in xs:
        for y in ys:
            for n in seps:
                c = C.cls(x, n, y)
                e, l, _ = r.outcome(f"{x}-{n}e-{y}", T=T, pad=T // 14 + 120)
                table[c].add(tuple(sorted(l)) + (() if e == l else ("UNSETTLED",)))
    print(xs, "+", yp, "classes:", len(table), flush=True)
    for c in sorted(table):
        print("   ", c, table[c], flush=True)

if __name__ == "__main__":
    run(sys.argv[4].split(";"), sys.argv[2], int(sys.argv[3]))
