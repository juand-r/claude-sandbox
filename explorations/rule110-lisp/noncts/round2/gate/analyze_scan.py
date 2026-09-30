"""Analyze counter_scan.json: clean counter effect e(P) of each packet, its
zero behaviour, and every A-conversion P -> Q with the change in effect.

e(P) is 'clean' if for every n in 2..NMAX and every class, E^n + P -> E^(n+e)
and nothing else. Zero classes: classes at n = 1 whose products are exactly
one E-chain object (plus, separately, E + single A = an answering DEC).
A conversion P -> Q is charge-conserving if e(Q) = e(P) - 1.
"""
import json
import re
from common import HERE, CHAIN

S = json.load(open(f"{HERE}/counter_scan.json"))
GB_E = {"GB3": -1, "GB4": 0, "GB5": 1, "GB6": 2, "GB7": 3, "GB8": 4}


def eff(prods, n):
    if len(prods) == 1 and prods[0] in CHAIN:
        return CHAIN.index(prods[0]) + 1 - n
    return None


def clean_effect(rec):
    es = set()
    for n, rows in rec["E"].items():
        n = int(n)
        if n < 2:
            continue
        for cls, st, ps in rows:
            e = eff(ps, n)
            if e is None or not st:
                return None
            es.add(e)
    return es.pop() if len(es) == 1 else None


def zero_info(rec):
    out = []
    for cls, st, ps in rec["E"]["1"]:
        e = eff(ps, 1)
        if e is not None:
            out.append((cls, f"E{e:+d}"))
        elif sorted(ps) == ["A", "E"]:
            out.append((cls, "E+A"))
    return out


E = {}
for P, rec in S.items():
    E[P] = clean_effect(rec)
E.update(GB_E)
if __name__ == "__main__":
    print("clean packets:", sum(1 for P in S if E[P] is not None), "/", len(S))
    rows = []
    for P, rec in S.items():
        if E[P] is None:
            continue
        for cls, ps in rec["A"]:
            if len(ps) == 0:
                eq = 0
            elif len(ps) == 1 and ps[0] in E and E[ps[0]] is not None:
                eq = E[ps[0]]
            else:
                eq = None
            tag = "?" if eq is None else ("cons" if eq == E[P] - 1 else f"NONCONS d={eq - E[P]}")
            rows.append((tag, P, E[P], zero_info(rec), cls, ps, eq))
    rows.sort(key=lambda r: r[0])
    for r in rows:
        print(*r)
