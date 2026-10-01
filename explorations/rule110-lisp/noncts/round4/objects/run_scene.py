"""Helpers: evolve a row and print the non-ether parts at chosen times."""
import re
import numpy as np
import objlib as O


def defects_at(row, x_lo, minlen=1):
    s = O.show(row)
    return [(x_lo + mt.start(), mt.group()) for mt in re.finditer(r"[01]+", s) if len(mt.group()) >= minlen]


def trace(row, x_lo, T, every):
    r = row
    for t in range(0, T + 1):
        if t % every == 0:
            ds = defects_at(r, x_lo + t)
            print(f"t={t}: " + "  ".join(f"[{x}:{len(b)}]" for x, b in ds))
        if t < T:
            r = O.step(r)
    return r
