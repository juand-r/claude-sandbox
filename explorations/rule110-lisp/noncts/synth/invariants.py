"""Linear conservation laws of glider collisions (all of them, from data).

Every verified reaction in collider's catalog (../collider/reactions.json,
base-glider expansion) gives an integer vector r = (#out - #in) over glider
types. A conserved quantity mod m is v with r . v = 0 (mod m) for all r.
The group of all such laws is determined by the Smith normal form of the
reaction matrix: Z^n / span(r) = Z^f + sum Z_{d_i}. f > 0 would be an exact
integer conservation law; each d_i > 1 a law mod d_i. Slip mod 14 must
appear. Restricted to reactions whose inputs and outputs are all in TYPES
(named gliders and tight bundles), so unnamed products do not add free
symbols."""
import json
from collections import Counter
from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

R = json.load(open("../collider/reactions.json"))
BASE = ["A", "B", "Bbar", "Bhat", "C1", "C2", "C3", "D1", "D2", "E", "Ebar",
        "F", "G", "H"]
TYPES = BASE + ["A^2", "A^3", "A^4", "A^5", "B^2", "B^3", "E^2", "E^3"]
rows = []
used = 0
for r in R:
    ins = [r["X"], r["Y"]]
    outs = [p if isinstance(p, str) else p[0] for p in r["out_base"]]
    if not all(g in TYPES for g in ins + outs):
        continue
    c = Counter(outs)
    c.subtract(Counter(ins))
    v = [c[g] for g in TYPES]
    if any(v):
        rows.append(v)
    used += 1
M = Matrix(rows)
print("reactions used:", used, "distinct nonzero vectors:", len(set(map(tuple, rows))))
rows = [list(t) for t in sorted(set(map(tuple, rows)))]
M = Matrix(rows)
S = smith_normal_form(M, domain=ZZ)
diag = [S[i, i] for i in range(min(S.shape)) if S[i, i] != 0]
print("rank:", len(diag), "of", len(TYPES), "types")
print("Smith diagonal (nonzero):", diag)
print("free part (exact integer laws):", len(TYPES) - len(diag))
