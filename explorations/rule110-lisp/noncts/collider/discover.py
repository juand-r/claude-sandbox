"""Glider discovery by random perturbation of the ether.

Each experiment: pure ether (random phase) with a random window of L cells
overwritten; evolve T generations; every isolated object of the final row
is handed to r110lib.isolate_glider, which decides by standalone
simulation whether it is a glider (and verifies it). Unique gliders are
identified by the set of their phase keys and saved to gliders_raw.json
with occurrence counts.

Usage: python discover.py N_EXPERIMENTS [seed]
"""

import json
import sys
import time

import numpy as np

from r110lib import (TILE, ether_cells, evolve_batch, isolate_glider,
                     obj_key, objects)

W = 2800
T = 1600
BATCH = 1024


def run(n, seed=0, out="gliders_raw.json"):
    rng = np.random.default_rng(seed)
    known = {}        # phase key -> glider index
    gliders = []      # list of dicts
    failed = set()
    done = 0
    t0 = time.time()
    while done < n:
        B = min(BATCH, n - done)
        rows = np.empty((B, W), np.uint8)
        for i in range(B):
            c = int(rng.integers(TILE))
            rows[i] = ether_cells(c, 0, W)
            L = int(rng.integers(3, 25))
            s = W // 2 - L // 2
            rows[i, s:s + L] = rng.integers(0, 2, L)
        final, _ = evolve_batch(rows, T)
        for i in range(B):
            for a, b, cl, cr in objects(final[i]):
                key = obj_key(final[i], a, b, cl, cr)
                if key in known:
                    gliders[known[key]]["count"] += 1
                    continue
                if key in failed:
                    continue
                try:
                    g = isolate_glider(*key)
                except ValueError:
                    failed.add(key)
                    continue
                idx = len(gliders)
                for bits, l, r, _ in g.phases:
                    known[(bits, l, r)] = idx
                j = g.to_json()
                j["count"] = 1
                gliders.append(j)
                print(f"  new glider #{idx}: p={g.p} d={g.d} v={g.velocity}"
                      f" width={g.width} slip={g.slip}", flush=True)
        done += B
        print(f"{done} experiments, {len(gliders)} gliders, "
              f"{len(failed)} non-glider keys, {time.time() - t0:.0f}s",
              flush=True)
    json.dump(gliders, open(out, "w"), indent=0)
    return gliders


if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 0)
