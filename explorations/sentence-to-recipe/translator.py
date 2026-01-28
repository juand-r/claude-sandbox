#!/usr/bin/env python3
"""
Sentence-to-Recipe Translator

Translates any sentence into a culinary recipe based on its meaning.
Abstract concepts become flavor profiles, emotions become cooking techniques.
"""

import argparse
import json
import subprocess
import sys


# Mapping of emotional/abstract concepts to culinary elements
CONCEPT_MAPPINGS = {
    # Emotions → Flavor profiles
    "love": "sweet, warm, comforting flavors with hints of vanilla and honey",
    "anger": "fiery spices, bold chilies, intense heat",
    "sadness": "mellow, subtle flavors with lavender and chamomile",
    "joy": "bright citrus, fresh herbs, effervescent textures",
    "fear": "dark, bitter notes with unexpected spice",
    "peace": "gentle herbs, calming lavender, smooth textures",
    "passion": "rich, decadent chocolate with warming spices",
    "nostalgia": "homey flavors, cinnamon, nutmeg, brown butter",

    # Abstract concepts → Techniques
    "time": "slow-cooked, aged, fermented elements",
    "memory": "preserved ingredients, pickled, smoked",
    "chaos": "contrasting textures and unexpected combinations",
    "order": "precisely measured, symmetrically plated",
    "freedom": "rustic presentation, foraging-inspired ingredients",
    "power": "bold proteins, reduction sauces, structured plating",
}

# Keywords to naturally incorporate
CULINARY_KEYWORDS = [
    "lavender", "spices", "saffron", "truffle", "reduction",
    "infusion", "emulsion", "caramelized", "herb-crusted"
]


def build_translation_prompt(sentence: str, mood: str = None) -> str:
    """Build the prompt for recipe translation."""

    mood_note = ""
    if mood:
        mood_note = f"\nThe cook's current mood is: {mood}. Let this subtly influence the recipe's character."

    return f"""You are a culinary poet who translates sentences into recipes. Your task is to interpret the meaning,
emotion, and imagery of a sentence and transform it into a delicious, evocative recipe.

SENTENCE TO TRANSLATE: "{sentence}"
{mood_note}

INTERPRETATION RULES:
- Abstract concepts (love, time, memory) become flavor profiles and textures
- Emotions become cooking techniques and heat levels
- Colors become visual garnishes and ingredient choices
- Actions in the sentence can inspire cooking methods
- Numbers or time references should appear in cooking times/temperatures
- Nouns can inspire ingredient choices

REQUIRED ELEMENTS:
- Use aromatic elements like lavender, spices, or herbs where fitting
- Include at least one unexpected twist that reflects the sentence's deeper meaning
- The recipe should feel like a metaphor made edible

OUTPUT FORMAT (follow exactly):

# [Creative Recipe Title that echoes the sentence]

## Essence
[1-2 sentences capturing how this recipe embodies the sentence's meaning]

## Ingredients
[List ingredients with quantities, each ingredient subtly connected to the sentence]

## Preparation
[Step-by-step instructions, numbered, with cooking times/temperatures where appropriate]

## Assembly
[Final plating/assembly instructions]

## Chef's Note
[A brief philosophical note on how eating this dish might affect the diner based on their state of mind]

---

Generate the recipe now. Be creative, evocative, and specific with measurements and times."""


def call_ollama(prompt: str, model: str = "llama3.2") -> str:
    """Call ollama CLI to generate response."""
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=120,
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
        "max_tokens": 1500,
        "temperature": 0.9,
    }).encode()

    req = urllib.request.Request(f"{base_url}/chat/completions", data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode())
        return result["choices"][0]["message"]["content"].strip()


def call_huggingface(prompt: str, model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0") -> str:
    """Run inference using Hugging Face transformers."""
    try:
        from transformers import pipeline
    except ImportError:
        raise RuntimeError("transformers not installed. Run: pip install transformers torch")

    pipe = pipeline("text-generation", model=model, device_map="auto", trust_remote_code=True)
    messages = [{"role": "user", "content": prompt}]
    result = pipe(messages, max_new_tokens=1500, temperature=0.9, do_sample=True)
    return result[0]["generated_text"][-1]["content"].strip()


def translate_sentence(sentence: str, mood: str = None, backend: str = "ollama",
                       model: str = None, base_url: str = None, api_key: str = None) -> str:
    """Translate a sentence into a recipe."""
    prompt = build_translation_prompt(sentence, mood)

    if backend == "huggingface":
        return call_huggingface(prompt, model or "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    elif backend == "ollama":
        return call_ollama(prompt, model or "llama3.2")
    elif backend == "openai":
        if not api_key:
            raise ValueError("OpenAI backend requires --api-key")
        return call_openai_compatible(
            prompt,
            base_url or "https://api.openai.com/v1",
            api_key,
            model or "gpt-4o-mini",
        )
    else:
        raise ValueError(f"Unknown backend: {backend}")


def main():
    parser = argparse.ArgumentParser(
        description="Translate sentences into culinary recipes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Love is patient and kind"
  %(prog)s "The quick brown fox jumps over the lazy dog" --mood anxious
  %(prog)s "Cook for 1 hour at high heat while thinking of summer" --backend openai --api-key KEY
        """
    )
    parser.add_argument("sentence", help="The sentence to translate into a recipe")
    parser.add_argument("--mood", help="Cook's current mood (influences recipe character)")
    parser.add_argument("--backend", choices=["huggingface", "ollama", "openai"],
                        default="ollama", help="LLM backend (default: ollama)")
    parser.add_argument("--model", help="Model name override")
    parser.add_argument("--base-url", help="API base URL for openai backend")
    parser.add_argument("--api-key", help="API key for openai backend")
    args = parser.parse_args()

    try:
        recipe = translate_sentence(
            args.sentence,
            mood=args.mood,
            backend=args.backend,
            model=args.model,
            base_url=args.base_url,
            api_key=args.api_key,
        )
        print(recipe)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
