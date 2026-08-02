"""
Test LLM consistency on colexification-ambiguous sentences.

For each source sentence containing a colexifying word, ask Claude Haiku
to translate it to English multiple times. Record which word it chooses
for the ambiguous concept.
"""

import json
import time
import os
import re
import subprocess

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-4-5-20251001"
N_RUNS = 5  # translations per sentence

DATA_FILE = "/home/claude/colexdiv/data/test_sentences.json"
OUT_FILE = "/home/claude/colexdiv/data/haiku_results.json"


def call_api(source_text, source_lang, target_lang="en"):
    """Call Claude Haiku to translate a sentence."""
    lang_names = {"ru": "Russian", "es": "Spanish", "ja": "Japanese", "en": "English"}
    src_name = lang_names.get(source_lang, source_lang)
    tgt_name = lang_names.get(target_lang, target_lang)

    prompt = (
        f"Translate the following {src_name} sentence into {tgt_name}. "
        f"Give only the translation, nothing else.\n\n{source_text}"
    )

    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 200,
        "messages": [{"role": "user", "content": prompt}],
    })

    cmd = [
        "curl", "-s", API_URL,
        "-H", "Content-Type: application/json",
        "-H", "x-api-key: " + os.environ.get("ANTHROPIC_API_KEY", ""),
        "-H", "anthropic-version: 2023-06-01",
        "-d", payload,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        resp = json.loads(result.stdout)
        if "content" in resp and resp["content"]:
            return resp["content"][0].get("text", "").strip()
        elif "error" in resp:
            return f"[ERROR: {resp['error'].get('message', 'unknown')}]"
        else:
            return f"[UNEXPECTED: {result.stdout[:200]}]"
    except json.JSONDecodeError:
        return f"[PARSE_ERROR: {result.stdout[:200]}]"


def detect_concept(translation, concept_a, concept_b):
    """Check which concept word appears in the translation."""
    t_lower = translation.lower()
    has_a = concept_a.lower() in t_lower
    has_b = concept_b.lower() in t_lower
    if has_a and not has_b:
        return concept_a
    elif has_b and not has_a:
        return concept_b
    elif has_a and has_b:
        return "both"
    else:
        return "neither"


def main():
    with open(DATA_FILE) as f:
        sentences = json.load(f)

    print(f"Loaded {len(sentences)} test sentences")
    print(f"Model: {MODEL}")
    print(f"Runs per sentence: {N_RUNS}")
    print()

    results = []

    for i, sent in enumerate(sentences):
        sid = sent["id"]
        source = sent["source"]
        src_lang = sent["source_lang"]
        concept_a = sent["concept_a"]
        concept_b = sent["concept_b"]

        print(f"[{i+1}/{len(sentences)}] {sid}: {source[:50]}...")

        translations = []
        choices = []

        for run in range(N_RUNS):
            translation = call_api(source, src_lang)
            choice = detect_concept(translation, concept_a, concept_b)
            translations.append(translation)
            choices.append(choice)
            print(f"  Run {run+1}: {translation[:60]}  -> {choice}")
            time.sleep(1)  # rate limiting

        # Consistency analysis
        unique_choices = set(choices)
        consistent = len(unique_choices) == 1

        result = {
            "id": sid,
            "pair": sent["pair"],
            "source": source,
            "source_lang": src_lang,
            "concept_a": concept_a,
            "concept_b": concept_b,
            "disambiguation": sent["disambiguation"],
            "translations": translations,
            "choices": choices,
            "consistent": consistent,
            "dominant_choice": max(set(choices), key=choices.count),
            "choice_distribution": {c: choices.count(c) for c in set(choices)},
        }
        results.append(result)
        print(f"  => {'CONSISTENT' if consistent else 'INCONSISTENT'}: {result['choice_distribution']}")
        print()

    # Save results
    with open(OUT_FILE, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for pair_name in ["LEG/FOOT", "WOMAN/WIFE", "HEAR/LISTEN"]:
        pair_results = [r for r in results if r["pair"] == pair_name]
        n_consistent = sum(1 for r in pair_results if r["consistent"])
        n_total = len(pair_results)
        print(f"\n{pair_name}: {n_consistent}/{n_total} sentences consistent across {N_RUNS} runs")
        for r in pair_results:
            status = "OK" if r["consistent"] else "INCONSISTENT"
            print(f"  {r['id']}: {r['choice_distribution']}  [{status}]  disambig={r['disambiguation']}")

    print(f"\nResults saved to {OUT_FILE}")


if __name__ == "__main__":
    main()
