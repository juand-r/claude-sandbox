"""Independent check of any SAT train record: type the n = 1 scene (the
scene whose E is a plain E) with collider's library to get the train and
E seeds, then run the train against E^n (n = 1..NMAX, E + B's) in exact
Rule 110 (ops.describe). Usage: python check_rec.py FILE INDEX [NMAX]"""
import json
import sys
from lsl import embed, parse_row, nval
from ops import describe


def train_of(rec):
    for j, (lo, pL, pR) in enumerate(rec["frames"]):
        row, x0 = embed(rec["rows0"][j], lo, pL, pR)
        ok, prods = parse_row(row, x0)
        assert all(p[0] != "?" for p in prods), prods
        Es = [p for p in prods if nval(p[0])]
        if len(Es) == 1 and Es[0][0] == "E":
            tr = [p for p in prods if p[2] < Es[0][2]]
            return tr, tuple(Es[0][1:])
    raise ValueError("no n = 1 scene")


if __name__ == "__main__":
    f, i = sys.argv[1], int(sys.argv[2])
    nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    rec = [json.loads(l) for l in open(f)][i]
    tr, e0 = train_of(rec)
    print("train", tr, "E", e0)
    for n in range(1, nmax + 1):
        r, out = describe(tr, e0, n)
        print(n, r, out if r[0] is None or r[3] else "")
