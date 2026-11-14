"""Print the best grids from a feature file (output of score_grids.py).

Usage: gallery.py FEATURES_PKL [N [MAX_SHARED]]
N grids are shown (default 20). Two shown grids share at most MAX_SHARED
words (default: half the cells).
"""

import pickle
import sys

from rank import combined_scores, diverse_top
from search import show


def main():
    with open(sys.argv[1], "rb") as f:
        feats = pickle.load(f)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    cells = len(feats[0]["grid"]) * len(feats[0]["grid"][0])
    max_shared = int(sys.argv[3]) if len(sys.argv) > 3 else cells // 2
    scores = combined_scores(feats)
    for rank, i in enumerate(diverse_top(feats, scores, n, max_shared), 1):
        f = feats[i]
        print(f"#{rank}  score {scores[i]:.2f}  fluency {f['fluency']:.2f}  "
              f"coherence {f['coherence']:.2f}  uncommon words {f['n_content']}  "
              f"min count {f['min_count']}")
        print("```")
        print(show(f["grid"]))
        print("```")
        print(f"Across: {f['rows_text']}")
        print(f"Down: {f['cols_text']}\n")


if __name__ == "__main__":
    main()
