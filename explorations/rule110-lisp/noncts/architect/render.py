"""Render a spacetime diagram of glider placements (PNG), ether filtered:
cells are shown only where the 14-periodic ether is broken."""
import sys
import numpy as np
from PIL import Image
from rx import G, history
sys.path.insert(0, "../..")
from census import ether_phase


def defect_mask(row):
    ph = ether_phase(row)
    ok = np.zeros(len(row), bool)
    idx = np.nonzero(ph >= 0)[0]
    for k in range(14):
        ok[np.minimum(idx + k, len(row) - 1)] = True
    return ~ok


def render(placements, T, path, every=1, lo=None, hi=None):
    H, x0 = history(placements, T)
    if lo is not None:
        H = H[:, lo - x0:hi - x0]
    rows = []
    for t in range(0, len(H), every):
        m = defect_mask(H[t])
        rows.append(np.where(m, 0, 235).astype(np.uint8))
    img = Image.fromarray(np.array(rows))
    img.save(path)
    return x0
