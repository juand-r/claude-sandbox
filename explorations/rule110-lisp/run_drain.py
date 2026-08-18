"""Halting-signature experiment: all-rejection drain race.
{YYYYNN} with an all-N tape: every read rejects, no moving data is
produced, so unspent ossifiers should eventually strike unread static
tape data -> F glider -> Cook's signatures."""
import sys
import numpy as np
from encoder import assemble, _left_v
from engine import step, save_png

NTAPE = int(sys.argv[1]) if len(sys.argv) > 1 else 12
T = int(sys.argv[2]) if len(sys.argv) > 2 else 60000
SSIG = "01101001101000"
TSIG = "110101010111111"

bits, placed = assemble("N" * NTAPE, ["YYYYNN"], left_periods=4,
                        right_periods=10, v_override=3 * _left_v(["YYYYNN"]))
c0 = -placed[0].gspan(0)[0]
print("width", len(bits), flush=True)
cur = bits
frames = []
first_s = None
cols = {}   # temporal traces near the tape region
lo, hi = c0 - 2000, c0 + 3000
tbuf = []
for t in range(T + 1):
    if t % 20 == 0:
        w = cur[lo:hi]
        frames.append((w ^ np.roll(w, 14)).copy())
    if first_s is None:
        s = cur.tobytes().translate(bytes.maketrans(b"\x00\x01", b"01")).decode()
        i = s.find(SSIG)
        if i >= 0:
            first_s = (t, i)
            print("SPATIAL signature at", first_s, flush=True)
    tbuf.append(cur[lo:hi].copy())
    if len(tbuf) == 4000:   # scan temporal traces in chunks
        tr = np.array(tbuf)
        for c in range(tr.shape[1]):
            ss = tr[:, c].tobytes().translate(bytes.maketrans(b"\x00\x01", b"01")).decode()
            j = ss.find(TSIG)
            if j >= 0:
                print(f"TEMPORAL signature col {c+lo} t~{t-4000+j}", flush=True)
                tbuf = None
                break
        if tbuf is None:
            break
        tbuf = tbuf[-14:]   # overlap so signatures crossing chunks aren't lost
    cur = step(cur)
h = np.array(frames)
hd = h.reshape(h.shape[0], -1, 4).max(axis=2)
save_png(hd, f"drain{NTAPE}.png")
print("done; spatial:", first_s)
