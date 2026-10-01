"""Behaviour table of gate's compound packets on a counter, all classes,
with the counter's DISPLACEMENT (trajectory change) made explicit.
For value v (counter E^(v+1) built at (0,0)) and packet P with seed phase t0
(0..41, which covers every class of P vs E), record the products at time T
and, for the counter product E^m, its offset from an untouched E^m built at
(0,0) and evolved T steps: (dphase, dlo) = (0, 0) means "same trajectory".
Packets are given in collider convention as parts with offsets; I place the
first part at (t0, X) in MY convention and the others at my-equivalent
offsets (offsets are convention-independent: a seed shift is a seed shift)."""
import sys
from collections import defaultdict
import vlib, libgen
import xlate          # convention offsets between glider types (collider -> mine)
libgen.load()

def my_offset(g1, g2, dt, dx):
    """collider part offset (dt, dx) of g2 relative to g1 -> my offset."""
    T1, X1, _ = xlate.mapping(g1)
    T2, X2, _ = xlate.mapping(g2)
    return dt + T2 - T1, dx + X2 - X1

PACKETS = {
    "Z": [("GB3", 0, 0), ("GB4", -25, 46)],
    "W": [("GB3", 0, 0), ("GB5", -14, 40)],
    "X": [("GB5", 0, 0), ("GB4", -4, 56)],
    "J": [("GB1", 0, 0), ("GB1", -1, 36)],
    "I": [("GB5", 0, 0)], "N": [("GB4", 0, 0)], "D": [("GB3", 0, 0)],
}
T = 4000

def Ename(v):
    return "E" if v == 0 else f"E^{v+1}"

REF = {}
def ref(nm):
    if nm not in REF:
        row, org, _ = vlib.build([(nm, 0, 0)], T=T)
        r = vlib.evolve(row, T)
        (n, x, w, k), = vlib.identify(r, org, T=T)
        REF[nm] = (n, x)
    return REF[nm]

def run(v, P, t0, X=40):
    items = [(Ename(v), 0, 0)]
    # place parts; the first part's snapped x defines the packet origin
    first = True
    g0 = PACKETS[P][0][0]
    for g, dt, dx in PACKETS[P]:
        if first:
            items.append((g, t0 + dt, X + dx)); first = False
        else:
            mdt, mdx = my_offset(g0, g, dt, dx)
            items.append((g, T0 + mdt, X0 + mdx))
        if len(items) == 2:
            row, org, placed = vlib.build(items, T=T)
            T0, X0 = placed[1][1], placed[1][2]
            items[1] = placed[1]
    try:
        row, org, placed = vlib.build(items, T=T)
    except ValueError as e:
        return None
    if [p[2] for p in placed] != [it[2] for it in items]:
        return "snapped"          # a part was not ether-compatible: skip
    r = vlib.evolve(row, T)
    out = []
    for n, x, w, k in vlib.identify(r, org, T=T):
        nm = n.split("@")[0]
        if nm == "E" or nm.startswith("E^"):
            rn, rx = ref(nm)
            out.append(f"{nm}[{n.split('@')[1]},{x - rx}]")
        else:
            out.append(nm)
    return " ".join(out)

if __name__ == "__main__":
  for P in (sys.argv[1:] or ["Z", "W", "X", "J"]):
    for v in range(0, 4):
        res = defaultdict(list)
        for t0 in range(42):
            o = run(v, P, t0)
            if o not in (None, "snapped"):
                res[o].append(t0)
        print(f"{P} on value {v}: " + "; ".join(f"[{k}] x{len(t)}" for k, t in sorted(res.items(), key=lambda kv: -len(kv[1]))), flush=True)
