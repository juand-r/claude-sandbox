"""Interpretable stylometric features for one text.

Dependency-light (stdlib + numbers). Each feature is a rate (per 100 words or
per sentence) so texts of different lengths are comparable. Grouped by family:
lexical, punctuation/orthography, syntax, markdown/structure, rhetoric, and
known-LLM lexical tics. See PLAN.md S3a.

The goal is characterization, not just detection: these features are meant to be
read, so the eventual "Claudeisms" tables name *what* differs, not just that it
does.
"""
from __future__ import annotations

import re
from collections import Counter

WORD_RE = re.compile(r"[A-Za-z']+")
SENT_SPLIT = re.compile(r"[.!?]+(?:\s|$)")

# A compact closed-class function-word list (stylometry staple — content-free,
# so it tracks style not topic).
FUNCTION_WORDS = set("""
a an the this that these those of in on at by for with about against between into
through during to from up down and but or nor so yet because although though while
i you he she it we they me him her us them my your his its our their is are was were
be been being have has had do does did will would shall should can could may might
must not no as if then than too very just also more most much many such only own same
""".split())

HEDGES = set("""
may might could can would often sometimes generally typically usually perhaps
possibly likely probably somewhat relatively fairly arguably tends seem seems
appears suggest suggests potentially essentially fundamentally
""".split())

# Lexical tics commonly attributed to LLM / Claude prose.
TICS = ["delve", "tapestry", "crucial", "boast", "realm", "navigate", "leverage",
        "underscore", "showcase", "intricate", "nuanced", "robust", "holistic",
        "meticulous", "seamless", "vibrant", "testament", "pivotal", "elevate",
        "foster", "myriad", "garner", "endeavor", "embark"]

# Canned discourse openers/markers (matched as phrases, case-insensitive).
CANNED = [
    r"it's worth noting", r"it is worth noting", r"i'd be happy to",
    r"i would be happy to", r"certainly[!,. ]", r"great question",
    r"i hope this helps", r"keep in mind", r"that said", r"in summary",
    r"in conclusion", r"importantly", r"ultimately", r"it's important to",
    r"it is important to", r"as an ai", r"i'm just an ai",
]


def _safe(n, d):
    return n / d if d else 0.0


def features(text: str) -> dict:
    t = text or ""
    low = t.lower()
    words = WORD_RE.findall(low)
    nw = len(words)
    sents = [s for s in SENT_SPLIT.split(t) if s.strip()]
    ns = max(len(sents), 1)
    sent_word_counts = [len(WORD_RE.findall(s)) for s in sents] or [0]

    # lexical
    types = set(words)
    counts = Counter(words)
    hapax = sum(1 for w, c in counts.items() if c == 1)
    fw = sum(1 for w in words if w in FUNCTION_WORDS)
    hedge = sum(1 for w in words if w in HEDGES)

    # sentence-length burstiness = std/mean of words-per-sentence
    mean_swc = _safe(sum(sent_word_counts), len(sent_word_counts))
    var = _safe(sum((x - mean_swc) ** 2 for x in sent_word_counts),
                len(sent_word_counts))
    burstiness = _safe(var ** 0.5, mean_swc)

    f = {
        # size (context, not style — kept for length controls)
        "n_words": float(nw),
        "n_sentences": float(ns),
        "mean_sentence_len": mean_swc,
        "sentence_burstiness": burstiness,
        # lexical (style)
        "ttr": _safe(len(types), nw),
        "hapax_rate": _safe(hapax, nw),
        "function_word_rate": _safe(fw, nw),       # fraction of tokens
        "hedge_rate_per100": _safe(hedge, nw) * 100,
        # punctuation / orthography (per 100 words)
        "emdash_per100": _safe(t.count("—") + t.count(" - "), nw) * 100,
        "comma_per100": _safe(t.count(","), nw) * 100,
        "semicolon_per100": _safe(t.count(";"), nw) * 100,
        "colon_per100": _safe(t.count(":"), nw) * 100,
        "exclaim_per100": _safe(t.count("!"), nw) * 100,
        "question_per100": _safe(t.count("?"), nw) * 100,
        "emoji_per100": _safe(len(re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", t)), nw) * 100,
        # markdown / structure
        "md_header_per100w": _safe(len(re.findall(r"(?m)^\s{0,3}#{1,6}\s", t)), nw) * 100,
        "md_bullet_per100w": _safe(len(re.findall(r"(?m)^\s*([-*+]|\d+\.)\s", t)), nw) * 100,
        "md_bold_per100w": _safe(len(re.findall(r"\*\*[^*]+\*\*", t)), nw) * 100,
        "md_code_per100w": _safe(t.count("```"), nw) * 100,
        # rhetoric
        "tricolon_per100w": _safe(len(re.findall(r"\w+,\s+\w+,\s+and\s+\w+", low)), nw) * 100,
        "not_just_but_per1k": _safe(len(re.findall(r"not (just|only)\b.{0,40}?\bbut\b", low)), nw) * 1000,
    }
    # canned phrases (per 1000 words, summed)
    canned = sum(len(re.findall(p, low)) for p in CANNED)
    f["canned_phrase_per1k"] = _safe(canned, nw) * 1000
    # lexical tics (per 1000 words, summed)
    tic = sum(counts.get(w, 0) for w in TICS)
    f["lexical_tic_per1k"] = _safe(tic, nw) * 1000
    return f


FEATURE_NAMES = list(features("x. y.").keys())
# style features only (exclude raw size) for ranking
STYLE_FEATURES = [k for k in FEATURE_NAMES if k not in ("n_words", "n_sentences")]


if __name__ == "__main__":
    import json
    demo = ("Certainly! It's worth noting that good coffee is a tapestry of "
            "flavor, aroma, and balance. Delve into the crucial details:\n\n"
            "- Fresh beans\n- Right grind\n\nNot just any water, but filtered water.")
    print(json.dumps(features(demo), indent=2))
