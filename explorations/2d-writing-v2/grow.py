"""Grow a grid step by step. Lines are sequences of sentences (see multi.py).

Each step adds a few columns or a few rows to the current grid, keeping all
earlier cells. The solver samples several ways to do it; the language model
picks one (fluency plus a bonus for uncommon words). Steps alternate between
columns and rows and the run stops when no tried step size works in either
direction. A step that the random search cannot do is tried exhaustively, so
a stop can be a proof that no extension exists (for these sentences).

Usage:
  grow.py SEED_FILE OUT_JSON [--min-counts "{3:50,4:10,...}"] [--steps 3 4 5]
          [--samples 10] [--max-nodes N] [--exhaustive-nodes N]
          [--restart-nodes N] [--max-repeats 0] [--ban-file FILE]

SEED_FILE: the starting grid, one row per line, words separated by spaces.
OUT_JSON: log of every stage (grid, cutting of each line, score, search
  statistics). Rewritten after each stage, so a stopped run keeps its results.
"""

import argparse
import ast
import json
import time

from lm import Scorer
from multi import cuttings, load_sentences, run_extend, usable_sentences
from rank import load_caps, load_common_words, surface
from search import columns
from sentences import load_opensub

N_PROCS = 4
SEED_MIN_COUNT = 3   # the seed's own sentences are accepted from this count
W_UNCOMMON = 1.0     # weight of the share of uncommon words among new cells


def line_text(line, sentences, caps):
    """The line as written: its sentences with capitals and final marks."""
    return " ".join(surface(key, sentences[key][1], caps) for key in cuttings(tuple(line), sentences))


def fluency(grid, sentences, caps, scorer):
    """Mean log-probability per token over all rows and columns."""
    texts = [line_text(line, sentences, caps) for line in tuple(grid) + columns(grid)]
    scores = scorer.logprobs(texts)
    return sum(lp for lp, _ in scores) / sum(n for _, n in scores)


def add_seed_sentences(seed, sentences):
    """Make sure the lines of the seed can be cut into known sentences, adding
    attested sentences with a count below the general thresholds if needed."""
    for line in tuple(seed) + columns(seed):
        if cuttings(tuple(line), sentences) is None:
            info = load_opensub(len(line), SEED_MIN_COUNT).get(tuple(line))
            if info is None:
                raise SystemExit(f"seed line {' '.join(line)!r} is not an attested sentence")
            sentences[tuple(line)] = info


def stage_record(grid, sentences, caps, score, extra):
    return {"n_rows": len(grid), "n_cols": len(grid[0]), "grid": [list(r) for r in grid],
            "rows_text": [line_text(r, sentences, caps) for r in grid],
            "cols_text": [line_text(c, sentences, caps) for c in columns(grid)],
            "fluency": score, **extra}


def new_cells(grid, old):
    """Words of `grid` outside its top-left block of the size of `old`."""
    return [w for r, row in enumerate(grid) for c, w in enumerate(row)
            if r >= len(old) or c >= len(old[0])]


def try_step(grid, direction, step, sentences, args, rng_seed):
    """Sample extensions of `grid` by `step` rows or columns.

    Returns (grids, info). If sampling finds nothing, an exhaustive search
    follows; info["proved_none"] is True if it finished without a solution."""
    # The solver fills cells row by row, which is fast when the new block is
    # narrow. To add rows we transpose, add columns, and transpose back (rows
    # and columns use the same sentences).
    flip = direction == "rows"
    seed = columns(grid) if flip else grid
    usable = usable_sentences(sentences, seed) if args.max_repeats == 0 else sentences
    start = time.time()
    common = dict(seed_grid=seed, max_repeats=args.max_repeats, max_solutions=args.samples)
    grids, _ = run_extend(usable, len(seed), len(seed[0]) + step, max_nodes=args.max_nodes,
                          seed=rng_seed, restart_nodes=args.restart_nodes, n_procs=N_PROCS,
                          **common)
    info = {"direction": direction, "step": step, "usable_sentences": len(usable),
            "proved_none": False}
    if not grids:
        grids, exhaustive = run_extend(usable, len(seed), len(seed[0]) + step,
                                       max_nodes=args.exhaustive_nodes, **common)
        info["proved_none"] = exhaustive and not grids
    info["candidates"], info["seconds"] = len(grids), round(time.time() - start)
    return [columns(g) for g in grids] if flip else grids, info


def main():
    p = argparse.ArgumentParser()
    p.add_argument("seed_file")
    p.add_argument("out_json")
    p.add_argument("--min-counts", default="{3: 50, 4: 10, 5: 10, 6: 10, 7: 10}")
    p.add_argument("--steps", type=int, nargs="+", default=[3, 4, 5])
    p.add_argument("--samples", type=int, default=10, help="solutions per process and step")
    p.add_argument("--max-nodes", type=int, default=100_000_000,
                   help="node limit of the random search, per process and step")
    p.add_argument("--exhaustive-nodes", type=int, default=20_000_000_000,
                   help="node limit of the exhaustive search that follows a failed random search")
    p.add_argument("--restart-nodes", type=int, default=200_000)
    p.add_argument("--max-repeats", type=int, default=0)
    p.add_argument("--rng-seed", type=int, default=1)
    p.add_argument("--ban-file", help="words that may not appear, one per line")
    args = p.parse_args()

    with open(args.seed_file) as f:
        grid = tuple(tuple(line.split()) for line in f if line.strip())
    sentences = load_sentences(ast.literal_eval(args.min_counts))
    if args.ban_file:
        with open(args.ban_file) as f:
            banned = set(f.read().split())
        sentences = {k: v for k, v in sentences.items() if banned.isdisjoint(k)}
    add_seed_sentences(grid, sentences)
    caps, scorer, common = load_caps(), Scorer(), load_common_words()
    print(f"{len(sentences)} sentences", flush=True)

    stages = [stage_record(grid, sentences, caps, fluency(grid, sentences, caps, scorer), {})]
    failures = []
    direction, failed, rng_seed = "cols", set(), args.rng_seed
    while len(failed) < 2:
        found = False
        for step in args.steps:
            grids, info = try_step(grid, direction, step, sentences, args, rng_seed)
            rng_seed += N_PROCS
            print(f"{len(grid)}x{len(grid[0])} + {step} {direction}: {info}", flush=True)
            if not grids:
                failures.append({"n_rows": len(grid), "n_cols": len(grid[0]), **info})
                continue
            # Choose by fluency plus a bonus for uncommon words in the new
            # cells: they read better and leave common words for later steps.
            def score(g):
                added = new_cells(g, grid)
                uncommon = sum(w not in common for w in added) / len(added)
                return fluency(g, sentences, caps, scorer) + W_UNCOMMON * uncommon
            grid = max(grids, key=score)
            stages.append(stage_record(grid, sentences, caps,
                                       fluency(grid, sentences, caps, scorer), info))
            for row in stages[-1]["rows_text"]:
                print("   ", row, flush=True)
            found = True
            break
        if found:
            failed.clear()
        else:
            failed.add(direction)
        with open(args.out_json, "w") as f:
            json.dump({"args": vars(args), "stages": stages, "failures": failures}, f, indent=1)
        direction = "rows" if direction == "cols" else "cols"
    print(f"final size {len(grid)}x{len(grid[0])}")


if __name__ == "__main__":
    main()
