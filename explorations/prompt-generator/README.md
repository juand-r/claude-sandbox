# Prompt Generator

Generates random, surprising project prompts for future explorations by combining elements from different categories, plus random "wild card" words to force creative connections.

## Run

```bash
python generator.py           # Generate one prompt
python generator.py -n 5      # Generate multiple prompts
python generator.py --seed 42 # Reproducible output
python generator.py --no-wild # Without wild card words
python generator.py --nouns 5 --verbs 3 --adjectives 2  # Custom counts
```

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
