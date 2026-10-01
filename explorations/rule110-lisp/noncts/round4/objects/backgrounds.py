"""Enumerate spatially periodic Rule 110 backgrounds: all cyclic binary rows of
length p <= PMAX (primitive period exactly p), evolved on the ring until the
orbit cycles; keep the cycles (orbits of rows up to rotation), canonical
representative = lexicographically smallest rotation over the cycle.
Output: one line per background: p, temporal period (up to rotation), shift,
density, canonical tile."""
import sys
import numpy as np

def step(c):
    l = np.roll(c, 1); r = np.roll(c, -1)
    return ((c | r) & (1 - (l & c & r))).astype(np.uint8)

def canon(row):
    s = "".join(map(str, row))
    return min(s[i:] + s[:i] for i in range(len(s)))

def primitive(s):
    p = len(s)
    return all(s != s[d:] + s[:d] for d in range(1, p) if p % d == 0)

PMAX = int(sys.argv[1])
found = {}
for p in range(1, PMAX + 1):
    seen_canon = set()
    for code in range(1 << p):
        s = format(code, f"0{p}b")
        if not primitive(s):
            continue
        c0 = canon(np.array([int(ch) for ch in s], np.uint8))
        if c0 in seen_canon:
            continue
        # iterate to a cycle (in canonical form)
        r = np.array([int(ch) for ch in c0], np.uint8)
        hist = []
        idx = {}
        while True:
            k = canon(r)
            seen_canon.add(k)
            if k in idx:
                cyc = hist[idx[k]:]
                break
            idx[k] = len(hist)
            hist.append(k)
            r = step(r)
        key = min(cyc)
        if key not in found and primitive(key):
            # temporal period with shift
            r0 = np.array([int(ch) for ch in key], np.uint8)
            r = r0
            for t in range(1, 10 * p * len(cyc) + 2):
                r = step(r)
                hit = [sh for sh in range(p) if np.array_equal(np.roll(r0, sh), r)]
                if hit:
                    sh = hit[0] if hit[0] <= p // 2 else hit[0] - p
                    break
            found[key] = (p, t, sh, r0.mean())
for key, (p, t, sh, dens) in sorted(found.items(), key=lambda z: (z[1][0], z[0])):
    print(p, t, sh, round(dens, 3), key)
