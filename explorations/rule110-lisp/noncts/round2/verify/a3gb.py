"""A^k (right-mover) + GBm (G-speed left-mover): all phases; list clean
outcomes (only G-speed / B / A products)."""
import vlib, libgen
from collections import defaultdict
libgen.load()
T = 500
for ak in ("A", "A^2", "A^3"):
    for m in range(0, 9):
        pk = "G" if m == 0 else f"GB{m}"
        outs = defaultdict(list)
        for t0 in range(42):
            for dx in (60, 74, 88):
                try:
                    row, org, placed = vlib.build([(ak, 0, 0), (pk, t0, dx)], T=T)
                except ValueError:
                    continue
                r = vlib.evolve(row, T)
                ids = tuple(n.split("@")[0] for n, x, w, k in vlib.identify(r, org, T=T))
                outs[ids].append((t0, dx))
        s = "; ".join(f"{'+'.join(k) or 'nothing'} x{len(v)}" for k, v in sorted(outs.items(), key=lambda kv: -len(kv[1])))
        print(f"{ak} + {pk}: {s}", flush=True)
