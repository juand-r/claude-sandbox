"""Walkers: library G-speed packets that are NEUTRAL on E^2 (all classes)
and leave a lone E on E (zero window) in some class; print the E's
intercept shift (cells; >0 = right, away from a rod on the left).
Data: scan_e2.jsonl (mine) + round-3 coupler scan_reflect_M1.jsonl."""
from wtable import *  # noqa
from fractions import Fraction

M1, M2 = load()
VE = Fraction(-4, 15)
out = []
for Y, r in M2.items():
    if 'rows' not in r:
        continue
    neu = [row['cls'] for row in r['rows'] if row['settled'] and [p[0] for p in row['products']] == ['E^2']]
    if len(neu) != len(r['rows']):
        continue
    shifts = []
    for row in M1[Y]['rows']:
        ps = row['products']
        if row['settled'] and len(ps) == 1 and ps[0][0] == 'E':
            shifts.append((row['cls'], float(Fraction(ps[0][2]) - VE * ps[0][1])))
        else:
            shifts.append((row['cls'], None))
    out.append((Y, shifts))
for Y, s in out:
    print(Y, s)
print(len(out), "packets neutral on E^2 in every class")
