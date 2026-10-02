"""Wall chemistry inside the E-bg: phonon (+2/5) x cut (-4/15, co-moving)
collisions. Does a phonon reflect off a cut into a left-moving (-3/5) wall?

Both kinds come from walls_ebg.jsonl (smallest W per phase kind g). A wall
record (g, row0, a0) is a configuration bg(0) | row0 | bg(g) at t = 0 in bg
coordinates. To put wall 2 behind wall 1 (whose right domain is g1), wall 2
is translated by g1: its scene is evolved t1 steps and shifted by s1, so its
left domain becomes bg(g1). Every (phonon, cut) pair has ONE collision class:
det((5,2),(15,-4)) = -50 and the bg lattice has index 50.
Outcome: domain map (10-cell windows -> bg phase) at times T and T+30;
walls = boundaries; velocity from their displacement.
Usage: python3 wallchem.py T out.jsonl"""
import json
import sys
import numpy as np
import cone
import objlib as O

BG = cone.Background(O.EBG)
T, OUT = int(sys.argv[1]), sys.argv[2]


def best(v):
    recs = {}
    for l in open("walls_ebg.jsonl"):
        r = json.loads(l)
        if r["found"] and abs(r["v"] - v) < 1e-9:
            g = tuple(r["g"])
            if g not in recs or r["W"] < recs[g]["W"]:
                recs[g] = r
    return recs


def wall_scene(rec, lo, hi, tt, ss):
    """cells [lo, hi) of (bg0 | row0 | bg_g) evolved tt steps, shifted by ss."""
    row0 = np.array([int(c) for c in rec["row0"]], np.uint8)
    a0 = rec["a0"]
    tg, sg = rec["g"]
    pad = tt + 2
    L0, H0 = lo - ss - pad, hi - ss + pad
    full = np.array([BG.bit(0, x) if x < a0 else
                     (row0[x - a0] if x < a0 + len(row0) else BG.bit(tg, x - sg))
                     for x in range(L0, H0)], np.uint8)
    r = O.evolve(full, tt)                     # covers [L0 + tt, H0 - tt)
    out = r[(lo - ss) - (L0 + tt):(hi - ss) - (L0 + tt)]
    assert len(out) == hi - lo
    return out


def compose(g1, g2):
    """phase of bg(g1) translated by g2: (t1+t2, s1+s2) reduced"""
    t = g1[0] + g2[0]
    s = g1[1] + g2[1]
    q, t = divmod(t, BG.tper)
    s = (s + q * BG.shift) % BG.p
    return (t, s)


def phase_map(a, xa, t, step=2):
    out = []
    for i in range(0, len(a) - 10, step):
        w = a[i:i + 10]
        hit = None
        for tt in range(BG.tper):
            rr = BG.row_at(t + tt)
            for s in range(BG.p):
                if all(w[j] == rr[(xa + i + j - s) % BG.p] for j in range(10)):
                    hit = (tt, s)
                    break
            if hit:
                break
        out.append((xa + i, hit))
    return out


def walls_of(pm):
    """boundaries: (x, left phase, right phase) between consecutive known windows"""
    res = []
    prev = None
    for x, h in pm:
        if h is None:
            continue
        if prev is not None and h != prev[1]:
            res.append((prev[0], x, prev[1], h))
        prev = (x, h)
    return res


if __name__ == "__main__":
    ph = best(0.4)
    cuts = best(-4 / 15)
    W = 2 * T + 600
    lo, hi = -W // 2, W // 2
    for gp, rp in sorted(ph.items()):
        for gc, rc in sorted(cuts.items()):
            # phonon near x = -60, cut at x ~ +60 (behind it in phase gp)
            # translate the cut by gp (time gp[0], shift gp[1]) and by +120
            # cells (a whole number of periods keeps the phase)
            cut_shift = 120 + gp[1]
            row = np.empty(hi - lo, np.uint8)
            mid = 0
            A = wall_scene(rp, lo, mid, 0, -60)
            B = wall_scene(rc, mid, hi, gp[0], cut_shift)
            row[:mid - lo] = A
            row[mid - lo:] = B
            # consistency at the junction: A's right domain == B's left domain
            ok_j = all(A[-1 - i] == BG.bit(gp[0], (mid - 1 - i) - gp[1]) for i in range(10))
            a1 = O.evolve(row, T)
            a2 = O.evolve(a1, 60)
            w1 = walls_of(phase_map(a1, lo + T, T))
            w2 = walls_of(phase_map(a2, lo + T + 60, T + 60))
            rec = {"phonon": list(gp), "cut": list(gc), "junction_ok": ok_j,
                   "walls_T": [(x1, x2, list(l), list(r)) for x1, x2, l, r in w1],
                   "walls_T60": [(x1, x2, list(l), list(r)) for x1, x2, l, r in w2]}
            print(json.dumps(rec), flush=True)
            with open(OUT, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
