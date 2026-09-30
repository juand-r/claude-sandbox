"""Print the non-Ebar clusters (answer path) in the Ebar frame."""
import sys
from view import StreamRun, frames
tape, apps, v, t0, t1, lo, hi, step = sys.argv[1:9]
apps = apps.split(","); v, t0, t1, lo, hi, step = map(int, (v, t0, t1, lo, hi, step))
run = StreamRun(tape, apps, t1 // (30 * v) + 3, 6, v_override=v)
for t, cells, cs in frames(run, t0, t1, lo, hi, step):
    print(t, " ".join(f"{k}{a + lo}-{b + lo}" for a, b, k in cs if k != "E"),
          "| nE", sum(k == "E" for *_, k in cs))
