"""Load corpora of real sentences and normalize them to tuples of words.

A "sentence key" is a tuple of lowercase words with punctuation removed.
Apostrophes inside words are kept ("don't"). Sentences with digits or any
other non-letter material are dropped, so every key can be shown as plain words.
"""

import bz2
import re
from collections import Counter

WORD_RE = re.compile(r"[a-z]+(?:'[a-z]+)*")
# Characters allowed in a raw sentence besides letters and apostrophes.
ALLOWED_RE = re.compile(r"^[a-z' .,!?;:\"-]+$")


def normalize(text):
    """Return the tuple of words of `text`, or None if it has odd characters."""
    text = text.lower().replace("’", "'").strip()
    if not ALLOWED_RE.match(text):
        return None
    return tuple(WORD_RE.findall(text))


def load_tatoeba(path):
    """Counter of sentence keys from a Tatoeba per-language TSV (id, lang, text)."""
    counts = Counter()
    with bz2.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            key = normalize(line.rstrip("\n").split("\t", 2)[2])
            if key:
                counts[key] += 1
    return counts


def by_length(counts):
    """Group sentence keys by number of words: {n: Counter}."""
    groups = {}
    for key, c in counts.items():
        groups.setdefault(len(key), Counter())[key] = c
    return groups
