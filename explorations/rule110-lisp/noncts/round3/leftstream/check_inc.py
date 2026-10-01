"""Independent check of a SAT INC-from-left solution: type the SAT row with
collider's library, then rebuild the scene physically as
    [train] + E + (n-1) B's (B's extend E at its back before the train
arrives) and run exact Rule 110 for n = 1..NMAX. The train is moved left by
m * P_E (same collision class w.r.t. E, later arrival)."""
import json
import sys
from lsl import LIB, En, nval, embed, parse_row, run, snap, names, state

PE = (15, -4)


def load(i, path="sat_inc_results.jsonl"):
    recs = [json.loads(l) for l in open(path)]
    return recs[i]


def typed_scene(rec, j=0):
    lo, pL, pR = rec["frames"][j]
    row, x0 = embed(rec["rows0"][j], lo, pL, pR)
    ok, prods = parse_row(row, x0)
    assert all(p[0] != '?' for p in prods), prods
    return prods


def scene(train, Eseed, n, m=None, bgap=40):
    """train: seeds left of E; E seed; n - 1 B's behind E."""
    m = m if m is not None else 60 + 40 * n
    tr = [(nm, t0 + m * PE[0], x0 + m * PE[1]) for nm, t0, x0 in train]
    pl = list(tr)
    pl.append(Eseed)
    x = Eseed[2] + 30
    for i in range(n - 1):
        x = snap(pl, "B", 0, x)
        pl.append(("B", 0, x))
        x += bgap
    return pl, m


if __name__ == "__main__":
    i = int(sys.argv[1])
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    rec = load(i)
    prods = typed_scene(rec, 0)
    print("typed scene 0 (n=%d):" % rec["ns"][0], prods)
    E = [p for p in prods if nval(p[0])]
    assert len(E) == 1
    Eseed = ("E",) + tuple(E[0][1:]) if E[0][0] == "E" else None
    train = [p for p in prods if p[2] < E[0][2]]
    assert Eseed is not None, "scene 0 must be n = 1"
    for n in range(1, nmax + 1):
        pl, m = scene(train, Eseed, n)
        T = 15 * m + 60 * n + 600
        ok, out = run(pl, T)
        print(n, ok, names(out), out[:3])
