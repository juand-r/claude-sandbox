"""Check coupler 06:02 item 1 with my construction: semantics of the right-
stream block "J I" with R2 to the left: R1 = 0 -> R2 += 2 (R1 back to 0 via
the echo A); R1 = v1 > 0 -> R1 += 2.  Also "J I J I" at R1 = 0: both Bbars
land in the clean class (R2 += 4).  R2 = 4 made by a fixed left program
(t1_IIIIII.json first 4 slots), R1 = E + v1 GB5's at phase class t1 = 0
(the clean class found in t2_class.py).  Control: t1 = 1, 2."""
import sys, json
import t1lib as L
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC
L.register_IL()
D = 600
slots = [tuple(s) for s in json.load(open("t1_IIIIII.json"))["slots"]][:4]
prog = [(L.OPS[o], t, x) for o, t, x in slots][::-1]
PH = [5, 3]      # block phases: the second found by second_block_scan()


def run(v1, t1, blocks):
    right = [("E", 0, 0), ("E", t1, D)]
    for j in range(v1):
        right += AC.parts("I", t1, D + 150 + 110 * j)
    x = D + 447 + 110 * v1
    for b in range(blocks):
        ph = PH[b] + t1
        right += AC.parts("J", ph, x) + AC.parts("I", ph, x + 110)
        x += 1500
    items = prog + right
    c0 = (L.C_E - sum(vlib.LIB[n].w for n, _, _ in prog)) % 14
    T = 15 * (x - D + 300) + 6 * D + 6000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    return [v3.base(n) for n, x_, w, k in vlib.identify(r, org, T=T)]


def want(v1, blocks):
    y, x = 4, v1
    for _ in range(blocks):
        if x == 0:
            y += 2
        else:
            x += 2
    nm = lambda v: "E" if v == 0 else f"E^{v + 1}"
    return [nm(y), nm(x)]


if __name__ == "__main__":
    bad = 0
    for blocks in (1, 2):
        for v1 in range(0, 4):
            got = run(v1, 0, blocks)
            ok = got == want(v1, blocks)
            bad += not ok
            print(f"(J I)^{blocks} v1={v1}: CA {got} model {want(v1, blocks)} {'ok' if ok else 'MISMATCH'}")
    for t1 in (1, 2):
        got = run(0, t1, 1)
        print(f"control t1={t1}, v1=0: {got} (must differ from {want(0, 1)})")
    print("mismatches:", bad)


def second_block_scan(v1=0):
    """Scan the second J I block's phase (42) at R1 = 0."""
    from collections import defaultdict
    out = defaultdict(list)
    for t2 in range(42):
        right = [("E", 0, 0), ("E", 0, D)]
        x = D + 447
        right += AC.parts("J", 5, x) + AC.parts("I", 5, x + 110)
        x += 1500
        right += AC.parts("J", t2, x) + AC.parts("I", t2, x + 110)
        items = prog + right
        c0 = (L.C_E - sum(vlib.LIB[n].w for n, _, _ in prog)) % 14
        T = 15 * (x - D + 300) + 6 * D + 6000
        row, org, placed = vlib.build(items, c0=c0, T=T)
        r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
        out[" + ".join(v3.base(n) for n, x_, w, k in vlib.identify(r, org, T=T))].append(t2)
    for k, v in out.items():
        print(f"   second block: {k:30s} t0 = {v}")
