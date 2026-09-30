"""Cook's extendible E_n gliders (scholar: unary counter in one glider).
E_1 = library E; E_{n+1} = E_n extended by one B arriving from the right
(B x E_n is single-class). Builds E_n by simulation and returns it as a
Fixed item (period (15,-4)), verified periodic. Diagnostic/constructor."""
import numpy as np
from lib import load_gliders, compose
from r110sat import CNF, TILE, ether_bit, simulate, phase_of
from react import Fixed
from identify import describe

G = load_gliders()


def en_row(n, T=None):
    """Simulate E + (n-1) B's; return (row, x0, t) with E_n settled."""
    E, B = G["E"], G["B"]
    sts = [E.state(0, 0, 0)]
    x = 40
    for i in range(n - 1):
        # B seeds spaced 30 cells apart to the right, ether-consistent
        rp = (sts[-1][2] - sts[-1][3]) % TILE
        s = x
        while True:
            st = B.state(0, s, 0)
            if (st[1] - st[3]) % TILE == rp:
                break
            s += 1
        sts.append(B.state(0, s, 0))
        x = s + 30
    T = T or (200 + 150 * n)
    lo, hi = -2 * T - 100, x + 2 * T + 100
    cells, pl, pr = compose(sts, 0, lo, hi)
    h = simulate(cells, T + 15)
    return h, lo, T


def en_item(cnf, n, width=None):
    h, lo, T = en_row(n)
    objs = describe(h, T, 3 * 14, h.shape[1] - 3 * 14, merge=6)
    near = [o for o in objs if o[2] == (15, -4)]
    if len(near) != 1:
        raise ValueError(f"E_{n}: expected one (15,-4) object, got {objs}")
    a, b = near[0][0], near[0][1]
    a0 = a - 2
    # align: item cell 0 must have my-phase 0 ether on its left (at time T)
    row = h[T]
    # phase of the ether left of a0 as a t=0 row: p with row[x] = ETHER[x + p]
    xs = np.arange(a0 - 14, a0)
    for p in range(TILE):
        if all(row[x] == ether_bit(p, 0, x + lo) for x in xs):
            break
    else:
        raise ValueError("no ether left of E_n")
    # shift start so that global start g satisfies (g + p) % 14 == 0 ... we
    # re-index the item from global column g: item x' = g_x - g, need
    # ETHER[g_x + p] = ETHER[x' + 0] -> g + p = 0 mod 14
    g = a0 + lo
    while (g + p) % TILE:
        g -= 1
    W = width or (b + lo - g + 4)
    cells = row[g - lo:g - lo + W]
    rp = None
    for q in range(TILE):
        if all(row[g - lo + W + i] == ether_bit(q, 0, W + i) for i in range(14)):
            rp = q
    if rp is None:
        raise ValueError("no ether right of E_n")
    it = Fixed(cnf, "".join(map(str, cells)), rp, (15, -4), name=f"E{n}")
    return it


if __name__ == "__main__":
    for n in range(1, 5):
        cnf = CNF()
        it = en_item(cnf, n)
        print(n, it.W, it.pR, "".join(map(str, it.bits)), it._tight[:3])
