"""Run a candidate shuttle exactly for a long time and report the counter
values over time: R2 = E^m at (0,0), a launched signal S (any registered
glider/train) at seed (t0, x0) between the counters, R1 = E^n at (t1, D).
Uses streamwin (no streams: the free references are pure ether) so the run
is exact and cheap.  Usage from Python:
  shuttle_run.run(m, n, D, t1, [('X', t0, x0)], T, every)"""
import v3
import streamwin as S


def run(m, n, D, t1, signal, T, every=2000):
    r2 = "E" if m == 1 else f"E^{m}"
    r1 = "E" if n == 1 else f"E^{n}"
    sw, placed = S.from_items([], [(r2, 0, 0)] + signal + [(r1, t1, D)], [])
    tl = S.timeline(sw, T, every)
    hist = []
    for t, objs, cs in tl:
        vals = [v for v, x, nm in cs]
        others = [v3.base(nm) for nm, x in objs if not (v3.base(nm) == "E" or v3.base(nm).startswith("E^"))]
        hist.append((t, vals, others))
    return hist, placed


if __name__ == "__main__":
    # demo with a known one-way event: Bbar from the right of R2 (class #1 gives +2 and an A
    # that then hits R1): one "half bounce"
    for t0 in range(12):
        h, pl = run(4, 4, 600, 0, [("Bbar", t0, 300)], 8000, 4000)
        print(t0, h[-1])
