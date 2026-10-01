"""Validate streamwin.StreamWindow against full exact runs (engine.py on a
cyclic tape with pad >= 2T), cell for cell on the whole span the scene can
influence, at several times.  Controls that must fail: (1) a wrong period
vector is rejected; (2) a window built from a DIFFERENT left stream than the
one in the reference run disagrees with it."""
import sys
import numpy as np
import v3, vlib, engine
from streamwin import StreamWindow, auto_cuts

T = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
LEFT = [("A", 0, -1500), ("A^2", 1, -1100), ("A", 2, -700), ("A^3", 0, -300), ("A", 1, -120)]
CORE = [("E^5", 0, 0)]
RIGHT = [("GB3", 0, 140), ("GB5", 5, 420), ("G", 11, 700), ("GB4", 3, 1000), ("GB1", 0, 1400)]


def scene(left):
    items = left + CORE + RIGHT
    row, org, placed = vlib.build_right(items, c_right=0, T=T)
    ex = [p for p in placed if p[0] == "E^5"][0][2]
    return row, org, ex


def full(row, org, times):
    out = {}
    w = engine.pack(row)
    t = 0
    for tt in times:
        w = engine.step_packed_n(w, tt - t)
        t = tt
        out[tt] = engine.unpack(w, len(row))
    return out


def compare(row, org, ex, times, sw_row=None, label=""):
    ref = full(row, org, times)
    src = row if sw_row is None else sw_row
    xa, xb = auto_cuts(row, org, len(LEFT), len(RIGHT))
    sw = StreamWindow(src, org, xa, xb, (3, 2), (42, -14))
    ok = True
    for tt in times:
        sw.run(tt)
        lo, hi = org + T + 50, org + len(row) - T - 50      # seam-free span
        a = ref[tt][lo - org:hi - org]
        b = sw.cells(lo, hi)
        same = np.array_equal(a, b)
        ok &= same
        objs = [n for n, x, w, k in vlib.identify(ref[tt], org, T=tt)]
        print(f"{label} t={tt}: equal={same}  window=[{sw.lo},{sw.hi}) width={sw.hi - sw.lo} "
              f"max={sw.max_width}  objects={[v3.base(n) for n in objs]}")
    return ok


if __name__ == "__main__":
    row, org, ex = scene(LEFT)
    times = [500, 2000, 4000, T]
    assert compare(row, org, ex, times, label="main"), "MISMATCH"
    # control 1: wrong period vector must be rejected
    try:
        StreamWindow(row, org, *auto_cuts(row, org, len(LEFT), len(RIGHT)), (3, 4), (42, -14))
        raise AssertionError("control 1 did not fail")
    except ValueError as e:
        print("control 1 (wrong period) rejected:", e)
    # control 2: window seeded with a different left stream -> must disagree
    alt = list(LEFT)
    alt[2] = ("A", 2, -728)
    row2, org2, ex2 = scene(alt)
    assert org2 == org and ex2 == ex and len(row2) == len(row)
    ok2 = compare(row, org, ex, times[-2:], sw_row=row2, label="control2")
    assert not ok2, "control 2 did not fail"
    print("control 2 (different left stream) disagrees, as required")
    print("ALL OK")
