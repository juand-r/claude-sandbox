"""Ether compatibility of two glider seeds (collider conventions)."""
import lane  # noqa: F401
from predict import LIB
from r110lib import TILE


def compatible(X, sx, Y, sy):
    """True if glider Y at seed sy (right) can follow X at sx (left) in a
    consistent ether (right phase of X == left phase of Y at time 0)."""
    bx, lx, rx, px = LIB.gliders[X].state_at(sx[0], sx[1], 0)
    by, ly, ry, py = LIB.gliders[Y].state_at(sy[0], sy[1], 0)
    return (rx - px) % TILE == (ly - py) % TILE
