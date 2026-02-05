# Measuring Novelty Within a Sequence

## Motivation

Previous chapters focused on generating coherent text along two dimensions simultaneously. But there's another important axis: **novelty within the output itself**.

A language model can produce grammatically perfect text that is utterly boring—"the the the the" is coherent but vacuous. Neural text generation suffers from a well-documented **degeneration problem**: models tend to fall into repetitive loops, especially with maximum-likelihood decoding.

For 2D grids, this is particularly relevant:
- A symmetric grid where rows = columns has half the information content
- Repetitive vocabulary ("the man the man the man") satisfies the LM but is uninteresting
- We want outputs that are both coherent *and* diverse

This chapter covers metrics for measuring novelty **within** a single output, treating the generated text as a sequence of N tokens.


## Token-Level Metrics

### Type-Token Ratio (TTR)

The simplest diversity measure:

```
TTR = |unique tokens| / |total tokens|
```

For the grid "but it is not / it was the only / is the way to / not only to the" (16 tokens):
- Unique tokens: {but, it, is, not, was, the, only, way, to} = 9
- TTR = 9/16 = 0.5625

**Limitations**: TTR monotonically decreases with sequence length (Heaps' law). A 1000-word passage will always have lower TTR than a 10-word passage, even if both are equally diverse relative to their length.

**Variants**:
- Root TTR: `|unique| / sqrt(|total|)`
- Log TTR: `log(|unique|) / log(|total|)`
- Moving-Average TTR (MATTR): average TTR over sliding windows


### Hapax Ratio

```
Hapax = |tokens appearing exactly once| / |total tokens|
```

Measures how much of the vocabulary is used only once—higher means more exploration of vocabulary.


## N-gram Based Metrics

### Distinct-n

Proposed by Li et al. (2016), this is the standard metric in text generation:

```
Distinct-n = |unique n-grams| / |total n-grams|
```

For our 4x4 grid read horizontally ("but it is not it was the only is the way to not only to the"):
- Distinct-1 = 9/16 = 0.5625 (same as TTR)
- Distinct-2 = 14/15 = 0.933 (only "is the" repeats)
- Distinct-3 = 14/14 = 1.0 (no trigram repetition)

Higher n captures longer-range repetition. Distinct-2 through Distinct-4 are commonly reported together.


### Rep-n (Repetition Rate)

The complement of Distinct-n, used in degeneration studies:

```
Rep-n = 1 - Distinct-n = |repeated n-grams| / |total n-grams|
```

Human-written text has very low Rep-n (≈0.02% for sentence-level repetitions in Wikitext-103). Degenerate models can have Rep-n > 50%.


### Self-BLEU

Originally for corpus-level diversity, but adaptable to intra-sequence use.

For a single sequence, partition it into k segments and compute BLEU scores between each segment and the rest. High self-BLEU indicates the sequence is repetitive with itself.


## Entropy-Based Metrics

### Unigram Entropy

Information-theoretic measure of vocabulary diversity:

```
H = -Σ p(w) · log₂(p(w))
```

where `p(w)` is the empirical frequency of word `w` in the sequence.

For our 4x4 grid (frequency counts: the=3, it=2, is=2, to=2, not=2, only=2, but=1, was=1, way=1):
```
H ≈ 3.09 bits
```

Maximum entropy for 16 tokens over 9 types would be log₂(9) ≈ 3.17 bits.

**Interpretation**: High entropy = flat distribution = more diversity. Low entropy = peaked distribution = repetitive.


### Conditional Entropy (Contextual Novelty)

Instead of treating tokens as i.i.d., measure how predictable each token is given its context:

```
H(X_t | X_{t-1}, ..., X_{t-k})
```

This is related to perplexity but measured on the *generated* sequence itself, not against a reference model. A sequence with high conditional entropy introduces new information at each step; low conditional entropy means tokens are predictable from context (potentially repetitive patterns).


### Positional Entropy Dynamics

Research shows human-like text maintains entropy in a "stable narrow band" throughout generation. Tracking how entropy evolves across positions reveals:
- **Entropy collapse**: the model gets stuck in a low-entropy loop (degeneration)
- **Entropy explosion**: the model becomes incoherent (often accompanied by high varentropy)

For 2D grids, we can track entropy along:
- Each row independently
- Each column independently
- The diagonal fill order


## Compression-Based Metrics

### Lempel-Ziv Complexity

Counts the number of unique substrings needed to construct the sequence:

```
LZ(s) = number of parsing steps in the LZ factorization
```

For highly repetitive text, LZ complexity is low (few unique substrings). For diverse text, LZ complexity approaches the sequence length.

**Intuition**: "the the the the" has LZ complexity ≈ 2 ("the " + copy). "but it is not was only way to" has LZ complexity ≈ 9.


### Compression Ratio

A practical proxy for Kolmogorov complexity:

```
CR = |compressed| / |original|
```

Using gzip, zlib, or LZ77:
- Repetitive text compresses well → low CR → low novelty
- Diverse text compresses poorly → high CR → high novelty

This has been used to detect plagiarism and measure text similarity.


## Embedding-Based Metrics

### Semantic Diversity

Using word embeddings (word2vec, BERT, etc.):

```
Diversity = mean pairwise cosine distance between token embeddings
```

Or equivalently, variance of the centroid.

This captures **semantic** novelty, not just lexical. The words "happy" and "joyful" are lexically distinct but semantically similar.


### Coverage Volume

For a set of token embeddings, measure the volume of the convex hull or the determinant of the covariance matrix. Larger volume = tokens span more of the semantic space.


## Application to 2D Grids

2D grids present unique measurement opportunities:

### Row/Column Decomposition

Measure diversity along:
- **Horizontal**: the full reading-order sequence
- **Vertical**: each column independently
- **Grid-level**: the bag of all words

A good 2D grid should have high novelty in *both* row and column readings.


### Symmetry as Anti-Novelty

A symmetric grid (where row_i = column_i) has at most half the effective vocabulary. Detecting and penalizing symmetry:

```
Symmetry = (Σ I[grid[r][c] == grid[c][r]]) / N²
```

Where I[·] is the indicator function. Our v2 results show many grids are fully symmetric (Symmetry = 1.0), which is mathematically interesting but semantically redundant.


### Diagonal Repetition

In diagonal fill order, adjacent positions share context. This can lead to diagonal patterns:

```
a b c
b c d
c d e
```

Detecting such patterns requires checking anti-diagonal sequences.


### Intersection as Novelty Constraint

The intersection-based beam search (accepting only tokens in top-k for *both* row and column) already provides implicit novelty pressure:
- Common words ("the", "to") appear in many intersections
- Rare words are less likely to satisfy both constraints
- This creates a natural regularization effect

But it's not sufficient—degenerate outputs like "the the / the the" still satisfy the intersection criterion.


## Recommended Metrics for 2D Writing

Given the constraints of 2D grid generation, I recommend:

1. **Distinct-2** for row and column sequences separately
   - Easy to compute
   - Interpretable
   - Standard in the literature

2. **TTR** for the entire grid (bag of words)
   - Penalizes vocabulary repetition

3. **Symmetry score** (custom for 2D)
   - Penalizes trivial row=column solutions

4. **Compression ratio** (gzip)
   - Captures complex patterns
   - Single number summary

5. **Entropy** for final ranking
   - Information-theoretic principled


## Implementation Sketch

```python
import math
import gzip
from collections import Counter

def distinct_n(tokens: list, n: int) -> float:
    """Distinct-n metric."""
    ngrams = [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
    return len(set(ngrams)) / len(ngrams) if ngrams else 0

def unigram_entropy(tokens: list) -> float:
    """Shannon entropy of token distribution."""
    counts = Counter(tokens)
    total = len(tokens)
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def compression_ratio(text: str) -> float:
    """Gzip compression ratio (higher = more diverse)."""
    original = text.encode('utf-8')
    compressed = gzip.compress(original)
    return len(compressed) / len(original)

def symmetry_score(grid: list) -> float:
    """Fraction of cells where grid[r][c] == grid[c][r]."""
    n = len(grid)
    matches = sum(1 for r in range(n) for c in range(n) if grid[r][c] == grid[c][r])
    return matches / (n * n)

def grid_novelty_report(grid: list):
    """Compute novelty metrics for a 2D grid."""
    # Flatten
    all_tokens = [w for row in grid for w in row]

    # Row readings
    row_tokens = [' '.join(row) for row in grid]

    # Column readings
    n = len(grid)
    col_tokens = [' '.join(grid[r][c] for r in range(n)) for c in range(n)]

    return {
        'ttr': len(set(all_tokens)) / len(all_tokens),
        'distinct_2': distinct_n(all_tokens, 2),
        'distinct_3': distinct_n(all_tokens, 3),
        'entropy': unigram_entropy(all_tokens),
        'compression': compression_ratio(' '.join(all_tokens)),
        'symmetry': symmetry_score(grid),
    }
```


## Theoretical Considerations

### Quality vs. Diversity Trade-off

High novelty alone is not the goal. Random tokens have maximum novelty but zero coherence. The challenge is maintaining coherence *while* achieving novelty—a Pareto frontier.

The 2D constraint naturally occupies an interesting point on this frontier: the intersection requirement forces coherence, but without additional diversity pressure, outputs collapse to common words.


### Entropy Bounds

For a sequence of N tokens:
- Minimum entropy: 0 (all tokens identical)
- Maximum entropy: log₂(V) where V = vocabulary size

But these bounds assume unlimited vocabulary. With the restricted VOCAB in v2 (100 words), maximum entropy is log₂(100) ≈ 6.64 bits. Practical outputs achieve much less due to:
- Language model preferences for common words
- The intersection constraint eliminating rare words
- Length constraints limiting vocabulary exploration


### Repetition as Attractor

Neural text generation exhibits "repetition attractors"—once a phrase repeats, it's more likely to repeat again (positive feedback). This is why degeneration often manifests as sudden loops rather than gradual decline.

In 2D grids, symmetric solutions are an attractor: if early cells create diagonal symmetry, subsequent cells are pushed toward maintaining it.


## Future Directions

Several open questions:

1. **Novelty-aware beam search**: Can we add a diversity term to the beam score without sacrificing coherence?

2. **Per-position novelty targets**: Should cell (0,0) have higher novelty than interior cells?

3. **Semantic vs. lexical novelty**: Our current metrics are lexical. Could embeddings reveal semantically interesting but lexically repetitive grids?

4. **Contrastive objectives**: Score novelty relative to a baseline distribution, not just self-comparison.


## Summary

Measuring novelty within a sequence complements the coherence metrics implicit in language model scoring. For 2D writing:

| Metric | What it measures | Range | Goal |
|--------|-----------------|-------|------|
| TTR | Vocabulary diversity | 0-1 | Higher |
| Distinct-n | N-gram diversity | 0-1 | Higher |
| Entropy | Information content | 0-log₂(V) | Higher |
| Compression | Pattern complexity | 0-1+ | Higher |
| Symmetry | Row/col redundancy | 0-1 | Lower |

The most useful single number is probably **Distinct-2**, with **Symmetry** as a 2D-specific complement. Together they capture: "does this grid avoid repetition, and does it differ when read horizontally vs. vertically?"


## References

- Li et al. (2016). "A Diversity-Promoting Objective Function for Neural Conversation Models"
- Holtzman et al. (2020). "The Curious Case of Neural Text Degeneration"
- Fu et al. (2021). "A Theoretical Analysis of the Repetition Problem in Text Generation"
- Pillutla et al. (2021). "MAUVE: Measuring the Gap Between Neural Text and Human Text"
- NeurIPS 2023: "Repetition In Repetition Out: Towards Understanding Neural Text Degeneration"
- Standardizing Text Diversity Measurement (2024): https://arxiv.org/html/2403.00553
