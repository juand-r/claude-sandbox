"""Validate hrun.HRun (hashlife) against the packed exact engine, cell for cell.

Scenes: random left-to-right placements of library gliders (A-family left
stream, E^n counters, G-family right stream, assorted others), so collisions
happen. For each scene, compare the hashlife row with the engine row on the
part of the engine's cyclic tape that the wrap seam cannot reach, at several
times. Controls that must fail: (1) hashlife at T+1 vs engine at T;
(2) a scene with one flipped cell vs the original."""
import time

import numpy as np

import hrun

vlib = hrun.vlib


def scene(rng, nleft=25, nright=15):
    items, x = [], 0
    for _ in range(nleft):
        items.append((rng.choice(["A", "A", "A^2", "A^3"]), int(rng.integers(0, 3)), x))
        x += int(rng.integers(12, 40))
    for nm in rng.choice(["E^3", "E^6", "E^9", "C2", "Ebar", "E"], 2):
        x += int(rng.integers(20, 60))
        items.append((str(nm), int(rng.integers(0, 15)), x))
        x += 80
    for _ in range(nright):
        x += int(rng.integers(30, 90))
        items.append((str(rng.choice(["G", "GB1", "GB3", "GB5", "B", "Bbar"])),
                      int(rng.integers(0, 42)), x))
    return items


def compare(row, org, T, hr):
    eng = vlib.evolve(row, T)
    lo, hi = org + T + 20, org + len(row) - T - 20     # unreachable by the seam
    hr.goto(T)
    return eng[lo - org:hi - org], hr.cells(lo, hi)


def main():
    rng = np.random.default_rng(7)
    n_ok = 0
    for s in range(6):
        Tmax = 2500
        while True:          # random placements may overlap: redraw
            items = scene(rng)
            try:
                row, org, _ = vlib.build(items, T=Tmax)
                break
            except ValueError:
                continue
        hr = hrun.HRun(row, org)
        for T in (1, 17, 500, 1333, Tmax):
            a, b = compare(row, org, T, hr)
            assert np.array_equal(a, b), (s, T, np.nonzero(a != b)[0][:10])
            n_ok += 1
        # control 1: wrong time
        a, _ = compare(row, org, Tmax - 1, hrun.HRun(row, org))
        hr2 = hrun.HRun(row, org)
        hr2.goto(Tmax)
        lo = org + Tmax + 20
        assert not np.array_equal(a, hr2.cells(lo, lo + len(a))), "control 1 passed?!"
        # control 2: one flipped cell inside the scene (at a defect) must change the result
        d = vlib.defects(row)[len(vlib.defects(row)) // 2]
        row3 = row.copy()
        row3[d["lo"] + 1] ^= 1
        a, b = compare(row3, org, Tmax, hrun.HRun(row, org))
        assert not np.array_equal(a, b), "control 2 passed?!"
        print(f"scene {s}: {len(items)} gliders, {len(row)} cells, 5 times equal; controls differ")
    # speed: a long run
    rng = np.random.default_rng(3)
    while True:              # rejection sampling of non-overlapping placements
        items = scene(rng, 200, 100)
        try:
            row, org, _ = vlib.build(items, pad=200)
            break
        except ValueError:
            continue
    t0 = time.time()
    hr = hrun.HRun(row, org)
    hr.goto(200_000)
    print(f"hashlife: {len(items)} gliders, 200k steps in {time.time() - t0:.1f}s, {hrun.stats()}")
    print(f"test_hrun ok ({n_ok} comparisons)")


if __name__ == "__main__":
    main()
