"""Summarize lane_scan.json: for each compound Y, C1 outcomes (EAT = C1
alone, GATE = only Ebar-speed products, PASS) and F outcomes (CROSS = F + Y,
ABSORB = F alone, CONV = F + other Ebar-speed objects only)."""
import json
from fractions import Fraction
from common import HERE, LIB
from behave import velocity

S = json.load(open(HERE + "/lane_scan.json"))
VE = Fraction(-4, 15)


def isE(n):
    try:
        return velocity(n) == VE
    except Exception:
        return False


rows = []
for Y, rec in S.items():
    c1 = {"EAT": [], "GATE": [], "PASS": []}
    for cls, st, ps in rec["C1"]:
        if not st:
            continue
        if ps == ["C1"]:
            c1["EAT"].append(cls)
        elif ps and all(isE(p) for p in ps):
            c1["GATE"].append((cls, ps))
        elif sorted(ps) == sorted(["C1", Y]):
            c1["PASS"].append(cls)
    f = {"CROSS": [], "ABSORB": [], "CONV": []}
    for cls, st, ps in rec["F"]:
        if not st:
            continue
        if ps == ["F"]:
            f["ABSORB"].append(cls)
        elif sorted(ps) == sorted(["F", Y]):
            f["CROSS"].append(cls)
        elif "F" in ps and all(p == "F" or isE(p) for p in ps):
            f["CONV"].append((cls, [p for p in ps if p != "F"]))
    if c1["EAT"] or c1["GATE"]:
        rows.append((Y, c1, f))
for Y, c1, f in rows:
    print(Y, "| C1:", {k: v for k, v in c1.items() if v}, "| F:", {k: v for k, v in f.items() if v})
print(len(S), "scanned;", len(rows), "with EAT or GATE")
