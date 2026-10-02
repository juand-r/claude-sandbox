"""Reverse drift switch, step 1 (exact CA, numpy stepper): a uniform LEFT
stream of K copies of an A-lattice train Q (copies 14*m cells apart, same
class against an unmoved rod) hits a zero window E (seed time t0 = 0,1,2).
Does the window keep walking? Then: a B^3 (what K3 sends through R1's zero)
arrives at the window's back at a varying time; does the window close
(E -> E^4) and stop walking, cleanly, for every arrival time?
Candidates: lgate4.jsonl (walk on E, unmoved and neutral on E^4).
Usage: python lwalk.py [K] [m]"""
import json, os, sys
from lscan import *  # noqa

K = int(sys.argv[1]) if len(sys.argv) > 1 else 10
M = int(sys.argv[2]) if len(sys.argv) > 2 else 6      # spacing 14*M cells


def scene(q, t0, b3_dx=None):
    sts = [(q[0], 0, q[2], -14 * M * j) for j in range(K)]
    first = max(sts, key=lambda s: s[3])
    st, seed = right_of("E", t0, first)
    out = sts + [st]
    if b3_dx is not None:
        g = LIB.gliders["B^3"]
        cR = (st[2] - st[3]) % TILE
        for k in range(st[3] + len(st[0]) + b3_dx, st[3] + len(st[0]) + b3_dx + 30):
            sb = g.state_at(0, k, 0)
            if (sb[1] - sb[3] - cR) % TILE == 0:
                out.append(sb)
                break
    return out, seed


def run_to(states, T):
    row, x0 = build_row(states, pad=400 + int(0.3 * T))
    for _ in range(T):
        row = step_rows(row)
    ok, prods, _ = products_of(LIB, row, x0, T)
    return prods


if __name__ == "__main__":
    cands = [json.loads(l) for l in open(os.path.join(HERE, "lgate4.jsonl"))]
    cands = [c for c in cands if c["E4_unmoved"]]
    T = int((14 * M * K + 200) / (14 / 15)) + 300
    for c in cands:
        q = (c["bits"], 0, c["pR"], 0)
        for t0 in (0, 1, 2):
            sts, seed = scene(q, t0)
            ref = Fraction(seed[1]) - VE * seed[0]
            prods = run_to(sts, T)
            names = [p[0] for p in prods]
            if names == ["E"]:
                sh = float(lat(prods[0]) - ref)
                print(c["i"], "t0", t0, "walk after", K, "packets:", round(sh, 2), flush=True)
            else:
                print(c["i"], "t0", t0, "not clean:", names[:6], flush=True)
