"""Type the t = 0 rows of SAT records (sat_shuttle_results.jsonl) with
collider's library and run them in the exact CA (fastca window) to list
the products. Usage: python ident_sat.py [filter: r1|r2|joint] [T]"""
import json
import sys
from cl import *  # noqa
from r110lib import ether_cells

OUT = os.path.join(HERE, "sat_shuttle_results.jsonl")


def scenes_of(rec):
    for (lo, pL, pR), bits in zip(rec["frames"], rec["rows0"]):
        seg = np.array([int(c) for c in bits], np.uint8)
        row = np.concatenate([ether_cells(pL, lo - 300, lo), seg,
                              ether_cells(pR, lo + len(seg), lo + len(seg) + 300)])
        yield row, lo - 300, pL, pR


if __name__ == "__main__":
    filt = sys.argv[1] if len(sys.argv) > 1 else None
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 800
    for l in open(OUT):
        r = json.loads(l)
        if not r["sat"]:
            continue
        kind = r.get("only") or "joint"
        if filt and kind != filt:
            continue
        print(kind, "py", r["py"], "sx", r["sx"], "K", r["K"], "c", r["c1"], r["c2"])
        for row, x0, pL, pR in scenes_of(r):
            ok0, p0, _ = products_of(LIB, row, x0, 0)
            w = Window(row, x0, pL, pR).run(T)
            ok, prods = ident(w)
            print("   t=0:", [p[0] for p in p0], " t=%d:" % T, [p[0] for p in prods], ok)
