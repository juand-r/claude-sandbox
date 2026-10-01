"""C2 x Ebar chains in isolation: a stationary C2 (library tile, phase 0) at
x = 0 and a train of Ebars to its left... no: Ebars move LEFT (-4/15), so
they must start to the RIGHT of the C2. For each first-Ebar placement
(k, x) (x = gap from C2 tile end), simulate and type the result.
Then: after one crossing, which placements of a SECOND Ebar (behind the
first, i.e. further right) are crossed?"""
import sys
import numpy as np
from q import *
from engine import ETHER
from census import census, MAX_DT
from engine import pack, unpack, step_packed_n
ETH = np.array([int(c) for c in ETHER], dtype=np.uint8)
C = glider_tiles("C2"); E = ebar_tiles()

def row_of(items, pad=1200):
    """items: list of (tiles, k, gap) left to right; gap = ether cells
    between consecutive tiles (adjusted up to the next phase-consistent
    value). Returns row, list of tile start indices."""
    arr0, cl0, cr0 = items[0][0][items[0][1]]
    p = 0
    parts = []; pos = 0; starts = []
    # leading ether of phase p
    for tiles, k, gap in items:
        arr, cl, cr = tiles[k]
        x = pos + gap
        while (cl - x) % TILE != p:
            x += 1
        parts.append(ETH[(p + np.arange(pos, x)) % TILE]); parts.append(arr); starts.append(x)
        pos = x + len(arr); p = (cr - x) % TILE
    parts.append(ETH[(p + np.arange(pos, pos + pad)) % TILE])
    lead = ETH[(0 + np.arange(-pad, 0)) % TILE]
    return np.concatenate([lead] + parts), [s + pad for s in starts]

def run_types(row, T):
    w = pack(row); w = step_packed_n(w, T - MAX_DT); rows = []
    for _ in range(MAX_DT + 1):
        rows.append(unpack(w, len(row))); w = step_packed_n(w, 1)
    return [(a, k) for a, b, k in census(np.array(rows))]

if __name__ == "__main__":
    # first crossing: C2 phase 0, Ebar k at gap g (g covers 4 classes x ...)
    for k in range(30):
        for g in range(0, 14):
            row, st = row_of([(C, 0, 20), (E, k, g)])
            if st[1] - st[0] - len(C[0][0]) != g:
                continue
            res = run_types(row, 600)
            print(k, g, " ".join(f"{t}{a - st[0]}" for a, t in res))
