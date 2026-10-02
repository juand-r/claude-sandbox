"""Extend the bouncer tables to the heads that reflections PRODUCE but that
are not in the enumerated head lists (the frontier), against one
representative of each physical wall, in EVERY collision class (heads off
the A/B/D lattices have several classes against a stationary wall).
Output rows have the same format as bounce_table.jsonl plus "cls" and
"ncls"; heads are given in list form (from head_out of the table).
Usage: python frontier.py side(L|R) out.jsonl"""
import sys, json, os
sys.dont_write_bytecode = True
import numpy as np
from fractions import Fraction
from rod import TILE, ether_bit, simulate, SYNTH
from frontsim import run_row, lib, placements
from backscan import placements_right
from collide import products_of
from bgraph import canon_bits, classify
import export as ex

T = 700


def scene_rows(head, wall, side):
    """all-class scenes: wall frame at column 0 (left phase 0)."""
    wb = [int(c) for c in wall["bits"]]
    W = len(wb)
    hb = [int(c) for c in head["bits"]]
    p, d = head["p"], head["d"]
    out = []
    if side == "L":     # head right of wall, moving left
        pls = placements_right(hb, head["pR"], p, d, wall["pR"] % TILE, W + 30, PE=(7, 0))
    else:               # head left of wall, moving right
        pls = placements(hb, head["pR"], p, d, 0, -30, PE=(7, 0))
    for lo_x, seg, phi, off in pls:
        lo, hi = min(lo_x, 0) - 2 * T - 200, max(lo_x + len(seg), W) + 2 * T + 200
        xs = np.arange(lo, hi)
        if side == "L":
            row = np.array([ether_bit(0, 0, x) if x < 0 else (wb[x] if x < W else
                            (ether_bit(wall["pR"], 0, x) if x < lo_x else
                             (seg[x - lo_x] if x < lo_x + len(seg) else ether_bit(phi, 0, x)))) for x in xs], np.uint8)
        else:
            row = np.array([ether_bit(phi, 0, x) if x < lo_x else (seg[x - lo_x] if x < lo_x + len(seg) else
                            (ether_bit(0, 0, x) if x < 0 else (wb[x] if x < W else ether_bit(wall["pR"], 0, x))))
                            for x in xs], np.uint8)
        out.append((row, lo))
    return out


def run(side, outname):
    tab = [json.loads(l) for l in open("bounce_table.jsonl")]
    walls = [json.loads(l) for l in open("trains_7_0_20.jsonl")]
    rep = {}
    for j, w in enumerate(walls):
        rep.setdefault(tuple(canon_bits(w["bits"], w["pR"], 7)), (j, w))
    listed = set()
    for r in tab:
        if r["side"] == side:
            h = r["head"]
            listed.add(tuple(canon_bits(h["bits"], h["pR"], h["p"])))
    src = "R" if side == "L" else "L"
    front = {}
    for r in tab:
        if r["side"] == src and r["kind"] == "reflect":
            g = tuple(r["head_out_canon"])
            if g not in listed and g not in front:
                ho = r["head_out"]
                front[g] = dict(p=ho["p"], d=ho["d"], bits=ho["bits"], pR=ho["pR"], members=ho["members"])
    print("frontier heads", len(front), "walls", len(rep), flush=True)
    done = set()
    if os.path.exists(outname):
        for l in open(outname):
            q = json.loads(l)
            done.add((tuple(q["head_canon"]), tuple(q["wall_canon"])))
    with open(outname, "a") as fh:
        for g, h in front.items():
            for wc, (j, w) in rep.items():
                if (g, wc) in done:
                    continue
                rows = scene_rows(h, w, side)
                for k, (row, lo) in enumerate(rows):
                    rT = run_row(row, T)
                    a, b = T + 5, len(row) - T - 5
                    try:
                        ok, pr, _ = products_of(lib(), rT[a:b], lo + a, T)
                        prods = []
                        for nm, t0, x0 in pr:
                            if nm == "?":
                                prods.append(dict(name="?", x=int(x0))); continue
                            gg = lib().gliders[nm]
                            key = min((ph[0], ph[1], ph[2]) for ph in gg.phases)
                            prods.append(dict(name=nm, p=gg.p, d=gg.d, t0=int(t0), x=int(x0), key=list(key)))
                        rec = dict(ok=bool(ok), prods=prods)
                    except RuntimeError as e:
                        rec = dict(err=str(e))
                    c = classify(rec, side)
                    out = dict(side=side, head=h, head_canon=list(g), wall_j=j, wall=w, wall_canon=list(wc),
                               cls=k, ncls=len(rows), T=T)
                    if "err" in rec:
                        out["kind"] = "dirty"
                    elif not rec["ok"]:
                        out["kind"] = "unsettled"
                    else:
                        out["kind"] = {"refl": "reflect", "pass": "pass", "absorb": "absorbed", "dirty": "dirty"}[c[0]]
                        if c[0] in ("refl", "pass", "absorb"):
                            mem = [(ex.name_of_key(q["key"]), q["t0"], q["x"]) for q in c[1]]
                            r_, lo2 = ex.render(mem, 0)
                            out["wall_out_canon"] = ex.canon_row(r_, lo2, 0, 7)
                            bits, pR, origin = ex.frame_form(r_, lo2, 0)
                            out["wall_out"] = dict(bits=bits, pR=pR, dx=int(origin), n_objects=len(c[1]))
                        if c[0] in ("refl", "pass"):
                            import math
                            mem = [(ex.name_of_key(q["key"]), q["t0"], q["x"]) for q in c[2]]
                            P = 1
                            for nm2, _, _ in mem:
                                P = P * lib().gliders[nm2].p // math.gcd(P, lib().gliders[nm2].p)
                            r_, lo2 = ex.render(mem, 0)
                            bits, pR, origin = ex.frame_form(r_, lo2, 0)
                            gq = lib().gliders[mem[0][0]]
                            v = Fraction(gq.d, gq.p)
                            out["head_out"] = dict(p=P, d=int(P * v), bits=bits, pR=pR, members=[m[0] for m in mem])
                            out["head_out_canon"] = ex.canon_row(r_, lo2, 0, P)
                    fh.write(json.dumps(out) + "\n")
            fh.flush()


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
