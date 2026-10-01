"""Class algebra of a stationary C1 messenger vs Ebar-speed packets.
Lattice L = <P_C1 = (7,0), P_Ebar = (30,-8)>, 4 classes. For every catalog
EAT combo (C1 + pair -> C1) print the C1 displacement and how the class of
a FIXED later packet relative to the C1 changes after the meal (as a
permutation of the 4 class indices of that later packet type)."""
import json
from common import LIB, canonical_reps, predict, class_key

PC, PE = (7, 0), (30, -8)
R = json.load(open("collisions.json"))
EAT = [(r["Y"], r["cls"]) for r in R if r["X"] == "C1" and [p[0] for p in r["products"]] == ["C1"]]
GATE = [(r["Y"], r["cls"], [p[0] for p in r["products"]]) for r in R
        if r["X"] == "C1" and r["products"] and all(str(LIB.gliders[p[0]].velocity) == "-4/15" for p in r["products"])]


def cls_of(Y, rel):
    reps = canonical_reps(LIB, "C1", Y)
    keys = [class_key(q, PC, (LIB.gliders[Y].p, LIB.gliders[Y].d)) for q in reps]
    return keys.index(class_key(rel, PC, (LIB.gliders[Y].p, LIB.gliders[Y].d)))


if __name__ == "__main__":
    for Y, c in EAT:
        rep = canonical_reps(LIB, "C1", Y)[c]
        _, prods = predict("C1", Y, rep)
        d = prods[0][1:]
        # a later packet Z at relative event r (class k) is, after the meal,
        # at relative event r - d: its new class index
        perm = {}
        for Z, k in EAT[:1]:
            pass
        shift_key = class_key(d, PC, PE)
        print(f"EAT {Y:28s} #{c}: C1 -> {d}, displacement key {shift_key}")
    print("GATES:")
    for Y, c, ps in GATE:
        print(f"  {Y:26s} #{c} -> {ps}")
