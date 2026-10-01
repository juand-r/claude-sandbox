"""Independent check of address's FIXED-stream two-register F lane
(address/fixed_stream.py, not yet posted; NOTES 01:40). Placements from
fixed_stream.build(program) (read-only import; they depend only on the slot
index and the instruction type). My translation (row equality asserted),
exact engine, my typer. Checks: exactly 3 F's; every other object
Ebar-family; F gaps (measured from MY F positions at time T, using each F's
seed position extrapolated to t = 0 with velocity -1/9) equal address's
arithmetic prediction within 0.5 cells. Also checks that the placements of
slot j do not depend on the program's earlier instructions (fixedness)."""
import os, sys, random
from fractions import Fraction
import vlib, xlate

ADDR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "address"))
sys.path.insert(0, ADDR)
cwd = os.getcwd(); os.chdir(ADDR)
import fixed_stream as FS       # noqa: E402
import tworeg_abs as T2         # noqa: E402
os.chdir(cwd)

FG = vlib.LIB["F"]

def seed_pos(name_at, lo, T):
    """x at t = 0 of an F observed at time T in phase s with defect lo."""
    s = int(name_at.split("@")[1])
    row, off = FG.snapshot(s)
    d = vlib.defects(row)
    lo_snap = min(dd["lo"] for dd in d) + off          # lo of phase-s snapshot, base coords
    # base seeded at (t0, x0): at time T, phase s = (T - t0) mod 36 and the row
    # is snapshot(s) shifted by x0 + q*D with q = (T - t0 - s)/36
    t0 = T - s                                          # choose q = 0
    x0 = lo - lo_snap
    return Fraction(x0) + Fraction(-4, 36) * (0 - t0)   # move back to t = 0

def check(prog):
    os.chdir(ADDR)
    try:
        pl = FS.build(prog)
        want = T2.predicted_gaps(prog)
    finally:
        os.chdir(cwd)
    ex = xlate.expand([(g, int(t), int(x)) for g, t, x in pl])
    items, c0, same = xlate.check(ex)
    assert same
    T = 36 * FS.SLOT * (len(prog) + 1) + 8000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = vlib.evolve(row, T)
    ids = vlib.identify(r, org, T=T)
    Fs = [(n, x) for n, x, w, k in ids if n.split("@")[0] == "F"]
    others = sorted({n.split("@")[0] for n, x, w, k in ids if n.split("@")[0] != "F"})
    xs = sorted(seed_pos(n, x, T) for n, x in Fs)
    got = [float(b - a) for a, b in zip(xs, xs[1:])]
    ok = len(Fs) == 3 and set(others) <= {"Ebar", "E"} and \
        all(abs(g - w) < 0.5 for g, w in zip(got, want))
    return ok, [round(g, 2) for g in got], [round(w, 2) for w in want], others

def fixedness(L=4, trials=6, seed=3):
    """slot j's movers must not depend on earlier instructions."""
    rnd = random.Random(seed)
    os.chdir(ADDR)
    try:
        for _ in range(trials):
            a = [rnd.choice(list(FS.BASE)) for _ in range(L)]
            b = [rnd.choice(list(FS.BASE)) for _ in range(L - 1)] + [a[-1]]
            pa, pb = FS.build(a), FS.build(b)
            na = len(FS.STD[a[-1]][0])
            if pa[-na:] != pb[-na:]:
                return False
    finally:
        os.chdir(cwd)
    return True

if __name__ == "__main__":
    print("fixedness (last slot independent of history):", fixedness())
    progs = [["UP2", "DN2", "UP2", "UP1", "UP1"], ["DN1", "UP1", "DN1", "DN2", "DN2"],
             ["DN1", "UP1", "DN1", "UP1", "UP1"], ["UP1", "UP1", "DN2"]]
    ok = 0
    for p in progs:
        good, got, want, others = check(p)
        ok += good
        print(" ".join(p), "| gaps mine", got, "address", want, "| others", others, "|", "OK" if good else "MISMATCH", flush=True)
    print(f"{ok}/{len(progs)} reproduced")


def control(prog, idx, shift):
    """Shift mover idx (counting after the 3 F's) by an ether-compatible
    vector that is not in <P_F, P_Ebar>; the result must change."""
    os.chdir(ADDR)
    try:
        pl = FS.build(prog)
        want = T2.predicted_gaps(prog)
    finally:
        os.chdir(cwd)
    name, t, x = pl[3 + idx]
    pl[3 + idx] = (name, t + shift[0], x + shift[1])
    ex = xlate.expand([(g, int(t), int(x)) for g, t, x in pl])
    items, c0 = xlate.translate(ex)
    T = 36 * FS.SLOT * (len(prog) + 1) + 8000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = vlib.evolve(row, T)
    ids = vlib.identify(r, org, T=T)
    Fs = [(n, x) for n, x, w, k in ids if n.split("@")[0] == "F"]
    others = sorted({n.split("@")[0] for n, x, w, k in ids if n.split("@")[0] != "F"})
    xs = sorted(seed_pos(n, x, T) for n, x in Fs)
    got = [round(float(b - a), 2) for a, b in zip(xs, xs[1:])]
    return got, [round(w, 2) for w in want], others, len(Fs)
