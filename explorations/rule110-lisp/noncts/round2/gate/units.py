"""Step 3: search two-packet units U = [D, X] on the E^n counter.

D = GB3 (DEC; at zero, in its designated class, E + A; the A flies right).
X = a G-speed packet from the scan with a clean A-conversion A + X -> X'
(class c). Unit semantics (value v = n - 1):
  v >= 2: D gives v-1 >= 1, then X acts at n >= 2 (class-free if clean)
  v == 1: D gives 0, then X acts at the ZERO state in some class k
  v == 0: D answers A, A + X -> X' (class c), X' acts at zero in class k'
Behaviours at zero may leave garbage LEFT of E (escapes) -- see behave.py.
Class compatibility of k, k', c is NOT checked here (done in the CA later);
this lists candidate semantic tables, flagging non-monotone units.
Output: units.json.
"""
import json
import sys
from common import HERE, CHAIN, LIB, collide_pair, names
from behave import classify

S = json.load(open(f"{HERE}/counter_scan.json"))
try:
    CACHE = json.load(open(f"{HERE}/xprime_cache.json"))
except FileNotFoundError:
    CACHE = {}


def table(P, nmax=3):
    """{n: [(cls, classification)]} for E^n + P."""
    if P in S:
        rows = {int(n): [(c, ps) for c, st, ps in r] for n, r in S[P]["E"].items()}
    elif P in CACHE:
        rows = {int(n): r for n, r in CACHE[P].items()}
    else:
        rows = {}
        for n in range(1, nmax + 1):
            rows[n] = [(r["cls"], names(r["products"])) for r in
                       collide_pair(LIB, CHAIN[n - 1], P)]
        CACHE[P] = rows
    return {n: [(c, ps, classify(ps, n)) for c, ps in r] for n, r in rows.items()}


def clean_e(tab):
    """Effect for n >= 2 if identical over classes and n, no garbage."""
    es = set()
    for n, r in tab.items():
        if n < 2:
            continue
        for c, ps, b in r:
            if b is None or b[1] or b[2]:
                return None
            es.add(b[0])
    return es.pop() if len(es) == 1 else None


out = []
for X, rec in S.items():
    tX = table(X)
    eX = clean_e(tX)
    if eX is None:
        continue
    zX = [(c, b) for c, ps, b in tX[1] if b is not None]
    for cA, prods in rec["A"]:
        if len(prods) != 1:
            continue           # absorbed to nothing or several objects: skip here
        Xp = prods[0]
        if Xp.startswith("GB") and len(Xp) == 3:
            k = int(Xp[2])
            tXp = None
        try:
            tXp = table(Xp)
        except Exception as ex:   # noqa: BLE001  (unknown pair geometry): log loudly
            print("FAILED", Xp, ex, file=sys.stderr)
            continue
        eXp = clean_e(tXp)
        zXp = [(c, b) for c, ps, b in tXp[1] if b is not None]
        for kx, bx in zX:
            for kp, bp in zXp:
                U = {0: bp[0], 1: 0 + bx[0], 2: 1 + eX, 3: 2 + eX}
                U = {v: max(u, -99) for v, u in U.items()}
                nonmono = any(U[v] > U[v + 1] for v in range(3))
                out.append(dict(X=X, eX=eX, cA=cA, Xp=Xp, eXp=eXp, kx=kx, bx=bx,
                                kp=kp, bp=bp, U=U, nonmono=nonmono))
json.dump(CACHE, open(f"{HERE}/xprime_cache.json", "w"))
json.dump(out, open(f"{HERE}/units.json", "w"))
print(len(out), "units;", sum(u["nonmono"] for u in out), "non-monotone")
for u in out:
    if u["nonmono"]:
        print(u)
