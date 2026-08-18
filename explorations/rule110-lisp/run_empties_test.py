"""Controlled experiment: does the machinery die when the appendant list
contains empty appendants (L blocks)? Program YYYYNN alone is known good
at v_override=3x. Variants add 1 or 2 empty appendants."""
import sys
import numpy as np
from encoder import assemble, _left_v
from engine import ETHER, pack, unpack, step_packed
from decoder import Decoder

def rot_of(chunk):
    s = "".join(map(str, chunk))
    return next((r for r in range(14) if ETHER[r:] + ETHER[:r] == s), None)

variant = int(sys.argv[1])
APPS = [["YYYYNN"], ["YYYYNN", ""], ["YYYYNN", "", ""]][variant]
T = 250_000
V = 3 * _left_v(APPS)
bits, placed = assemble("YYYYNN", APPS, left_periods=T // (V * 30) + 3,
                        right_periods=12, v_override=V)
for back in range(0, 4000):
    j = len(bits) - back
    if all(rot_of(bits[j - k - 14:j - k]) is not None for k in (0, 14, 28)):
        bits = bits[:j]; break
c0 = -placed[0].gspan(0)[0]
rl, rr = rot_of(bits[:14]), rot_of(bits[-14:])
assert rl is not None and rr is not None
LPAD = 300_000 // 14 * 14; RPAD = 350_000 // 14 * 14
lt = np.array([int(c) for c in ETHER[rl:] + ETHER[:rl]], dtype=np.uint8)
rt = np.array([int(c) for c in ETHER[rr:] + ETHER[:rr]], dtype=np.uint8)
row = np.concatenate([np.tile(lt, LPAD // 14), bits, np.tile(rt, RPAD // 14)])
c0 += LPAD
d = Decoder()
a = pack(row)
print(f"variant {variant} apps={APPS} v={V} width={len(row)}", flush=True)
for t in range(T + 1):
    if t % 12500 == 0:
        center = c0 + int(round(-8 * t / 30))
        lo, hi = (center - 5000) // 64, (center + 50000) // 64
        cur = unpack(a[lo:hi], (hi - lo) * 64)
        try:
            tape = "".join(sym for _, sym in d.read(cur))
        except ValueError:
            tape = "?"
        print(f"t={t}: {tape}", flush=True)
    a = step_packed(a)
