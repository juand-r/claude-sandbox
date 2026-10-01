"""rawscene.py - assemble scenes from raw cell strings and run them exactly.

Format (shuttle's tables, theory 23:45): an object is (bits, pR): its cells
at time 0 with ether of phase 0 to the LEFT (cell i of the row right before
the object is ETHER[(i) mod 14] in the object's own coordinates, i < 0) and
ether of phase pR to the right (cell i >= len(bits) is ETHER[(i + pR) mod 14]).

assemble([(bits, pR, gap), ...]) places objects left to right, `gap` = the
number of ether cells before the object; the global phase constraint is
handled exactly (the object start x must satisfy (x + c) = 0 mod 14 for the
current left phase c, so the gap is rounded UP to the next valid value).
Returns (row, origin, starts). Nothing is assumed about the objects.

Ether convention (same as vlib / engine): at time 0 a region of phase c is
ETHER[(x + c) mod 14] at global x."""
import numpy as np

import hrun

vlib = hrun.vlib
ETHER = vlib.ETHER


def assemble(objs, pad=400, c0=0):
    pieces, c, x = [], c0, 0
    starts = []
    for bits, pR, gap in objs:
        x += gap
        while (x + c) % 14:
            x += 1
        seg = np.array([int(b) for b in bits], np.uint8)
        pieces.append((x, seg, c))
        starts.append(x)
        c = (pR - x) % 14
        x += len(seg)
    lo, hi = -pad, x + pad
    row = np.empty(hi - lo, np.uint8)
    xs = np.arange(lo, hi)
    # ether of each region, then objects
    bounds = [p[0] for p in pieces] + [hi]
    cl = c0
    prev = lo
    for (xs0, seg, cphase), nxt in zip(pieces, bounds[1:]):
        row[prev - lo:xs0 - lo] = ETHER[(xs[prev - lo:xs0 - lo] + cphase) % 14]
        row[xs0 - lo:xs0 - lo + len(seg)] = seg
        prev = xs0 + len(seg)
    row[prev - lo:] = ETHER[(xs[prev - lo:] + c) % 14]
    return row, lo, starts


def run(row, origin, T):
    h = hrun.HRun(row, origin)
    h.goto(T)
    return h


def selftest():
    # E^3 from my library, written as raw bits, must behave as E^3
    g = vlib.LIB["E^3"]
    ds = vlib.defects(g.base)
    a, b = min(d["lo"] for d in ds), max(d["hi"] for d in ds)
    a -= a % 14                      # base has left ether phase 0 at x = 0
    bits = "".join(map(str, g.base[a:b]))
    pR = (g.w - 0) % 14
    # right phase in the object's own coords: cells i >= len are ETHER[(i + a + w) mod 14]
    pR = (a + g.w) % 14
    row, org, st = assemble([(bits, pR, 50), (bits, pR, 300)])
    h = run(row, org, 150)
    objs = h.objects(org - 200, org + len(row) + 200)
    assert [n.split("@")[0] for n, x, w in objs] == ["E^3", "E^3"], objs
    # control that can fail: a wrong right phase must be detected as non-ether
    row2, org2, _ = assemble([(bits, (pR + 1) % 14, 50)])
    objs2 = run(row2, org2, 0).objects(org2, org2 + len(row2))
    assert [n.split("@")[0] for n, x, w in objs2] != ["E^3"], objs2
    print("rawscene selftest ok")


if __name__ == "__main__":
    selftest()
