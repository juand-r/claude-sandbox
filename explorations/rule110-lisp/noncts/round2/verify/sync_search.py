"""Look for SYNCHRONIZERS: a packet P at a fixed phase that, acting on a
counter of value m arriving in ANY of the 3 trajectory classes, outputs the
same value in the same class. Then inputs whose zero-histories differ can be
re-aligned. Counter E^(m+1) seeded at (c, 0), c = 0, 1, 2 (my convention;
t mod 3 is the class). Output class = output phase mod 3 at a common T."""
import vlib, libgen
import adaptive_ca as A
libgen.load()
T = 4000

def out(m, c, P, p, X=60):
    nm = "E" if m == 0 else f"E^{m+1}"
    items = [(nm, c, 0)] + A.parts(P, p, X)
    row, org, placed = vlib.build(items, T=T)
    deltas = {q[2] - it[2] for q, it in zip(placed[1:], items[1:])}
    if len(deltas) != 1:
        return "snap"          # packet parts shifted unequally: geometry broken
    r = vlib.evolve(row, T)
    ids = [n for n, x, w, k in vlib.identify(r, org, T=T)]
    es = [n for n in ids if n.split("@")[0] in ("E",) or n.startswith("E^")]
    other = sorted(n.split("@")[0] for n in ids if n not in es)
    if len(es) != 1:
        return ("bad", tuple(other))
    nm2, s = es[0].split("@")
    return (nm2, int(s) % 3, tuple(other))

for P, m in (("Z", 1), ("N", 0), ("I", 0), ("Z", 0), ("J", 0), ("W", 1), ("X", 0), ("W", 0), ("D", 1)):
    syncs = []
    table = {}
    for p in range(42):
        o = [out(m, c, P, p) for c in range(3)]
        if "snap" in o:
            continue
        table[p] = o
        if all(isinstance(x, tuple) and len(x) == 3 for x in o) and len({x for x in o}) == 1:
            syncs.append((p, o[0]))
    print(f"{P} on value {m}: synchronizing phases: {syncs[:6]}{' ...' if len(syncs) > 6 else ''} ({len(syncs)})", flush=True)
