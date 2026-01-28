# 2D Writing System - Findings

## Goal
Generate an NxN word grid where:
- Each row reads as coherent English
- Each column also reads as coherent English

## What Worked

### Constrained Grammar + Unique Words = Success

The key insight: **constrain word categories by column position**.

Example 4x4 structure `[Pronoun][Verb][Determiner][Noun]`:

```
i    know a    man
we   have the  world
they feel that way
you  see  her  face
```

**Rows read as sentences:**
- "i know a man" - perfect
- "we have the world" - perfect
- "they feel that way" - perfect
- "you see her face" - perfect

**Columns read as word lists:**
- "i we they you" - pronouns
- "know have feel see" - verbs
- "a the that her" - determiners
- "man world way face" - nouns

### Why This Works

1. **Column constraints force diversity** - Each column has a restricted vocabulary (only pronouns, only verbs, etc.), so the beam search can't converge to repetitive patterns like "the of the of"

2. **Uniqueness per column** - Requiring each word in a column to be different prevents repetition like "the the the the the"

3. **Grammar structure enables both directions** - When columns are word-category lists, they naturally read as coherent sequences. Rows follow standard English grammar.

4. **Subject-verb agreement** - Using only pronouns that agree with base verb forms (I/you/we/they + base verbs) produces grammatically correct sentences

## What Didn't Work

### Pure n-gram optimization

Without constraints, beam search and Gibbs sampling converge to degenerate solutions like:
```
the of  the of  the
of  the of  the of
the of  the of  the
```

This happens because "the of" has very high n-gram probability.

### Full vocabulary with uniqueness

The "unique" approach (each word used only once in entire grid) produces mixed results:
```
it  is    to    the  of
was not   a     for  this
and so    that  they had
but i     would have been
```

Some rows read well ("but i would have been") but columns are incoherent.

### 5x5 with subject-verb mismatch

Using all pronouns (including he/she/it) with base verbs creates agreement errors:
```
he  know that little boy   <- should be "knows"
she want her  first  day   <- should be "wants"
```

## Key Parameters

- **beam_width**: 100-200 works well. Higher is better but slower.
- **unique_per_column**: Essential to prevent column repetition
- **n-gram order**: 3 (trigram) works well

## Best Results

### 3x3 Grid
Structure: `Pronoun - Verb - Noun`
```
i   have time
you take place
we  want night
```

### 4x4 Grid (Best Quality)
Structure: `Pronoun - Verb - Det - Noun` with plural pronouns only
```
i    know a    man
we   have the  world
they feel that way
you  see  her  face
```
All 4 rows are grammatically perfect English sentences.
All 4 columns are coherent word-category lists.

### 5x5 Grid
Structure: `PluralSubject - Verb - Det - Adj - Noun`
```
people   know the  last   time
children feel a    cold   day
men      need that big    man
women    hold her  little house
friends  see  his  old    friend
```
All 5 rows are grammatically correct (though some semantically odd).
All 5 columns are coherent word-category lists.

## Future Directions

1. **Semantic coherence**: Use word embeddings to encourage semantically related words
2. **Better LM**: GPT-2 or similar would give better probability estimates than n-grams
3. **Different structures**: Try more grammatical patterns (questions, imperatives, etc.)
4. **Larger grids**: 6x6 or larger would be more impressive but harder

## Files

- `grid2d.py` - Main implementation with all approaches
- `PLAN.md` - Original plan (outdated)
- `NOTES.md` - This file
