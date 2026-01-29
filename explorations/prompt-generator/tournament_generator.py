#!/usr/bin/env python3
"""
Tournament-style prompt generator.

1. Sample N sets of 10 keywords (N must be power of 2)
2. Generate initial texts using keywords, then continue with GPT-2
3. Merge pairs in tournament style until 1 remains
4. Use final merged text to inspire the final prompt
"""

import argparse
import math
import random
import sys
from pathlib import Path

from generator import load_word_list

SCRIPT_DIR = Path(__file__).parent

# Cache pipelines so we don't recreate them on every call
_pipelines: dict[str, object] = {}


def _get_pipeline(model: str, **kwargs) -> object:
    """Get or create a cached pipeline for the given model."""
    if model not in _pipelines:
        from transformers import pipeline
        _pipelines[model] = pipeline("text-generation", model=model, **kwargs)
    return _pipelines[model]


def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def sample_keywords(rng: random.Random, count: int = 10) -> list[str]:
    """Sample random keywords from all word lists."""
    all_words = []
    for name in ["nouns", "verbs", "adjectives"]:
        all_words.extend(load_word_list(name))
    return rng.sample(all_words, min(count, len(all_words)))


def call_qwen(prompt: str, model: str = "Qwen/Qwen2-1.5B-Instruct", max_tokens: int = 200) -> str:
    """Call Qwen model via HuggingFace."""
    pipe = _get_pipeline(model, device_map="auto", trust_remote_code=True)
    messages = [{"role": "user", "content": prompt}]
    result = pipe(messages, max_new_tokens=max_tokens, temperature=1.0, do_sample=True)
    return result[0]["generated_text"][-1]["content"].strip()


def call_gpt2(text: str, max_tokens: int = 200) -> str:
    """Continue text with GPT-2."""
    pipe = _get_pipeline("gpt2", device_map="auto")
    result = pipe(text, max_new_tokens=max_tokens, do_sample=True, temperature=1.0)
    return result[0]["generated_text"]


def generate_initial_text(keywords: list[str], model: str) -> str:
    """Generate initial text using keywords."""
    word_list = ", ".join(keywords)
    prompt = f"I want you to write something creative and surprising. Use these words: {word_list}"
    return call_qwen(prompt, model=model)


def merge_texts(text_a: str, text_b: str, model: str) -> str:
    """Merge two texts harmoniously."""
    prompt = f"""You are inspired by the following two texts. Merge them together harmoniously into a new creative piece.

Text 1:
{text_a}

Text 2:
{text_b}

Now write!"""
    return call_qwen(prompt, model=model)


def judge_creativity(text: str, model: str) -> bool:
    """Judge if text is creative and interesting."""
    prompt = f"""You are a judge evaluating creative writing. Read the following text and decide:
Is this text interesting, creative, original and surprising? Or is it just generic bullshit?

Text:
{text}

Answer with exactly one word: Yes or No"""
    response = call_qwen(prompt, model=model, max_tokens=10)
    # Parse response - look for Yes/No
    response_lower = response.lower().strip()
    return response_lower.startswith("yes")


def build_final_prompt(inspiration: str) -> str:
    """Build final prompt template with inspiration."""
    return f"""You are writing a prompt for an LLM to follow. The prompt must describe a game to build.

Your game description should be inspired by the following:
{inspiration}

Requirements:
- Be original, unique, surprising
- The game must be completable in a single coding session
- It should be playable and fun

Be creative. Be weird. Surprise me.

Start your response with: "Build a game"

Keep it to 2-3 sentences max."""


