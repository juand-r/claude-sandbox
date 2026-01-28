# Prompt Generator

Generates random, surprising project prompts for future explorations. Two modes:

1. **Template mode** (`generator.py`) — combines random elements from predefined lists
2. **LLM mode** (`llm_generator.py`) — uses a language model for truly wild prompts

## Template Mode

```bash
python generator.py           # Generate one prompt
python generator.py -n 5      # Generate multiple prompts
python generator.py --seed 42 # Reproducible output
python generator.py --no-wild # Without wild card words
```

## LLM Mode (wilder)

Uses an LLM to generate original prompts, seeded with random words.

```bash
# With Hugging Face (default) — pip install transformers torch
python llm_generator.py                              # Uses TinyLlama by default
python llm_generator.py --model Qwen/Qwen2-0.5B-Instruct  # Different model
python llm_generator.py -n 3                         # Multiple prompts

# With ollama
python llm_generator.py --backend ollama --model llama3.2

# With OpenAI-compatible API
python llm_generator.py --backend openai --api-key $OPENAI_API_KEY
```

The LLM receives a meta-prompt like:
> "You are writing a prompt for an LLM. Be original, unique, surprising.
> MUST incorporate these words: {random nouns, verbs, adjectives}..."

## Example Output

```
Challenge: a file organizer as a REST API. Must be with vim keybindings,
but it speaks/reads aloud.

🎲 Wild cards — incorporate these somehow: nouns: democracies, feast,
distraction; verbs: rehearsed, drank; adjectives: seated
```

## How It Works

Combines random elements from:
- **Domains** - What to build (tracker, manager, etc.)
- **Formats** - How to deliver (CLI, API, bot, etc.)
- **Constraints** - Limitations (100 LOC, no deps, etc.)
- **Twists** - Unexpected angles (plain text storage, gamification, etc.)

Plus **wild cards** sampled from 10k-word lists of nouns, verbs, and adjectives to inject randomness and force creative thinking.

## Customizing

- Edit the lists in `generator.py` to change domains/formats/constraints/twists
- Replace files in `words/` to use different vocabulary
- Word lists from [david47k/top-english-wordlists](https://github.com/david47k/top-english-wordlists)
