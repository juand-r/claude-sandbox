"""Statistics of the 3-marker transition graph: for each residue pair,
how many movers are clean, and how many winding steps each register can
take in one mover (single-mover net changes that are not P_F multiples)."""
from tworeg import residues, transitions, normP, D0
from lane import KEY
from collections import Counter
R = sorted(residues().values())
tot = Counter()
for D1 in R:
    for D2 in R:
        tr = transitions(D1, D2)
        tot["pairs"] += 1
        tot["clean"] += len(tr)
print(tot)
# how connected is the residue graph?
import itertools
edges = Counter()
for D1 in R:
    for D2 in R:
        for mv, d1, d2 in transitions(D1, D2):
            edges[((KEY(D1), KEY(D2)), (KEY((D1[0]+d1[0], D1[1]+d1[1])), KEY((D2[0]+d2[0], D2[1]+d2[1]))))] += 1
print("distinct residue edges", len(edges))
