"""Write docs/gallery.md: the best grids of each scored set.

Usage: make_gallery.py

For each entry of SETS the top grids are chosen as in gallery.py. Sentences
are shown as most often written in the corpus; the lookup needs one pass over
the raw corpus (about 4 minutes) and is cached in data/forms_gallery.pkl.
"""

import os
import pickle

from rank import combined_scores, diverse_top, load_caps, recase
from search import columns, show
from surface_forms import find_surface_forms

# (title, feature file, number of grids to show, description of the run)
SETS = [
    ("4x4, sentences seen 7+ times, at least 5 uncommon words", "data/feat_4x4_k7_u5.pkl", 15,
     "no names; uncommon = outside the 300 most frequent words"),
    ("4x4, sentences seen 10+ times, at least 4 uncommon words", "data/feat_4x4_k10_u4.pkl", 15,
     "no names; uncommon = outside the 300 most frequent words"),
    ("4x4, sentences seen 20+ times", "data/feat_4x4_k20.pkl", 10, "names allowed"),
    ("4x5, sentences seen 10+ times", "data/feat_4x5_k10.pkl", 12, "no names"),
    ("3x5, rows seen 10+ times, columns 100+ times", "data/feat_3x5_k10_kc100.pkl", 10, "no names"),
    ("3x5, sentences seen 20+ times, at least 2 uncommon words", "data/feat_3x5_k20.pkl", 6,
     "no names; uncommon = outside the 200 most frequent words"),
    ("3x6, sentences seen 10+ times", "data/feat_3x6_k10.pkl", 6,
     "no names; many 3-word columns are fragments, see the report"),
]
FORMS_CACHE = "data/forms_gallery.pkl"
OUT = "docs/gallery.md"


def main():
    chosen = []
    for title, path, n, note in SETS:
        if not os.path.exists(path):
            print(f"skipping {path}: not found")
            continue
        with open(path, "rb") as f:
            feats = pickle.load(f)
        cells = len(feats[0]["grid"]) * len(feats[0]["grid"][0])
        scores = combined_scores(feats)
        top = [feats[i] for i in diverse_top(feats, scores, n, cells // 2)]
        chosen.append((title, note, len(feats), top))

    forms = {}
    if os.path.exists(FORMS_CACHE):
        with open(FORMS_CACHE, "rb") as f:
            forms = pickle.load(f)
    keys = {k for _, _, _, top in chosen for f in top for k in list(f["grid"]) + list(columns(f["grid"]))}
    if keys - set(forms):
        forms.update(find_surface_forms(keys - set(forms)))
        with open(FORMS_CACHE, "wb") as f:
            pickle.dump(forms, f)
    missing = keys - set(forms)
    if missing:
        raise RuntimeError(f"sentences not found in the corpus: {sorted(missing)[:3]}")

    caps = load_caps()
    forms = {k: recase(v, caps) for k, v in forms.items()}
    with open(OUT, "w") as out:
        out.write("# Gallery\n\nBest grids of each scored set, chosen by `make_gallery.py` "
                  "(combined score of `rank.py`, near duplicates removed). Every row and "
                  "every column is a sentence from the OpenSubtitles corpus; all words in a "
                  "grid are distinct. Sentences are shown with the punctuation they most "
                  "often have in the corpus.\n")
        for title, note, n_scored, top in chosen:
            out.write(f"\n## {title}\n\n{n_scored} grids scored; {note}.\n")
            for f in top:
                across = " ".join(forms[k] for k in f["grid"])
                down = " ".join(forms[k] for k in columns(f["grid"]))
                out.write(f"\n```\n{show(f['grid'])}\n```\n\nAcross: {across}\n\nDown: {down}\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
