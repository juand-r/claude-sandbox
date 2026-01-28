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

SCRIPT_DIR = Path(__file__).parent


def load_word_list(name: str) -> list[str]:
    """Load a word list from the words/ directory."""
    path = SCRIPT_DIR / "words" / f"{name}.txt"
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


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


def build_meta_prompt(sampled: dict) -> str:
    """Build the prompt we send to the LLM."""
    word_list = ", ".join(sampled["nouns"] + sampled["verbs"] + sampled["adjectives"])

    return f"""You are writing a prompt for an LLM to follow. The prompt must describe a software project to build.

Requirements:
- Be original, unique, surprising
- The project must be completable in a single coding session
- Include a clear deliverable (CLI tool, web app, API, bot, etc.)
- Add an unexpected twist or constraint
- MUST incorporate these words somehow: {word_list}

Be creative. Be weird. Surprise me.

Start your response with: "You are a fantastic programmer. I want you to create a"

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


def generate_prompt(rng: random.Random, backend: str = "ollama", model: str = None,
                    base_url: str = None, api_key: str = None) -> str:
    """Generate a prompt using an LLM."""
    sampled = sample_words(rng)
    meta_prompt = build_meta_prompt(sampled)

    if backend == "ollama":
        return call_ollama(meta_prompt, model or "llama3.2")
    elif backend == "openai":
        return call_openai_compatible(
            meta_prompt,
            base_url or "https://api.openai.com/v1",
            api_key or "",
            model or "gpt-4o-mini",
        )
    else:
        raise ValueError(f"Unknown backend: {backend}")


def main():
    parser = argparse.ArgumentParser(description="Generate prompts using an LLM")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of prompts")
    parser.add_argument("--seed", type=int, help="Random seed for word selection")
    parser.add_argument("--backend", choices=["ollama", "openai"], default="ollama",
                        help="LLM backend (default: ollama)")
    parser.add_argument("--model", help="Model name (default: llama3.2 for ollama, gpt-4o-mini for openai)")
    parser.add_argument("--base-url", help="API base URL for openai backend")
    parser.add_argument("--api-key", help="API key for openai backend")
    args = parser.parse_args()

    rng = random.Random(args.seed)

    for i in range(args.count):
        if args.count > 1:
            print(f"\n[{i + 1}]")
        try:
            print(generate_prompt(
                rng,
                backend=args.backend,
                model=args.model,
                base_url=args.base_url,
                api_key=args.api_key,
            ))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
