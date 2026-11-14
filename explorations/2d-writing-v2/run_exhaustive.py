"""Exhaustive search for grids over OpenSubtitles sentences.

Usage: run_exhaustive.py --rows R --cols C --min-count K [options]

The search is split into --parts independent parts (by a hash of the first two
words of row 0). Each finished part leaves a file in data/runs/<name>/, so an
interrupted run can be restarted and continues with the missing parts. When
all parts are done the grids are collected into grids.pkl in that directory.

Options that restrict the grids:
  --max-repeats N        cells allowed to hold a word already in the grid
  --min-uncommon-line N  every row and column has at least N words outside the
                         --n-common most frequent words
  --min-uncommon N       the whole grid has at least N such words
  --no-names             drop sentences containing a normally capitalized word
"""

import argparse
import os
import pickle
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

from grids import SOLVERS, decode, write_inputs
from ngrams import load_names
from rank import N_COMMON, load_common_words
from sentences import load_opensub


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--rows", type=int, required=True)
    p.add_argument("--cols", type=int, required=True)
    p.add_argument("--min-count", type=int, required=True)
    p.add_argument("--max-repeats", type=int, default=0)
    p.add_argument("--min-uncommon-line", type=int, default=0)
    p.add_argument("--min-uncommon", type=int, default=0)
    p.add_argument("--n-common", type=int, default=N_COMMON)
    p.add_argument("--no-names", action="store_true")
    p.add_argument("--procs", type=int, default=4)
    p.add_argument("--parts", type=int, default=64)
    return p.parse_args()


def load_lines(n, args, common, names):
    """Sentences of n words that satisfy the per-line restrictions."""
    return {s for s in load_opensub(n, args.min_count)
            if sum(w not in common for w in s) >= args.min_uncommon_line
            and (not args.no_names or names.isdisjoint(s))}


def main():
    args = parse_args()
    n_rows, n_cols, n_parts = args.rows, args.cols, args.parts
    name = (f"{n_rows}x{n_cols}_k{args.min_count}_rep{args.max_repeats}"
            f"_ul{args.min_uncommon_line}_u{args.min_uncommon}_c{args.n_common}"
            + ("_nonames" if args.no_names else ""))
    run_dir = f"data/runs/{name}"
    os.makedirs(run_dir, exist_ok=True)
    with open(os.path.join(run_dir, "n_parts"), "a+") as f:
        f.seek(0)
        previous = f.read().strip()
        if previous and int(previous) != n_parts:
            raise SystemExit(f"{run_dir} was started with {previous} parts")
        if not previous:
            f.write(str(n_parts))
    common = load_common_words(n=args.n_common)
    names = load_names() if args.no_names else set()
    row_set = load_lines(n_cols, args, common, names)
    col_set = row_set if n_rows == n_cols else load_lines(n_rows, args, common, names)
    vocab, paths = write_inputs(run_dir, row_set, col_set, {w: 1 for w in common})
    max_cost = n_rows * n_cols - args.min_uncommon
    print(f"{len(row_set)} row sentences, {len(col_set)} column sentences", flush=True)

    def run_part(part):
        out = os.path.join(run_dir, f"part_{part}.txt")
        if os.path.exists(out):
            return
        start = time.time()
        cmd = [SOLVERS["trie"], *paths, n_rows, n_cols, args.max_repeats, max_cost, 0, 0, 0, -1, 0,
               part, n_parts]
        with open(out + ".tmp", "w") as f:
            proc = subprocess.run([str(a) for a in cmd], stdout=f, stderr=subprocess.PIPE,
                                  text=True, check=True)
        with open(os.path.join(run_dir, "log.txt"), "a") as log:
            log.write(f"part {part} {time.time() - start:.0f} s {proc.stderr.strip()}\n")
        os.rename(out + ".tmp", out)

    with ThreadPoolExecutor(args.procs) as pool:
        list(pool.map(run_part, range(n_parts)))
    grids = set()
    for part in range(n_parts):
        with open(os.path.join(run_dir, f"part_{part}.txt")) as f:
            grids |= {decode(line, vocab, n_rows, n_cols) for line in f}
    with open(os.path.join(run_dir, "grids.pkl"), "wb") as f:
        pickle.dump({"grids": sorted(grids), "args": vars(args)}, f)
    print(f"{len(grids)} grids -> {run_dir}/grids.pkl")


if __name__ == "__main__":
    main()
