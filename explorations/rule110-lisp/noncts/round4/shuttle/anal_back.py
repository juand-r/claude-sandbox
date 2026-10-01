"""Classify backscan output: for each (Y, cls), per n: rod objects (E-speed),
right-movers, left-movers, unknown. Report consistent categories."""
import sys, json, re
from fractions import Fraction
from collections import defaultdict
Gj = {g['name']: g for g in json.load(open('../../collider/gliders.json'))['gliders']}
E = Fraction(-4, 15)


def vel(nm):
    if nm in Gj:
        return Fraction(Gj[nm]['velocity'])
    m = re.match(r"v(-?\d+)/(\d+)s", nm)
    if m:
        return Fraction(int(m.group(1)), int(m.group(2)))
    parts = [q for q in re.split(r"[_@()+,]", nm) if q and not q.lstrip('-').isdigit()]
    vs = {Fraction(Gj[q]['velocity']) for q in parts if q in Gj}
    return vs.pop() if len(vs) == 1 else None


def chain_n(nm):
    """E^k index if nm is a standard rod (by name), else None"""
    if nm == "E":
        return 1
    m = re.match(r"E\^(\d+)$", nm)
    return int(m.group(1)) if m else None


recs = [json.loads(l) for l in open(sys.argv[1])]
cat = defaultdict(list)
for r in recs:
    sig = []
    for n, pr in sorted(r["prods"].items(), key=lambda kv: int(kv[0])):
        rods = [p for p in pr if vel(p) == E]
        rights = [p for p in pr if vel(p) is not None and vel(p) > E]
        lefts = [p for p in pr if vel(p) is not None and vel(p) < E]
        unk = [p for p in pr if vel(p) is None]
        sig.append((len(rods), tuple(sorted(rights)), len(lefts), len(unk)))
    s = set(sig)
    if len(s) == 1:
        nr, rights, nl, nu = s.pop()
        cat[("const", nr, rights, nl, nu)].append((r["X"], r["cls"], r["prods"]))
    else:
        cat[("varies",)].append((r["X"], r["cls"]))
for k in sorted(cat, key=lambda k: -len(cat[k])):
    print(len(cat[k]), k)

if len(sys.argv) > 2:
    key = eval(sys.argv[2])
    for x in cat[key][:int(sys.argv[3]) if len(sys.argv) > 3 else 30]:
        print(x)
