"""Check coupler's edge-invariance claim with my code: a DEC from the LEFT
(A, or Z_L's answer) leaves the counter's RIGHT end on its old trajectory;
a right-stream DEC (GB3) leaves the LEFT end.  Measure the right/left ends
(defect hi/lo at times T..T+29) of: R untouched vs R after the event."""
import sys
import numpy as np
import t1lib as L
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC
L.register_IL()


def ends(items, c0, T, n=30):
    row, org, placed = vlib.build(items, c0=c0, T=T + n)
    w = engine.pack(row)
    w = engine.step_packed_n(w, T)
    out = []
    for k in range(n):
        r = engine.unpack(w, len(row))
        cut = T + k + 16
        d = vlib.defects(r[cut:len(r) - cut])
        out.append((d[0]["lo"] + cut + org, d[-1]["hi"] + cut + org, len(d)))
        w = engine.step_packed(w)
    return out


def compare(a, b, label):
    dl = {x[0] - y[0] for x, y in zip(a, b)}
    dr = {x[1] - y[1] for x, y in zip(a, b)}
    print(f"{label}: left-end offsets {sorted(dl)}  right-end offsets {sorted(dr)}")


if __name__ == "__main__":
    T = 3000
    for n in (3, 4, 6):
        nm = f"E^{n}"
        # A from the left in its DEC class (scan 3 phases, keep the clean one)
        base = ends([(nm, 0, 0)], 0, T)
        for tp in range(3):
            items = [("A", tp, -300), (nm, 0, 0)]
            c0 = (0 - vlib.LIB["A"].w) % 14
            objs, *_ = v3.run(items, T, right=False, c=c0)
            if v3.names(objs) == [f"E^{n - 1}"]:
                compare(ends(items, c0, T), base, f"{nm} + A(left, t0={tp}) vs {nm}")
        # right-stream DEC GB3 (class-free)
        items = [(nm, 0, 0)] + AC.parts("D", 0, 200)
        objs, *_ = v3.run(items, T, right=False)
        assert v3.names(objs) == [f"E^{n - 1}"], objs
        compare(ends(items, 0, T), base, f"{nm} + GB3(right) vs {nm}")


def more(T=3000):
    for n in (3, 5):
        nm = f"E^{n}"
        base = ends([(nm, 0, 0)], 0, T)
        for tp in range(3):
            for dx in range(14):
                items = [("IL", tp, -300 - dx), (nm, 0, 0)]
                c0 = (0 - 6) % 14
                objs, *_ = v3.run(items, T, right=False, c=c0)
                if v3.names(objs) == [f"E^{n + 1}"]:
                    compare(ends(items, c0, T), base, f"{nm} + I_L(left) vs {nm}")
                    break
            else:
                continue
            break
        items = [(nm, 0, 0)] + AC.parts("I", 0, 200)
        objs, *_ = v3.run(items, T, right=False)
        assert v3.names(objs) == [f"E^{n + 1}"], objs
        compare(ends(items, 0, T), base, f"{nm} + GB5(right) vs {nm}")


more()
