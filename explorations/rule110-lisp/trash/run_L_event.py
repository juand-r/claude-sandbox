"""Render the read-2 rejector interaction zone for the L run and control."""
import sys
import numpy as np
from encoder import assemble, _left_v
from engine import ETHER, pack, unpack, step_packed, save_png

def rot_of(chunk):
    s = "".join(map(str, chunk))
    return next((r for r in range(14) if ETHER[r:] + ETHER[:r] == s), None)

variant = int(sys.argv[1])
APPS = [["YNNNNN", ""], ["YNNNNN", "YNNNNN"]][variant]
V = 3 * _left_v(APPS)
bits, placed = assemble("YN", APPS, left_periods=8, right_periods=14, v_override=V)
for back in range(0, 4000):
    j = len(bits) - back
    if all(rot_of(bits[j - k - 14:j - k]) is not None for k in (0, 14, 28)):
        bits = bits[:j]; break
c0 = -placed[0].gspan(0)[0]
rl, rr = rot_of(bits[:14]), rot_of(bits[-14:])
LPAD = 200_000 // 14 * 14; RPAD = 250_000 // 14 * 14
lt = np.array([int(c) for c in ETHER[rl:] + ETHER[:rl]], dtype=np.uint8)
rt = np.array([int(c) for c in ETHER[rr:] + ETHER[:rr]], dtype=np.uint8)
row = np.concatenate([np.tile(lt, LPAD // 14), bits, np.tile(rt, RPAD // 14)])
c0 += LPAD
a = pack(row)
frames = []
T0, T1, S = 30_000, 90_000, 40
for t in range(T1 + 1):
    if t >= T0 and (t - T0) % S == 0:
        center = c0 + int(round(-8 * t / 30))
        lo = (center + 500) // 64
        cur = unpack(a[lo:lo + 6400 // 64], 6400)
        frames.append((cur ^ np.roll(cur, 14)).copy())
    a = step_packed(a)
h = np.array(frames)
wc = h.shape[1] // 4 * 4
hd = h[:, :wc].reshape(h.shape[0], -1, 4).max(axis=2)
save_png(hd, f"L_event_{variant}.png")
print("saved", hd.shape)
