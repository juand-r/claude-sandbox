"""Independent check of synth's claim (BOARD, synth 03:45 real clock): an
A-packet (tight train of 7k+1 A's) crosses a stationary C, the C restored
(displaced) and one A (or A^2) continuing right.

We embed synth's packet string H in ether by trying all 14 x 14 left/right
ether rotations and keeping those embeddings in which H is a single (3,2)
object (a valid right-moving packet). Then place C1/C2/C3 (Martinez strings)
to its right and run."""
import numpy as np
import r110check as r
from engine import ETHER, parse

TILE = 14


def embeddings(H):
    out = []
    for lr in range(TILE):
        for rr in range(TILE):
            left = "".join(ETHER[(lr - 20 * TILE + i) % TILE] for i in range(20 * TILE))
            right = "".join(ETHER[(rr + i) % TILE] for i in range(20 * TILE))
            row = parse(left + H + right)
            h = r.evolve(row, 120)
            obj = r.objects(h, 120, 60, len(row) - 60)
            if len(obj) == 1:
                pd = r.local_period(h, 120, obj[0][0], obj[0][1])
                if pd == (3, 2):
                    out.append((lr, rr, obj[0][2]))
    return out


def cross(H, lr, rr, cell, n=10, T=900):
    left = "".join(ETHER[(lr - 150 * TILE + i) % TILE] for i in range(150 * TILE))
    k = (TILE - rr) % TILE                     # continue to a tile boundary
    right = "".join(ETHER[(rr + i) % TILE] for i in range(k))
    row = parse(left + H + right + ETHER * n + r.PHASES[cell] + ETHER * 150)
    h = r.evolve(row, T)
    lo, hi = T + 20, len(row) - T - 20
    return [o[2] for o in r.objects(h, T, lo, hi)], [o[2] for o in r.objects(h, T - 150, lo, hi)]


if __name__ == "__main__":
    for H in ["111110111110111011111011", "111110111110111011101001",
              "111110111011101110111011", "111110111110111110111011"]:
        emb = embeddings(H)
        print(H, "valid embeddings:", emb[:4], len(emb))
        for lr, rr, name in emb[:2]:
            for cell in ["C1(A,f1_1)", "C2(A,f1_1)", "C3(A,f1_1)"]:
                a, b = cross(H, lr, rr, cell)
                print("   ", name, "+", cell, "->", a, "" if a == b else "UNSETTLED")
