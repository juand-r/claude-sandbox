"""Catalog scan for 'phase-free head' reactions (route LN, ROUTES.md).

Question: in collider's verified catalog (../../collider/reactions.json), is
there any reaction  H + S -> S' + H'  with S, S' stationary (period (7,0)),
H a rigid packet on the A, D or B lattice (period exactly (3,2), (10,2) or
(4,-2), which makes the collision single-class against any stationary
object), and H' a set of moving gliders that all share ONE such period
(so H' is again a rigid single-class head)?
Prints counts per pattern; no Rule 110 runs (catalog only).
"""
import json, collections
from fractions import Fraction
CAT = '../../collider/'
G = {g['name']: g for g in json.load(open(CAT + 'gliders.json'))['gliders']}
R = json.load(open(CAT + 'reactions.json'))
HEAD = {(3, 2): 'A', (10, 2): 'D', (4, -2): 'B'}

def per(n):
    g = G.get(n)
    return None if g is None else (g['p'], g['d'])

def stationary(n):
    return per(n) == (7, 0)

unknown = set()
hits = collections.defaultdict(list)
for r in R:
    X, Y = r['X'], r['Y']
    for H, S in ((X, Y), (Y, X)):
        if per(H) is None:
            unknown.add(H)
            continue
        if per(H) not in HEAD or not stationary(S):
            continue
        outs = r['out']
        if any(per(o) is None for o in outs):
            unknown.update(o for o in outs if per(o) is None)
            continue
        st = [o for o in outs if stationary(o)]
        mv = [o for o in outs if not stationary(o)]
        pers = {per(o) for o in mv}
        key = (HEAD[per(H)], len(st), tuple(sorted(HEAD.get(p, str(p)) for p in pers)))
        hits[key].append((r['id'], outs))

for k in sorted(hits, key=lambda k: -len(hits[k])):
    print(k, len(hits[k]))
print('\n== clean head reactions: exactly 1 stationary out + moving outs of ONE head period ==')
for k, v in hits.items():
    if k[1] == 1 and len(k[2]) == 1 and k[2][0] in 'ADB':
        for rid, outs in v:
            print(k, rid, outs)
print('\nunknown names (no period in gliders.json):', len(unknown))
