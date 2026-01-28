# 2D Writing System - Findings

## Goal
Generate an NxN word grid where:
- Each row reads as coherent English
- Each column ALSO reads as coherent English (not just word lists)

## What Actually Worked: True 2D Beam Search (v2)

The key insight: for interior cells (row > 0 AND col > 0), only accept tokens that appear in the **intersection** of top-k likely tokens from both row context AND column context.

### Algorithm

1. Fill cells in diagonal order: (0,0), then (0,1) and (1,0), then (0,2), (1,1), (2,0), etc.
2. For first row cells: use row context only
3. For first column cells: use column context only
4. For interior cells: get top-k from row context, get top-k from column context, take INTERSECTION
5. If intersection is empty, that branch dies
6. Keep top-k beams by total score

### Results

**4x4 Grid (True 2D text):**
```
but it is not
it was the only
is the way to
not only to the
```

**Rows (all valid phrases):**
- "but it is not"
- "it was the only"
- "is the way to"
- "not only to the"

**Columns (all valid phrases):**
- "but it is not"
- "it was the only"
- "is the way to"
- "not only to the"

This actually achieves the goal: both rows AND columns are coherent English.

**3x3 Grid:**
```
but it is
it was the
is the only
```

**5x5 Grid (partial success):**
```
but it is not a
it was the only man
is the way to a
not only to the man
a man a man of
```
First 4 rows/columns work; 5th degenerates due to repetition.

## What Didn't Work (v1 attempts)

### Adding row + column scores

My original approach scored tokens by `score(row_context) + score(col_context)`. This is WRONG because it allows tokens that are great for rows but terrible for columns.

Example failure:
```
i    know a    man
we   have the  world
they feel that way
you  see  her  face
```
Rows are sentences, but columns are just word lists ("i we they you"), not sentences.

### Constrained vocabulary per column

Forcing column 1 = pronouns, column 2 = verbs, etc. makes rows grammatical but columns are just category lists, not sentences.

### Pure n-gram optimization

Converges to degenerate "the of the of" patterns.

## Key Insight

**Intersection, not summation.** The token at position (r,c) must be plausible as:
- Continuation of row r (from left)
- Continuation of column c (from above)

If a token isn't in top-k for BOTH contexts, it doesn't belong there.

## Files

- `grid2d_v2.py` - Working implementation with true 2D beam search
- `grid2d.py` - Original failed attempts (kept for reference)
- `PLAN.md` - Task tracking
- `NOTES.md` - This file
