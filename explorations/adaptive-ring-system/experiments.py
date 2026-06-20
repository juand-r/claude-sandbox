"""Run a battery of Ring System configurations and report the discriminating
metrics side by side. See RESEARCH_PLAN.md.

Usage: python3 experiments.py [--ticks 400] [--init 16] [--seed 0]
"""

from __future__ import annotations

import argparse
import os

import analyze
import ring_system as rs

CORE = ((0, 8), (8, 16), (16, 24), (24, 32))   # full genotype (RULE+addr+ORDER)

# name -> kwargs for Universe (beyond nmax/seed)
CONFIGS = {
    "baseline":        dict(),
    "mut_off":         dict(mut_scale=0.0),
    "no_transform":    dict(transform_off=True),      # drift-only control
    "protect_core":    dict(protect=((0, 8), (8, 16), (16, 24))),  # H1
    "protect_lowmut":  dict(protect=((0, 8), (8, 16), (16, 24)),
                            mut_scale=0.3),            # H1 + H3
    # H2: conditional reproduction AND death on a heritable key (low nibble of
    # ORDER). spawn_code != death_code, so key==15 rings reproduce and never
    # die, key==0 rings die and never reproduce, others persist statically.
    "h2_protected":    dict(protect=CORE, spawn_code=15, death_code=0),
    "h2_key_only":     dict(protect=((28, 32),), spawn_code=15, death_code=0),
    "h2_unprotected":  dict(spawn_code=15, death_code=0),   # control: key not heritable
    # H4: spatial. local addressing + heritable rule -> domains form.
    "local_faithful":  dict(local_addr=True),
    "local_stable":    dict(local_addr=True, protect=((0, 8), (8, 16), (16, 24)),
                            mut_scale=0.3),
}

# configs that should be seeded full (spatial runs start from a filled grid)
FULL_SEED = {"local_faithful", "local_stable"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticks", type=int, default=400)
    ap.add_argument("--init", type=int, default=16)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--outdir", default="out")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    rows = []
    for name, kw in CONFIGS.items():
        u = rs.Universe(nmax=256, seed=args.seed, record_history=True, **kw)
        u.seed_random(256 if name in FULL_SEED else args.init)
        u.run(args.ticks)
        path = os.path.join(args.outdir, f"exp_{name}.npz")
        u.save_history(path)
        m = analyze.summarize(path, label=name)
        if kw.get("spawn_code") is not None:
            import numpy as np
            d = np.load(path)
            ks = analyze.key_share_series(d["bits"], d["occ"],
                                          kw.get("key_span", (28, 32)),
                                          kw["spawn_code"])
            print(f"  key==spawn_code share   {ks[0]:.3f} -> {ks[-1]:.3f}   "
                  f"(selection signal; chance = {1/16:.3f})")
            m["key_final"] = float(ks[-1])
        rows.append((name, m))

    print("\n\n==== comparison (means over run / last ticks) ====")
    hdr = f"{'config':16} {'pop':>7} {'turnover':>9} {'conc':>7} " \
          f"{'persist':>8} {'compress':>9} {'moran':>7}"
    print(hdr); print("-" * len(hdr))
    for name, m in rows:
        print(f"{name:16} {m['meanpop']:7.1f} {m['turnover']:9.3f} "
              f"{m['concentration']:7.3f} {m['persistence_max']:8d} "
              f"{m['compressibility']:9.3f} {m['moran']:7.3f}")


if __name__ == "__main__":
    main()
