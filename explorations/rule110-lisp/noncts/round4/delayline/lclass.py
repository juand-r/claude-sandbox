"""Analyse lscan.jsonl: LEFT window behaviours of A-lattice trains.
Prints counts and the trains that are neutral on E^2 (lone E^2, any shift)
in some class AND walk a zero window E (lone E) in some class, with the
walk direction (>0: toward the right, i.e. toward the gap's far side)."""
import json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import LIB, HERE
from cl import vel
from fractions import Fraction
VE = Fraction(-4, 15)
rs = [json.loads(l) for l in open(os.path.join(HERE, "lscan.jsonl"))]
err = [r for r in rs if "error" in r]
rs = [r for r in rs if "error" not in r]
print(len(rs), "trains,", len(err), "errors")
walkE = Counter(); neuE2 = 0; shooters = []
cand = []
for r in rs:
    e = {k: r[k] for k in r if k.startswith("E/")}
    e2 = {k: r[k] for k in r if k.startswith("E^2/")}
    wk = {k: v[1] for k, v in e.items() if v[0] == ["E"]}
    nk = {k: v[1] for k, v in e2.items() if v[0] == ["E^2"]}
    for v in wk.values():
        walkE[round(v, 2)] += 1
    neuE2 += len(nk)
    if nk and wk:
        cand.append((r["i"], r["bits"], r["pR"], nk, wk))
    # zero window passes the train on as right-movers only (a left "gun")
    for k, v in e.items():
        names = v[0]
        if names and names.count("E") == 1 and len(names) > 1:
            try:
                oth = [n for n in names if n != "E"]
                if all(vel(n) > VE for n in oth) and nk:
                    shooters.append((r["i"], k, names, nk))
            except KeyError:
                pass
print("walk shifts of a zero window (lone E), counts:", sorted(walkE.items()))
print("(train, class) neutral on E^2:", neuE2)
print("trains neutral on E^2 in some class AND walking E in some class:", len(cand))
neg = [c for c in cand if any(v < 0 for v in c[4].values())]
print("  of which walk LEFT (away from the gap's far side) in some class:", len(neg))
for c in cand[:15]:
    print("  ", c)
print("neutral on E^2 and passing right-movers through E:", len(shooters))
for s in shooters[:15]:
    print("  ", s)
# gates: closed window (E^2) exactly unmoved in some class, open window walks
gates = [c for c in cand if any(abs(v) < 1e-9 for v in c[3].values()) and any(abs(v) > 1e-9 for v in c[4].values())]
gl = [c for c in gates if any(v < -1e-9 for v in c[4].values())]
gr = [c for c in gates if any(v > 1e-9 for v in c[4].values())]
print("GATES (E^2 unmoved in some class, E walks in some class):", len(gates), "| walk left:", len(gl), "| walk right:", len(gr))
for c in gl[:10]:
    print("  L", c)
for c in gr[:5]:
    print("  R", c)
