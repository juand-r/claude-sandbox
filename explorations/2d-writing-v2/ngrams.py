"""N-gram rules that generalize the attested sentences (see ngram.c).

A line w_1..w_L is admissible for order k if its first k words begin some
attested sentence, its last k words end one, and every k-word window in
between occurs somewhere in an attested sentence.
"""

import os
import pickle
from collections import Counter

SENTENCE_LENGTHS = range(3, 8)
# Capitalized words that are not names and may appear in grids.
KEEP_CAPITALIZED = {"i", "i'm", "i'll", "i've", "i'd"}


def load_names(path="data/caps.tsv"):
    """Words that are normally capitalized (names, places, days), minus "I"."""
    with open(path) as f:
        return {line.split("\t")[0] for line in f} - KEEP_CAPITALIZED


def build_kgrams(k, min_count, data_dir="data"):
    """Return (P, M, F): k-grams that begin, occur in, and end sentences.

    Counts are summed over all OpenSubtitles sentences of 3 to 7 words; a
    k-gram is kept if its count in the given role is at least min_count and
    it contains no name. The result is cached in data_dir.
    """
    cache = os.path.join(data_dir, f"kgrams_k{k}_min{min_count}.pkl")
    if os.path.exists(cache):
        with open(cache, "rb") as f:
            return pickle.load(f)
    names = load_names(os.path.join(data_dir, "caps.tsv"))
    begin, inside, end = Counter(), Counter(), Counter()
    for n in SENTENCE_LENGTHS:
        if n < k:
            continue
        with open(os.path.join(data_dir, f"opensub_len{n}.tsv"), encoding="ascii") as f:
            for line in f:
                count, _, text = line.rstrip("\n").split("\t")
                words, count = tuple(text.split(" ")), int(count)
                begin[words[:k]] += count
                end[words[-k:]] += count
                for i in range(n - k + 1):
                    inside[words[i:i + k]] += count
    result = tuple({g for g, c in counter.items() if c >= min_count and names.isdisjoint(g)}
                   for counter in (begin, inside, end))
    with open(cache, "wb") as f:
        pickle.dump(result, f)
    return result


def admissible(line, k, begin, inside, end):
    """Whether a tuple of words satisfies the order-k rules."""
    n = len(line)
    return (n > k and line[:k] in begin and line[-k:] in end
            and all(line[i:i + k] in inside for i in range(1, n - k)))
