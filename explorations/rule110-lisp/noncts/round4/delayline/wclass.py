"""Classify every library G-speed packet's action on a window (E = value 0,
E^2 = value 1), from scan_reflect_M1.jsonl (E) and scan_e2.jsonl (E^2).
Categories per (packet, class):
  NEU   E^2 -> E^2 alone (neutral at value 1)
  VAL   single E^k alone (k != input)
  LPASS E^k + only left-movers (faster than E)  [shot into the gap]
  RPASS E^k + only right-movers                 [answer into the stream]
  WALK  E -> E alone (with intercept shift)
  DEB   anything else
Prints the target lists (see THEORY_DL.md s.8). Usage: python wclass.py"""
from wtable import *  # noqa
from fractions import Fraction
VE = Fraction(-4, 15)


def velo(n):
    from cl import vel
    return vel(n)


def cat(products, nin):
    es = [p for p in products if p[0] in CHAIN]
    oth = [p for p in products if p[0] not in CHAIN]
    if len(es) != 1:
        return "DEB", None
    k = CHAIN.index(es[0][0]) + 1
    shift = float(Fraction(es[0][2]) - VE * es[0][1])
    if not oth:
        if k == nin:
            return ("WALK" if nin == 1 else "NEU"), (k, round(shift, 2))
        return "VAL", (k, round(shift, 2))
    try:
        vs = [velo(p[0]) for p in oth]
    except KeyError:
        return "DEB", None
    if all(v < VE for v in vs):
        return "LPASS", (k, [p[0] for p in oth])
    if all(v > VE for v in vs):
        return "RPASS", (k, [p[0] for p in oth])
    return "DEB", None


M1, M2 = load()
table = {}
for Y in M2:
    if 'rows' not in M2[Y] or 'rows' not in M1[Y]:
        continue
    e1 = [(r['cls'],) + cat(r['products'], 1) if r['settled'] else (r['cls'], "DEB", None) for r in M1[Y]['rows']]
    e2 = [(r['cls'],) + cat(r['products'], 2) if r['settled'] else (r['cls'], "DEB", None) for r in M2[Y]['rows']]
    table[Y] = (e1, e2)

allneu = [Y for Y, (e1, e2) in table.items() if all(c[1] == "NEU" for c in e2)]
someneu = [Y for Y, (e1, e2) in table.items() if any(c[1] == "NEU" for c in e2)]
print(len(table), "packets;", len(allneu), "neutral on E^2 in all classes;", len(someneu), "in some class")
print("\n-- neutral on E^2 (some class) AND shooting left on E (some class): reflector/shooter candidates")
for Y in someneu:
    e1, e2 = table[Y]
    if any(c[1] == "LPASS" for c in e1):
        print(Y, "slip", LIB.gliders[Y].slip, "E^2:", e2, "E:", e1)
print("\n-- walkers with a LEFT shift on E (neutral on E^2 in some class)")
for Y in someneu:
    e1, e2 = table[Y]
    if any(c[1] == "WALK" and c[2][1] < 0 for c in e1):
        print(Y, "E^2:", e2, "E:", e1)
print("\n-- pass-through at value 1: E^2 -> E^k + left-movers")
for Y, (e1, e2) in table.items():
    if any(c[1] == "LPASS" for c in e2):
        print(Y, "slip", LIB.gliders[Y].slip, "E^2:", [c for c in e2 if c[1] == "LPASS"], "E:", e1)
