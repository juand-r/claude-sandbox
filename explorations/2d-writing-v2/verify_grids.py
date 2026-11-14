"""Independent check of a set of grids against the sentence files.

Usage: verify_grids.py GRIDS_OR_FEATURES_PKL MIN_COUNT [MAX_REPEATS]

For every grid, every row and every column must occur in
data/opensub_len{n}.tsv with count >= MIN_COUNT, and at most MAX_REPEATS
(default 0) cells may repeat a word. The check reads the sentence files
directly and does not use the solver or its input files. Exits with an error
on the first violation.
"""

import pickle
import sys


def main():
    path, min_count = sys.argv[1], int(sys.argv[2])
    max_repeats = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    with open(path, "rb") as f:
        data = pickle.load(f)
    if isinstance(data, dict):
        data = data["grids"]
    grids = [d["grid"] if isinstance(d, dict) else d for d in data]
    needed = {" ".join(line) for g in grids for line in list(g) + list(zip(*g))}
    counts = {}
    for n in {len(s.split(" ")) for s in needed}:
        with open(f"data/opensub_len{n}.tsv", encoding="ascii") as f:
            for row in f:
                count, _, text = row.rstrip("\n").split("\t")
                if text in needed:
                    counts[text] = int(count)
    for g in grids:
        for line in list(g) + list(zip(*g)):
            text = " ".join(line)
            if counts.get(text, 0) < min_count:
                raise SystemExit(f"FAIL: '{text}' has count {counts.get(text, 0)} < {min_count}")
        words = [w for row in g for w in row]
        if len(words) - len(set(words)) > max_repeats:
            raise SystemExit(f"FAIL: too many repeated words in {g}")
    print(f"ok: {len(grids)} grids, {len(needed)} distinct sentences, all with count >= {min_count}")


if __name__ == "__main__":
    main()
