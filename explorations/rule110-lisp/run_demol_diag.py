"""Diagnose the t~520-650k death of the Collatz run: record a defect video
around the tape region."""
import numpy as np
from encoder import assemble
from engine import ETHER, pack, unpack, step_packed, save_png

def rot_of(chunk):
    s = "".join(map(str, chunk))
    return next((r for r in range(14) if ETHER[r:] + ETHER[:r] == s), None)

apps = ["NYNNNNNNYNNN", "YNNNNN", "YNNNNNYNNNNNYNNNNN"] + [""] * 9
bits, placed = assemble("YNNNNN" * 3, apps, left_periods=13, right_periods=7)
bits = bits[:-16]
c0 = -placed[0].gspan(0)[0]
rl, rr = rot_of(bits[:14]), rot_of(bits[-14:])
LPAD = 700_000 // 14 * 14
RPAD = 1_000_000 // 14 * 14
ltile = np.array([int(c) for c in ETHER[rl:] + ETHER[:rl]], dtype=np.uint8)
rtile = np.array([int(c) for c in ETHER[rr:] + ETHER[:rr]], dtype=np.uint8)
row = np.concatenate([np.tile(ltile, LPAD // 14), bits, np.tile(rtile, RPAD // 14)])
c0 += LPAD
W = len(row)
a = pack(row)
T0, T1, SAMPLE = 420_000, 660_000, 120
frames = []
for t in range(T1 + 1):
    if t >= T0 and (t - T0) % SAMPLE == 0:
        center = c0 + int(round(-8 * t / 30))
        lo = center - 12_000
        wlo = lo // 64
        cur = unpack(a[wlo:wlo + (60_000 // 64)], 60_000 // 64 * 64)
        frames.append((cur ^ np.roll(cur, 14)).copy())
    a = step_packed(a)
h = np.array(frames)
hd = h.reshape(h.shape[0], -1, 30).max(axis=2)
save_png(hd, "demol_death.png")
print("saved", hd.shape)
