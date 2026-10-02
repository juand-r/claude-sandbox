"""For table rows whose wall_out disagrees with mine (spot_bounce), test
whether their wall_out is my stationary product at ANOTHER time phase
(i.e. an export phase error), and report the phase offset and dx error.
python3 spot_phase.py TABLE SIDE KIND N [seed]"""
import json
import random
import sys

import hrun
import rawscene
import spot_bounce as SB


def phases(r, gap=40, T0=840):
    hd, w = r["head"], r["wall"]
    objs = [(hd["bits"], hd["pR"], 100), (w["bits"], w["pR"], gap)] if r["side"] == "R" else \
           [(w["bits"], w["pR"], 100), (hd["bits"], hd["pR"], gap)]
    row, org, st = rawscene.assemble(objs)
    wall_x = st[1] if r["side"] == "R" else st[0]
    out = []
    # stationary span at T0 (velocity-typed, my code)
    h0 = hrun.HRun(row, org)
    h0.goto(T0)
    lo0 = org - T0 - 200
    _, ds = SB.defects_with_velocity(h0, lo0, org + len(row) + T0 + 200)
    st_ = [(a + lo0, b + lo0) for a, b, v in ds if v == (0, 1)]
    if not st_:
        return None
    xa, xb = min(a for a, b in st_) - 10, max(b for a, b in st_) + 10
    h = hrun.HRun(row, org)
    for k in range(7):
        T = T0 + k
        h.goto(T)
        lo = org - T - 200
        r0 = h.cells(lo, org + len(row) + T + 200)
        dd = [d for d in hrun.vlib.defects(r0) if xa <= d["lo"] + lo and d["hi"] + lo <= xb]
        if not dd:
            return None
        a, b = min(d["lo"] for d in dd), max(d["hi"] for d in dd)
        bits, pR, origin = SB.list_form(r0, lo, T, a, b)
        out.append((bits, pR, origin - wall_x))
    return out


def main(table, side, kind, n, seed=1):
    rows = [json.loads(l) for l in open(table)]
    rows = [r for r in rows if r["side"] == side and r["kind"] == kind]
    rnd = random.Random(seed)
    stats = {}
    for r in rnd.sample(rows, n):
        ph = phases(r)
        wo = (r["wall_out"]["bits"], r["wall_out"]["pR"], r["wall_out"]["dx"])
        if ph is None:
            res = "no product"
        elif ph[0] == wo:
            res = "phase 0 exact"
        else:
            ks = [k for k, p in enumerate(ph) if p[:2] == wo[:2]]
            res = f"phase {ks[0]} dx err {wo[2] - ph[ks[0]][2]}" if ks else "not found"
        stats[res] = stats.get(res, 0) + 1
    for k, v in sorted(stats.items(), key=lambda kv: -kv[1]):
        print(f"  {v:4d}  {k}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]) if len(sys.argv) > 5 else 1)
