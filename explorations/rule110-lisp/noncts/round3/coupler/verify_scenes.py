"""T2 milestone scenes, glider level (collider glidersim) AND exact Rule 110
(gate's fastca moving window, margins checked every step), with controls.

Scene A, "R1 zero -> R2": R1 = E(0,0) + v1 GB5's (round-2 canonical
  prefix), R1 program J I N N (rafast text, classes 1,0,0,0, x-shifted by
  rafast.shift_for for ether compatibility). R2 = E at a fixed seed left of
  R1 (gap ~1500, seed time R2T0) raised to v2 by leftstream's I_L trains
  (rigid left stream, leftstream's bookkeeping rule), arriving long before
  the Bbar. Expected: v1 = 0: (R1, R2) -> (0, v2 + 2); v1 > 0: (v1 + 2, v2).
  Known exception (physics, catalog): v2 = 1 (E^2 + Bbar is garbage in
  every class); v2 = 0 needs another class (verify 05:4x) - reported.
Scene B, "R2 zero -> R1": R1 = E(0,0) + v1 GB5's; R2 = E at a fixed seed
  (seed time R2T0B), left stream I_L^v2 then Z_L (leftstream), arriving
  after R1 holds v1. Expected: v2 = 0: (v1 - 1, 0) (Z_L's answer A DECs
  R1); v2 > 0: (v1, v2 - 1). Needs v1 >= 1.
Controls: R2's seed time moved to the other two classes (expected to fail
  for the class-sensitive cases).
Usage: python verify_scenes.py [A|B|all] [--noca]
"""
import sys
from two import *  # noqa

GAP_A, R2T0 = 1500, 2
K3 = "GB1@(0,0)+GB3@(-18,30)"     # zero crossing: E + K3 #0 -> E + B^3 (left)
ALIAS["T"] = K3                     # op letter T for rafast.Program
GAP_C = 1500
GAP_B, R2T0B = 1200, 0


def outcome(state):
    """-> (R2 value, R1 value) if exactly two E-chain objects and nothing
    else, else None."""
    if len(state) != 2 or any(g[0] not in CHAIN for g in state):
        return None
    a, b = sorted(state, key=lambda g: pos(g, 0))
    return CHAIN.index(a[0]), CHAIN.index(b[0])


def scene_A(v1, v2, r2t0=R2T0):
    items = r1_program("JINN", [1, 0, 0, 0])
    sc = r1_scene(v1, items)
    r2 = ("E",) + place_left_of(sc, "E", -GAP_A, r2t0)
    ls = left_stream("i" * v2, r2[1:], t0=400)
    T = 15 * (sc[-1][2] + 3000)
    return ls + [r2] + sc, T


def expect_A(v1, v2):
    return (v2 + 2, 0) if v1 == 0 else (v2, v1 + 2)


def scene_B(v1, v2, r2t0=R2T0B, vmax=5):
    pre = input_prefix(v1)
    r2 = ("E",) + place_left_of(pre, "E", -GAP_B, r2t0)
    t0 = 7000 * vmax + 2000
    ls = left_stream("i" * v2 + "z", r2[1:], t0=t0)
    T = t0 + 150 * (v2 + 1) + 6000
    return ls + [r2] + pre, T


def expect_B(v1, v2):
    return (0, v1 - 1) if v2 == 0 else (v2 - 1, v1)


def scene_C(v1, v2, prog="TNN", classes=(0, 0, 0), r2t0=0):
    """R1 program starting with K3 (= T): R1 = 0 -> R2 += 3 via a B^3 that
    is class-free at R2's back; R1 > 0 -> R1 += 3. R2 = E raised by I_L's."""
    items = r1_program(prog, list(classes))
    sc = r1_scene(v1, items)
    r2 = ("E",) + place_left_of(sc, "E", -GAP_C, r2t0)
    ls = left_stream("i" * v2, r2[1:], t0=400)
    T = 15 * (sc[-1][2] + 3000)
    return ls + [r2] + sc, T


