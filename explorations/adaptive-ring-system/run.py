"""Run an Adaptive Ring System simulation.

Writes a JSONL metrics log and a .npz state history, prints a readable
per-tick summary, and (optionally) renders the dashboard.

Examples:
    python3 run.py --ticks 400 --init 16 --seed 0
    python3 run.py --ticks 400 --init 1 --seed 0 --render
"""

from __future__ import annotations

import argparse
import os

import ring_system as rs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=256)
    ap.add_argument("--init", type=int, default=16,
                    help="number of random rings to seed")
    ap.add_argument("--ticks", type=int, default=400)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--print-every", type=int, default=20)
    ap.add_argument("--outdir", default="out")
    ap.add_argument("--render", action="store_true",
                    help="also render the dashboard (GIF + summary)")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    log_path = os.path.join(args.outdir, "metrics.jsonl")
    hist_path = os.path.join(args.outdir, "history.npz")

    u = rs.Universe(nmax=args.nmax, seed=args.seed, record_history=True)
    u.seed_random(args.init)

    print(f"seeded {args.init} rings in {args.nmax} slots (seed={args.seed})")
    with rs.Logger(log_path) as logger:
        results = u.run(args.ticks, logger=logger, print_every=args.print_every)
    u.save_history(hist_path)

    final = results[-1]
    print(f"\nfinished at t={final.tick}: pop={final.population}, "
          f"unique={final.unique_genotypes}, rules={final.rule_diversity}")
    print(f"log:     {log_path}")
    print(f"history: {hist_path}")

    if args.render:
        from viz import load, compute_metrics, render_summary, render_gif
        bits, occ = load(hist_path)
        m = compute_metrics(bits, occ)
        summ = os.path.join(args.outdir, "summary.png")
        gif = os.path.join(args.outdir, "evolution.gif")
        render_summary(m, summ)
        render_gif(bits, occ, m, gif, side=16, fps=10, max_frames=200)
        print(f"render:  {summ}, {gif}")


if __name__ == "__main__":
    main()
