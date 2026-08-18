"""Long validation run: canonical conforming CTS {YYYYYY,e,NNNNNN,e}, tape Y.
Decodes the tape every DECODE_EVERY generations, logs reads to
canonical_run.log, saves a defect-map overview PNG."""
import time
import numpy as np
from encoder import assemble
from engine import step, save_png
from decoder import Decoder

TAPE, APPS = "Y", ["YYYYYY", "", "NNNNNN", ""]
T = 120_000
DECODE_EVERY = 50
PNG_EVERY = 60

bits, placed = assemble(TAPE, APPS, left_periods=4, right_periods=19)
W = len(bits)
c0 = -placed[0].gspan(0)[0]
print("width", W, "tape starts at", c0 + placed[len(placed)//1-1].gspan(0)[0] if False else "")
d = Decoder()
log = open("canonical_run.log", "w")
frames = []
cur = bits
t0 = time.time()
for t in range(T + 1):
    if t % DECODE_EVERY == 0:
        try:
            reads = d.read(cur)
            msg = " ".join(f"{p}{s}" for p, s in reads)
            tape = "".join(s for _, s in reads)
        except ValueError as e:
            tape, msg = "?", str(e)
        log.write(f"{t}\t{tape}\t{msg}\n")
    if t % PNG_EVERY == 0:
        center = c0 + int(round(-8 * t / 30))
        wnd = cur[max(0, center - 3600):center + 3600]
        frames.append((wnd ^ np.roll(wnd, 14)).copy())
    if t % 20000 == 0:
        log.flush()
        print(f"t={t} elapsed={time.time()-t0:.0f}s", flush=True)
    cur = step(cur)
log.close()
h = np.array(frames)
hd = h.reshape(h.shape[0], -1, 4).max(axis=2)
save_png(hd, "canonical_defects.png")
print("done", hd.shape)
