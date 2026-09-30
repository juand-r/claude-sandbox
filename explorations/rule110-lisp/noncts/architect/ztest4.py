"""Stage 6: for the two-packet identities (m1, m2) that split the value-0
compound into two separate F's (ztest3.log), record the split pair's D
and predict (catalog) what each identity mover m3 does to that pair:
we want m3 to be the identity on normal pairs (it is, by choice) and to
emit a stationary messenger at the split pair without right-movers."""
import ast, json, sys
from collections import defaultdict
sys.path.insert(0, "../collider")
from collide import simulate
from winding3 import movers, apply, cross, lateral, predict
from zc_fast import slot_anchor
from xstream import build, SLOT_LEN, PF
from rx import LIB

rows = []
for l in open("ztest3.log"):
    if not l.startswith("("):
        continue
    i = l.index(") (") + 1
    j = l.index(") [") + 1
    m1 = ast.literal_eval(l[:i]); m2 = ast.literal_eval(l[i + 1:j])
    names = ast.literal_eval(l[j + 1:l.index("]", j) + 1])
    if names == ["F", "F"]:
        rows.append((m1, m2))

res = simulate(LIB, build(["DEC", "DEC"]), 36 * (SLOT_LEN + 5) * 2 + 8000)
cname, ct, cx = [p for p in res["products"] if p[0].startswith("F_19_F")][0]
a = slot_anchor(2)
Ds = defaultdict(list)
for m1, m2 in rows:
    ev1 = (m1[0], a[0] + m1[1] + 20 * PF[0], a[1] + m1[2] + 20 * PF[1])
    T1 = cross((0, 0), m1)[0]
    ev2 = (m2[0], a[0] + T1[0] + m2[1] + 40 * PF[0], a[1] + T1[1] + m2[2] + 40 * PF[1])
    k = ev1[1] // 36 - 3
    pl = [(cname, ct - 36 * k, cx + 4 * k)] + [(e[0], e[1] - 36 * k, e[2] + 4 * k) for e in (ev1, ev2)]
    r = simulate(LIB, pl, 5000)
    fs = sorted([p for p in r["products"] if p[0] == "F"], key=lambda p: p[2] - p[1] / 9)
    (_, tp, xp), (_, tt, xt) = fs
    D = (tt - tp, xt - xp)
    # normalise D modulo F's period on T
    q = D[0] // 36
    D = (D[0] - 36 * q, D[1] + 4 * q)
    Ds[D].append((m1, m2))
print("distinct split D:", {d: len(v) for d, v in Ds.items()}, flush=True)
ids = [mv for mv in movers() if apply(mv, (0, 43)) == (0, 43)]
for D in Ds:
    for m3 in ids:
        T2, outs = cross((0, 0), m3)
        P = (-D[0], -D[1])
        for o in sorted(outs, key=lateral):
            try:
                k3, prods = predict("F", o[0], (o[1] - P[0], o[2] - P[1]), eX=P)
            except Exception as e:
                print("D", D, "m3", m3, "predict error", str(e)[:60]); break
            names = [p[0] for p in prods]
            if names.count("F") == 1 and all(n == "F" or n.startswith("Ebar") for n in names):
                P = [(p[1], p[2]) for p in prods if p[0] == "F"][0]
                continue
            right = [n for n in names if n.startswith("A") or n.startswith("D") or n.startswith("v2/3")]
            print("D", D, "gap %.2f" % (D[1] + D[0] / 9), "m3", m3, "->", names,
                  "CANDIDATE" if not right and any(n in ("C1", "C2", "C3") for n in names) else "",
                  "example (m1,m2):", Ds[D][0], flush=True)
            break
