"""Exact-CA census of 'phase-free head' reactions (route LN in ROUTES.md).

A head H is a rigid packet whose period is exactly A=(3,2), D=(10,2) or
B=(4,-2); a cell S is a stationary object (period (7,0)). By the lattice
count |det(P_H, P_S)|/14 = 1 every such collision has ONE class, so its
outcome cannot depend on spacing (THEORY.md, Lemma LN1).  We collide every
library head with every library cell (one simulation each, collider's exact
pipeline, which re-checks the class count) and record the products.

A reaction is a CLEAN HEAD STEP if the products are exactly one stationary
object S' plus moving objects that all share ONE head period (a new rigid
head H' moving right (A or D lattice) or left (B lattice)), or nothing
moving (absorption: H' = none).

Output: lnscan2.jsonl (one line per pair).  Usage:
  nice -n 10 python3 lnscan2.py [max_cell_parts]
Library is used read-only (auto-registered names live in memory only).
"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../collider'))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../collider'))
from library import Library
from collide import collide_pair
from r110lib import n_classes

HEADP = {(3, 2): 'A', (10, 2): 'D', (4, -2): 'B'}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lnscan2.jsonl')

def nparts(name):
    g = LIB.gliders[name]
    return len(g.parts) if g.parts else name.count('_C') + 1

LIB = Library.load()
maxparts = int(sys.argv[1]) if len(sys.argv) > 1 else 2
heads = [n for n, g in LIB.gliders.items() if (g.p, g.d) in HEADP]
cells = [n for n, g in LIB.gliders.items() if (g.p, g.d) == (7, 0) and nparts(n) <= maxparts]
done = set()
if os.path.exists(OUT):
    for line in open(OUT):
        j = json.loads(line); done.add((j['H'], j['S']))
print(len(heads), 'heads', len(cells), 'cells', len(done), 'done', flush=True)
t0 = time.time()
with open(OUT, 'a') as f:
    for S in cells:
        for H in heads:
            if (H, S) in done:
                continue
            g = LIB.gliders[H]
            fam = HEADP[(g.p, g.d)]
            X, Y = (H, S) if fam in 'AD' else (S, H)
            assert n_classes((LIB.gliders[X].p, LIB.gliders[X].d), (LIB.gliders[Y].p, LIB.gliders[Y].d)) == 1
            try:
                res = collide_pair(LIB, X, Y)
            except Exception as e:  # overlap / edge errors: record loudly
                f.write(json.dumps({'H': H, 'S': S, 'err': repr(e)}) + '\n'); continue
            assert len(res) == 1
            r = res[0]
            prods = r['products']
            st = [p for p in prods if p[0] != '?' and (LIB.gliders[p[0]].p, LIB.gliders[p[0]].d) == (7, 0)]
            mv = [p for p in prods if p not in st]
            fams = sorted({HEADP.get((LIB.gliders[p[0]].p, LIB.gliders[p[0]].d), '?') if p[0] != '?' else '?' for p in mv})
            clean = r['settled'] and len(st) == 1 and len(fams) <= 1 and '?' not in fams
            f.write(json.dumps({'H': H, 'fam': fam, 'S': S, 'settled': r['settled'], 'clean': clean,
                                'S_out': st, 'H_out': mv, 'H_fam': fams, 'Y_event': r['Y_event']}) + '\n')
        f.flush()
        print(S, 'done', round(time.time() - t0), 's', flush=True)
