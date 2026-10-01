"""Wall-converter scan by exact simulation (theory s.6.5; complements
verify's parked E/Ebar/E^k scan): every co-moving library object O
(velocity -4/15) parked behind R2 = E^4 (library glider), every phase of
O and small gaps; keep placements where E^4 | O is stable alone; then
send the front op F (I_L or Z_L, in its working class against E^4) and
record the products. Flag: exactly one E^k, O (same name) and only
right-movers otherwise. Resumable: appends JSON lines to conv_scan.jsonl.
Usage: python conv_scan.py"""
import json
import os
import sys
from fractions import Fraction
from lsl import LIB, run, snap, nval, names, state
from lpk import PK

OUT = "conv_scan.jsonl"
V = Fraction(-4, 15)
E0 = ("E^4", 0, 0)


def working(F, n_out):
    """Seeds of packet F (lpk) placed left of E0 so that F + E^4 gives
    n_out cleanly: scan time phase j and offset dx (ether-consistent
    ones only), distance m * P_E."""
    base = PK[F]["seeds"]
    t_, x_ = base[0][1], base[0][2]
    m = 6
    for j in range(3):
        for dx in range(0, 42):
            sh = [(nm, t - t_ + j + 15 * m, x - x_ - 80 + dx - 4 * m)
                  for nm, t, x in base]
            try:
                ok, out = run(sh + [E0], 15 * m + 700)
            except ValueError:
                continue
            if ok and names(out) == n_out:
                return sh, out
    raise RuntimeError(f"no working placement for {F}")


def back_end():
    b, l, r, s = state(*E0)
    return s + len(b)


if __name__ == "__main__":
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            r = json.loads(l)
            done.add((r["O"], r["t0"], r["x0"]))
    ops = {"I_L": working("I", ["E^5"])[0], "Z_L": working("Z", ["E^3"])[0]}
    print("working placements", ops, flush=True)
    xb = back_end()
    objs = sorted([n for n, g in LIB.gliders.items() if g.velocity == V],
                  key=lambda n: (LIB.gliders[n].width, n))   # small first
    with open(OUT, "a") as fh:
        for O in objs:
            g = LIB.gliders[O]
            for t0 in range(g.p):
                seen_x = set()
                for gap in range(0, 15):    # verify: the back moves <= ~8 cells
                    try:
                        x0 = snap([E0], O, t0, xb + gap)
                    except AssertionError:
                        continue
                    if x0 in seen_x or (O, t0, x0) in done:
                        continue
                    seen_x.add(x0)
                    rec = {"O": O, "t0": t0, "x0": x0}
                    try:
                        ok, out = run([E0, (O, t0, x0)], 500)
                    except ValueError as e:      # overlap at t = 0
                        rec["skip"] = str(e)[:60]
                        fh.write(json.dumps(rec) + "\n")
                        continue
                    rec["alone"] = names(out)
                    if names(out) != ["E^4", O]:
                        fh.write(json.dumps(rec) + "\n")
                        continue
                    for F, seeds in ops.items():
                        ok2, out2 = run(seeds + [E0, (O, t0, x0)], 15 * 12 + 1200)
                        nm = names(out2)
                        rec[F] = nm
                        Es = [n for n in nm if nval(n)]
                        rest = [n for n in nm if not nval(n)]
                        flag = (ok2 and len(Es) == 1 and O in rest and
                                all(LIB.gliders[n].velocity > 0 for n in rest if n != O)
                                and len(rest) > 1)
                        rec[F + "_flag"] = flag
                    fh.write(json.dumps(rec) + "\n")
                    fh.flush()
    print("done", flush=True)
