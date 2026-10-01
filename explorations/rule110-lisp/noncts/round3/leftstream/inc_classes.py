"""For a SAT train (record i of sat_inc_results.jsonl): shift the train by
j * (1, -4) (j = 0, 1, 2: the three collision classes w.r.t. E) and run it
against E^n (n = 1..NMAX, built from E by B's) in exact Rule 110.
Prints outcome and displacement of the result (disp.py) per n."""
import sys
import check_inc as ci
from disp import disp, cls, PE
from lsl import nval, names, run

if __name__ == "__main__":
    i = int(sys.argv[1]); nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    rec = ci.load(i)
    prods = ci.typed_scene(rec, 0)
    E = [p for p in prods if nval(p[0])][0]
    e0 = tuple(E[1:])
    train = [p for p in prods if p[2] < E[2]]
    for j in range(3):
        tr = [(nm, t0 + j, x0 - 4 * j) for nm, t0, x0 in train]
        res = []
        for n in range(1, nmax + 1):
            pl, m = ci.scene(tr, ("E",) + e0, n)
            ok, out = run(pl, 15 * m + 60 * n + 600)
            if ok and len(out) == 1 and nval(out[0][0]):
                k = nval(out[0][0])
                d = disp(e0, k, out[0][1:])
                res.append(f"{n}->{k} d={d} c={cls(d)}")
            else:
                res.append(f"{n}-> {names(out)}")
        print(f"class shift {j}:"); print("   " + "\n   ".join(res))
