"""Reflection tables for the BOUNCER (route 14 / perpetual shuttle between
two stationary walls). Single class (R4-L1): A-, D- and B-lattice heads
meet a stationary object in exactly one collision class, so each (head,
wall) pair has ONE outcome, independent of distance and timing.

R-table: right-moving head (A (3,2) or D (10,2) train) hits wall W from
the left. L-table: left-moving head (B (4,-2) train) hits W from the right.
Each outcome is parsed into objects (collider typer). A REFLECTION is:
exactly one stationary object W' plus one or more movers going back the
way the head came (all on one lattice), nothing going on.
Usage: python bounce.py heads.jsonl walls.jsonl side(R|L) out.jsonl [T]
"""
import os, sys, json, time
sys.dont_write_bytecode = True
import numpy as np
from fractions import Fraction
from rod import TILE, ether_bit, simulate
from frontsim import run_row, lib
from collide import products_of

GAP = 24


def frame_row(bits, pR, lo, hi, x0):
    """train/object with frame (left phase 0 at t=0) placed so frame col 0
    is global col x0: global phase of left ether = -x0, right = pR - x0."""
    W = len(bits)
    return np.array([ether_bit(0, 0, x - x0) if x < x0 else
                     (bits[x - x0] if x < x0 + W else ether_bit(pR, 0, x - x0))
                     for x in range(lo, hi)], np.uint8)


def scene(head, wall, side, T):
    """t = 0 row with the wall at frame position 0 and the head on `side`.
    Phases: wall left ether phase global 0 (x0 = 0). Head placed so its
    ether matches."""
    wb = [int(c) for c in wall["bits"]]
    wpR = wall["pR"]
    hb = [int(c) for c in head["bits"]]
    hpR = head["pR"]
    W, H = len(wb), len(hb)
    lo, hi = -2 * T - 200, W + 2 * T + 200
    xs = np.arange(lo, hi)
    if side == "R":
        # head left of wall: its right ether must be global phase 0
        # head frame at x0h: right global phase = hpR - x0h = 0 mod 14
        x0h = -GAP - H
        x0h -= (x0h - hpR) % TILE
        pl = (-x0h) % TILE
        row = np.array([ether_bit(pl, 0, x) if x < x0h else
                        (hb[x - x0h] if x < x0h + H else
                         (ether_bit(0, 0, x) if x < 0 else
                          (wb[x] if x < W else ether_bit(wpR, 0, x)))) for x in xs], np.uint8)
    else:
        # head right of wall: its left ether (frame phase 0) must equal the
        # wall's right global phase wpR: -x0h = wpR mod 14
        x0h = W + GAP
        x0h += (-wpR - x0h) % TILE
        row = np.array([ether_bit(0, 0, x) if x < 0 else
                        (wb[x] if x < W else
                         (ether_bit(wpR, 0, x) if x < x0h else
                          (hb[x - x0h] if x < x0h + H else ether_bit(hpR - x0h, 0, x)))) for x in xs], np.uint8)
    return row, lo


def describe(name):
    g = lib().gliders[name]
    b, l, r, off = g.phases[0] if hasattr(g, "phases") else (None, None, None, None)
    return dict(name=name, p=g.p, d=g.d, v=str(g.velocity))


def outcome(head, wall, side, T):
    row, lo = scene(head, wall, side, T)
    rT = run_row(row, T)
    a, b = T + 5, len(row) - T - 5
    try:
        ok, pr, _ = products_of(lib(), rT[a:b], lo + a, T)
    except RuntimeError as e:
        return dict(err=str(e))
    prods = []
    for nm, t0, x0 in pr:
        if nm == "?":
            prods.append(dict(name="?", x=int(x0)))
            continue
        g = lib().gliders[nm]
        key = min((ph[0], ph[1], ph[2]) for ph in g.phases)
        prods.append(dict(name=nm, p=g.p, d=g.d, t0=int(t0), x=int(x0), key=list(key)))
    return dict(ok=bool(ok), prods=prods)


if __name__ == "__main__":
    hf, wf, side, out = sys.argv[1:5]
    T = int(sys.argv[5]) if len(sys.argv) > 5 else 500
    heads = [json.loads(l) for l in open(hf)]
    walls = [json.loads(l) for l in open(wf)]
    done = 0
    if os.path.exists(out):
        done = sum(1 for _ in open(out))
    t0 = time.time()
    k = 0
    with open(out, "a") as fh:
        for i, h in enumerate(heads):
            for j, w in enumerate(walls):
                if k < done:
                    k += 1
                    continue
                k += 1
                res = outcome(h, w, side, T)
                fh.write(json.dumps(dict(i=i, j=j, side=side, **res)) + "\n")
            if i % 20 == 0:
                print(i, k, round(time.time() - t0, 1), flush=True)
