"""M1 end to end: a fresh E (value 0), a rigid stream [GB5]*v then the
gadget [GB3 test][G]. The gadget's geometry is anchored to the right ether
(build_right), so it is identical for every v; only the counter set-up
differs. Expected (from m1_scan): v=0 -> E^3 only; v=1 -> E + A^4;
v>=2 -> E^(v-1) + A^3.
Control: the same with the G shifted by (7,0) (changes the A x G class):
v = 0 must NOT give E^3 alone."""
import sys
import vlib, libgen
libgen.load()
SP = 70          # spacing of the GB5 prefix (cells)
T = 12000

def scene(v, gshift=(0, 0)):
    # right-anchored: G, GB3 at fixed places; GB5's to their left
    items = [("E", 0, 0)]
    x = 60
    for i in range(v):
        items.append(("GB5", 0, x)); x += SP
    items.append(("GB3", 1, x + 30))
    items.append(("G", 36 + gshift[0], x + 84 + gshift[1]))
    return items

def run(v, gshift=(0, 0)):
    items = scene(v, gshift)
    row, org, placed = vlib.build_right(items, T=T)
    r = vlib.evolve(row, T)
    ids = [n.split("@")[0] for n, x, w, k in vlib.identify(r, org, T=T)]
    rel = (placed[-1][1] - placed[-2][1], placed[-1][2] - placed[-2][2])
    return ids, rel

ok = True
for gshift in ((0, 0), (7, 0)):
    print("G shift", gshift)
    for v in range(0, 7):
        ids, rel = run(v, gshift)
        exp = ["E^3"] if v == 0 else (None if v == 1 else
                                      [("E" if v == 2 else f"E^{v-1}"), "A^3"])
        good = (exp is None) or ids == exp
        print(f"  v={v}: {ids}  G-GB3 offset {rel}  {'as predicted' if good else 'DIFFERENT'}")
        if gshift == (0, 0):
            ok &= good
        elif v == 0:
            ok &= not good      # control must fail
print("M1 program check:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
