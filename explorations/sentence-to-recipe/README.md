# Sentence-to-Recipe Translator

Translates any sentence into a culinary recipe based on its meaning. Abstract concepts become flavor profiles, emotions become cooking techniques.

## Usage

```bash
# Basic usage (requires ollama with llama3.2)
python translator.py "Love is patient and kind"

# With cook's mood (influences recipe character)
python translator.py "The storm clouds gathered on the horizon" --mood melancholy

# Using OpenAI API
python translator.py "Time flies when you're having fun" --backend openai --api-key YOUR_KEY

# Using Hugging Face (local, no API needed)
python translator.py "Anger burns like fire" --backend huggingface
```

## How It Works

The translator interprets sentences through a culinary lens:

- **Emotions** (love, anger, sadness) → Flavor profiles and heat levels
- **Abstract concepts** (time, memory, freedom) → Cooking techniques
- **Colors and imagery** → Visual presentation and garnishes
- **Numbers/time references** → Cooking times and temperatures
- **Nouns and actions** → Ingredients and methods

## Output Format

Each recipe includes:
1. **Title** - Creative name echoing the sentence
2. **Essence** - How the recipe embodies the sentence's meaning
3. **Ingredients** - With quantities, each subtly connected to the input
4. **Preparation** - Step-by-step numbered instructions
5. **Assembly** - Final plating instructions
6. **Chef's Note** - How eating the dish might affect the diner

## Requirements

One of:
- `ollama` with a model like `llama3.2` (default)
- OpenAI API key (use `--backend openai --api-key KEY`)
- `transformers` and `torch` for Hugging Face (use `--backend huggingface`)

## Examples

Input: `"Love is patient and kind"`
→ Recipe featuring gentle, warm flavors with vanilla, honey, and lavender

Input: `"The deadline looms like a storm"`
→ Recipe with intense spices, dark reduction sauces, and nervous energy in the plating

Input: `"Cook for 1 hour at high heat while remembering summer"`
→ Recipe incorporating the literal instruction with nostalgic summer herbs
