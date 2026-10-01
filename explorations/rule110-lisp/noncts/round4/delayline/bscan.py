"""Burst-safe refill search (THEORY_DL.md s.7): a left-moving B-lattice
train Q (period (4,-2)) that
  (a) CROSSES an A (A + Q -> A + Q', both survive)  and
  (b) INCREMENTS a rod from its back: E^m + Q -> E^(m+k), nothing else.
Both pairs have ONE collision class (|det|/14 = 1 for (3,2),(4,-2) and
(15,-4),(4,-2)), so each test is one simulation and the outcome does not
depend on timing. Trains: theory's SAT enumeration of all (4,-2) trains of
width <= 30 (round4/theory/trains_4_-2_30.jsonl, read-only).
Positive controls: Q = B (library) must give A + B -> nothing (catalog
annihilation) and E^m + B -> E^(m+1); Q = B^3 -> E^(m+3).
Exact automaton (collider r110lib stepper, collider typer).
Output: bscan.jsonl (this directory). Usage: python bscan.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import LIB, CHAIN, HERE
from collide import products_of
from r110lib import build_row, step_rows, TILE
import numpy as np

SRC = os.path.abspath(os.path.join(HERE, "..", "theory", "trains_4_-2_30.jsonl"))
OUT = os.path.join(HERE, "bscan.jsonl")


def left_of(name, xq_abs_phase, gap=40):
    """Library glider state at t = 0 left of a train starting at 0 whose left
    ether has absolute phase xq_abs_phase (= lph - start)."""
    g = LIB.gliders[name]
    best = None
    for k in range(-400, 0):
        st = g.state_at(0, k, 0)
        if st[3] + len(st[0]) <= -gap and (st[2] - st[3] - xq_abs_phase) % TILE == 0:
            best = st
    return best


def run_pair(lname, qstate, T):
    st = left_of(lname, (qstate[1] - qstate[3]) % TILE)
    row, x0 = build_row([st, qstate], pad=300)
    for _ in range(T):
        row = step_rows(row)
    ok, prods, _ = products_of(LIB, row, x0, T)
    return [p[0] for p in prods]


def lib_state(name):
    g = LIB.gliders[name]
    return g.state_at(0, 0, 0)


def classify(lname, prods):
    if lname == "A":
        return "CROSS" if "A" in prods and len(prods) == 2 and "?" not in prods else ("NONE" if not prods else "OTHER")
    es = [p for p in prods if p in CHAIN]
    if len(prods) == 1 and es:
        return "INC%+d" % (CHAIN.index(es[0]) - CHAIN.index(lname))
    return "OTHER"


if __name__ == "__main__":
    LEFTS = ["A", "E", "E^2", "E^3", "E^5"]
    # positive controls with library B-family trains
    for q in ("B", "B^3"):
        qs = lib_state(q)
        res = {l: run_pair(l, qs, 900 if l != "A" else 400) for l in LEFTS}
        print("control", q, res, flush=True)
    trains = [json.loads(l) for l in open(SRC)]
    hits = 0
    with open(OUT, "w") as f:
        for i, tr in enumerate(trains):
            qs = (tr["bits"], 0, tr["pR"], 0)
            rec = {"i": i, "bits": tr["bits"], "pR": tr["pR"]}
            try:
                for l in LEFTS:
                    pr = run_pair(l, qs, 900 if l != "A" else 400)
                    rec[l] = pr
                    rec["c_" + l] = classify(l, pr)
            except Exception as e:
                rec["error"] = repr(e)
            good = rec.get("c_A") == "CROSS" and all(str(rec.get("c_" + l, "")).startswith("INC+") for l in ("E^2", "E^3", "E^5"))
            rec["target"] = good
            hits += good
            f.write(json.dumps(rec) + "\n")
            if good or i % 50 == 0:
                print(i, rec, flush=True)
    print("trains:", len(trains), "targets:", hits)
