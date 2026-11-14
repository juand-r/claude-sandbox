"""Aggregate data/opensub_short_counts.txt into one file per sentence length.

Writes data/opensub_len{n}.tsv with lines "count<TAB>punct<TAB>words", for
sentences of n words whose total count is at least MIN_COUNT.
"""

import re

MIN_COUNT = 3
LENGTHS = range(2, 8)
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


if __name__ == "__main__":
    main()
