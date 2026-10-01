"""rodval.py - value of an E-family rod of any length, by my own measurement.

A rod E^k is one defect, invariant under (15,-4). Its value k is pinned by
two independent measurements:
  charge  w = 9 + 6 (k - 1) mod 14  ->  k mod 7  (checked on my library k = 1..15)
  length  mean core span over 15 steps ~ a + b k  (fit on my library k = 1..15)
k = the unique integer with the right residue mod 7 within 3.5 of the length
estimate (raises if the length residual is > 1.5, i.e. not a clean rod)."""
import numpy as np
import hrun

vlib = hrun.vlib


def _span_charge(row, org, T0=0):
    """(mean defect span over steps T0..T0+14, charge, (15,-4)-periodic?)
    for a row holding a single defect; None otherwise."""
    h = hrun.HRun(row, org)
    h.goto(T0)
    lo, hi = org - T0 - 400, org + len(row) + T0 + 400     # whole light cone: escapes count
    spans = []
    for s in range(16):
        r = h.cells(lo, hi)
        ds = vlib.defects(r)
        if len(ds) != 1:
            return None
        if s == 0:
            r0, w = r, ds[0]["w"]
        if s < 15:
            spans.append(ds[0]["hi"] - ds[0]["lo"])
            h.goto(h.t + 1)
    per = np.array_equal(r[:-4], r0[4:])      # row(T0+15)[x] = row(T0)[x+4]
    return float(np.mean(spans)), w, per


def _fit():
    ks, sp = [], []
    for k in range(1, 16):
        nm = "E" if k == 1 else f"E^{k}"
        row, org, _ = vlib.build([(nm, 0, 0)], pad=300)
        s, w, per = _span_charge(row, org)
        assert per and w == (9 + 6 * (k - 1)) % 14, (k, w, per)
        ks.append(k); sp.append(s)
    b, a = np.polyfit(ks, sp, 1)
    res = np.array(sp) - (a + b * np.array(ks))
    return a, b, float(np.abs(res).max())


A, B, RES = _fit()
_RES7 = {(9 + 6 * (k - 1)) % 14: k % 7 for k in range(1, 8)}


def value(row, org, T0=0):
    """k if the row at time T0 holds exactly one clean rod E^k, else None."""
    sc = _span_charge(row, org, T0)
    if sc is None:
        return None
    s, w, per = sc
    if not per or w not in _RES7:
        return None
    kest = (s - A) / B
    cands = [k for k in range(max(1, int(kest) - 4), int(kest) + 5)
             if k % 7 == _RES7[w] and abs(k - kest) < 3.5]
    if len(cands) != 1 or abs(cands[0] - kest) * B > RES + 1.5 * B:
        return None
    return cands[0]


if __name__ == "__main__":
    print(f"fit span = {A:.2f} + {B:.3f} k, max residual {RES:.2f} cells")
    import sys
    sys.path.insert(0, hrun.R3V)
    import longrod
    for n in (15, 18, 30, 45, 60):
        r, org = longrod.rod(n)
        print(n, "->", value(r, org))
    # control: two rods side by side are not one rod
    row, org, _ = vlib.build([("E^3", 0, 0), ("E^4", 0, 300)], pad=300)
    print("two rods ->", value(row, org))
