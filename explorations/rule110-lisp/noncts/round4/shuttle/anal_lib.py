"""Classify libscan outputs. For each (X, cls): rod-like products (speed
-4/15 'E'-family names) and the rest, per n."""
import sys, json, re
from fractions import Fraction
Gj = {g['name']: g for g in json.load(open('../../collider/gliders.json'))['gliders']}


def vel(nm):
    if nm in Gj:
        return Fraction(Gj[nm]['velocity'])
    m = re.match(r"v(-?\d+)/(\d+)s", nm)
    if m:
        return Fraction(int(m.group(1)), int(m.group(2)))
    parts = [q for q in nm.split("_") if not q.isdigit()]
    vs = {Fraction(Gj[q]['velocity']) for q in parts if q in Gj}
    if len(vs) == 1:
        return vs.pop()
    if nm.startswith("E@") or nm.startswith("Ebar@"):
        return Fraction(-4, 15)
    return None


E = Fraction(-4, 15)
cats = {}
for l in open(sys.argv[1]):
    r = json.loads(l)
    desc = []
    for n, pr in sorted(r["prods"].items(), key=lambda kv: int(kv[0])):
        rods = [p for p in pr if vel(p) == E]
        left = [p for p in pr if vel(p) is not None and vel(p) < E]
        right = [p for p in pr if vel(p) is not None and vel(p) > E]
        unk = [p for p in pr if vel(p) is None]
        desc.append((len(rods), len(left), len(right), len(unk)))
    key = tuple(sorted(set(desc)))
    cats.setdefault(key, []).append((r["X"], r["cls"], r["prods"]))
for key in sorted(cats, key=lambda k: -len(cats[k])):
    if len(key) == 1 and key[0][0] == 1 and key[0][1] >= 1 and key[0][2] == 0:
        tag = "ROD+LEFT ONLY"
    elif len(key) == 1 and key[0][0] == 0 and key[0][2] == 0 and key[0][3] == 0:
        tag = "LEFT ONLY (dump)"
    else:
        tag = ""
    print(len(cats[key]), key, tag)
    if tag:
        for x in cats[key][:40]:
            print("    ", x)
