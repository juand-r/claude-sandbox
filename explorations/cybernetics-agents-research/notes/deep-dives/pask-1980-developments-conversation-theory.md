# Pask — Developments in Conversation Theory (1980) and the Protologic Lp

## Bibliographic Details

### Primary Papers
- Pask, G. (1980). "Developments in Conversation Theory — Part 1." *International Journal
  of Man-Machine Studies* 13, 357–411.
  [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0020737380800022)
  [Pangaro PDF](https://www.pangaro.com/pask/Pask%20Developments%20In%20Conversation%20Theory%20Part%20Ir.pdf)
- Pask, G. (1980). "Developments in Conversation Theory: Actual and Potential
  Applications." [Pangaro PDF](https://www.pangaro.com/pask/pask%20developments%20in%20conversation%20theory%20actual%20and%20potential%20applications.pdf)
- Pask, G. (1979/1980). "An Essay on the Kinetics of Language as Illustrated by a
  Protologic Lp." *ARS Semiotica III*, 1, 95–122.
  [Pangaro PDF](https://www.pangaro.com/pask/pask%20essay%20on%20kinetics%20of%20language.pdf)
- Pask, G. (1984). "Review of conversation theory and a protologic (or protolanguage),
  Lp." *ECTJ* 32, 3–40.
  [Springer](https://link.springer.com/article/10.1007/BF02768767)

## Context

By 1980, Pask had published the foundational CT books (1975, 1976). These papers represent
the next phase: deepening the formalism, especially around the protologic Lp, and exploring
applications beyond education.

## The Protologic Lp in Depth

### What Lp Is

Lp is not just a "metalanguage" in the loose sense. It is a **formal logic of process**
that governs how conceptualization works. Key properties:

1. **Logic of process AND coherence** — unlike standard logics which deal only with static
   propositions, Lp handles ongoing dynamics
2. **Injunctive** — contains rules about how conceptual entities *can and may* interact,
   including how conflicts arise and resolve
3. **Self-referential** — Lp describes the logic of CT, which includes Lp itself
4. **The formal dual of CT** — CT describes what happens in conversations; Lp describes
   the logic that makes them well-formed

### Lp Contains

- Rules for how concepts form (conceptual construction)
- Rules for how concepts interact (conflict, agreement, analogy)
- Rules for how concepts reproduce (self-referential generation)
- Rules for how descriptions are produced from concepts: `Ap(Con(T)) => D(T)`

### Why Lp Matters

Most implementations of CT-like systems (including modern AI agents) operate only at the
Lo level — they pass messages about subject matter. Lp provides the **meta-level** that
governs how those conversations should be structured. Without Lp, you have communication
but not structured conversation.

## Entailment Meshes: Deeper Analysis

### Beyond Nodes and Links
From Pangaro's analysis: "Entailment meshes as models of cognitive processes are often
misunderstood to consist of no more than nodes and the links between them. That
characterization is a shadow of the cognitive model that Pask intended."

At minimum, nodes in entailment meshes are **placeholders for complementary processes
that undergo parallel execution**, with intricate interdependencies. They are not static
labels but dynamic computational elements.

### Structure of an Entailment Mesh
The mesh consists of:
- **Topics** — named conceptual units
- **Relations** — grouped into types:
  - **Analogies** — structural similarities between topics
  - **Coherences** — mutual dependencies between topics
- **Concepts** — processes that understand topics (the Ap operator executing on topics)

Topics are grouped into relations (analogies, coherences) that comprise concepts in a
mental repertoire. This is not a flat graph — it is a structured, typed, dynamic network.

### Entailment Meshes as "Abstractions and Distillations of Thought Processes"
Pask quite intentionally named the elements 'concepts', 'topics', 'analogies' and the
like. They are not abstract graph-theoretic constructs — they are intended as direct
models of cognitive processes.

## The 1984 Review Paper

Pask's 1984 ECTJ paper "Review of conversation theory and a protologic (or protolanguage),
Lp" is the most accessible summary of the mature CT formalism. It consolidates the
developments from the 1980 papers into a single coherent presentation.

## Relevance to Agent Architectures

### The Need for Lp in Agent Systems
Current multi-agent systems lack Lp. They have:
- Message formats (Lo-level)
- Routing protocols (infrastructure)
- Tool schemas (domain-specific Lo)

What they lack:
- Formal rules for how conversations should be structured
- Meta-protocols governing when understanding must be verified
- Logic for resolving conflicting beliefs between agents
- Rules for when analogies are valid vs. when they are misleading

This is arguably the single most important gap in current agent architectures from a
Paskian perspective.

### Entailment Meshes vs. Modern Knowledge Representations

| Property | Pask's Entailment Meshes | Modern Knowledge Graphs | Vector Embeddings |
|----------|-------------------------|------------------------|-------------------|
| Cyclic | Yes | Usually no (DAGs) | N/A |
| Typed relations | Yes (analogy, coherence) | Yes | No |
| Perspective-dependent | Yes | No | No |
| Dynamic | Yes (processes) | No (static) | No (fixed) |
| Self-reproducing | Yes | No | No |
| Supports teachback | Yes | No | No |

### Process-Based vs. Product-Based Knowledge
Pask's complementarity principle warns against treating knowledge as a static product.
Modern agent systems tend to store knowledge as products (documents, embeddings, cached
results). Pask's framework insists that knowledge is fundamentally a process — it must
be continuously re-enacted through conversation to remain "alive."

This suggests that agents should not just store and retrieve knowledge but should
continuously reconstruct it through conversational processes. RAG (Retrieval-Augmented
Generation) retrieves products; a Paskian system would re-enact processes.
