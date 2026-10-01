"""Export bounce.py tables in the documented format for the graph search.

One JSON line per (head, wall) pair:
  side      "R" (right-moving head hits the wall from the left) or "L"
  head_i    line index in heads_R.jsonl (R) or heads_L.jsonl (L)
  wall_j    line index in trains_7_0_20.jsonl
  head      {p, d, bits, pR}   (copied from the list)
  wall      {bits, pR}         (copied from the list)
  kind      reflect | pass | absorbed | dirty | unsettled
            reflect = exactly one stationary product + movers going back
            pass    = one stationary product + movers continuing
            absorbed= one stationary product only
            dirty   = anything else (0 or >= 2 stationary objects, movers
                      of different speeds, or unparsed debris)
  wall_out  {bits, pR, dx}: the stationary product as a t = 0 row in LIST
            FORM (left ether phase 0, first non-ether cell in [0, 14),
            trimmed right); dx = global column of that frame's origin
            minus the input wall's frame origin (rows at t = 0 mod 7, so
            frames are directly comparable; no separate dt is needed).
            wall_out_j = list index if this exact row is in the list.
  wall_canon / wall_out_canon: (bits, pR) minimised over the 7 time
            phases: equal canon = same physical object.
  head_out  {p, d, bits, pR}: the movers as one t = 0 row in LIST FORM;
            head_out_i = exact list index if present (heads_L for R rows,
            heads_R for L rows); head_out_canon minimised over phases.
  T         simulation length (products settled by then, else unsettled)
Usage: python export.py  -> bounce_table.jsonl"""
import sys, json, math
sys.dont_write_bytecode = True
import numpy as np
from fractions import Fraction
from bgraph import render, canon_row, canon_bits, name_of_key, classify, lib
from rod import TILE, ether_bit

ETH = "11111000100110"


def frame_form(row, lo, t):
    """list form of the single object/train in row (time t, 4t = 0 mod 14
    assumed so frames are t = 0 rows): returns (bits, pR, origin_global)."""
    n = len(row)
    e0 = 60
    pl = next(q for q in range(TILE) if all(row[i] == ether_bit(q, t, lo + i) for i in range(e0, e0 + 14)))
    pr = next(q for q in range(TILE) if all(row[i] == ether_bit(q, t, lo + i) for i in range(n - e0 - 14, n - e0)))
    le = np.array([ether_bit(pl, t, lo + i) for i in range(n)])
    re = np.array([ether_bit(pr, t, lo + i) for i in range(n)])
    dl = np.nonzero(row != le)[0]
    dr = np.nonzero(row != re)[0]
    a, b = dl[0], dr[-1] + 1
    phi = (lo + a + 4 * t + pl) % TILE
    origin = lo + a - phi
    bits = ETH[:phi] + "".join(map(str, row[a:b]))
    return bits, (pr - pl) % TILE, origin


def main(sides=("L", "R"), outname="bounce_table.jsonl"):
    heads = {"R": [json.loads(l) for l in open("heads_R.jsonl")],
             "L": [json.loads(l) for l in open("heads_L.jsonl")]}
    walls = [json.loads(l) for l in open("trains_7_0_20.jsonl")]
    wall_index = {(w["bits"], w["pR"]): j for j, w in enumerate(walls)}
    head_index = {s: {(h["bits"], h["pR"], h["p"], h["d"]): i for i, h in enumerate(heads[s])} for s in "RL"}
    wall_canon = {}
    out = open(outname, "w")
    for side, fn in (("L", "bounce_L.jsonl"), ("R", "bounce_R.jsonl")):
        if side not in sides:
            continue
        for l in open(fn):
            rec = json.loads(l)
            h = heads[side][rec["i"]]
            w = walls[rec["j"]]
            row = dict(side=side, head_i=rec["i"], wall_j=rec["j"],
                       head={k: h[k] for k in ("p", "d", "bits", "pR")},
                       wall={"bits": w["bits"], "pR": w["pR"]}, T=500)
            if rec["j"] not in wall_canon:
                wall_canon[rec["j"]] = canon_bits(w["bits"], w["pR"], 7)
            row["wall_canon"] = wall_canon[rec["j"]]
            if "err" in rec:
                row["kind"] = "dirty"
            elif not rec["ok"]:
                row["kind"] = "unsettled"
            else:
                c = classify(rec, side)
                row["kind"] = {"refl": "reflect", "pass": "pass", "absorb": "absorbed", "dirty": "dirty"}[c[0]]
                if c[0] in ("refl", "pass", "absorb"):
                    st = c[1]
                    nm = name_of_key(st["key"])
                    r_, lo = render([(nm, st["t0"], st["x"])], 0)
                    bits, pR, origin = frame_form(r_, lo, 0)
                    row["wall_out"] = dict(bits=bits, pR=pR, dx=int(origin))
                    row["wall_out_j"] = wall_index.get((bits, pR))
                    row["wall_out_canon"] = canon_row(r_, lo, 0, 7)
                if c[0] in ("refl", "pass"):
                    mem = [(name_of_key(p["key"]), p["t0"], p["x"]) for p in c[2]]
                    P = 1
                    for nm2, _, _ in mem:
                        P = P * lib().gliders[nm2].p // math.gcd(P, lib().gliders[nm2].p)
                    r_, lo = render(mem, 0)
                    bits, pR, origin = frame_form(r_, lo, 0)
                    g = lib().gliders[mem[0][0]]
                    v = Fraction(g.d, g.p)
                    # period of the head = lcm of its members' periods
                    pp, dd = P, int(P * v)
                    row["head_out"] = dict(p=pp, d=dd, bits=bits, pR=pR, members=[m[0] for m in mem], period_lcm=P)
                    other = "L" if side == "R" else "R"
                    row["head_out_i"] = head_index[other].get((bits, pR, pp, dd))
                    row["head_out_canon"] = canon_row(r_, lo, 0, P)
            out.write(json.dumps(row) + "\n")
    out.close()


if __name__ == "__main__":
    sides = sys.argv[1] if len(sys.argv) > 1 else "LR"
    main(tuple(sides), sys.argv[2] if len(sys.argv) > 2 else "bounce_table.jsonl")
