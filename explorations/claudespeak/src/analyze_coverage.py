"""Coverage audit: what slice of Claude behavior do our prompts actually elicit?

Classifies every corpus prompt into an intent taxonomy via Claude, and flags
interaction properties (subjective/opinion, sensitive, implies-multi-turn).
Output quantifies the corpus's coverage and exposes gaps. Cheap: batched
classification, thinking disabled.

Tracks come from per-track manifests (see MANIFESTS). Large diversity tracks
(WildChat, NoRobots) are sub-sampled deterministically to SAMPLE_CAP so the
per-track coverage distributions stay comparable and the cost stays bounded.
Resumable: prompts already present in coverage_labels.csv are not re-labeled.
"""
from __future__ import annotations

import csv
import json
import os
import random
from collections import Counter

from schema import REPO
from generate import _anthropic

TAXONOMY = [
    "factual_qa", "explanation", "instruction_task", "code",
    "creative_writing", "summarize_rewrite_edit", "advice_recommendation",
    "opinion_subjective", "math_reasoning", "personal_emotional",
    "roleplay", "classification_extraction", "other",
]
# track -> (manifest path, sample cap or None for all)
MANIFESTS = {
    "HC3": ("data/sources/hc3_pilot_manifest.jsonl", None),
    "AlpacaEval": ("data/sources/alpaca_pilot_manifest.jsonl", None),
    "WildChat": ("data/sources/wildchat_manifest.jsonl", 400),
    "NoRobots": ("data/sources/norobots_manifest.jsonl", 400),
}
SEED = 42
OUT_CSV = os.path.join(REPO, "data", "corpus", "coverage_labels.csv")

SPEECH_ACT = ["question", "directive", "assertion", "expressive", "other"]
REGISTER = ["formal", "neutral", "casual"]
TONE = ["neutral", "emotional", "playful", "urgent", "hostile"]
TOPIC = ["science_tech", "health_medicine", "finance_business",
         "society_politics", "arts_humanities", "personal_life",
         "education_howto", "software_code", "math_logic", "entertainment",
         "other"]
DIMS = ["category", "speech_act", "register", "tone", "topic"]
FLAGS = ["subjective", "sensitive", "multiturn_implied"]

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


def load_existing():
    """Return {prompt_id: row dict} already labeled, and track_of map."""
    labeled, track_of = {}, {}
    if os.path.exists(OUT_CSV):
        with open(OUT_CSV, newline="") as f:
            for row in csv.DictReader(f):
                labeled[row["prompt_id"]] = row
                track_of[row["prompt_id"]] = row["track"]
    return labeled, track_of


def load_manifests():
    """Return (rows, track_of) where rows = [(track, pid, prompt), ...], with
    deterministic per-track sub-sampling for capped tracks."""
    rows, track_of = [], {}
    for track, (path, cap) in MANIFESTS.items():
        items = []
        with open(os.path.join(REPO, path)) as f:
            for l in f:
                if l.strip():
                    d = json.loads(l)
                    items.append((track, d["prompt_id"], d["prompt"]))
        if cap and len(items) > cap:
            random.Random(SEED).shuffle(items)
            items = items[:cap]
        for it in items:
            track_of[it[1]] = track
        rows.extend(items)
    return rows, track_of


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
    rows, track_of = load_manifests()
    existing, _ = load_existing()
    todo = [r for r in rows if r[1] not in existing]
    print(f"{len(rows)} prompts in scope; {len(existing)} already labeled; "
          f"{len(todo)} to label.")

    labels = {}  # pid -> label obj (new this run)
    CH = 20
    for i in range(0, len(todo), CH):
        chunk = todo[i:i + CH]
        for attempt in range(3):
            try:
                for obj in classify_chunk(chunk):
                    labels[obj["id"]] = obj
                break
            except Exception as e:
                print(f"chunk {i} retry: {type(e).__name__} {str(e)[:80]}")
        print(f"  labeled {len(labels)}/{len(todo)}")

    # merge new labels with existing rows, rewrite full CSV
    merged = dict(existing)  # pid -> row dict (existing already have track)
    for pid, o in labels.items():
        merged[pid] = {"track": track_of.get(pid, "?"), "prompt_id": pid,
                       **{d: o.get(d) for d in DIMS},
                       **{fl: o.get(fl) for fl in FLAGS}}

    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["track", "prompt_id"] + DIMS + FLAGS)
        w.writeheader()
        for row in merged.values():
            w.writerow(row)

    # report distributions over the full (merged) label set
    tracks = list(MANIFESTS)
    rows_by_track = {t: [r for r in merged.values() if r["track"] == t]
                     for t in tracks}
    for dim in DIMS:
        print(f"\n=== {dim} by track ===")
        for t in tracks:
            c = Counter(r.get(dim) for r in rows_by_track[t])
            n = sum(c.values()) or 1
            print(f"[{t}] " + ", ".join(f"{k}:{c2}({100 * c2 // n}%)"
                                        for k, c2 in c.most_common()))
    print("\nflags (count):")
    for t in tracks:
        fc = {fl: sum(1 for r in rows_by_track[t]
                      if str(r.get(fl)).lower() == "true") for fl in FLAGS}
        print(f"[{t}] {fc}")
    print(f"\nwrote {OUT_CSV} ({len(merged)} rows)")


if __name__ == "__main__":
    main()
