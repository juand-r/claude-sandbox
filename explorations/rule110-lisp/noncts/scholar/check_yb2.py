"""Independent evaluation of architect's order-independent lane (m1_yb.py).

Placements (seed events) come from architect's m1_yb.build (collider's
glider library), but the evolution uses ../../engine.step via my
r110check.evolve, and the outcome is typed by MY census-based typer
(r110check.objects), not collider's. Negative control: a triple that is
pairwise clean but not order-independent (architect's first attempt used
C2 x F#1, F x Ebar#8, C2 x Ebar#2).
Usage: python check_yb2.py [yb|control]"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parent / "architect"
sys.path.insert(0, str(ARCH))
sys.path.insert(0, str(HERE.parent / "collider"))
cwd = os.getcwd()
os.chdir(ARCH)                     # rx.py uses relative paths
import m1_yb                        # noqa: E402
from rx import G as GL              # noqa: E402
from r110lib import build_row       # noqa: E402
os.chdir(cwd)
sys.path.insert(0, str(HERE))
import r110check as r               # noqa: E402

T = 12000


def evaluate(placements):
    states = [GL[n].state_at(t0, x0, 0) for n, t0, x0 in placements]
    row, xo = build_row(states, pad=T + 200)
    h_last = row.copy()
    # evolve keeping only the last MAX_P+1 rows needed by the typer
    import numpy as np
    from engine import step
    keep = []
    cur = row
    for t in range(T):
        cur = step(cur)
        if t >= T - 160:
            keep.append(cur)
    h = np.array(keep)
    lo, hi = 150, len(row) - 150
    objs = r.objects(h, len(h) - 1, lo, hi)
    return sorted(o[2] for o in objs)


def main(mode):
    if mode == "control":
        m1_yb.M, m1_yb.kMF, m1_yb.kFS, m1_yb.kMS = "C2", 1, 8, 2
    os.chdir(ARCH)
    G, S = m1_yb.design()
    os.chdir(cwd)
    print(mode, "G", G, "S", S, flush=True)
    want = sorted([m1_yb.M] + ["F"] * 4 + ["E-"] * 16)
    clean = 0
    runs = 0
    for a in range(0, 40, 4):
        pl = m1_yb.build(G, S, a)
        got = evaluate(pl)
        ok = got == want
        clean += ok
        runs += 1
        print(f"a={a:2d} {'CLEAN' if ok else got}", flush=True)
    print(f"{mode}: clean {clean}/{runs}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "yb")
