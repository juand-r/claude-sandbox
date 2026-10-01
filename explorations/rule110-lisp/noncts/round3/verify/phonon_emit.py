"""Which front reactions launch a phonon?  For a left packet P hitting my
E^n (in the class that gives a clean result), compare the run at time
T - 15k with the final clean rod moved back along its own period
(15, -4): any difference inside the rod at intermediate times is a
transient; one that moves at +2/5 is a phonon."""
import sys
import numpy as np
import t1lib as L
import v3, vlib, engine
L.register_IL()

T = 1200


def first_clean(P, n, want):
    for t0 in range(3):
        for dx in range(14):
            items = [(P, t0, -60 - dx), (f"E^{n}", 0, 0)]
            objs, r, org, placed = v3.run(items, T)
            if v3.names(objs) == want:
                return items
    return None


def transients(items, ks=range(78, 4, -1)):
    row, org, placed = vlib.build_right(items, c_right=0, T=T)
    hist = {}
    w = engine.pack(row)
    t = 0
    times = sorted({T - 15 * k for k in ks} | {T})
    for tt in times:
        w = engine.step_packed_n(w, tt - t)
        t = tt
        hist[tt] = engine.unpack(w, len(row))
    fin = hist[T]
    out = []
    for k in ks:
        a = hist[T - 15 * k]
        b = np.roll(fin, 4 * k)
        cut = T + 50
        d = np.nonzero(a[cut:-cut] != b[cut:-cut])[0]
        out.append((T - 15 * k, (int(d.min()) + cut + org, int(d.max()) + cut + org) if len(d) else None))
    return out


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    for P, want in (("IL", [f"E^{n + 1}"]), ("A", [f"E^{n - 1}"]), ("ZL", [f"E^{n - 1}"])):
        items = first_clean(P, n, want)
        if items is None:
            print(P, "no clean class"); continue
        tr = transients(items)
        live = [(t, s) for t, s in tr if s]
        print(f"{P} + E^{n}: transient differences at times {[(t, s) for t, s in live][:12]} ...; last at {live[-1] if live else None}")
