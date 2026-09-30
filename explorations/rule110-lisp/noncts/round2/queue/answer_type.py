"""Type the non-Ebar objects (the answer) in the lab frame over time."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".." / "scholar"))
import r110check as rc
from view import StreamRun, frames
tape, apps, v, t0, t1, lo, hi, step = sys.argv[1:9]
apps = apps.split(","); v, t0, t1, lo, hi, step = map(int, (v, t0, t1, lo, hi, step))
run = StreamRun(tape, apps, t1 // (30 * v) + 3, 6, v_override=v)
H = 200
t = t0
run.step(t0 - H)
while run.t + H <= t1:
    sh = run.ebar_frame(run.t + H)
    L0, L1 = lo + sh - 400, hi + sh + 400      # lab window, generous
    h = run.history(L0, L1, H)
    objs = rc.objects(h, H, 120, len(h[0]) - 120, merge=6)
    print(run.t, " ".join(f"{n}@{a + L0 - sh}" for a, b, n in objs
                          if lo <= a + L0 - sh < hi and n not in ("Ebar",)), flush=True)
    run.step(step - H)
