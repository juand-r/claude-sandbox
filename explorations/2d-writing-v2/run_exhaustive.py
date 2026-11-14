"""Exhaustive search for square grids over OpenSubtitles sentences.

Usage: run_exhaustive.py N MIN_COUNT MAX_REPEATS [N_PROCS]
Writes data/grids_{N}x{N}_k{MIN_COUNT}_rep{MAX_REPEATS}.pkl with
{"grids": [...], "exhaustive": bool, "seconds": float, "n_sentences": int}.
"""

import pickle
import sys
import time

from grids import run_solver
from sentences import load_opensub


def main():
    n, min_count, max_repeats = (int(x) for x in sys.argv[1:4])
    n_procs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    sentences = load_opensub(n, min_count)
    start = time.time()
    grids, exhaustive = run_solver(sentences, sentences, n, n, max_repeats=max_repeats,
                                   n_procs=n_procs, verbose=True)
    seconds = time.time() - start
    out = f"data/grids_{n}x{n}_k{min_count}_rep{max_repeats}.pkl"
    with open(out, "wb") as f:
        pickle.dump({"grids": grids, "exhaustive": exhaustive, "seconds": seconds,
                     "n_sentences": len(sentences)}, f)
    print(f"{len(sentences)} sentences, {len(grids)} grids, exhaustive={exhaustive}, "
          f"{seconds:.0f} s -> {out}")


if __name__ == "__main__":
    main()
