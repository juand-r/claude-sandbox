"""Compute ranking features (rank.py) for a file of grids.

Usage: score_grids.py GRIDS_PKL MIN_COUNT OUT_PKL [MIN_UNCOMMON]

With MIN_UNCOMMON, only grids with at least that many words outside the
common-word list are scored (the language model is slow, so large sets need a
cheap first cut).

GRIDS_PKL holds {"grids": [...]} (output of run_exhaustive.py) or a plain
list of grids. Sentences are looked up in the OpenSubtitles sets with the
given minimum count. A grid and its transpose are scored once. Features are
computed in chunks and OUT_PKL is rewritten after each chunk, so a killed run
can be restarted and continues where it stopped.
"""

import os
import pickle
import sys

import torch

from lm import Scorer
from rank import canonical, features, load_caps, load_common_words
from sentences import load_opensub

CHUNK = 500


def main():
    grids_path, min_count, out_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    torch.set_num_threads(int(os.environ.get("LM_THREADS", "1")))
    with open(grids_path, "rb") as f:
        data = pickle.load(f)
    grids = data["grids"] if isinstance(data, dict) else data
    grids = sorted({canonical(g) for g in grids})
    common = load_common_words()
    if len(sys.argv) > 4:
        min_uncommon = int(sys.argv[4])
        grids = [g for g in grids if sum(w not in common for row in g for w in row) >= min_uncommon]
    print(f"{len(grids)} grids to score", flush=True)
    lengths = {len(grids[0]), len(grids[0][0])}
    sentence_sets = {n: load_opensub(n, min_count) for n in lengths}
    done = []
    if os.path.exists(out_path):
        with open(out_path, "rb") as f:
            done = pickle.load(f)
    scorer, caps = Scorer(), load_caps()
    for start in range(len(done), len(grids), CHUNK):
        done += features(grids[start:start + CHUNK], sentence_sets, scorer, caps, common)
        with open(out_path + ".tmp", "wb") as f:
            pickle.dump(done, f)
        os.replace(out_path + ".tmp", out_path)
        print(f"{len(done)}/{len(grids)}", flush=True)


if __name__ == "__main__":
    main()
