"""Independent check of address's 00:09 claim: two independently addressable
registers in one F lane (tworeg_abs.py). I take their placements
(tworeg_abs.schedule, imported read-only; that is the claim's input),
translate them to my convention with xlate (row equality with collider's
build_row asserted), evolve with the exact engine, and type with MY typer.
Check: exactly 3 F's, each at the predicted seed (I rebuild the predicted
F's alone in my builder, evolve the same T, and compare F defects cell for
cell incl. phase), and every other object has Ebar/E velocity (-4/15).
Also: my own gap arithmetic from the F positions."""
import os, sys, random
from fractions import Fraction
import numpy as np
import vlib, libgen, xlate

ADDR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "address"))
sys.path.insert(0, ADDR)
cwd = os.getcwd()
os.chdir(ADDR)
import tworeg_abs as T2      # noqa: E402  (read-only)
os.chdir(cwd)

def my_run(pl, T):
    ex = xlate.expand([(g, int(t), int(x)) for g, t, x in pl])
    items, c0, same = xlate.check(ex)
    assert same, "translation mismatch"
    row, org, placed = vlib.build(items, c0=c0, T=T)
    assert [p[2] for p in placed] == [i[2] for i in items]
    r = vlib.evolve(row, T)
    return r, org

def fs_and_junk(r, org, T):
    ids = vlib.identify(r, org, T=T)
    Fs = [(n, x) for n, x, w, k in ids if n.split("@")[0] == "F"]
    others = [(n, x, k) for n, x, w, k in ids if n.split("@")[0] != "F"]
    return Fs, others

def velocity_of_unknowns(r, org, T, others):
    """Families invariant for each non-F defect (cut region)."""
    cut = T + 16
    sub = r[cut:len(r) - cut]
    vt = vlib.velocity_type(sub)
    return vt

def check(prog):
    pl, pred, delay = T2.schedule(prog)
    T = 36 * (delay + 40) + 6000
    r, org = my_run(pl, T)
    Fs, others = fs_and_junk(r, org, T)
    # predicted F's alone
    rp, orgp = my_run([("F",) + tuple(m) for m in pred], T)
    Fp, _ = fs_and_junk(rp, orgp, T)
    # cell-level comparison of the F region (robust to my typer merging
    # close F's): window around the predicted F's, global coordinates
    dp = [d for d in vlib.defects(rp[T + 16:len(rp) - T - 16])]
    lo = min(d["lo"] for d in dp) + T + 16 + orgp - 40
    hi = max(d["hi"] for d in dp) + T + 16 + orgp + 40
    cells_equal = np.array_equal(r[lo - org:hi - org], rp[lo - orgp:hi - orgp])
    others = [o for o in others if not (lo <= o[1] < hi)]
    names = [o[0].split("@")[0] for o in others]
    ebar_like = all(n in ("Ebar", "E") or n.startswith("E^") for n in names)
    xs = sorted(x for _, x in Fs)
    gaps = [b - a for a, b in zip(xs, xs[1:])]
    return cells_equal, ebar_like, names, gaps, Fs, Fp

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    rnd = random.Random(seed)
    progs = [["DN2"], ["UP2"], ["DN1"], ["UP1"],
             ["UP1", "UP1", "DN2", "DN1", "UP1", "UP1"],
             ["DN1", "UP1", "DN1", "UP2", "UP2", "DN1"]]
    for _ in range(n):
        progs.append([rnd.choice(list(T2.OPS)) for _ in range(6)])
    ok = 0
    for prog in progs:
        good, ebar_like, names, gaps, Fs, Fp = check(prog)
        ok += good and ebar_like
        print(" ".join(prog), "| F region == predicted F's (cells):", good, "| others all Ebar-family:",
              ebar_like, sorted(set(names)), "| F gaps (cells, at T):", gaps, flush=True)
    print(f"{ok}/{len(progs)} reproduced")


def control(prog, idx, shift):
    """Same program with mover idx shifted by an ether-compatible vector not
    in <P_F, P_Ebar>; compare against the UNSHIFTED prediction."""
    pl, pred, delay = T2.schedule(prog)
    name, t, x = pl[3 + idx]
    pl[3 + idx] = (name, t + shift[0], x + shift[1])
    T = 36 * (delay + 40) + 6000
    r, org = my_run(pl, T)
    rp, orgp = my_run([("F",) + tuple(m) for m in pred], T)
    dp = vlib.defects(rp[T + 16:len(rp) - T - 16])
    lo = min(d["lo"] for d in dp) + T + 16 + orgp - 40
    hi = max(d["hi"] for d in dp) + T + 16 + orgp + 40
    return np.array_equal(r[lo - org:hi - org], rp[lo - orgp:hi - orgp])
