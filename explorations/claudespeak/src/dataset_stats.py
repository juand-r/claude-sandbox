"""Reproducible dataset statistics for the Claudespeak corpus.

Computes, for every track (HC3, AlpacaEval, WildChat, NoRobots, ...) and source:
  - volume: #prompts, #records, total response words & sentences;
  - prompt-length and response-length distributions (mean/median/p25/p75);
  - per-domain volume;
  - sentence-mood split (interrogative / imperative / exclamatory / declarative)
    for prompts and responses -> the "questions vs declaratives" view;
  - register signals: 1st/2nd-person pronoun rates, Flesch Reading Ease;
  - intent-taxonomy distribution + coverage flags (from analyze_coverage.py, if run).

Writes reports/dataset_stats.md and CSVs under data/corpus/. All from saved
records; no API calls.
"""
from __future__ import annotations

import glob
import os
import re
import statistics as st
from collections import Counter, defaultdict

import pandas as pd

from schema import read_records, CORPUS_DIR, REPO

REPORTS = os.path.join(REPO, "reports")
WORD = re.compile(r"[A-Za-z']+")
SENT = re.compile(r"[^.!?]*[.!?]+|\S[^.!?]*$")
WH = {"what", "why", "how", "when", "where", "who", "whom", "whose", "which"}
AUX = {"is", "are", "was", "were", "do", "does", "did", "can", "could", "would",
       "should", "will", "shall", "may", "might", "has", "have", "had", "am"}
IMPERATIVE_VERBS = {"write", "explain", "describe", "list", "give", "make",
                    "create", "tell", "summarize", "translate", "compare",
                    "generate", "provide", "name", "find", "calculate", "draft",
                    "suggest", "compose", "outline", "define", "show", "design",
                    "recommend", "convert", "rewrite", "consider", "imagine"}
P1 = {"i", "me", "my", "mine", "we", "us", "our", "ours", "myself"}
P2 = {"you", "your", "yours", "yourself", "yourselves"}


# Display order for tracks; any dataset not listed is appended alphabetically.
TRACK_ORDER = ["HC3", "AlpacaEval", "WildChat", "NoRobots"]


def track_of(rec) -> str:
    return (rec.get("prompt_source") or {}).get("dataset") or "?"


def tracks_present(recs):
    present = {r["_track"] for r in recs}
    ordered = [t for t in TRACK_ORDER if t in present]
    ordered += sorted(present - set(ordered))
    return ordered


def sentences(text: str):
    return [s.strip() for s in SENT.findall(text or "") if s.strip()]


def mood(sent: str) -> str:
    s = sent.strip()
    first = (WORD.findall(s.lower()) or [""])[0]
    if s.endswith("?") or first in WH or (first in AUX):
        return "interrogative"
    if s.endswith("!"):
        return "exclamatory"
    if first in IMPERATIVE_VERBS:
        return "imperative"
    return "declarative"


def prompt_mood(prompt: str) -> str:
    """Primary speech-act/mood of a whole prompt (syntactic heuristic)."""
    p = (prompt or "").strip()
    first = (WORD.findall(p.lower()) or [""])[0]
    if "?" in p or first in WH or first in AUX:
        return "interrogative"
    if first in IMPERATIVE_VERBS:
        return "imperative"
    return "declarative"


def syllables(word: str) -> int:
    w = word.lower()
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and n > 1:
        n -= 1
    return max(n, 1)


def flesch(text: str) -> float:
    sents = sentences(text)
    words = WORD.findall(text or "")
    if not sents or not words:
        return float("nan")
    syl = sum(syllables(w) for w in words)
    return 206.835 - 1.015 * (len(words) / len(sents)) - 84.6 * (syl / len(words))


