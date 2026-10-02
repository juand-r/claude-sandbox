"""Lead item 2, library-object scan: CONTACT of a walking left window with a
co-moving marker. A uniform left stream (K copies of a walking train,
14*M apart) walks a zero window W_L = E right (train #499: +11.2/packet)
into a marker X parked to its right (X in E, E^2, E^3, E^4, Ebar), placed at
every ether-compatible offset in a range and every seed time (all relative
classes). Exact CA (numpy stepper, collider typer). Classify the end state:
  STOP   one E-family rod, nothing else (merged; walking stopped or not)
  EMIT   E-family object(s) + only RIGHT-movers (the contact sends a signal
         toward the far window: what route 20 needs)
  KEEP   W_L and X both survive separately (passed / no contact yet)
  DEB    anything else
Output contact.jsonl. Usage: python contact.py [train] [t0] [K] [M]"""
import json, os, sys
from lscan import *  # noqa
from cl import vel

TRI = int(sys.argv[1]) if len(sys.argv) > 1 else 499
T0 = int(sys.argv[2]) if len(sys.argv) > 2 else 1
K = int(sys.argv[3]) if len(sys.argv) > 3 else 16
M = int(sys.argv[4]) if len(sys.argv) > 4 else 6
Q = [json.loads(l) for l in open(os.path.join(HERE, "lscan.jsonl")) if json.loads(l).get("i") == TRI][0]
EF = set(CHAIN) | {"Ebar"}


def run_to(states, T):
    row, x0 = build_row(states, pad=400 + int(0.3 * T))
    for _ in range(T):
        row = step_rows(row)
    ok, prods, _ = products_of(LIB, row, x0, T)
    return prods


def classify(prods):
    names = [p[0] for p in prods]
    rods = [n for n in names if n in EF or (n.startswith("v-4/15"))]
    oth = [n for n in names if n not in rods]
    try:
        vs = [vel(n) for n in oth]
    except KeyError:
        return "DEB"
    if len(rods) == 1 and not oth:
        return "STOP"
    if rods and oth and all(v > VE for v in vs):
        return "EMIT"
    if len(rods) == 2 and not oth:
        return "KEEP"
    return "DEB"


qs = [(Q["bits"], 0, Q["pR"], -14 * M * j) for j in range(K)]
first = max(qs, key=lambda s: s[3])
wl, seed = right_of("E", T0, first)
T = int((14 * M * K + 600) / (14 / 15)) + 400
out = open(os.path.join(HERE, f"contact_{TRI}_{T0}.jsonl"), "w")
tally = {}
for X in ("E", "E^2", "E^3", "E^4", "Ebar"):
    g = LIB.gliders[X]
    cR = (wl[2] - wl[3]) % TILE
    for t0 in range(g.p):
        for k in range(wl[3] + len(wl[0]) + 10, wl[3] + len(wl[0]) + 130):
            st = g.state_at(t0, k, 0)
            if st[3] < wl[3] + len(wl[0]) + 8 or (st[1] - st[3] - cR) % TILE:
                continue
            try:
                prods = run_to(qs + [wl, st], T)
            except Exception as e:
                prods = [("ERR:" + repr(e)[:40], 0, 0)]
            c = classify(prods) if not prods or not prods[0][0].startswith("ERR") else "DEB"
            tally[(X, c)] = tally.get((X, c), 0) + 1
            rec = {"X": X, "t0": t0, "k": k, "dist": st[3] - wl[3] - len(wl[0]), "cls": c,
                   "products": [[p[0], int(p[1]) if p[1] is not None else None, int(p[2]) if p[2] is not None else None] for p in prods]}
            out.write(json.dumps(rec) + "\n")
            out.flush()
            if c in ("EMIT", "STOP"):
                print(rec, flush=True)
print(tally, flush=True)
