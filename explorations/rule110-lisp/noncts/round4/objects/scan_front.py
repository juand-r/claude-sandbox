"""Mirror of scan_back.py: every library RIGHT-mover (v = 2/3 or 1/5), every
time phase, hits the FRONT of E^N. Does anything reach the BACK (a
front->back wall = phonon, or a crossing)? back hit = first time a cell right
of the back line (x > back(t) - MARGIN) differs from the rod-alone run.
Also records the final types (rod clean or not) for the hits.
Usage: python3 scan_front.py N T out.jsonl"""
import json, sys
import numpy as np
import objlib as O

N, T, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
L = O.lib()
names = [n for n, g in L.items() if g["velocity"] in ("2/3", "1/5")]
eb, el, er = O.en_bits(N)
PAD = 2 * T + 200
GAP, MARGIN = 20, 3


def scene(name, k):
    items = ([("g", name, k, 0)] if name else []) + [("raw", eb, el, er, GAP if name else 0, "E")]
    row, x_lo, objs, c = O.build(items, pad=PAD)
    s = [o for o in objs if o[0] == "E"][0][1]
    return row, x_lo, s


res = []
for name in names:
    for k in range(L[name]["p"]):
        row, x_lo, s = scene(name, k)
        # reference: the rod alone at the same place (rebuild with same left phase)
        b, l, r = eb, el, er
        ref = row.copy()
        # wipe the glider: cells left of the rod -> ether of the rod's left phase
        cl = (l - s) % 14
        ref[:s - x_lo] = O.ether(cl, x_lo, s)
        A = np.stack([row, ref])
        back0 = s + len(eb)
        first = None
        for t in range(1, T + 1):
            A = ((A[:, 1:-1] | A[:, 2:]) & (1 - (A[:, :-2] & A[:, 1:-1] & A[:, 2:]))).astype(np.uint8)
            xs = x_lo + t
            bx = back0 + (-4 * t) // 15 - MARGIN
            i0 = bx - xs
            assert 0 <= i0 < A.shape[1]
            if (A[0, i0:] != A[1, i0:]).any():
                first = t
                break
        rec = {"g": name, "k": k, "back_hit": first}
        if first is not None:
            a = O.evolve(row, T)
            rec["types"] = [x[0] for x in O.types_rods(a, x_lo + T, nmax=60)]
        res.append(rec)
        with open(OUT, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
hits = [r for r in res if r["back_hit"] is not None]
print(len(res), "scenes,", len(hits), "back hits")
for r in hits[:40]:
    print(json.dumps(r))
