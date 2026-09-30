import vlib, libgen
from collections import Counter
libgen.load()
T = 800
def run(items, T=T):
    row, org, placed = vlib.build(items, T=T)
    r = vlib.evolve(row, T)
    return r, org, vlib.identify(r, org, T=T)
for k in (0, 1, 2):
    pk = "G" if k == 0 else f"GB{k}"
    for n in (1, 2, 3, 4, 5, 6):
        nm = "E" if n == 1 else f"E^{n}"
        outs = Counter()
        for t0 in range(42):
            r, org, ids = run([(nm, 0, 0), (pk, t0, 30)])
            outs[" ".join(n2.split('@')[0] if n2 != '?' else f"?w{w}v{vlib.velocity_type(r[T+16:-T-16])[i][2]}" for i,(n2, x, w, key) in enumerate(ids))] += 1
        print(f"{nm} + {pk}:", dict(outs))
