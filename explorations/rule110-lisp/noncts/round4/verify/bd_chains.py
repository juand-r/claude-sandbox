"""Count reflections in the long-lived (escaped_T2) runs of bouncer_direct:
sample every 50 steps; the mover = defects farther than 25 cells from both
walls' initial places; count reversals of the mover's mean position.
python3 bd_chains.py TABLE BD_JSONL N"""
import json
import sys

import numpy as np

import hrun
import rawscene

vlib = hrun.vlib


def reversals(row, org, st, wlen, Tmax=20000, dt=50):
    h = hrun.HRun(row, org)
    xl, xr = st[0], st[2]
    pos, rev, last_dir = [], 0, 0
    for t in range(0, Tmax, dt):
        h.goto(t)
        lo = xl - 400
        r = h.cells(lo, xr + wlen + 400)
        mv = [(d["lo"] + d["hi"]) / 2 + lo for d in vlib.defects(r)
              if abs(d["lo"] + lo - xl) > 25 and abs(d["lo"] + lo - xr) > 25]
        if not mv:
            pos.append(None)
            continue
        p = float(np.mean(mv))
        if pos and pos[-1] is not None:
            d = np.sign(p - pos[-1])
            if d != 0 and last_dir != 0 and d != last_dir:
                rev += 1
            if d != 0:
                last_dir = d
        pos.append(p)
    return rev


if __name__ == "__main__":
    table, bd, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    rows, walls = {}, {}
    for l in open(table):
        r = json.loads(l)
        if r["side"] == "L":
            walls.setdefault(tuple(r["wall_canon"]), (r["wall"]["bits"], r["wall"]["pR"]))
            if r["kind"] == "reflect":
                rows[(r["head_i"], r["wall_j"])] = r
    wl = sorted(walls.values())
    al = [json.loads(l) for l in open(bd)]
    al = [a for a in al if a["res"] == "escaped_T2"]
    import random
    random.Random(1).shuffle(al)
    hist = {}
    for a in al[:n]:
        r = rows[(a["head_i"], a["wall_j"])]
        wb, wp = wl[a["wr"]]
        row, org, st = rawscene.assemble([(r["wall"]["bits"], r["wall"]["pR"], 100),
                                          (r["head"]["bits"], r["head"]["pR"], 40), (wb, wp, 150)])
        k = reversals(row, org, st, len(wb))
        hist[k] = hist.get(k, 0) + 1
        print(a, "reversals", k, flush=True)
    print("histogram of reversals:", dict(sorted(hist.items())))