def run_tournament(n: int, model: str, use_judge: bool, verbose: bool, rng: random.Random) -> str:
    """Run the full tournament process."""

    # Stage 1: Generate N initial texts
    print(f"\n{'='*60}")
    print(f"STAGE 1: Generating {n} initial texts")
    print('='*60)

    texts = []
    for i in range(n):
        keywords = sample_keywords(rng, count=10)
        if verbose:
            print(f"\n[{i+1}/{n}] Keywords: {', '.join(keywords)}")

        # Generate with Qwen
        initial = generate_initial_text(keywords, model)
        if verbose:
            print(f"  Qwen output: {initial[:100]}...")

        # Continue with GPT-2
        continued = call_gpt2(initial, max_tokens=200)
        if verbose:
            print(f"  GPT-2 continued: {continued[:150]}...")

        texts.append(continued)
        print(f"  [{i+1}/{n}] Generated text ({len(continued)} chars)")

    # Stage 2: Tournament merging
    round_num = 0
    while len(texts) > 1:
        round_num += 1
        target_count = len(texts) // 2

        print(f"\n{'='*60}")
        print(f"STAGE 2.{round_num}: Merging {len(texts)} -> {target_count} texts")
        print('='*60)

        merged = []
        attempts = 0
        max_attempts = target_count * 10  # Prevent infinite loops

        while len(merged) < target_count and attempts < max_attempts:
            attempts += 1

            # Sample two texts randomly (with replacement)
            idx_a = rng.randint(0, len(texts) - 1)
            idx_b = rng.randint(0, len(texts) - 1)
            while idx_b == idx_a:
                idx_b = rng.randint(0, len(texts) - 1)

            text_a = texts[idx_a]
            text_b = texts[idx_b]

            if verbose:
                print(f"\n  Attempt {attempts}: Merging texts {idx_a} + {idx_b}")

            # Merge
            result = merge_texts(text_a, text_b, model)

            if use_judge:
                is_creative = judge_creativity(result, model)
                status = "ACCEPTED" if is_creative else "REJECTED"
                print(f"  Judge: {status}")

                if is_creative:
                    merged.append(result)
                    print(f"  [{len(merged)}/{target_count}] Merged text accepted ({len(result)} chars)")
                    if verbose:
                        print(f"\n  --- MERGED TEXT ---")
                        print(f"  {result[:500]}{'...' if len(result) > 500 else ''}")
                        print(f"  --- END ---\n")
                else:
                    if verbose:
                        print(f"  Rejected, trying different pair...")
            else:
                merged.append(result)
                print(f"  [{len(merged)}/{target_count}] Merged text ({len(result)} chars)")
                if verbose:
                    print(f"\n  --- MERGED TEXT ---")
                    print(f"  {result[:500]}{'...' if len(result) > 500 else ''}")
                    print(f"  --- END ---\n")

        if len(merged) < target_count:
            print(f"\n  WARNING: Only got {len(merged)}/{target_count} merges after {max_attempts} attempts")

        texts = merged

    # Stage 3: Final prompt generation
    print(f"\n{'='*60}")
    print("STAGE 3: Generating final prompt")
    print('='*60)

    final_inspiration = texts[0] if texts else ""
    if verbose:
        print(f"\nFinal inspiration text:\n{final_inspiration}\n")

    final_prompt = build_final_prompt(final_inspiration)
    if verbose:
        print(f"Meta-prompt:\n{final_prompt}\n")

    result = call_qwen(final_prompt, model=model)

    # Combine final output with merged text and instruction
    final_output = f"""{result}

---

INSPIRATION TEXT:
{final_inspiration}

---

Build this end to end."""

    return final_output


def main():
    parser = argparse.ArgumentParser(description="Tournament-style prompt generator")
    parser.add_argument("-n", "--count", type=int, default=8,
                        help="Number of initial texts (must be power of 2, default: 8)")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--model", default="Qwen/Qwen2-1.5B-Instruct",
                        help="Qwen model to use (default: Qwen/Qwen2-1.5B-Instruct)")
    parser.add_argument("--judge", action="store_true",
                        help="Use LLM judge to filter uninteresting merges")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show detailed output")
    args = parser.parse_args()

    if not is_power_of_two(args.count):
        print(f"Error: --count must be a power of 2 (got {args.count})", file=sys.stderr)
        sys.exit(1)

    rng = random.Random(args.seed)

    print(f"Tournament Generator")
    print(f"  N = {args.count}")
    print(f"  Model = {args.model}")
    print(f"  Judge = {args.judge}")
    print(f"  Seed = {args.seed}")

    try:
        result = run_tournament(
            n=args.count,
            model=args.model,
            use_judge=args.judge,
            verbose=args.verbose,
            rng=rng,
        )

        print(f"\n{'='*60}")
        print("FINAL RESULT")
        print('='*60)
        print(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
