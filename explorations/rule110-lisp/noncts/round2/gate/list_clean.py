"""List scan packets that are clean for n >= 2 (single effect e, no garbage)
with their zero behaviour per class: (delta, left garbage, right garbage)."""
import json
from common import HERE, LIB
from behave import classify

S = json.load(open(HERE + '/counter_scan.json'))
for P, rec in S.items():
    es = set()
    ok = True
    for n in '234':
        for c, st, ps in rec['E'][n]:
            b = classify(ps, int(n))
            if b is None or b[1] or b[2]:
                ok = False
            else:
                es.add(b[0])
    if not ok or len(es) != 1:
        continue
    e = es.pop()
    z = []
    for c, st, ps in rec['E']['1']:
        b = classify(ps, 1)
        z.append(None if b is None else (b[0], '+'.join(b[1]) or '-', '+'.join(b[2]) or '-'))
    print(f'{P:28s} e={e:+d} zero:', z, ' A:', rec['A'])
