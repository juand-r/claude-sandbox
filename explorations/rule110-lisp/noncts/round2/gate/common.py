"""Shared setup: import collider's tools (read-only) from ../../collider.

collider modules open their JSON files relative to the cwd, so we chdir there
while importing. Nothing here writes to collider/.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COLLIDER = os.path.abspath(os.path.join(HERE, "..", "..", "collider"))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, COLLIDER)
sys.path.insert(0, ROOT)
os.chdir(COLLIDER)

import engine  # noqa: E402,F401
from collide import canonical_reps, collide_pair, simulate  # noqa: E402,F401
from predict import LIB, norm, predict  # noqa: E402,F401
from r110lib import class_key, build_row  # noqa: E402,F401

CHAIN = ["E"] + [f"E^{n}" for n in range(2, 10)]


def isG(name):
    return str(LIB.gliders[name].velocity) == "-1/3"


def names(prods):
    return [p[0] for p in prods]
