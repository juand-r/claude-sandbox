"""Parse cross0.log: list packets that are CLEAN at n >= 2 (every class
gives one E^(n+e), same e for all n = 2..NMAX) and report their zero
outcome per class. Usage: python cross0_clean.py"""
import ast
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
cur, rows = None, {}
for line in open(os.path.join(HERE, "cross0.log")):
    if line.startswith("== "):
        cur = line.split()[1]
        rows[cur] = {}
    m = re.match(r"\s+E\^(\d+): (.*)$", line)
    if m and cur:
        rows[cur][int(m.group(1))] = ast.literal_eval(m.group(2))
for X, r in rows.items():
    es = set()
    ok = len(r) >= 3
    for n, res in r.items():
        if n == 1:
            continue
        for c, ps in res:
            if len(ps) != 1 or not ps[0].startswith("E^"):
                ok = False
            else:
                es.add(int(ps[0][2:]) - n)
    if ok and len(es) == 1:
        print(X, "n>=2: +%d class-free;" % es.pop(), "zero:", r.get(1), "n up to", max(r))
