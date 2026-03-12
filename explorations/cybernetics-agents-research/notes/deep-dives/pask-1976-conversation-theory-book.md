# Pask — Conversation Theory: Applications in Education and Epistemology (1976)

## Bibliographic Details
- **Author:** Gordon Pask
- **Title:** *Conversation Theory: Applications in Education and Epistemology*
- **Publisher:** Elsevier, 1976
- **Full text:** Available as searchable PDF from [Pangaro archive](https://pangaro.com/pask/Pask_Conversation_Theory_(indexed).pdf)
- **Companion volume:** *Conversation, Cognition and Learning* (1975, Elsevier).
  [ZIP](https://pangaro.com/pask/Conversationcognitionandlearning.zip)

## The Core Formalism

### The Conversational Loop

The atomic unit of Conversation Theory is the **conversational loop** between two
participants (P-individuals) about a topic T:

1. Participant A produces a description D_A(T) — explains topic T to B using derivations
   in the object language Lo.
2. Participant B processes this, constructs their own understanding.
3. B performs **teachback** — demonstrates their understanding by producing D_B(T),
   a description that must be:
   - Not rote repetition of A's description
   - Demonstrably equivalent in meaning
   - Possibly using different derivations or examples
4. A evaluates B's teachback.
5. If successful: **agreement** is established — T becomes a shared public concept.
6. If unsuccessful: the conversation continues with further exchanges.

### The Ap Operator

The key formal operator in the protolanguage Lp:

```
Ap(Con(T)) => D(T)
```

Where:
- T = a Topic (named conceptual unit)
- Con(T) = the Concept of T (the cognitive process that "understands" T)
- Ap = operator that concurrently executes the concept
- D(T) = the Description produced (observable, communicable representation)

Pask noted that three indexes are required for concurrent execution: two for parallel
processes and one for a serial process. Understanding is inherently concurrent —
not sequential.

### Entailment Structures

Directed graphs where:
- **Nodes** = topics
- **Arrows** = derivation relations (how one topic can be derived from others)

These represent "what may be known" in a domain. They are **permission-giving structures**
— showing what a learner *may* come to know, not prescribing a fixed order.

### Entailment Meshes

The full, unpruned form of entailment structures. When cyclical relationships are
included (concepts explained in terms of each other), you get an **entailment mesh**:
- **Cyclic** — concepts form circular derivation chains
- **Self-reproducing** — they have the formal property of self-reproducing automata
- **Toroidal topology** — Pask modeled coherence by imagining edges extending until they
  meet (top-bottom, left-right), forming a torus

An entailment structure is a **particular perspective** on an entailment mesh — a pruning
chosen for pedagogical purposes. The mesh is "objective" (intersubjective); the structure
is the individual's path through it.

### Lo and Lp Languages

**Lo (Object Language):**
- Vocabulary and formalism for discussing a subject matter
- Enables descriptions and derivations within a domain
- Includes the entailment structures themselves

**Lp (Protolanguage / Protologic):**
- Metalanguage governing how conceptualization works
- Language for talking about *how conversations work*
- Contains rules of inference for conceptual formulation
- The formal dual of CT itself: CT describes conversations; Lp describes the logic
  that makes them well-formed

**L\* Languages:**
- Enable the teachback mechanism specifically
- Languages in which understanding is reproduced and verified

### M-Individuals vs. P-Individuals

**M-Individuals (Mechanical Individuals):**
- Physical/computational substrate — human bodies, machines, hardware
- Defined by physical embodiment
- "Taciturn" — reach stability through internal state changes

**P-Individuals (Psychological Individuals):**
- Conceptual operators — perspectives, rules, points of view
- The participants in conversations
- Not identical with their physical substrate

**Critical non-isomorphism:**
- One M-individual can host multiple P-individuals (one person, multiple perspectives)
- Multiple M-individuals can host one P-individual (a team with shared perspective)
- P-individuals can migrate between M-individuals

### The No Doppelgangers Theorem

**Statement:** No two products of concurrent interaction can be identical.

**Formal expression:**
```
A_A = A(A) != B_A = B(A)
```

**Proof 1 (Dynamic):** Two participants A and B producing interaction T experience
different durations — time is incommensurable between actors. Therefore the interaction
is different for each.

**Proof 2 (Epistemological):** Your concept of your concept is not my concept of your
concept. Every reproduction introduces the perspective of the reproducer.

**Consequence:** Knowledge cannot be "transferred" identically. Every act of learning
produces something genuinely new. Shared understanding is always an approximation
achieved through conversational negotiation.

### Complementarity Principle

> "Processes produce products and all products (finite, bounded coherences) are produced
> by processes."

A conversation has a **wave aspect** (ongoing process) and a **particle aspect** (bounded
products — descriptions, agreements). You cannot fully capture both simultaneously.
This creates a fundamental tension that drives the conversational dynamic.

## Relevance to Agent Architectures

### Teachback as Agent Verification Protocol
The formal requirement of teachback maps directly onto multi-agent verification:
- Agent B must demonstrate understanding of Agent A's output
- Not by echoing tokens, but by re-deriving, applying, or transforming
- This is exactly what "critic" or "verifier" agents do in modern architectures

### Entailment Meshes as Knowledge Graphs
Pask's entailment meshes are a specific kind of knowledge graph — one that is:
- Cyclic (not just hierarchical)
- Perspective-dependent (different agents see different prunings)
- Self-reproducing (concepts generate related concepts)

Modern knowledge graphs used in agent systems tend to be acyclic and "objective."
Pask's meshes are richer — they accommodate the fact that different agents have
different perspectives on the same knowledge.

### P-Individuals and Agent Roles
The P-individual/M-individual distinction maps perfectly onto LLM agent systems:
- M-individual = LLM instance (computational substrate)
- P-individual = agent role/persona (perspective, instructions, tools)
- One LLM hosts multiple P-individuals (multi-role agents)
- Multiple LLM instances can embody one P-individual (distributed agent)

### Lo/Lp and Agent Communication Protocols
- Lo = the domain-specific language agents use to discuss tasks (MCP tool schemas,
  API specifications, domain ontologies)
- Lp = the meta-protocol governing how agents coordinate their communication
  (when to escalate, how to resolve conflicts, how to verify understanding)

Current agent protocols focus almost entirely on Lo. Pask's framework says Lp is
equally necessary — you need a meta-protocol governing the conversational structure,
not just the message format.

## Key Secondary Sources on CT

- Scott, B.C.E. (2001). "Gordon Pask's Conversation Theory: A Domain Independent
  Constructivist Model of Human Knowing." *Foundations of Science* 6, 343-360.
- Pangaro, P. (2001). "THOUGHTSTICKER 1986: A personal history of conversation theory
  in software." *Kybernetes*.
- Manning, T. (2023). "Paskian Algebra: A Discursive Approach to Conversational
  Multi-agent Systems." *Cybernetics & Human Knowing* 30(1-2):67-81.
