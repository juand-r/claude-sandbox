"""Collide two zoo gliders X (left) and Y (right) over all relative phases."""
import sys, pickle
import numpy as np
from lab import *

W = 14 * 60


def embed(g, width=W, center=None):
    """Glider g's standalone row re-embedded into a wider ether row."""
    a, b = g.span()
    n = len(g.row)
    row = np.empty(width, np.uint8)
    center = width // 2 if center is None else center
    sh = center - (a + b) // 2
    sh -= sh % TILE          # keep phase: shift by multiple of 14
    y = np.arange(width)
    src = y - sh
    # outside the original row, continue ether with original edge phases
    ph = ether_phase(g.row)
    lph = ph[0]; rph = ph[-1]
    out = np.where(src < 0, EB[(lph + src) % TILE], 0)
    inside = (src >= 0) & (src < n)
    out[inside] = g.row[src[inside]]
    right = src >= n
    out[right] = EB[(rph + src[right]) % TILE]
    return out.astype(np.uint8)


def collide(X, Y, kx, ky, gap, T=400, width=W):
    """X at phase kx on the left, Y at phase ky, roughly `gap` cells apart."""
    rx = X.at(kx); ry = Y.at(ky)
    gx = Glider(rx, (X.dt, X.dx)); gy = Glider(ry, (Y.dt, Y.dx))
    L = embed(gx, width, center=width // 3)
    R = embed(gy, width, center=width // 3)
    ax, bx = clusters(L)[0]
    ay, by = clusters(R)[0]
    # we want Y's cluster to start near bx + gap; shift R by s with phase match
    phL = ether_phase(L)[bx + 20]
    phR = ether_phase(R)[ay - 20]
    # after shifting R by s, phase at x is phR - s; need == phL mod 14
    s0 = bx + gap - ay
    s = s0 + ((phR - s0 - phL) % TILE)
    row = splice(L, R, bx + gap // 2, s)
    return row


def outcome(row, T):
    H = evolve(row, T)
    return census_typed(H[-121:])
