import vlib, libgen
from collections import Counter
libgen.load()
T = 800
for k in (3, 4, 5, 0):
    pk = "G" if k == 0 else f"GB{k}"
    for n in range(1, 6):
        nm = "E" if n == 1 else f"E^{n}"
        outs = Counter()
        for t0 in range(42):
            row, org, placed = vlib.build([(nm, 0, 0), (pk, t0, 30)], T=T)
            r = vlib.evolve(row, T)
            ids = vlib.identify(r, org, T=T)
            desc = []
            for name, x, w, key in ids:
                if name == "?":
                    # type by velocity
                    sub = r
                    desc.append(f"?w{w}")
                else:
                    desc.append(f"{name}:{x}")
            outs[" ".join(desc)] += 1
        print(f"{nm} + {pk}:", dict(outs))
