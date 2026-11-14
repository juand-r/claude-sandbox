"""Find words that are normally capitalized (names, "I", ...).

Reads the first N_LINES lines of the OpenSubtitles file and counts, for every
word that is not the first word of its line, how often it is capitalized.
Writes data/caps.tsv with lines "lowercase<TAB>Capitalized form" for words
capitalized in more than THRESHOLD of at least MIN_SEEN occurrences.
"""

import gzip
import re
from collections import Counter

N_LINES = 30_000_000
THRESHOLD = 0.8
MIN_SEEN = 20
TOKEN_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)*")


def main():
    seen, capitalized, form = Counter(), Counter(), {}
    with gzip.open("data/opensub_en.txt.gz", "rt", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if i >= N_LINES:
                break
            for tok in TOKEN_RE.findall(line)[1:]:
                low = tok.lower()
                seen[low] += 1
                if tok[0].isupper() and not tok.isupper() or tok == "I":
                    capitalized[low] += 1
                    form[low] = tok
    with open("data/caps.tsv", "w") as out:
        for w, n in seen.items():
            if n >= MIN_SEEN and capitalized[w] / n > THRESHOLD:
                out.write(f"{w}\t{form[w]}\n")


if __name__ == "__main__":
    main()
