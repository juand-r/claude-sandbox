# 2D Writing System

Generate word grids that read as coherent text in both dimensions.

## Quick Start

```bash
pip install nltk numpy
python grid2d.py
```

## Example Output

4x4 grid where rows are sentences and columns are word lists:

```
i    know a    man
we   have the  world
they feel that way
you  see  her  face
```

**Rows:** "i know a man" / "we have the world" / "they feel that way" / "you see her face"

**Columns:** pronouns / verbs / determiners / nouns

## How It Works

1. Train n-gram language model on Brown corpus
2. Use beam search with grammatical constraints per column
3. Require unique words per column to force diversity

See `NOTES.md` for detailed findings.
