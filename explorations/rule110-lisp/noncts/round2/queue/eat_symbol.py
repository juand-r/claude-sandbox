"""Can a B packet eat one Cook tape symbol cleanly? (anti-symbol test)
Cut a clean tape symbol (4 stationary C's) from a running machine, put it
alone in ether, add k B's to its right at all phases/offsets (B + B spacing
fixed by tiles), evolve, and type what is left with r110check."""
import sys
from splice import *

def tape_symbol(tape="YYYY", t=22500):
    m = Machine(tape, ["YNNNNN"], t + 10, left_periods=3, right_periods=2)
    r = Run(m.row, m.origin)
    r.step(t)
    lo, hi = m.origin - 6000, m.origin + 3000
    row = r.window(lo, hi)
    # find a group of 4 C-type clusters isolated by >= 60 cells of ether
    h = r.history(lo, hi, MAX_DT)
    cs = census(h)
    row = h[-1]
    from slips import groups
    for a, b in groups(row):
        inside = [k for x, y, k in cs if a <= x < b]
        if len(inside) == 4 and all(k == "C" for k in inside):
            return row[a - 40:b + 40].copy()
    raise RuntimeError("no isolated symbol")

if __name__ == "__main__":
    sym = tape_symbol()
    print("symbol cells", len(sym), "slip", (phase_at(sym, len(sym) - TILE) - phase_at(sym, 0)) % TILE)
    btile = ebar_tiles("B(f1_1)", 16, 4)
    k_B = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    results = {}
    for ph in range(4):
        for off in range(0, 70):
            # sym + gap + k B's spaced by one tile each (tight as tiles allow)
            row = np.concatenate([fill_ether(600, phase_at(sym, 0), -600), sym])
            ok = True
            pos = len(row) + off
            for j in range(k_B):
                arr, cl, cr = btile[(ph + j) % 4]
                cph = phase_at(row, len(row) - TILE)
                x = pos if j == 0 else len(row)
                x += (cl - x - cph) % TILE
                if x < len(row):
                    ok = False; break
                row = np.concatenate([row, fill_ether(x - len(row), cph, len(row)), arr])
            if not ok:
                continue
            row = np.concatenate([row, fill_ether(400, phase_at(row, len(row) - TILE), len(row))])
            h = rc.evolve(row, 1400)
            objs = rc.objects(h, 1400, 50, len(row) - 50)
            key = tuple(sorted(n for _, _, n in objs))
            results.setdefault(key, []).append((ph, off))
    for key, v in sorted(results.items(), key=lambda kv: len(kv[0])):
        print(len(v), key, v[:3])
