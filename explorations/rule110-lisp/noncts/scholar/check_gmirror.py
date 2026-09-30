"""Check collider's G-mirror: Ebar + G -> Ebar + A^4 with the Ebar on
EXACTLY its original trajectory and phase (in some classes).
For each configuration Ebar(fixed) - n e - G(phase), compare the Ebar's
anchors after the collision with the free extrapolation."""
import r110check as r, locate as L

T = 2200
res = {}
for g in [k for k in r.PHASES if k.startswith("G(")]:
    for n in (8, 9, 10):
        spec = f"E-(A,f1_1)-{n}e-{g}"
        row, s0 = r.build(spec, pad=300)
        h = r.evolve(row, T)
        e, l, _ = r.outcome(spec, T=T, pad=300)
        if sorted(l) != ["A^4", "E-"]:
            continue
        a0 = L.find(h, 0, "E-", s0 - 50, s0 + 100)[0]
        after = L.find(h, T - 60, "E-", 400, len(row) - 400)
        t0, x0 = a0
        shifts = set()
        for t1, x1 in after:
            if (t1 - t0) % 30 == 0:
                shifts.add(x1 - (x0 - 8 * (t1 - t0) // 30))
        res.setdefault(tuple(sorted(shifts)), []).append(spec)
for k, v in res.items():
    print("Ebar shift vs free trajectory:", k, len(v), "e.g.", v[:2])
