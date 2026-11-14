"""Aggregate data/opensub_short_counts.txt into one file per sentence length.

Writes data/opensub_len{n}.tsv with lines "count<TAB>punct<TAB>words", for
sentences of n words whose total count is at least MIN_COUNT.

Also writes data/word_counts.pkl: a Counter of word frequencies over the
sentences of WORD_COUNT_LENGTHS words, each weighted by its count. rank.py
uses it to define the "common" words.
"""

import pickle
import re
from collections import Counter

MIN_COUNT = 3
LENGTHS = range(2, 8)
WORD_COUNT_LENGTHS = (3, 4, 5, 6)
WORD_RE = re.compile(r"[a-z]+(?:'[a-z]+)*")


def main():
    out = {n: open(f"data/opensub_len{n}.tsv", "w") for n in LENGTHS}
    kept = dict.fromkeys(LENGTHS, 0)

    def flush(text, by_punct):
        total = sum(by_punct.values())
        words = text.split(" ")
        if total >= MIN_COUNT and len(words) in out and all(WORD_RE.fullmatch(w) for w in words):
            out[len(words)].write(f"{total}\t{max(by_punct, key=by_punct.get)}\t{text}\n")
            kept[len(words)] += 1

    prev, by_punct = None, {}
    with open("data/opensub_short_counts.txt", encoding="ascii") as f:
        for line in f:
            head, punct = line.rstrip("\n").split("\t")
            count, _, text = head.lstrip().partition(" ")
            if text != prev:
                if prev is not None:
                    flush(prev, by_punct)
                prev, by_punct = text, {}
            by_punct[punct] = by_punct.get(punct, 0) + int(count)
    flush(prev, by_punct)
    for f in out.values():
        f.close()
    print(kept)
    write_word_counts()


def write_word_counts():
    counts = Counter()
    for n in WORD_COUNT_LENGTHS:
        with open(f"data/opensub_len{n}.tsv", encoding="ascii") as f:
            for line in f:
                count, _, text = line.rstrip("\n").split("\t")
                for w in text.split(" "):
                    counts[w] += int(count)
    with open("data/word_counts.pkl", "wb") as f:
        pickle.dump(counts, f)


if __name__ == "__main__":
    main()
