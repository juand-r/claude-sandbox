"""Class (mod V) of a single-remnant debris relative to the standard remnant.
Find a lab translation (dt, dx) mapping the plain N-read debris window onto
the candidate's debris window (static Ebar-frame objects: compare the
candidate at time T with the plain scene at time T - dt shifted by dx).
Reduce (dt, dx) modulo V = <(12,8),(30,-8)>: canonical form via the
invariants  u = dt mod 6 ... computed by brute force over representatives.
Returns the translation found (or None)."""
import numpy as np
import zscreen
from zscreen import *

def debris_translation(S, tape, seg, K0, ref_tape="NNYY", dts=range(0, 30), dxs=range(-80, 81)):
    T = zscreen.T
    sc = S[tape][1]; scr = S[ref_tape][1]; K0r = S[ref_tape][0]
    lo, hi = K0 + zscreen.WLO + 100, K0 + zscreen.SPLIT - 10
    W = unpack(step_packed_n(pack(seg), T), len(seg))
    i0 = sc.ebar_to_seg(lo, zscreen.TIN + T)
    Wc = W[i0:i0 + (hi - lo)]
    base = unpack(step_packed_n(pack(scr.seg), T - max(dts)), len(scr.seg))
    cur = pack(base)
    for dt in sorted(dts, reverse=True):
        Wr = unpack(cur, len(scr.seg))
        i = scr.ebar_to_seg(K0r + zscreen.WLO + 100, zscreen.TIN + T)
        for dx in dxs:
            j = i - dx
            if np.array_equal(Wc, Wr[j:j + (hi - lo)]):
                return (dt, dx)
        cur = step_packed_n(cur, 1)
    return None

def mod_V(dt, dx):
    """Canonical representative of (dt, dx) modulo V = <(12,8),(30,-8)>."""
    best = None
    for a in range(-6, 7):
        for b in range(-6, 7):
            t, x = dt + 12 * a + 30 * b, dx + 8 * a - 8 * b
            if 0 <= t < 30:
                key = (t, x % 56 if True else x)
                # (0,56) = 5*(12,8) - 2*(30,-8) is in V
                if best is None or key < best:
                    best = key
    return best
