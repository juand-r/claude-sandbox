"""Zero test, stage 5: two-packet tests (m1, m2).
Conditions:
  (a) on a separated pair at the standard residue, m1 then m2 is exactly
      the identity with clean crossings (predicted from the catalog);
  (b) on the value-0 compound, m1 is one of the packets that transform it
      cleanly (zc_fast.jsonl: products = F's / F-compounds + Ebar-speed);
  (c) simulate [m1, m2] on the compound and report the products; wanted:
      a stationary messenger + a recoverable register + leftward debris.
"""
import json, re, sys
from fractions import Fraction
sys.path.insert(0, "../collider")
from collide import simulate
from winding3 import movers, apply
from zc_fast import slot_anchor
from xstream import build, SLOT_LEN, PF
from rx import LIB

D0 = (0, 43)
EB = Fraction(-4, 15)

if __name__ == "__main__":
    recs = [json.loads(l) for l in open("zc_fast.jsonl")]
    def clean_tr(d):
        ps = d["products"]
        return all(p[0].startswith("F") or LIB.gliders.get(p[0]) is not None and
                   LIB.gliders[p[0]].velocity == EB for p in ps if not p[0].startswith("Ebar")) \
            and any(p[0].startswith("F") for p in ps) and \
            all(p[0].startswith("F") or p[0].startswith("Ebar") for p in ps)
    m1s = [tuple(d["mover"]) for d in recs if clean_tr(d)]
    MV = [m for m in movers() if not re.search(r"E(?!bar)", m[0])]
    print("m1 candidates", len(m1s), "m2 pool", len(MV), flush=True)
    pairs = []
    for m1 in m1s:
        D1 = apply(m1, D0)
        if D1 is None:
            continue
        for m2 in MV:
            if apply(m2, D1) == D0:
                pairs.append((m1, m2))
    print("identity pairs", len(pairs), flush=True)
    # simulate on the compound
    res = simulate(LIB, build(["DEC", "DEC"]), 36 * (SLOT_LEN + 5) * 2 + 8000)
    cname, ct, cx = [p for p in res["products"] if p[0].startswith("F_19_F")][0]
    a = slot_anchor(2)
    for m1, m2 in pairs:
        ev1 = (m1[0], a[0] + m1[1] + 20 * PF[0], a[1] + m1[2] + 20 * PF[1])
        # m2 relative to T after m1: approximate with the standard plan (T drift of m1
        # on a separated pair); m2 is placed 20 periods later relative to predicted T
        from winding3 import cross
        T1 = cross((0, 0), m1)[0]
        ev2 = (m2[0], a[0] + T1[0] + m2[1] + 40 * PF[0], a[1] + T1[1] + m2[2] + 40 * PF[1])
        k = ev1[1] // 36 - 3
        pl = [(cname, ct - 36 * k, cx + 4 * k)] + [(e[0], e[1] - 36 * k, e[2] + 4 * k) for e in (ev1, ev2)]
        r = simulate(LIB, pl, 5000)
        names = sorted(p[0] for p in r["products"] if not p[0].startswith("Ebar"))
        tag = "MSG" if any(n in ("C1", "C2", "C3") for n in names) else ""
        print(m1, m2, names, tag, flush=True)
