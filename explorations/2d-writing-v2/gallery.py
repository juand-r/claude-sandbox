"""Print the best grids from a feature file (output of score_grids.py).

Usage: gallery.py FEATURES_PKL [-n N] [--max-shared M] [--forms FORMS_PKL]

N grids are shown (default 20). Two shown grids share at most M words
(default: half the cells). With --forms (output of surface_forms.py) the
sentences are printed as they were written in the corpus, with commas.
"""

import argparse
import pickle

from rank import combined_scores, diverse_top
from search import columns, show


def main():
    p = argparse.ArgumentParser()
    p.add_argument("features")
    p.add_argument("-n", type=int, default=20)
    p.add_argument("--max-shared", type=int)
    p.add_argument("--forms")
    args = p.parse_args()
    with open(args.features, "rb") as f:
        feats = pickle.load(f)
    forms = None
    if args.forms:
        with open(args.forms, "rb") as f:
            forms = pickle.load(f)
    cells = len(feats[0]["grid"]) * len(feats[0]["grid"][0])
    max_shared = args.max_shared if args.max_shared is not None else cells // 2
    scores = combined_scores(feats)
    for rank, i in enumerate(diverse_top(feats, scores, args.n, max_shared), 1):
        f = feats[i]
        across, down = f["rows_text"], f["cols_text"]
        if forms:
            across = " ".join(forms[k] for k in f["grid"])
            down = " ".join(forms[k] for k in columns(f["grid"]))
        print(f"#{rank}  score {scores[i]:.2f}  fluency {f['fluency']:.2f}  "
              f"coherence {f['coherence']:.2f}  uncommon words {f['n_content']}  "
              f"min count {f['min_count']}")
        print("```")
        print(show(f["grid"]))
        print("```")
        print(f"Across: {across}")
        print(f"Down: {down}\n")


if __name__ == "__main__":
    main()
