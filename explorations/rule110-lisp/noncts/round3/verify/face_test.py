"""Generic independent tester for face reactions (for shuttle candidates).
A train given as raw cells (left ether phase 0 at x = 0, time 0), its slip
and period vector is registered in MY library (vlib.register checks the
period), then placed against my E^n:
  side='left'  : train left of the counter (right-mover, hits the FRONT
                 of R1 / R2 as seen from the left),
  side='right' : train right of the counter (left-mover, hits the back).
All time phases t0 < P and 14 x offsets (deduplicated by snapped seed);
outcomes typed by my typer.  Usage from Python:
  face_test.test('X', '1111...', slip, (3, 2), 'left', ns=range(1, 9))"""
import numpy as np
from collections import defaultdict
import v3, vlib, engine


def register(name, bits, slip, period):
    core = np.array([int(c) for c in bits], np.uint8)
    left = vlib.ETHER[np.arange(-56, 0) % 14]
    right = vlib.ETHER[(np.arange(len(core), len(core) + 56) + slip) % 14]
    vlib.register(name, np.concatenate([left, core, right]), period)


def test(name, bits, slip, period, side, ns=range(1, 9), T=3000, gap=80):
    if name not in vlib.LIB:
        register(name, bits, slip, period)
    P = vlib.LIB[name].P
    out = {}
    for n in ns:
        R = "E" if n == 1 else f"E^{n}"
        res = defaultdict(list)
        seen = set()
        for t0 in range(P):
            for dx in range(14):
                if side == "left":
                    items = [(name, t0, -gap - dx), (R, 0, 0)]
                else:
                    items = [(R, 0, 0), (name, t0, gap + 40 + dx)]
                objs, r, org, placed = v3.run(items, T)
                key = tuple((p[1], p[2]) for p in placed)
                if key in seen:
                    continue
                seen.add(key)
                res[" + ".join(v3.names(objs))].append((t0, dx))
        out[n] = dict(res)
        print(f"{name} ({side}) + {R}: " + " | ".join(
            f"{k} x{len(v)}" for k, v in sorted(res.items(), key=lambda kv: -len(kv[1]))), flush=True)
    return out


if __name__ == "__main__":
    # self-check on known trains: I_L (INC) and Z_L (zero test) from the left
    test("IL", "111110111110111110001110", 6, (3, 2), "left", ns=range(1, 5))
    test("ZL", "111110111110111000111011", 8, (3, 2), "left", ns=range(1, 5))
