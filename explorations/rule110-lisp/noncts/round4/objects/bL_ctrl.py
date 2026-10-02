"""Positive control for the bouncer L scene machinery (Reaction with left
B-lattice head, free wall, far right ("is", h1) + separation band):
known physics (shuttle's L table): B-lattice head (slip 10, width 30) + wall
(slip 8, width 20) -> new wall (slip 10) + one A (slip 8). Here the wall may
change (middle = any nonempty stationary) and h1 is a free A-lattice train
of slip 8 (width 12). Must be SAT."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "synth")))
from r110sat import CNF, TILE, ether_bit, neg
from react import TrainVar, ObjectVar, Reaction, verify_reaction
import bouncer_sat as BS
cnf = CNF()
h2 = TrainVar(cnf, 30, 4, -2, 10, name="h2")
h1 = TrainVar(cnf, 12, 3, 2, 8, name="h1")
V = ObjectVar(cnf, 20, 8, name="V")
r = Reaction(cnf, V, h2, 200, left=None, middle=("stationary",), right=("is", h1), mL=12, mR=12)
BS.separate(r, 200, "R", 8)
st = r.st
for ph in range(TILE):           # middle nonempty
    cl = [-r.bandL[ph]] + [neg(st.lit(200, x)) if ether_bit(ph, 200, x) else st.lit(200, x) for x in range(r.a, r.b)]
    cnf.add(cl)
sol = cnf.solve()
print("SAT" if sol else "UNSAT")
if sol:
    print(verify_reaction(r, sol))
    print("h2", "".join(map(str, h2.decode(sol))), "V", "".join(map(str, V.decode(sol))), "h1", "".join(map(str, h1.decode(sol))))
