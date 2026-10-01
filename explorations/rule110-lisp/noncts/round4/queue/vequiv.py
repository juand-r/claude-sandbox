"""V-equivalence of the debris left by a modified read (rej path scenes of
zscreen): is the left part [K0+WLO, K0+SPLIT) at t_in + T, in the LAB frame,
equal to the plain N-read's left part translated by a*(12,8) + k*(0,56)
(a = 0..4, |k| <= 3)? V = <(12,8),(30,-8)> preserves the classes of a
static Ebar-frame object against tape C's (<(7,0),(30,-8)>) and against
ossifier A4's (<(3,2),(30,-8)>).
Positive control: the plain N-read vs itself (a=0,k=0); a V-translated copy
of the plain debris (a=1) must be recognised; a 2-cell shift must not."""
import numpy as np
import zscreen
from zscreen import *

def lab_window(sc, seg, t, xlo, xhi):
    """Lab-frame cells at time t_in + t over lab columns that coincide with
    Ebar-frame columns [xlo, xhi) at time t_in + T (fixed lab range)."""
    w = unpack(step_packed_n(pack(seg), t), len(seg))
    i = sc.ebar_to_seg(xlo, zscreen.TIN + zscreen.T)
    return w[i:i + (xhi - xlo)]

def vclass(S, tape, seg, K0, ref_tape="NNYY"):
    """Return (a, k) such that the left part equals the plain ref_tape left
    part translated by a*(12,8)+k*(0,56), or None."""
    T = zscreen.T
    sc = S[tape][1]; scr = S[ref_tape][1]; K0r = S[ref_tape][0]
    lo, hi = K0 + zscreen.WLO + 60, K0 + zscreen.SPLIT       # stay clear of edges
    lor, hir = K0r + zscreen.WLO + 60, K0r + zscreen.SPLIT
    W = lab_window(sc, seg, T, lo, hi)
    for a in range(5):
        Wr = unpack(step_packed_n(pack(scr.seg), T - 12 * a), len(scr.seg))
        for k in range(-3, 4):
            d = 8 * a + 56 * k
            i = scr.ebar_to_seg(lor, zscreen.TIN + T) - d
            if i < 0 or i + (hi - lo) > len(Wr):
                continue
            if np.array_equal(W, Wr[i:i + (hi - lo)]):
                return (a, k)
    return None
