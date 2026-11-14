"""Recover how sentences were written in the corpus (commas, capitals, marks).

The sentence sets store lowercase words only. For display we look up the most
frequent original spelling of each sentence in the raw OpenSubtitles file.

Usage as a script: surface_forms.py FEATURES_PKL N OUT_PKL
  collects the row and column sentences of the top N diverse grids of a
  feature file (as gallery.py would show them) and writes {key: raw form}.
"""

import pickle
import subprocess
import sys
from collections import Counter

# Same line filter as extract_opensub.sh.
PIPELINE = ("zcat data/opensub_en.txt.gz | LC_ALL=C grep -E \"^[A-Z][A-Za-z' ,]*[.?!]$\" "
            "| awk 'NF >= 2 && NF <= 7'")


def find_surface_forms(keys):
    """Return {key: most frequent raw line} for the given word tuples."""
    wanted = {" ".join(k) for k in keys}
    forms = {}
    proc = subprocess.Popen(PIPELINE, shell=True, stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        raw = line.rstrip("\n")
        norm = " ".join(raw[:-1].replace(",", "").lower().split())
        if norm in wanted:
            forms.setdefault(norm, Counter())[raw] += 1
    if proc.wait() != 0:
        raise RuntimeError("corpus scan failed")
    return {tuple(norm.split(" ")): counts.most_common(1)[0][0] for norm, counts in forms.items()}


def main():
    from rank import combined_scores, diverse_top
    from search import columns

    with open(sys.argv[1], "rb") as f:
        feats = pickle.load(f)
    n = int(sys.argv[2])
    cells = len(feats[0]["grid"]) * len(feats[0]["grid"][0])
    top = diverse_top(feats, combined_scores(feats), n, cells // 2)
    keys = {k for i in top for k in list(feats[i]["grid"]) + list(columns(feats[i]["grid"]))}
    forms = find_surface_forms(keys)
    missing = keys - set(forms)
    if missing:
        raise RuntimeError(f"{len(missing)} sentences not found in the corpus, e.g. {sorted(missing)[:3]}")
    with open(sys.argv[3], "wb") as f:
        pickle.dump(forms, f)
    print(f"{len(forms)} sentences")


if __name__ == "__main__":
    main()
