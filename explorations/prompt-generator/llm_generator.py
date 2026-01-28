#!/usr/bin/env python3
"""
LLM-powered prompt generator — uses a language model to create wild, original prompts.
"""

import argparse
import json
import random
import subprocess
import sys
from pathlib import Path

from generator import DOMAINS, FORMATS, CONSTRAINTS, TWISTS, load_word_list

SCRIPT_DIR = Path(__file__).parent


def sample_words(rng: random.Random, nouns: int = 3, verbs: int = 2, adjectives: int = 1) -> dict:
    """Sample random words from each category."""
    words = {
        "nouns": load_word_list("nouns"),
        "verbs": load_word_list("verbs"),
        "adjectives": load_word_list("adjectives"),
    }
    return {
        "nouns": rng.sample(words["nouns"], min(nouns, len(words["nouns"]))),
        "verbs": rng.sample(words["verbs"], min(verbs, len(words["verbs"]))),
        "adjectives": rng.sample(words["adjectives"], min(adjectives, len(words["adjectives"]))),
    }


def sample_structure(rng: random.Random) -> dict:
    """Sample domain, format, constraint, and twist."""
    return {
        "domain": rng.choice(DOMAINS),
        "format": rng.choice(FORMATS),
        "constraint": rng.choice(CONSTRAINTS),
        "twist": rng.choice(TWISTS),
    }


def build_meta_prompt(sampled_words: dict, structure: dict) -> str:
    """Build the prompt we send to the LLM."""
    word_list = ", ".join(sampled_words["nouns"] + sampled_words["verbs"] + sampled_words["adjectives"])

    return f"""You are writing a prompt for an LLM to follow. The prompt must describe a software project to build.

Base idea: {structure['domain']}
Format: {structure['format']}
Constraint: {structure['constraint']}
Twist: {structure['twist']}

Additional requirements:
- Be original, unique, surprising
- The project must be completable in a single coding session
- Incorporate the base idea, format, constraint, and twist creatively
- MUST incorporate these wild card words somehow: {word_list}

Be creative. Be weird. Surprise me.

Start your response with: "Build {structure['domain']}"

Keep it to 2-3 sentences max."""


def call_ollama(prompt: str, model: str = "llama3.2") -> str:
    """Call ollama CLI to generate response."""
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            raise RuntimeError(f"ollama error: {result.stderr}")
        return result.stdout.strip()
    except FileNotFoundError:
        raise RuntimeError("ollama not found. Install from https://ollama.ai")


def call_openai_compatible(prompt: str, base_url: str, api_key: str, model: str) -> str:
    """Call OpenAI-compatible API."""
    import urllib.request

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 1.0,
    }).encode()

    req = urllib.request.Request(f"{base_url}/chat/completions", data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
        return result["choices"][0]["message"]["content"].strip()


def call_huggingface(prompt: str, model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0") -> str:
    """Run inference using Hugging Face transformers."""
    try:
        from transformers import pipeline
    except ImportError:
        raise RuntimeError("transformers not installed. Run: pip install transformers torch")

    pipe = pipeline("text-generation", model=model, device_map="auto", trust_remote_code=True)

    # Format as chat for instruction-tuned models
    messages = [{"role": "user", "content": prompt}]

    result = pipe(messages, max_new_tokens=200, temperature=1.0, do_sample=True)
    return result[0]["generated_text"][-1]["content"].strip()


def generate_prompt(rng: random.Random, backend: str = "huggingface", model: str = None,
                    base_url: str = None, api_key: str = None,
                    nouns: int = 3, verbs: int = 2, adjectives: int = 1,
                    verbose: bool = False) -> str | dict:
    """Generate a prompt using an LLM. Returns dict with details if verbose=True."""
    sampled_words = sample_words(rng, nouns=nouns, verbs=verbs, adjectives=adjectives)
    structure = sample_structure(rng)
    meta_prompt = build_meta_prompt(sampled_words, structure)

    if backend == "huggingface":
        output = call_huggingface(meta_prompt, model or "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    elif backend == "ollama":
        output = call_ollama(meta_prompt, model or "llama3.2")
    elif backend == "openai":
        output = call_openai_compatible(
            meta_prompt,
            base_url or "https://api.openai.com/v1",
            api_key or "",
            model or "gpt-4o-mini",
        )
    else:
        raise ValueError(f"Unknown backend: {backend}")

    if verbose:
        return {
            "sampled_words": sampled_words,
            "structure": structure,
            "meta_prompt": meta_prompt,
            "output": output,
        }
    return output


def print_verbose(result: dict):
    """Print verbose output showing all intermediate steps."""
    words = result["sampled_words"]
    structure = result["structure"]

    print("=" * 60)
    print("SAMPLED WORDS:")
    print(f"  nouns:      {', '.join(words['nouns'])}")
    print(f"  verbs:      {', '.join(words['verbs'])}")
    print(f"  adjectives: {', '.join(words['adjectives'])}")
    print()
    print("SAMPLED STRUCTURE:")
    print(f"  domain:     {structure['domain']}")
    print(f"  format:     {structure['format']}")
    print(f"  constraint: {structure['constraint']}")
    print(f"  twist:      {structure['twist']}")
    print()
    print("META-PROMPT TO LLM:")
    print("-" * 40)
    print(result["meta_prompt"])
    print("-" * 40)
    print()
    print("LLM OUTPUT:")
    print(result["output"])
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Generate prompts using an LLM")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of prompts")
    parser.add_argument("--seed", type=int, help="Random seed for word selection")
    parser.add_argument("--backend", choices=["huggingface", "ollama", "openai"], default="huggingface",
                        help="LLM backend (default: huggingface)")
    parser.add_argument("--model", help="Model name (default: TinyLlama for hf, llama3.2 for ollama)")
    parser.add_argument("--base-url", help="API base URL for openai backend")
    parser.add_argument("--api-key", help="API key for openai backend")
    parser.add_argument("--nouns", type=int, default=3, help="Number of random nouns (default: 3)")
    parser.add_argument("--verbs", type=int, default=2, help="Number of random verbs (default: 2)")
    parser.add_argument("--adjectives", type=int, default=1, help="Number of random adjectives (default: 1)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show all intermediate steps")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    for i in range(args.count):
        if args.count > 1:
            print(f"\n[{i + 1}]")
        try:
            result = generate_prompt(
                rng,
                backend=args.backend,
                model=args.model,
                base_url=args.base_url,
                api_key=args.api_key,
                nouns=args.nouns,
                verbs=args.verbs,
                adjectives=args.adjectives,
                verbose=args.verbose,
            )
            if args.verbose:
                print_verbose(result)
            else:
                print(result)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
