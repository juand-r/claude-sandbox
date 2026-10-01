"""R2 -> R1 channel: R2 = E (value 0) gets Z_L from the left -> E + A; the A
travels right to R1 = E^(m+1) (value m, written by m right-stream I = GB5
packets at fixed slots before the A arrives) -> expect A + E^(m+1) -> E^m.
Scan Z_L phase (3 x 14 offsets) for the zero class, and R1 time phase t1
(15), report outcome by (m, class).  Exact CA, my builder/typer."""
import sys
from collections import defaultdict
import t1lib as L
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC
L.register_IL()

D = 600
XZ = -6000          # Z_L far left so the A reaches R1 after the I's
SPI = 110


def run(m, t1, tz, dz):
    right = [("E", 0, 0), ("E", t1, D)]
    for k in range(m):
        right += AC.parts("I", t1, D + 150 + SPI * k)
    items = [("ZL", tz, XZ - dz)] + right
    c0 = (L.C_E - vlib.LIB["ZL"].w) % 14
    T = 15 * (D + 150 + SPI * 6) + 9000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    return " + ".join(v3.base(n) for n, x, w, k in vlib.identify(r, org, T=T))


if __name__ == "__main__":
    # 1. zero class of Z_L on R2 alone (no R1): want E + A
    zc = None
    for tz in range(3):
        for dz in range(14):
            items = [("ZL", tz, XZ - dz), ("E", 0, 0)]
            c0 = (L.C_E - vlib.LIB["ZL"].w) % 14
            row, org, placed = vlib.build(items, c0=c0, T=8000)
            r = engine.unpack(engine.step_packed_n(engine.pack(row), 8000), len(row))
            o = [v3.base(n) for n, x, w, k in vlib.identify(r, org, T=8000)]
            if o == ["E", "A"] and zc is None:
                zc = (tz, dz)
    print("Z_L zero class at", zc)
    for m in range(0, 6):
        out = defaultdict(list)
        for t1 in range(15):
            out[run(m, t1, *zc)].append(t1)
        print(f"R1 = {m}: " + " | ".join(f"{k} {v}" for k, v in out.items()), flush=True)
