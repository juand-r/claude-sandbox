"""Displacement of an F that absorbs a kick packet (catalog), and whether
it lies in L_F = <P_F, P_Ebar> (then an extra 'messenger F' upstream keeps
its class and can absorb every later kick of the block)."""
from common import LIB, canonical_reps, predict, class_key
PF, PE = (36, -4), (30, -8)
for Y in ["Ebar@(0,0)+Ebar@(-9,29)", "Ebar@(0,0)+Ebar@(-26,27)"]:
    rep = canonical_reps(LIB, "F", Y)[4]
    _, prods = predict("F", Y, rep)
    d = prods[0][1:]
    print(Y, "#4 -> F at", d, "key mod <P_F,P_E>:", class_key(d, PF, PE))
