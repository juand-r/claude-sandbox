"""Identify the objects in a simulated row: split by ether (census.clusters),
find each cluster's period vector among the library's, and name it by
matching its bits against every phase of every library glider (collider's
gliders.json), else report (p, d) and the bits. Diagnostic tool."""
import numpy as np
import r110sat  # noqa: F401  (puts the project root on sys.path)
from census import clusters
from lib import load_gliders

G = load_gliders()
PERIODS = sorted({(g.p, g.d) for g in G.values()} | {(7, 0)})


def period_of(h, t, a, b, margin=3):
    for p, d in sorted(PERIODS):
        if t + p >= len(h):
            continue
        lo, hi = a - margin, b + margin
        if np.array_equal(h[t + p, lo + d:hi + d], h[t, lo:hi]):
            return (p, d)
    return None


def rel_phase(row, x, s):
    """Relative ether phase (collider convention: cell y reads
    ETHER[(ph + y - s) % 14]) of the 14 cells starting at x, or None."""
    from r110sat import ETHER_BITS
    w = row[x:x + 14]
    for ph in range(14):
        if all(w[i] == ETHER_BITS[(ph + x + i - s) % 14] for i in range(14)):
            return ph
    return None


def name_of(bits, lph=None, rph=None):
    """Library name matching bits AND (if given) the relative ether phases
    on both sides; bit strings alone are ambiguous (e.g. '' or '0')."""
    s = "".join(map(str, bits))
    for g in G.values():
        for ph in g.phases:
            if ph[0] == s and (lph is None or (ph[1] == lph and ph[2] == rph)):
                return g.name
    return None


def describe(h, t, lo=0, hi=None, merge=6):
    """Objects in row t of history h (cells lo..hi): list of
    (start, end, (p,d) or None, name or None, bits, slip)."""
    hi = h.shape[1] if hi is None else hi
    cl = clusters(h[t, lo:hi])
    # merge clusters closer than `merge`
    out = []
    for a, b in cl:
        a += lo; b += lo
        if out and a - out[-1][1] < merge:
            out[-1][1] = b
        else:
            out.append([a, b])
    res = []
    for a, b in out:
        per = period_of(h, t, a, b)
        bits = h[t, a:b]
        lph = rel_phase(h[t], a - 14, a) if a >= 14 else None
        rph = rel_phase(h[t], b, a) if b + 14 <= h.shape[1] else None
        nm = name_of(bits, lph, rph) if lph is not None and rph is not None else None
        slip = (rph - lph) % 14 if lph is not None and rph is not None else None
        res.append((a, b, per, nm, "".join(map(str, bits)), slip))
    return res
