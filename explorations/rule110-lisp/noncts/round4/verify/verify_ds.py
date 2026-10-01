"""Rebuild delayline's drift-switch scenes (ds_scenes.json, collider seeds)
with MY builder (rows asserted equal to collider's build_row), run them to
their T with hrun (HashLife, validated), type with my typer, compare with
their result_CA, and measure R1's walk (worldline shift vs the no-walk run).

Usage: python3 verify_ds.py [scene-json-file]"""
import json
import sys

import numpy as np

import clib
import hrun
import xlate

vlib = hrun.vlib
FIRST = {"c": 2, "v2": 0, "tz": 20000, "T": 138300,
         "seeds": [["v2/3s8w16", 0, -19893], ["E", 0, -1195], ["E", 0, 0], ["GB5", -10, 452]]
         + [["GB4", -2, 936 + 476 * i] for i in range(10)],
         "result_CA": [["E", 9, -1195], ["E", 2, 182]]}


def run_scene(sc):
    scene = [tuple(s) for s in sc["seeds"]]
    clib.ensure_scene(scene)
    items, c0, same = xlate.check(scene)
    assert same, "rebuilt row differs"
    row, org, placed = vlib.build(items, c0=c0, pad=400)
    h = hrun.HRun(row, org)
    T = sc["T"]
    h.goto(T)
    lo, hi = org - T - 400, org + len(row) + T + 400
    objs = h.objects(lo, hi)
    # reference: their result seeds, built by my builder and run to the same T
    ref = [tuple(s) for s in sc["result_CA"]]
    clib.ensure_scene(ref)
    ri, rc0, rsame = xlate.check(ref)
    assert rsame
    rrow, rorg, _ = vlib.build(ri, c0=rc0, pad=400)
    hr = hrun.HRun(rrow, rorg)
    hr.goto(T)
    robjs = hr.objects(lo, hi)
    # cell equality around every reference object (+-60 cells)
    eq = all(np.array_equal(h.cells(x - 60, x + 60), hr.cells(x - 60, x + 60)) for n, x, w in robjs)
    return objs, robjs, eq


if __name__ == "__main__":
    clib.register_auto("ZL"); clib.register_auto("IL")
    scenes = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else [FIRST]
    for sc in scenes:
        objs, robjs, eq = run_scene(sc)
        same = [(n, x) for n, x, w in objs] == [(n, x) for n, x, w in robjs]
        print({k: sc[k] for k in ("c", "v2", "tz", "T")}, "mine:",
              [(n, x) for n, x, w in objs], "| their result seeds run by me:",
              [(n, x) for n, x, w in robjs], "| objects equal:", same, "cells equal:", eq, flush=True)
