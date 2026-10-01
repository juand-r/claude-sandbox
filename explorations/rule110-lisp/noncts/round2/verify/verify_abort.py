"""Independent check of gate's 01:22 abort step 1: C1 + sequence of neutral
eaters (a, b) + gate -> one Ebar. Scenes from gate/abort_scene.build
(read-only), my translation (row equality asserted), exact engine, my typer.
Also: abort-start independence: the SAME fixed packet list with the first k
packets removed (abort starting later) must still give one Ebar; without the
C1 the packets must pass untouched; shifted controls must fail."""
import os, sys
import vlib, xlate
HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.abspath(os.path.join(HERE, "..", "gate"))
COLL = os.path.abspath(os.path.join(HERE, "..", "..", "collider"))
sys.path.insert(0, GATE)
cwd = os.getcwd()
import common  # noqa: E402,F401
import abort_scene as AS  # noqa: E402
os.chdir(cwd)

def scene(seq, c1=True, shifts=None, drop=0):
    os.chdir(COLL)
    try:
        sc = AS.build(seq, c1=c1, shifts=shifts)
    finally:
        os.chdir(cwd)
    if drop:
        sc = sc[:1] + sc[1 + drop:] if c1 else sc[drop:]
    return [(g, int(t), int(x)) for g, t, x in sc]

def run(sc, T=None):
    ex = xlate.expand(sc)
    items, c0, same = xlate.check(ex)
    assert same
    span = items[-1][2] - items[0][2]
    T = T or int(span * 30 / 8 + 3000)       # Ebar closes on C1 at 4/15
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = vlib.evolve(row, T)
    return sorted(n.split("@")[0] for n, x, w, k in vlib.identify(r, org, T=T))

if __name__ == "__main__":
    for seq in ("abbaabg", "aaag", "bg", "g"):
        print(seq, "->", run(scene(seq)), flush=True)
    full = "abbaabg"
    for k in (1, 3, 5):
        print(f"{full} with the C1 meeting only from packet {k} on ->", run(scene(full, drop=k)), flush=True)
    print("no C1:", run(scene(full, c1=False)))
    print("control pair 2 shifted (0,14):", run(scene(full, shifts={1: (0, 14)})))
    print("control pair 1 shifted (1,-4):", run(scene(full, shifts={0: (1, -4)})))