def dist(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return {}
    qs = st.quantiles(vals, n=4) if len(vals) > 1 else [vals[0]] * 3
    return {"n": len(vals), "mean": round(st.mean(vals), 1),
            "median": round(st.median(vals), 1),
            "p25": round(qs[0], 1), "p75": round(qs[2], 1)}


def main():
    os.makedirs(REPORTS, exist_ok=True)
    recs = []
    for p in sorted(glob.glob(os.path.join(CORPUS_DIR, "*.jsonl"))):
        recs += read_records(p)

    for r in recs:
        r["_track"] = track_of(r)
        r["_rwords"] = len(WORD.findall(r["completion"] or ""))
        r["_rsents"] = len(sentences(r["completion"]))

    TRACKS = tracks_present(recs)

    # unique prompts (dedupe by prompt_id) for prompt-side stats
    seen, prompts = set(), []
    for r in recs:
        if r["prompt_id"] not in seen:
            seen.add(r["prompt_id"])
            prompts.append(r)

    lines = ["# Corpus statistics (reproducible: src/dataset_stats.py)\n"]

    # 1. volume + response length by track and source
    lines.append("## 1. Volume and response length by source\n")
    rows = []
    for t in TRACKS:
        for g in sorted({r["generator"] for r in recs if r["_track"] == t}):
            sub = [r for r in recs if r["_track"] == t and r["generator"] == g]
            d = dist([r["_rwords"] for r in sub])
            rows.append({"track": t, "source": g, "records": len(sub),
                         "resp_words_total": sum(r["_rwords"] for r in sub),
                         "resp_words_mean": d["mean"], "resp_words_median": d["median"],
                         "resp_words_p25": d["p25"], "resp_words_p75": d["p75"]})
    vol = pd.DataFrame(rows)
    vol.to_csv(os.path.join(CORPUS_DIR, "stats_volume.csv"), index=False)
    lines.append(vol.to_markdown(index=False) + "\n")

    # 2. prompt-length stats by track (unique prompts)
    lines.append("## 2. Prompt length by track (unique prompts)\n")
    prows = []
    for t in TRACKS:
        pl = [len(WORD.findall(r["prompt"] or "")) for r in prompts if r["_track"] == t]
        nq = sum(1 for r in prompts if r["_track"] == t and "?" in (r["prompt"] or ""))
        d = dist(pl)
        prows.append({"track": t, "prompts": d.get("n"),
                      "prompt_words_mean": d.get("mean"),
                      "prompt_words_median": d.get("median"),
                      "prompt_words_p25": d.get("p25"), "prompt_words_p75": d.get("p75"),
                      "pct_with_question_mark": round(100 * nq / max(d.get("n", 1), 1))})
    lines.append(pd.DataFrame(prows).to_markdown(index=False) + "\n")

    # 2b. PROMPT mood / speech act (syntactic), per track — the coverage view
    lines.append("## 2b. Prompt mood (syntactic; % of unique prompts)\n")
    lines.append("Questions vs declaratives etc. for the PROMPTS (what we ask Claude).\n")
    pm = []
    for t in TRACKS:
        c = Counter(prompt_mood(r["prompt"]) for r in prompts if r["_track"] == t)
        n = sum(c.values()) or 1
        pm.append({"track": t,
                   "interrogative%": round(100 * c["interrogative"] / n),
                   "imperative%": round(100 * c["imperative"] / n),
                   "declarative%": round(100 * c["declarative"] / n)})
    pd.DataFrame(pm).to_csv(os.path.join(CORPUS_DIR, "stats_prompt_mood.csv"), index=False)
    lines.append(pd.DataFrame(pm).to_markdown(index=False) + "\n")

    # 3. per-domain volume (response words summed across sources)
    lines.append("## 3. Volume by domain (response words, all sources)\n")
    dom = defaultdict(lambda: {"prompts": set(), "words": 0, "records": 0})
    for r in recs:
        key = (r["_track"], r.get("domain") or "?")
        dom[key]["prompts"].add(r["prompt_id"])
        dom[key]["words"] += r["_rwords"]
        dom[key]["records"] += 1
    drows = [{"track": t, "domain": d, "prompts": len(v["prompts"]),
              "records": v["records"], "resp_words_total": v["words"]}
             for (t, d), v in sorted(dom.items())]
    pd.DataFrame(drows).to_csv(os.path.join(CORPUS_DIR, "stats_domain.csv"), index=False)
    lines.append(pd.DataFrame(drows).to_markdown(index=False) + "\n")

    # 4. sentence-mood split (responses) by source
    lines.append("## 4. Sentence mood in responses by source "
                 "(% of sentences; questions vs declaratives etc.)\n")
    mrows = []
    for t in TRACKS:
        for g in sorted({r["generator"] for r in recs if r["_track"] == t}):
            cnt = Counter()
            for r in recs:
                if r["_track"] == t and r["generator"] == g:
                    for s in sentences(r["completion"]):
                        cnt[mood(s)] += 1
            tot = sum(cnt.values()) or 1
            mrows.append({"track": t, "source": g,
                          "interrog%": round(100 * cnt["interrogative"] / tot),
                          "imper%": round(100 * cnt["imperative"] / tot),
                          "exclam%": round(100 * cnt["exclamatory"] / tot),
                          "declar%": round(100 * cnt["declarative"] / tot)})
    pd.DataFrame(mrows).to_csv(os.path.join(CORPUS_DIR, "stats_mood.csv"), index=False)
    lines.append(pd.DataFrame(mrows).to_markdown(index=False) + "\n")

    # 5. register: pronoun rates + readability by source
    lines.append("## 5. Register signals by source (per 100 words; Flesch readability)\n")
    rr = []
    for t in TRACKS:
        for g in sorted({r["generator"] for r in recs if r["_track"] == t}):
            sub = [r for r in recs if r["_track"] == t and r["generator"] == g]
            words = [w for r in sub for w in WORD.findall((r["completion"] or "").lower())]
            nw = len(words) or 1
            p1 = sum(1 for w in words if w in P1)
            p2 = sum(1 for w in words if w in P2)
            fre = st.mean([flesch(r["completion"]) for r in sub
                           if r["_rwords"] > 5] or [float("nan")])
            rr.append({"track": t, "source": g,
                       "first_person_per100": round(100 * p1 / nw, 2),
                       "second_person_per100": round(100 * p2 / nw, 2),
                       "flesch": round(fre, 1)})
    pd.DataFrame(rr).to_csv(os.path.join(CORPUS_DIR, "stats_register.csv"), index=False)
    lines.append(pd.DataFrame(rr).to_markdown(index=False) + "\n")

    # 6. PROMPT variety along every audited dimension (from analyze_coverage.py)
    cov = os.path.join(CORPUS_DIR, "coverage_labels.csv")
    if os.path.exists(cov):
        cl = pd.read_csv(cov)
        lines.append("## 6. Prompt variety by dimension (counts of 200 per track)\n")
        for dim in ["category", "speech_act", "register", "tone", "topic"]:
            if dim in cl.columns:
                tab = cl.groupby(["track", dim]).size().unstack(fill_value=0).T
                lines.append(f"\n### {dim}\n")
                lines.append(tab.to_markdown() + "\n")
        fl = cl.groupby("track")[["subjective", "sensitive", "multiturn_implied"]].sum()
        lines.append("\n### interaction flags (count)\n\n" + fl.to_markdown() + "\n")
    else:
        lines.append("## 6. Prompt variety\n\n"
                     "_Run src/analyze_coverage.py first to populate._\n")

    with open(os.path.join(REPORTS, "dataset_stats.md"), "w") as f:
        f.write("\n".join(lines))
    print("\n".join(lines[:1]))
    print(vol.to_string(index=False))
    print("\nwrote reports/dataset_stats.md + stats_*.csv")


if __name__ == "__main__":
    main()
