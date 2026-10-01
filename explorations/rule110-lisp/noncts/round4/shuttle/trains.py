"""Enumerate all (p,d)-periodic trains of width <= W embedded in ether
(left phase 0 at t = 0, right phase pR), by incremental SAT with blocking.
A train is stored canonically: the t=0 row trimmed to its non-ether
extent [a, b) together with the global phases left/right.
Every hit is checked periodic by forward simulation.
Usage: python trains.py p d W pR [maxn]  -> trains_p_d_W.jsonl (appends)"""
import sys
import json
sys.dont_write_bytecode = True
import numpy as np
from rod import TILE, ether_bit, simulate, SYNTH  # noqa
from r110sat import CNF, Spacetime, neg  # noqa


def enumerate_trains(p, d, W, pR, maxn=100000, require_start=True):
    cnf = CNF()
    st = Spacetime(cnf, p, 0, W, 0, pR)
    for x in range(-p - abs(d) - 2, W + p + abs(d) + 2):
        cnf.equal(st.lit(p, x + d), st.lit(0, x))
    # nonempty, and the defect starts at column 0 (dedupes translations)
    if require_start:
        st.differs(0, 0, TILE, [ether_bit(0, 0, x) for x in range(TILE)])
    else:
        st.differs(0, 0, W, [ether_bit(0, 0, x) for x in range(W)])
    s = cnf.solver()
    out = []
    while len(out) < maxn and s.solve():
        m = set(l for l in s.get_model() if l > 0)
        row = [int(st.lit(0, x) in m) for x in range(W)]
        out.append(row)
        s.add_clause([-st.lit(0, x) if row[x] else st.lit(0, x) for x in range(W)])
    s.delete()
    return out


def check_periodic(row, pR, p, d):
    W = len(row)
    pad = 4 * p + 60
    xs = range(-pad, W + pad)
    r0 = np.array([ether_bit(0, 0, x) if x < 0 else (row[x] if x < W else ether_bit(pR, 0, x))
                   for x in xs], np.uint8)
    h = simulate(r0, 2 * p)
    a, b = 2 * p + 10, len(r0) - 2 * p - 10
    return np.array_equal(h[p, a + d:b + d], h[0, a:b]) and np.array_equal(h[2 * p, a + 2 * d:b + 2 * d], h[0, a:b])


def trim(row, pR):
    W = len(row)
    b = W
    while b > 0 and row[b - 1] == ether_bit(pR, 0, b - 1):
        b -= 1
    return row[:b]


if __name__ == "__main__":
    p, d, W, pR = map(int, sys.argv[1:5])
    maxn = int(sys.argv[5]) if len(sys.argv) > 5 else 100000
    rows = enumerate_trains(p, d, W, pR, maxn)
    seen = set()
    n_ok = 0
    with open(f"trains_{p}_{d}_{W}.jsonl", "a") as fh:
        for r in rows:
            t = "".join(map(str, trim(r, pR)))
            if t in seen:
                continue
            seen.add(t)
            ok = check_periodic(r, pR, p, d)
            assert ok, ("not periodic", t)
            n_ok += 1
            fh.write(json.dumps(dict(p=p, d=d, pR=pR, bits=t)) + "\n")
    print(p, d, W, pR, "found", len(rows), "distinct", n_ok)
