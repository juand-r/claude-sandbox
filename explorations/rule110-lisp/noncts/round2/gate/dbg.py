from common import LIB, class_key
from r110lib import TILE
from stream import build
E = LIB.gliders["E"]
sc = build(["I"])
g5 = LIB.gliders["GB5"]
prev = g5.state_at(sc[1][1], sc[1][2], 0)
print(sc, prev[1:], (prev[2]-prev[3]) % 14)
for name in ["GB3", "GB3@(0,0)+GB4@(-25,46)", "GB4"]:
    g = LIB.gliders[name]
    pb, pl, pr, ps = prev
    c = (pr - ps) % TILE
    keys = {}
    for t0 in range(g.p):
        b, l, r, s_rel = g.state_at(-t0, 0, 0)
        base = (l - s_rel - c) % TILE
        lo = ps + len(pb) + 40 - s_rel
        x = lo + (base - lo) % TILE
        for k in range(3):
            keys.setdefault(class_key((-t0, x + 14 * k), (E.p, E.d), (g.p, g.d)), (-t0, x+14*k))
    print(name, len(keys), keys)
