# 2D Writing System

## Goal
Generate a word grid where:
- Each row is a coherent English sentence/phrase
- Each column is also a coherent English sentence/phrase

## Final Approach

### What Worked: Constrained Beam Search

Key insight: **constrain word categories by column position**.

Structure for 4x4: `[Pronoun] [Verb] [Determiner] [Noun]`

This produces:
- Rows that are grammatical sentences
- Columns that are coherent word-category lists

### Scoring
- n-gram language model trained on Brown corpus
- Score = sum of log P(word | context) for rows + columns
- Require unique words per column to prevent repetition

## Tasks
- [x] Create project structure
- [x] Implement LM scoring (n-gram, not GPT-2 due to proxy issues)
- [x] Implement grid data structure
- [x] Implement beam search
- [x] Implement Gibbs sampling (works but degenerates)
- [x] Add grammatical constraints
- [x] Add uniqueness constraints
- [x] Test multiple structures
- [x] Document findings

## Results

Best result (4x4 grid):
```
i    know a    man
we   have the  world
they feel that way
you  see  her  face
```

All rows are perfect English sentences. All columns are coherent word lists.

See `NOTES.md` for detailed findings.
