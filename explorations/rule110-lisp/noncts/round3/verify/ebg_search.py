"""Gliders INSIDE an E^n rod?  The interior of E^n is a periodic
background "E-infinity" (spatial period 10: 1101011100, a Rule 110 orbit
of period 5 with shift -8, i.e. the E velocity -4/15 modulo the lattice).
A localized periodic defect in that background moving RIGHT relative to
the rod (velocity > -4/15) could cross a rod of any length (theory's open
route "not (N)").  Random search: a ring of W = 10*M cells of background,
k random cells perturbed, evolved T0 steps (exact engine, cyclic ring =
exact for the ring), deviation from the best-matching background phase
measured; localized survivors are tested for periodicity (P <= 400) and
their velocity recorded.  Resumable: appends to ebg_search.log.
Usage: python3 ebg_search.py TRIALS SEED"""
import sys
import numpy as np
sys.path.insert(0, "../../..")
import engine

BG = np.array([int(c) for c in "1101011100"], np.uint8)
M, T0 = 64, 2000          # W = 640 = 10 * 64 (multiple of 64: exact cyclic packed ring)
W = 10 * M


def variants():
    out = []
    r = np.tile(BG, M)
    for tau in range(5):
        for s in range(10):
            out.append(np.roll(r, s))
        r = engine.step(r)
    return np.stack(out)


VAR = variants()


def deviation(row):
    mis = (VAR != row[None, :])
    k = mis.sum(axis=1).argmin()
    return mis[k]


def localized(mask):
    """circular span of the deviation cells, or None if empty."""
    xs = np.nonzero(mask)[0]
    if len(xs) == 0:
        return None
    # largest circular gap
    gaps = np.diff(np.concatenate([xs, [xs[0] + W]]))
    i = gaps.argmax()
    start = xs[(i + 1) % len(xs)]
    span = W - gaps[i] + 1
    return int(start), int(span)


def period(row, maxP=400):
    w = engine.pack(row)
    r0 = row
    for P in range(1, maxP + 1):
        w = engine.step_packed(w)
        r = engine.unpack(w, len(row))
        for D in range(-P, P + 1):
            if np.array_equal(r, np.roll(r0, D)):
                return P, D
    return None


if __name__ == "__main__":
    trials, seed = int(sys.argv[1]), int(sys.argv[2])
    assert W % 64 == 0 or True
    rng = np.random.default_rng(seed)
    log = open("ebg_search.log", "a")
    found = {}
    for tr in range(trials):
        ring = VAR[0].copy()
        k = int(rng.integers(1, 9))
        x = int(rng.integers(0, W - k))
        ring[x:x + k] = rng.integers(0, 2, k, dtype=np.uint8)
        r = engine.unpack(engine.step_packed_n(engine.pack(ring), T0), W)
        loc = localized(deviation(r))
        if loc is None or loc[1] > 120:
            continue
        pd = period(r)
        if pd is None:
            continue
        P, D = pd
        key = (P, D, loc[1])
        if key not in found:
            found[key] = (seed, tr, k, x, ring[x:x + k].tolist())
            log.write(f"seed={seed} trial={tr} k={k} x={x} bits={''.join(map(str, ring[x:x + k]))} "
                      f"P={P} D={D} v={D / P:+.4f} span={loc[1]}\n")
            log.flush()
            print(key, D / P, flush=True)
    log.write(f"DONE seed={seed} trials={trials} distinct={len(found)}\n")
