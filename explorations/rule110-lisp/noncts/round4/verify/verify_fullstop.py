"""Check delayline 00:19 (fullstop): R1's own zero (K3 -> B^3 through R1 = E)
closes the walking left window W_L, end to end. Their scenes come as t = 0
object states (bits, lph, rph, start) in r110lib conventions (left ether at
y < start: ETHER[(lph + y - start) mod 14]; right ether: ETHER[(rph + y -
start) mod 14]). I assemble the row myself, run with hrun to their T, type
with my typer, and compare (a) product names, (b) every product's worldline
intercept: mine minus theirs must be one constant per product type over all
41 scenes (same coordinates), (c) the stated semantics: v1 = 0 clean scenes
end with E^4 + E, the 11.2 steps; v1 = 1, 2 controls: W_L walked 40 packets."""
import json
import sys
from fractions import Fraction

import numpy as np

import hrun

vlib = hrun.vlib
ETH = vlib.ETHER
VEL = {"E": Fraction(-4, 15), "E^4": Fraction(-4, 15), "E^5": Fraction(-4, 15), "E^6": Fraction(-4, 15),
       "Ebar": Fraction(-8, 30), "D1": Fraction(2, 10), "A": Fraction(2, 3)}
PER = {"E": 15, "E^4": 15, "E^5": 15, "E^6": 15, "Ebar": 30, "D1": 10, "A": 3}


def row_from_states(states, pad=400):
    st = sorted(states, key=lambda s: s[3])
    lo = st[0][3] - pad
    hi = st[-1][3] + len(st[-1][0]) + pad
    y = np.arange(lo, hi)
    row = np.empty(hi - lo, np.uint8)
    b0, l0, r0, s0 = st[0]
    row[:] = ETH[(l0 + y - s0) % 14]          # left ether of the first object
    for i, (b, l, r, s) in enumerate(st):
        if i > 0:
            pb, pl, pr, ps = st[i - 1]
            assert (pr - ps - (l - s)) % 14 == 0, "ether phases disagree"
        seg = np.array([int(c) for c in b], np.uint8)
        row[s - lo:s - lo + len(seg)] = seg
        nxt = st[i + 1][3] if i + 1 < len(st) else hi
        a = s + len(seg)
        row[a - lo:nxt - lo] = ETH[(r + y[a - lo:nxt - lo] - s) % 14]
    return row, lo


_ref = {}


def my_intercept(name, x, T):
    """intercept x(t=0) of the worldline of object name@s seen at x at time T,
    in the coordinates where the same object built by vlib at x0 = 0, t0 = 0
    has intercept 0 (my convention)."""
    base, P = name.split("@")[0], PER[name.split("@")[0]]
    v = VEL[base]
    for a in range(P):
        key = (base, T + a)
        if key not in _ref:
            row, org, _ = vlib.build([(base, 0, 0)], pad=300)
            h = hrun.HRun(row, org)
            h.goto(T + a)
            _ref[key] = h.objects(org - T - 400, org + len(row) + T + 400)
        objs = _ref[key]
        assert len(objs) == 1
        n, xa, _ = objs[0]
        if n == name:
            return Fraction(x - xa) + v * a      # alone(t+a) = mine(t) - shift: intercept shift
    raise AssertionError(name)


def main(path):
    scenes = json.load(open(path))
    offs = {}
    ok_names = 0
    for sc in scenes:
        st = sc["states"] if isinstance(sc["states"], list) else eval(sc["states"])
        row, org = row_from_states(st)
        T = sc["T"]
        h = hrun.HRun(row, org)
        h.goto(T)
        objs = h.objects(org - T - 400, org + len(row) + T + 400)
        mine = [n.split("@")[0] for n, x, w in objs]
        theirs = sorted(sc["products"], key=lambda p: p[1])
        same = sorted(mine) == sorted(p[0] for p in theirs)
        ok_names += same
        if same:
            # match by type in left-to-right order (intercept order = position order here)
            for (n, x, w), tp in zip(sorted(objs, key=lambda o: o[1]),
                                     sorted(theirs, key=lambda p: (p[1]))):
                pass
            bytype = {}
            for n, x, w in objs:
                bytype.setdefault(n.split("@")[0], []).append(my_intercept(n, x, T))
            for t, vals in bytype.items():
                th = sorted(p[1] for p in theirs if p[0] == t)
                for a, b in zip(sorted(vals), th):
                    offs.setdefault(t, set()).add(round(float(a) - b - sc["wl_ref"], 2))
        print(sc["v1"], sc["shift"], sc["k3class"], "mine:", mine, "theirs:", [p[0] for p in theirs],
              "OK" if same else "DIFF", flush=True)
    print(f"names equal in {ok_names}/{len(scenes)} scenes")
    print("intercept offsets (mine - theirs - wl_ref) per type:", {t: sorted(v) for t, v in offs.items()})


if __name__ == "__main__":
    main(sys.argv[1])
