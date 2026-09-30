"""Independent check of synth's claim: the only linear conservation law of
the verified reaction catalog (collider/reactions.json) is slip mod 14.
Rows = (products - inputs) as count vectors over named base glider types;
packets like 'E@(0,0)+E@(-13,15)' are split into their members. The group
Z^k / (row lattice) is computed by Smith normal form (sympy)."""
import json
import re
from pathlib import Path
from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_form
from sympy import ZZ

CAT = Path(__file__).resolve().parents[1] / "collider" / "reactions.json"
NAMED = {"A", "A^2", "A^3", "A^4", "A^5", "B", "B^2", "B^3", "Bbar", "Bhat",
         "C1", "C2", "C3", "D1", "D2", "E", "E^2", "E^3", "Ebar", "F", "G", "H"}
# my widths (sign convention of r110check); tight bundles: k * width mod 14
W = {"A": 8, "B": 6, "Bbar": 6, "Bhat": 3, "C1": 5, "C2": 11, "C3": 3,
     "D1": 3, "D2": 9, "E": 9, "Ebar": 7, "F": 13, "G": 4, "H": 3}


def members(name):
    return [re.sub(r"@.*$", "", p) for p in name.split("+")]


def width(n):
    m = re.fullmatch(r"(A|B|E)\^(\d)", n)
    if m:
        base, k = m.group(1), int(m.group(2))
        return (W[base] + 6 * (k - 1)) % 14 if base == "E" else (k * W[base]) % 14
    return W[n]


def main():
    rows, types = [], sorted(NAMED)
    idx = {t: i for i, t in enumerate(types)}
    used = 0
    for x in json.load(open(CAT)):
        ins = members(x["X"]) + members(x["Y"])
        outs = [p[0] for p in x["products_base"]]
        if not all(n in NAMED for n in ins + outs):
            continue
        v = [0] * len(types)
        for n in outs:
            v[idx[n]] += 1
        for n in ins:
            v[idx[n]] -= 1
        rows.append(v)
        used += 1
    M = Matrix(rows)
    print(f"{used} reactions among {len(types)} named types; rank {M.rank()}")
    snf = smith_normal_form(M, domain=ZZ)
    diag = [snf[i, i] for i in range(min(snf.shape)) if snf[i, i] != 0]
    print("nonzero SNF diagonal (invariant factors):", [abs(d) for d in diag if abs(d) != 1], "and", sum(1 for d in diag if abs(d) == 1), "ones")
    wv = [width(t) for t in types]
    bad = [r for r in rows if sum(a * b for a, b in zip(r, wv)) % 14]
    print("rows violating slip mod 14 (my width table):", len(bad))


if __name__ == "__main__":
    main()
