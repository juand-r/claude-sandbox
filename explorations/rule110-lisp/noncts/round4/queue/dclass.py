"""Per-object debris classes. After a read, the left part of a scene holds
static Ebar-frame objects (remnant, moving data, markers). For each object
of the candidate, find a reference object and a lab spacetime translation
(dt, dx) with candidate(T) = reference(T - dt) shifted by dx on a window
around the object; report its class modulo V = <(12,8),(30,-8)>
(rclass.mod_V; (0,0) = harmless: C-crossing class and ossifier class
both standard)."""
import numpy as np
from lscene import *
from census import clusters
from rclass import mod_V

def lab_rows(sc, seg, T, depth):
    """rows[d] = lab cells at time t_in + T - d (d = 0..depth)."""
    w = pack(seg); w = step_packed_n(w, T - depth)
    rows = []
    for _ in range(depth + 1):
        rows.append(unpack(w, len(seg))); w = step_packed_n(w, 1)
    return rows[::-1]

def objects(sc, K0, seg_T, lo, hi, t_abs):
    """Clusters (array coords) of the Ebar-frame interval [K0+lo, K0+hi)."""
    a = sc.ebar_to_seg(K0 + lo, t_abs)
    return [(x + a, y + a) for x, y in clusters(seg_T[a:a + hi - lo])]

def debris_classes(sc, K0, cand, ref, T, lo=-380, hi=100, pad=14):
    t_abs = sc.t_in + T
    C = lab_rows(sc, cand, T, 0)[0]
    R = lab_rows(sc, ref, T, 29)            # R[d] = time T - d
    oc = objects(sc, K0, C, lo, hi, t_abs)
    orf = objects(sc, K0, R[0], lo, hi, t_abs)
    out = []
    for (x, y) in oc:
        win = C[x - pad:y + pad]
        hit = None
        for (u, v) in orf:
            for dt in range(30):
                Rd = R[dt]
                for dx in range(-70, 71):
                    # reference object near u at time T-dt, shifted by dx
                    s = x - pad - dx
                    if s < 0 or s + len(win) > len(Rd): continue
                    if abs((x - dx) - u) > 12: continue
                    if np.array_equal(win, Rd[s:s + len(win)]):
                        hit = (u - sc.ebar_to_seg(K0, t_abs), dt, dx, mod_V(dt, dx)); break
                if hit: break
            if hit: break
        out.append((x - sc.ebar_to_seg(K0, t_abs), hit))
    return out, [u - sc.ebar_to_seg(K0, t_abs) for u, v in orf]
