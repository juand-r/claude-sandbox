"""Exact multi-cell check: a head (raw list-form bits) launched at a tape
of N identical walls (raw list-form bits), all in one Rule 110 row with
consistent ether; reports the products after T steps (collider typer).
Used to follow chains that leave shuttle's tables.
Usage (module): tape(head, wall, n, gap, T, side)"""
import ptm
from collide import products_of
from r110lib import build_row, _pack_batch, _unpack_batch, _step_state, TILE


def _place(after, c):
    """smallest start s >= after with s = -c (mod 14): a list-form pattern
    (defined with left ether phase 0 at its own column 0) placed at s has
    absolute left phase -s, which must equal the phase c of the ether there."""
    return after + ((-c - after) % TILE)


def tape(head, wall, n=4, gap=60, T=3000, side='L'):
    Ww = len(wall['bits'])
    sts = []
    c = 0
    s = 0
    for k in range(n):
        s = _place(s, c)
        sts.append((wall['bits'], (c + s) % TILE, (c + wall['pR'] + s) % TILE, s))
        c = (c + wall['pR']) % TILE
        s += Ww + gap
    if side != 'L':
        raise NotImplementedError
    S = _place(s + 40, c)
    sts.append((head['bits'], (c + S) % TILE, (c + head['pR'] + S) % TILE, S))
    row, x0 = build_row(sts, pad=int(T * 0.7) + 200)
    st = _pack_batch(row[None, :])
    for _ in range(T):
        st = _step_state(st)
    ok, prods, objs = products_of(ptm.LIB, _unpack_batch(st, 1)[0], x0, T)
    return ok, prods
