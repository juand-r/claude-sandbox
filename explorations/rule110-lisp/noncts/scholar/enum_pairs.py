"""Enumerate outcomes of X + Y over all phases of Y and a range of
separations (Martinez notation). Distinct outcome sets are printed with
one example spec each. Usage: python enum_pairs.py X_PREFIX Y_PREFIX"""
import sys
from collections import OrderedDict
import r110check as r

def main(xp, yp, seps=range(2, 5), T=900):
    xs = [k for k in r.PHASES if k.startswith(xp + "(") ]
    ys = [k for k in r.PHASES if k.startswith(yp + "(") ]
    res = OrderedDict()
    for x in xs:
        for y in ys:
            for n in seps:
                spec = f"{x}-{n}e-{y}"
                early, late, _ = r.outcome(spec, T=T)
                key = tuple(sorted(late)) + (("" if early == late else "UNSETTLED"),)
                res.setdefault(key, []).append(spec)
    for k, v in res.items():
        print(f"{len(v):3d}  {list(k)}  e.g. {v[0]}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
