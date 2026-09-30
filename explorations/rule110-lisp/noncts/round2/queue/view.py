"""Typed spacetime views of Cook's machine in the Ebar frame.

    python view.py TAPE APPS V T0 T1 LO HI STEP out.png

Runs casim.StreamRun (exact Rule 110) for the CTS (TAPE, APPS) with
ossifier spacing V, and renders generations T0..T1 (every STEP, which
should be a multiple of 30 so Ebar-frame-static objects are vertical)
over Ebar-frame columns [LO, HI) (encoder global columns at t = 0).
Colors: ether white, C gray/black, A red, Ebar blue, untyped green.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from casim import StreamRun  # noqa: E402
from census import MAX_DT, census  # noqa: E402

COLORS = {"C": (0, 0, 0), "A": (220, 30, 30), "E": (30, 60, 220),
          "?": (20, 160, 20)}


def frames(run, t0, t1, lo, hi, step):
    """Yield (t, cells, census) in Ebar-frame coordinates [lo, hi)."""
    if run.t > t0 - MAX_DT:
        raise ValueError("run already past t0")
    run.step(t0 - MAX_DT - run.t)
    while run.t + MAX_DT <= t1:
        shift = run.ebar_frame(run.t + MAX_DT)
        h = run.history(lo + shift, hi + shift, MAX_DT)
        yield run.t, h[-1], census(h)
        run.step(step - MAX_DT)


def render(rows, path, scale=1):
    img = np.full((len(rows), len(rows[0][1]), 3), 255, dtype=np.uint8)
    for i, (_, cells, cs) in enumerate(rows):
        img[i][cells == 1] = (200, 200, 200)
        for a, b, k in cs:
            seg = cells[a:b] == 1
            col = np.array(COLORS[k], dtype=np.uint8)
            img[i, a:b][seg] = col
            img[i, a:b][~seg] = (np.array(COLORS[k]) * 0.3 + 178).astype(np.uint8)
    im = Image.fromarray(img)
    if scale != 1:
        im = im.resize((int(im.width * scale), int(im.height * scale)))
    im.save(path)


def main():
    tape, apps, v, t0, t1, lo, hi, step, out = sys.argv[1:10]
    apps = apps.split(",")
    v, t0, t1, lo, hi, step = map(int, (v, t0, t1, lo, hi, step))
    run = StreamRun(tape, apps, t1 // (30 * v) + 3, 6, v_override=v)
    rows = list(frames(run, t0, t1, lo, hi, step))
    for t, _, cs in rows[:: max(1, len(rows) // 12)]:
        print(t, " ".join(f"{k}{a + lo}" for a, b, k in cs))
    render(rows, out)


if __name__ == "__main__":
    main()
