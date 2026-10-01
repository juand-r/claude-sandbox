"""R1 -> R2 coupling seen from R2's front: E^m (built from E at e0 by m-1
B's) hit from the right by a Bbar (3 classes, Bbar moved by j*(1,-4)...
we scan Bbar time offsets). Report products and the FRONT displacement of
the resulting E^k (disp.py: relative to E^k built from e0 by B's)."""
from lsl import run, snap, nval, names
from disp import disp, cls

e0 = (0, 0)


def scene(m, tb, xb_min, bgap=40):
    pl = [("E",) + e0]
    x = e0[1] + 30
    for i in range(m - 1):
        x = snap(pl, "B", 0, x)
        pl.append(("B", 0, x))
        x += bgap
    x = snap(pl, "Bbar", tb, max(x, xb_min))
    pl.append(("Bbar", tb, x))
    return pl


if __name__ == "__main__":
    for m in range(1, 7):
        seen = {}
        for tb in range(0, 12):
            for dx in range(0, 14 * 3, 2):
                pl = scene(m, tb, 200 + 40 * m + dx)
                ok, out = run(pl, 2500 + 200 * m)
                Es = [p for p in out if nval(p[0])]
                key = tuple(names(out))
                if ok and len(Es) == 1:
                    k = nval(Es[0][0])
                    d = disp(e0, k, Es[0][1:])
                    key = key + (("disp", d, cls(d)),)
                seen.setdefault(key, 0)
                seen[key] += 1
        print("m =", m)
        for k, c in sorted(seen.items(), key=lambda kv: -kv[1]):
            print("   ", c, k)
