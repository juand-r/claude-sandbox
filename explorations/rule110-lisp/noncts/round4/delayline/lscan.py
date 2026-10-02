"""LEFT window table: every (3,2) A-lattice train Q of width <= 30
(shuttle's SAT enumeration, round4/shuttle/trains_3_2_30.jsonl, read-only)
arriving from the LEFT at a zero window E and at E^2, in each of the 3
collision classes (E seed time t0 = 0, 1, 2). Exact CA (collider stepper
and typer). Records the products and, for a lone E / E^2, its intercept
shift relative to the unhit rod (>0 = to the right, toward a rod on the
right). Positive control first: Q = A (library) must give the catalog's
A + E -> D1, D1, C3 (3 classes) and A + E^2 -> E (all classes).
Resumable; output lscan.jsonl (this directory). Usage: python lscan.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from dl import LIB, CHAIN, HERE
from collide import products_of
from r110lib import build_row, step_rows, TILE

SRC = os.path.abspath(os.path.join(HERE, "..", "shuttle", "trains_3_2_30.jsonl"))
OUT = os.path.join(HERE, "lscan.jsonl")
VE = Fraction(-4, 15)
T = 420


def right_of(name, t0, qstate, gap=40):
    """Rod `name` seeded at time t0, as a t=0 state right of train qstate."""
    g = LIB.gliders[name]
    qend = qstate[3] + len(qstate[0])
    cR = (qstate[2] - qstate[3]) % TILE
    for k in range(qend + gap, qend + gap + 400):
        st = g.state_at(t0, k, 0)
        if st[3] >= qend + gap and (st[1] - st[3] - cR) % TILE == 0:
            return st, (t0, k)
    raise ValueError("no placement")


def run(states, xr):
    row, x0 = build_row(states, pad=320)
    for _ in range(T):
        row = step_rows(row)
    ok, prods, _ = products_of(LIB, row, x0, T)
    return prods


def lat(p):
    return Fraction(p[2]) - LIB.gliders[p[0]].velocity * p[1]


def test(qstate):
    rec = {}
    for rod in ("E", "E^2"):
        for t0 in (0, 1, 2):
            st, seed = right_of(rod, t0, qstate)
            ref = Fraction(seed[1]) - VE * seed[0]       # unhit rod's intercept
            prods = run([qstate, st], None)
            names = [p[0] for p in prods]
            sh = None
            if len(prods) == 1 and names[0] in CHAIN:
                sh = float(lat(prods[0]) - ref)
            rec[f"{rod}/{t0}"] = [names, sh]
    return rec


if __name__ == "__main__":
    A = LIB.gliders["A"]
    qa = A.state_at(0, 0, 0)
    print("control A:", test(qa), flush=True)
    done = set()
    if os.path.exists(OUT):
        done = {json.loads(l)["i"] for l in open(OUT)}
    trains = [json.loads(l) for l in open(SRC)]
    with open(OUT, "a") as f:
        for i, tr in enumerate(trains):
            if i in done:
                continue
            q = (tr["bits"], 0, tr["pR"], 0)
            try:
                rec = {"i": i, "bits": tr["bits"], "pR": tr["pR"], **test(q)}
            except Exception as e:
                rec = {"i": i, "error": repr(e)}
            f.write(json.dumps(rec) + "\n")
            if i % 500 == 0:
                print(i, rec, flush=True)
    print("done", flush=True)
