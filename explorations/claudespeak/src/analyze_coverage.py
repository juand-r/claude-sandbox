"""Coverage audit: what slice of Claude behavior do our prompts actually elicit?

Classifies every pilot prompt (HC3 + AlpacaEval) into an intent taxonomy via
Claude, and flags interaction properties (subjective/opinion, sensitive,
implies-multi-turn). Output quantifies the current corpus's coverage and exposes
gaps. Cheap: batched classification, effort=low.
"""
from __future__ import annotations

import glob
import json
import os
from collections import Counter

from schema import REPO
from generate import _anthropic

TAXONOMY = [
    "factual_qa", "explanation", "instruction_task", "code",
    "creative_writing", "summarize_rewrite_edit", "advice_recommendation",
    "opinion_subjective", "math_reasoning", "personal_emotional",
    "roleplay", "classification_extraction", "other",
]
MANIFESTS = {
    "HC3": "data/sources/hc3_pilot_manifest.jsonl",
    "AlpacaEval": "data/sources/alpaca_pilot_manifest.jsonl",
}
OUT_CSV = os.path.join(REPO, "data", "corpus", "coverage_labels.csv")

SPEECH_ACT = ["question", "directive", "assertion", "expressive", "other"]
REGISTER = ["formal", "neutral", "casual"]
TONE = ["neutral", "emotional", "playful", "urgent", "hostile"]
TOPIC = ["science_tech", "health_medicine", "finance_business",
         "society_politics", "arts_humanities", "personal_life",
         "education_howto", "software_code", "math_logic", "entertainment",
         "other"]

SYS = (
    "You characterize USER PROMPTS for a corpus-coverage audit. For each prompt "
    "return, from fixed lists:\n"
    "- category (primary intent): " + ", ".join(TAXONOMY) + "\n"
    "- speech_act (its dominant illocutionary force): " + ", ".join(SPEECH_ACT) +
    " (question=asks; directive=command/request to do something; "
    "assertion=states a claim/opinion; expressive=feelings/venting)\n"
    "- register: " + ", ".join(REGISTER) + "\n"
    "- tone: " + ", ".join(TONE) + "\n"
    "- topic: " + ", ".join(TOPIC) + "\n"
    "and booleans: subjective (asks for opinion/values/taste), "
    "sensitive (safety/medical/legal/controversial), multiturn_implied (only "
    "fully answerable via back-and-forth, correction, or follow-up).\n"
    "Return ONLY a JSON array of objects {id, category, speech_act, register, "
    "tone, topic, subjective, sensitive, multiturn_implied}."
)


def load():
    rows = []
    for track, path in MANIFESTS.items():
        for l in open(os.path.join(REPO, path)):
            if l.strip():
                d = json.loads(l)
                rows.append((track, d["prompt_id"], d["prompt"]))
    return rows


def classify_chunk(chunk):
    payload = [{"id": pid, "prompt": p[:1200]} for _, pid, p in chunk]
    msg = ("Label these prompts. Return JSON array only.\n"
           + json.dumps(payload, ensure_ascii=False))
    r = _anthropic().messages.create(
        model="claude-opus-4-8", max_tokens=4000,
        thinking={"type": "disabled"},
        system=SYS, messages=[{"role": "user", "content": msg}])
    txt = "".join(b.text for b in r.content if getattr(b, "type", None) == "text")
    txt = txt[txt.find("["): txt.rfind("]") + 1]
    return json.loads(txt)


def main():
    rows = load()
    track_of = {pid: t for t, pid, _ in rows}
    labels = {}
    CH = 20
    for i in range(0, len(rows), CH):
        chunk = rows[i:i + CH]
        for attempt in range(3):
            try:
                for obj in classify_chunk(chunk):
                    labels[obj["id"]] = obj
                break
            except Exception as e:
                print(f"chunk {i} retry: {type(e).__name__} {str(e)[:80]}")
        print(f"  labeled {len(labels)}/{len(rows)}")

    # aggregate
    import csv
    dims = ["category", "speech_act", "register", "tone", "topic"]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["track", "prompt_id"] + dims +
                   ["subjective", "sensitive", "multiturn_implied"])
        for pid, o in labels.items():
            w.writerow([track_of.get(pid, "?"), pid]
                       + [o.get(d) for d in dims]
                       + [o.get("subjective"), o.get("sensitive"),
                          o.get("multiturn_implied")])

    def dist_by_track(dim):
        d = {t: Counter() for t in MANIFESTS}
        for pid, o in labels.items():
            d[track_of.get(pid, "?")][o.get(dim)] += 1
        return d

    for dim in dims:
        print(f"\n=== {dim} by track ===")
        d = dist_by_track(dim)
        for t in MANIFESTS:
            n = sum(d[t].values()) or 1
            print(f"[{t}] " + ", ".join(f"{k}:{c}({100*c//n}%)"
                                        for k, c in d[t].most_common()))
    flags = {t: Counter() for t in MANIFESTS}
    for pid, o in labels.items():
        for fl in ("subjective", "sensitive", "multiturn_implied"):
            if o.get(fl):
                flags[track_of.get(pid, "?")][fl] += 1
    print("\nflags:", {t: dict(flags[t]) for t in MANIFESTS})
    print(f"\nwrote {OUT_CSV}")


if __name__ == "__main__":
    main()
