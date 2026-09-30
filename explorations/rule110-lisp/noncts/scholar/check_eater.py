"""Check collider's claim: C1 eats certain Ebar PAIRS (C1 + pair -> C1 alone)."""
import r110check as r
ys = [k for k in r.PHASES if k.startswith("E-(")]
hits = []
for y2 in ys:
    for g in (0, 1):
        for n in (8, 9, 10, 11):
            spec = f"C1(A,f1_1)-{n}e-E-(A,f1_1)-{g}e-{y2}"
            e, l, _ = r.outcome(spec, T=1300, pad=220)
            if e == l and l == ["C1"]:
                hits.append(spec)
print(len(hits), "pair/position combos give C1 alone; e.g.", hits[:6])