def expect_C(v1, v2):
    return (v2 + 3, 0) if v1 == 0 else (v2, v1 + 3)


def check(scene, T, exp, do_ca=True):
    sim, err = run(scene, T)
    got = outcome(sim.state()) if err is None else None
    res = {"glider": got, "glider_ok": got == exp}
    if do_ca:
        ok, prods = ca(scene, T)
        cag = outcome(prods)
        res["ca"] = cag
        res["ca_ok"] = cag == exp
        res["ca_eq_glider"] = (err is None and sorted(prods) == sorted(sim.state()))
        res["ca_products"] = [p[0] for p in prods]
    return res


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    do_ca = "--noca" not in sys.argv
    fails = 0
    if which in ("A", "all"):
        print("Scene A: R1 zero -> R2 (+2)")
        for v1 in (0, 1, 2):
            for v2 in (0, 1, 2, 3, 4, 5):
                sc, T = scene_A(v1, v2)
                r = check(sc, T, expect_A(v1, v2), do_ca)
                tag = "" if v2 > 1 or v1 > 0 else "  (documented exception)"
                print(f"  v1={v1} v2={v2} exp={expect_A(v1, v2)} {r}{tag}", flush=True)
                if v2 > 1 or v1 > 0:
                    fails += not (r["glider_ok"] and r.get("ca_ok", True))
        print("Scene A controls (R2 seed time moved to the other classes):")
        for r2t0 in (0, 1):
            for v2 in (2, 3, 4):
                sc, T = scene_A(0, v2, r2t0)
                r = check(sc, T, expect_A(0, v2), do_ca)
                print(f"  R2T0={r2t0} v1=0 v2={v2} {r}", flush=True)
    if which in ("B", "all"):
        print("Scene B: R2 zero -> R1 (-1)")
        for v1 in (1, 2, 3, 4, 5):
            for v2 in (0, 1, 2):
                sc, T = scene_B(v1, v2)
                r = check(sc, T, expect_B(v1, v2), do_ca)
                print(f"  v1={v1} v2={v2} exp={expect_B(v1, v2)} {r}", flush=True)
                fails += not (r["glider_ok"] and r.get("ca_ok", True))
        print("Scene B controls (R2 seed time moved to the other classes):")
        for r2t0 in (1, 2):
            for v1 in (2, 3, 4):
                sc, T = scene_B(v1, 0, r2t0)
                r = check(sc, T, expect_B(v1, 0), do_ca)
                print(f"  R2T0={r2t0} v1={v1} v2=0 {r}", flush=True)
    if which in ("C", "all"):
        print("Scene C: R1 zero -> R2 += 3 via K3's B^3 (class-free at R2)")
        for v1 in (0, 1, 2, 3):
            for v2 in (0, 1, 2, 3, 4, 5, 6):
                sc, T = scene_C(v1, v2)
                r = check(sc, T, expect_C(v1, v2), do_ca)
                print(f"  v1={v1} v2={v2} exp={expect_C(v1, v2)} {r}", flush=True)
                fails += not (r["glider_ok"] and r.get("ca_ok", True))
        print("Scene C, R2 at all three seed times (B^3 has ONE class at R2):")
        for r2t0 in (1, 2):
            for v2 in (0, 1, 3):
                sc, T = scene_C(0, v2, r2t0=r2t0)
                r = check(sc, T, expect_C(0, v2), do_ca)
                print(f"  R2T0={r2t0} v1=0 v2={v2} {r}", flush=True)
                fails += not (r["glider_ok"] and r.get("ca_ok", True))
        print("Scene C controls (K3 in the other two R1 classes, v1 = 0):")
        for c in (1, 2):
            for v2 in (0, 3):
                sc, T = scene_C(0, v2, classes=(c, 0, 0))
                r = check(sc, T, expect_C(0, v2), do_ca)
                print(f"  K3 class {c} v1=0 v2={v2} {r}", flush=True)
    print("FAILURES (non-exception, non-control):", fails)


if __name__ == "__main__":
    main()
