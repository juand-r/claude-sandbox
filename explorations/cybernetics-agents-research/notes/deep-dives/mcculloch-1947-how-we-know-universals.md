# Pitts & McCulloch — "How We Know Universals: The Perception of Auditory and Visual Forms" (1947)

**Authors:** Walter Pitts & Warren S. McCulloch
**Published:** Bulletin of Mathematical Biophysics, Vol. 9, pp. 127-147, 1947
**DOI:** 10.1007/BF02478291
**Full text:** Behind paywall (Springer). Reprinted in *Embodiments of Mind*.

## What This Paper Does

Extends the 1943 paper from pure logic to **pattern recognition**. While the 1943 paper showed neural nets can compute any Boolean function, this paper asks: how does the brain recognize a shape as "the same shape" regardless of size, position, or orientation?

This is one of the first formal treatments of **invariant pattern recognition** — a problem that modern CNNs solve with pooling layers and weight sharing.

## Two Mechanisms Proposed

### Mechanism 1: Averaging Over a Group
- Averages an "apparition" (stimulus pattern) over a group of transformations
- Uses scanning to convert spatial patterns into temporal sequences
- Example: recognizing a chord regardless of pitch (the *intervals* between notes are preserved even if all notes are transposed)
- Example: recognizing a shape regardless of size

This is essentially what we now call **invariance through aggregation** — the same principle behind global average pooling in CNNs.

### Mechanism 2: Reduction to Canonical Form
- Reduces a stimulus to a standard/canonical representation selected from among its many legitimate presentations
- Example: the eye reflex that moves objects to the fovea (center of vision) — physically translating the stimulus to a canonical position before processing it

This is essentially **normalization** — the same principle behind spatial transformer networks and various attention mechanisms.

## Why It Matters

### Prefigures Key Ideas in Modern Deep Learning

| Pitts & McCulloch (1947) | Modern Equivalent |
|---|---|
| Averaging over group of transformations | Pooling layers, invariant representations |
| Reduction to canonical form | Spatial transformer networks, attention |
| Scanning for temporal conversion | Recurrent processing of spatial data |
| Form recognition independent of size | Scale invariance in CNNs |

### Norbert Wiener's Reaction
Wiener was deeply excited by this paper. He saw it as evidence for a general method by which animals recognize objects — by scanning a scene from multiple transformations and finding a canonical representation. This influenced his thinking in *Cybernetics* (1948).

### The Tragedy
This was the last major collaboration between McCulloch and Pitts. Wiener's wife allegedly turned Wiener against McCulloch (for personal/social reasons), and Wiener cut off contact. Pitts, devastated, withdrew from academic life, burned his unpublished manuscripts, descended into alcoholism, and died in 1969 at age 46. A genuine tragedy for the field.

## Relevance to Agent Architectures

The idea of recognizing "universals" — invariant patterns across different presentations — is directly relevant to how AI agents should generalize:
- An agent should recognize "the same situation" even when surface details differ
- Pattern recognition across contexts is essential for transfer learning in agents
- The two mechanisms (averaging vs. canonical reduction) represent two fundamentally different strategies for achieving generalization

## Publication History
- Original: Bulletin of Mathematical Biophysics, 1947
- Reprinted in *Embodiments of Mind* (MIT Press, 1965)
- Reprinted in *Neurocomputing: Foundations of Research* (MIT Press, 1988)
