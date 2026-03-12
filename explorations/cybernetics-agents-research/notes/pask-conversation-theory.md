# Gordon Pask's Conversation Theory: Detailed Research Notes

## Overview

Conversation Theory (CT) is a formal cybernetic theory developed by Gordon Pask (1928-1996)
describing how learning and knowing emerge through conversational interactions between
participants. It is not a metaphorical use of "conversation" — Pask intended a rigorous,
computable account of how two or more cognitive systems achieve shared understanding of a topic.

CT was primarily developed in the 1970s, with key publications being *Conversation, Cognition
and Learning* (1975) and *Conversation Theory: Applications in Education and Epistemology*
(1976). It was later generalized into Interactions of Actors Theory (IA) in the 1980s-90s.

CT is recognized as a founding theory of second-order cybernetics.

**Key collaborators:** Bernard Scott, Dionysius Kallikourdis, Robin McKinnon-Wood, Paul Pangaro,
Gerard de Zeeuw.

---

## 1. The Lp and Lo Languages

Pask distinguished multiple levels of language within a conversation:

### Lo: The Object Language
- The vocabulary and formalism for discussing a subject matter within a particular domain.
- Lo enables participants to make **descriptions** of topics and to state **derivations**
  (how one topic can be derived from or explained in terms of others).
- It is the language *about* the domain being learned or discussed.
- Lo includes the entailment structures that represent relationships between topics.

### Lp: The Protolanguage (or Protologic)
- Lp is the "sister theory" of CT — a metalanguage or meta-logic that governs how
  conceptualization itself works.
- It is the language for talking about *how conversations work*, how concepts are formed,
  and how derivations are justified.
- Lp contains the **rules of inference** governing conceptual formulation and modulation.
- Lp is the **formal dual** of CT: CT describes what happens in conversations;
  Lp describes the logic that makes those conversations well-formed.

### Formal Operators in Lp

The key formal operator is:

```
Ap(Con(T)) => D(T)
```

Where:
- **T** = a Topic (a named conceptual unit in the domain)
- **Con(T)** = the Concept of topic T (the cognitive process that "understands" T)
- **Ap** = an operator that concurrently executes the concept
- **D(T)** = the Description produced (an observable, communicable representation)
- **=>** = "produces" or "generates"

Pask noted that three indexes are required for concurrent execution: two for parallel
processes and one to designate a serial process. This reflects the inherently concurrent
nature of conceptualization — understanding is not a sequential operation but involves
parallel processing.

### L* Languages
There are also L* languages that enable the **teachback** mechanism — these are the
languages in which one participant reproduces and verifies another's understanding.

### Key Insight
The distinction between Lo and Lp maps roughly to the distinction between **talking about
a subject** and **talking about how we talk about a subject**. CT is unusual in that it
requires both levels to be formalized — you cannot have a complete theory of conversation
without a theory of how the conversation's own logic works.

---

## 2. Entailment Structures and Entailment Meshes

### Entailment Structures
- Directed graphs composed of **nodes** (topics) and **arrows** (derivation relations).
- They represent "what may be known" in a domain — a map of possible conceptual relationships.
- An entailment structure shows how one topic can be **derived from** or **explained in terms of**
  other topics.
- They are **permission-giving structures**: they show what a learner *may* come to know,
  not what they *must* know in a fixed order.
- The hierarchical or "pruned" form of an entailment structure is a pedagogical convenience —
  it hides the underlying cyclic organization.

### Entailment Meshes
- The full, unpruned form: when cyclical relationships between concepts are included
  (concepts explained in terms of each other), you get an **entailment mesh**.
- Entailment meshes are **cyclic** and **self-reproducing** — they have the formal property
  that concepts and topics form circular processes (self-reproducing automata).
- Pask modeled coherence by imagining the edges of an entailment mesh extending until they
  meet, top-bottom and left-right, forming a **torus**. This topological closure represents
  the self-contained, self-referential nature of a coherent body of knowledge.
- In his later work, Pask modeled these as **knots, links, and braids** from knot theory,
  calling them "tapestries."

### Entailment Structures vs. Entailment Meshes
- An entailment structure is a **particular perspective** on an entailment mesh — a pruning
  chosen for pedagogical purposes.
- The learner navigates the mesh by choosing starting points, pruning the circular hypertext
  into a heterarchical structure that reflects their individual learning path.
- The mesh is the "objective" (intersubjective) structure; the structure is the learner's
  individual path through it.

### Complementary Structures
- **Entailment structures** show "what may be known" (comprehension learning).
- **Task structures** show "what may be done" (operation learning).
- These are complementary — knowing-why and knowing-how.

---

## 3. The Teachback Mechanism

Teachback is the critical verification method in CT. It is not a pedagogical trick but a
**formal requirement** for establishing that understanding has been achieved.

### How It Works
1. Participant A explains topic T to participant B using a derivation in Lo.
2. Participant B must then **teach back** their understanding of T to A — not by rote
   repetition, but by demonstrating understanding through:
   - Applying the knowledge to an unfamiliar situation
   - Explaining it in their own terms (possibly using different derivations)
   - Demonstrating it concretely and non-verbally
3. A evaluates whether B's teachback constitutes genuine understanding.
4. If successful, this constitutes an **agreement** — a shared public concept.

### Why It Matters Formally
- Teachback is the mechanism by which **private concepts** become **public concepts**
  (shared agreements).
- It creates a **closed loop**: the conversation is not one-directional transfer but a
  cybernetic feedback cycle.
- Rote memory responses are explicitly **not accepted** as demonstrations of understanding.
- The act of teaching back often transforms and deepens the understanding of both participants.

### Role Reversal
- The learner becomes the teacher; the teacher becomes the evaluator-learner.
- This is not merely pedagogical — it is constitutive of what "understanding" means in CT.
  Understanding is not a mental state; it is a **demonstrable capacity** verified through
  conversational role reversal.
- Pask's fundamental teaching theorem: "Systems that teach must learn from students who
  can reverse roles as teachers."

---

## 4. M-Individuals vs. P-Individuals

This is one of Pask's most important and subtle distinctions.

### M-Individuals (Mechanical Individuals)
- Any system with **physical embodiment**: a human body, a machine, a computer, hardware.
- The biomechanical substrate that carries or embodies cognitive processes.
- M-individuals are "taciturn" — they reach stability by changing internal states in
  response to environmental stimuli, but they do not inherently converse.

### P-Individuals (Psychological Individuals)
- **Conceptual operators**: a concept, a topic, a perspective, a rule system, a "point of view."
- P-individuals are the participants in conversations — they are what *thinks*, *knows*,
  and *converses*.
- They are not identical with the physical system that hosts them.

### The Critical Non-Isomorphism
The relationship between M-individuals and P-individuals is **not one-to-one**:
- One M-individual can embody **multiple** P-individuals (one person can hold multiple
  perspectives, play multiple roles).
- Multiple M-individuals can together embody **one** P-individual (a team can share a
  single perspective or cognitive process).
- P-individuals can migrate between M-individuals.

### Why This Matters
- It separates the question of "who is physically present" from "what perspectives are
  interacting" — these are different questions with different answers.
- It means **cognition is unbounded** — conceptual operators require physical embodiment
  but are not reducible to any particular physical substrate.
- A conversation is between P-individuals, not M-individuals. The same conversation can be
  carried by different physical substrates.
- Example: in a traffic jam, each car-person becomes an M-individual embodying a
  P-individual (the "driver trying to navigate"). The collective behavior emerges from
  P-individual interactions, not from the physical properties of the cars.

### Relevance to AI/LLM Systems
This distinction is directly applicable: an LLM instance is an M-individual; the
perspectives, roles, or "personas" it can adopt are P-individuals. Multiple LLM instances
could collectively embody a single P-individual (distributed cognition), or a single
instance could embody multiple P-individuals (multi-perspective reasoning).

---

## 5. The "No Doppelgangers" Theorem

This is Pask's **exclusion principle** — a fundamental theorem of his cybernetics.

### Statement
**No two products of concurrent interaction can be identical.**

Formal expression:
```
A_A = A(A) ≠ B_A = B(A)
```
Hence, there are no Doppelgangers.

### First Proof (Physical/Dynamic)
Consider two dynamic participants A and B producing an interaction T:
- Their separation varies during T.
- The duration of T **observed from A** differs from the duration of T **observed from B**.
- Therefore the interaction, as experienced and produced, is different for each participant.
- Time is incommensurable between actors.

### Second Proof (Epistemological)
- Your concept of your concept is **not** my concept of your concept.
- A reproduced concept is not the same as the original concept.
- Every reproduction introduces the perspective and context of the reproducer.

### Consequences
- No Doppelgangers applies in both the **kinematic domain** of CT (bounded by beginnings
  and ends, where times are commensurable) and in the **eternal kinetic domain** of IA
  (where times are incommensurable).
- The small differences between seemingly identical coherences are **productive** — they
  drive differentiation in evolution and learning.
- This connects to Pask's Last Theorem (1995): **"Like concepts repel, unlike concepts
  attract."** After sufficient interaction ("faith"), even like-seeming concepts will
  produce a difference and thus an attraction.

### Significance
This is not merely a philosophical observation — it is a formal constraint on the theory.
It means:
- Knowledge cannot be "transferred" identically from one participant to another.
- Every act of learning produces something genuinely new.
- Shared understanding is always an approximation achieved through conversational
  negotiation, never a duplication.

---

## 6. Complementarity

### Pask's Complementarity Principle
> "Processes produce products and all products (finite, bounded coherences) are produced
> by processes."

Or equivalently:
> "Products are produced by processes and all processes produce products."

### What This Means Formally
- A **process** is an ongoing, potentially unbounded dynamic activity (a conversation,
  a cognitive operation, a spin).
- A **product** is a finite, bounded coherence — a description, a concept, an agreement,
  a stable structure.
- Every process leaves traces (products); every product implies the process that created it.
- There is no "pure process" without observable products, and no "pure product" that exists
  without a generative process.

### Connection to Physics
Pask drew an explicit analogy to Bohr's complementarity in quantum mechanics:
- A conversation has a **wave aspect** (the ongoing process of interaction) and a
  **particle aspect** (the bounded products — descriptions, agreements — that recipients
  recompile to form meaning or emotion).
- You cannot fully capture both aspects simultaneously — observing the product freezes
  the process; participating in the process dissolves fixed products.

### Formal Implications
- Entailment meshes (products) are snapshots of ongoing conceptualization processes.
- Understanding (a process) cannot be reduced to a description (a product), but descriptions
  are the only way to externalize and share understanding.
- This creates a fundamental tension that drives the conversational dynamic: the need to
  produce shareable products from inherently process-based understanding.

---

## 7. Learning as Interaction, Not Transfer

CT is explicitly opposed to "transmission" or "transfer" models of learning.

### The CT Model
- Learning occurs through **conversations about a subject matter** that serve to make
  knowledge explicit.
- Knowledge is not a commodity that moves from teacher to learner. It is **constructed**
  through the interaction itself.
- The conversation is between two a priori asynchronous cognitive systems (P-individuals)
  that achieve a posteriori synchronization — shared understanding of a topic from their
  respective perspectives.

### Two Complementary Aspects of Learning
1. **Comprehension learning**: Making descriptions of "what may be known" — understanding
   the conceptual relationships (navigating entailment structures).
2. **Operation learning**: Mastering particular skills and procedures — knowing "what may
   be done" (navigating task structures).

### Learning Strategies
Pask identified characteristic individual differences:
- **Serialists**: Process information in small sequential steps, building up from details.
- **Holists**: Take a "big picture" view, assimilating concepts as wholes and seeking
  higher-order relations.
- **Versatile learners**: Can do both, switching as needed (the ideal).

Pathological forms:
- **Globe-trotting**: Vacuous holism — seeing connections everywhere without grounding.
- **Improvidence**: Narrow serialism — knowing details without understanding context.

### The Conversational Loop
1. A presents a derivation of topic T to B.
2. B attempts to understand, asks questions, proposes alternative derivations.
3. B teaches back their understanding to A.
4. A evaluates, provides feedback, adjusts.
5. Agreement is reached (or the conversation continues, or fails).

This loop is not a pedagogical method — it is Pask's model of **what understanding is**.
Understanding = successful completion of a conversational loop with teachback.

---

## 8. Connection to Second-Order Cybernetics

### First vs. Second Order
- **First-order cybernetics** (Wiener, Ashby): "The science of observed systems" —
  studying feedback, control, and communication in systems from an external vantage point.
- **Second-order cybernetics** (von Foerster, Maturana, Pask): "The science of observing
  systems" — the observer is included within the system being observed.

### CT as Second-Order
CT is second-order because:
1. **The theory applies to itself.** CT is a theory of how theories are constructed through
   conversational processes. It must therefore account for its own construction.
2. **The observer is a participant.** Pask rejected non-participant observer status. The
   theorist/researcher is placed within the system, with coordinates on a participant
   rather than claiming external objectivity.
3. **Organizational closure.** Pask extended Maturana's concept of autopoiesis to
   psychosocial systems. Conversational systems are organizationally closed — they
   self-produce through interaction.
4. **Radical constructivism.** CT explicitly adopts a constructivist epistemology:
   knowledge is not a representation of external reality but a construction produced
   through conversational processes.

### Self-Reference
- Scott (2009) describes Pask's theorizing as employing "second order (reflexive)
  metatheorising" — the theory explains its own formation.
- The complementarity principle embeds self-reference: the theory (a product) is produced
  by the theorizing process (conversations among researchers), which in turn produces
  further products.

### Connection to Maturana
At the "First International Conference on Self-Referential Systems," Pask extended
Maturana's ideas about organizationally closed brain-body systems to psychosocial
conversations. While biomechanical systems (M-individuals) are taciturn and reach stability
through internal state changes, conversational systems (P-individuals) interact and
self-produce new meanings as observers of activity in context.

---

## 9. Practical Applications in Educational Technology

### CASTE (Course Assembly System and Tutorial Environment)
- Developed with Bernard Scott and Dionysius Kallikourdis.
- One of the first adaptive educational systems designed around the insight that "students
  fare very differently according to whether the teaching materials are or are not adapted
  to suit their idiosyncrasies."
- Matched students to learning strategies (serialist/holist/versatile).
- Empirical results: matching students to preferred strategies using CASTE produced
  significantly better outcomes than mismatched instruction.
- Teachback of ideas produced more effective learning than conventional tests.
- Tools could be customized by teachers in real-time to match each learner's skill level.

### THOUGHTSTICKER (1985-1986)
- Pask's most ambitious software implementation of CT.
- An adaptive, personalized information browser — a decade before web browsers.
- Built on entailment meshes as the underlying knowledge structure.
- Key features:
  - **Adaptive hyperlinks**: Unlike static HTML, clicking the same link produced different
    results based on individual user profiles.
  - **Personalization**: User Profile (learner background), User History (tracked actions
    across sessions), User Model (preferred learning styles).
  - **Uncertainty regulation**: ~20 overlapping measures to minimize user uncertainty.
  - **Contradiction handling**: Structural detection of conflicts between statements,
    with systematic resolution through questioning about synonymy, context, and topic
    additions. Could accommodate contradictory statements by placing them in different
    contexts.
  - **Authoring tools**: Automatic topic suggestion via stemming, relationship detection,
    saturation analysis of underdeveloped areas, metadata preserving author identity and
    dissenting views.
- Pangaro's assessment: "Named after Pask's first implementation of an interactive
  knowledge structuring tool... it had all the components of modern Web browsers plus an
  organising principle for the hyperlinks — something the Web still needs."

### The Cognitive Reflector
- A virtual machine for selecting and executing concepts/topics from an entailment mesh
  shared by at least a pair of participants.
- Features an external modeling facility where agreement between teacher and pupil can be
  shown by reproducing public descriptions of behavior.
- The theoretical basis for how CT-based systems work: converting internal knowledge into
  observable behaviors via teachback protocols.

### EXTEND
- An earlier system that "permitted and recorded the product" of learning processes.
- THOUGHTSTICKER went further by "exteriorizing the innovation of ideas in learning."

### ThoughtShuffler (Pangaro, 2008)
- Extended Pask's interface designs to facilitate information search on the Internet.
- An attempt to bring CT's organizing principles to web-scale information.

### What Modern Systems Still Lack
Pangaro argues that today's browsers and knowledge management systems lack what Pask's
entailments can bring: "an organizing principle and the fine-grained, adaptive nature of
a conversation." The Web has hyperlinks but no conversational structure governing them.

---

## 10. Relevance to Multi-Agent LLM Communication

CT was developed decades before LLMs, but its concepts map remarkably well onto
contemporary multi-agent AI architectures. The following are not speculative leaps but
direct structural correspondences.

### M-Individuals and P-Individuals in LLM Systems
- An LLM instance (or a running process) is an M-individual — a physical/computational
  substrate.
- The roles, personas, or specialized perspectives an LLM adopts are P-individuals.
- The non-isomorphism holds: one LLM can embody multiple P-individuals (multi-perspective
  reasoning); multiple LLM instances can collectively embody one P-individual (distributed
  agent teams working toward a shared perspective).

### Teachback as Verification Protocol
- In multi-agent systems, how do you verify that Agent B actually "understood" Agent A's
  output, rather than merely passing tokens?
- CT's answer: teachback. Agent B must demonstrate understanding by reproducing the
  knowledge in a different form, applying it to a new case, or deriving it from
  different premises.
- This maps directly to verification protocols in multi-agent architectures: having one
  agent summarize, critique, or re-derive another's output.

### Entailment Structures as Shared Ontologies
- Multi-agent systems need shared conceptual frameworks. CT's entailment meshes are
  exactly this — structured representations of how concepts relate, with formal rules
  for derivation and analogy.
- Modern agent protocols (MCP, A2A) are developing "semantic layers" that establish shared
  meaning — this is what Pask's Lo language was designed to do.

### No Doppelgangers and Agent Diversity
- The No Doppelgangers theorem predicts that even agents with identical architectures and
  training will produce different outputs given different interaction histories and contexts.
- This is not a bug but a feature — it is the source of productive diversity in multi-agent
  systems.
- "Like concepts repel, unlike concepts attract" — diverse agent perspectives generate
  more productive interactions than homogeneous ones.

### Conversation as Protocol, Not Just Channel
- Current multi-agent communication protocols (MCP, A2A, Agora) focus on message format
  and routing. CT suggests this is necessary but insufficient.
- What is needed is what Pask called the **cognitive reflector** — not just a communication
  channel but a virtual machine that manages the *conversational structure*: who can say
  what to whom, when teachback is required, how agreements are tracked, how contradictions
  are resolved.
- Recent research on the "Internet of Agents" proposes exactly this: an Agent Semantic
  Layer (L9) for shared meaning and collective coordination, and an Agent Communication
  Layer (L8) for interaction structure. This is a reinvention (likely unknowing) of
  Pask's Lo/Lp distinction.

### Learning as Interaction
- CT's core insight — that knowledge is constructed through interaction, not transferred —
  applies directly to multi-agent LLM systems.
- When Agent A sends a message to Agent B, no knowledge "transfers." Agent B constructs
  its own understanding based on its own context, history, and perspective.
- Effective multi-agent systems must be designed with this in mind: explicit protocols for
  verifying shared understanding, not assumptions of perfect transmission.

### Complementarity in Agent Architectures
- Pask's complementarity principle (processes produce products, products are produced by
  processes) suggests that multi-agent systems need both:
  - **Process-oriented components**: ongoing conversations, negotiations, feedback loops.
  - **Product-oriented components**: cached results, agreed-upon facts, stable knowledge
    bases.
- Neither alone is sufficient. A system that only processes (never commits to products)
  cannot build on prior work. A system that only stores products (never re-engages
  processes) becomes brittle and unable to adapt.

---

## 11. Later Developments: Interactions of Actors Theory (IA)

IA is Pask's generalization of CT, developed in the 1980s-90s with Gerard de Zeeuw.

### Key Differences from CT
- CT focuses on analyzing specific features that allow a conversation to **emerge** between
  two participants.
- IA focuses on the broader domain in which conversations may **appear, disappear, and
  reappear** over time.
- CT operates in a **kinematic domain** (bounded by beginnings and ends).
- IA operates in an **eternal kinetic domain** (processes have no fixed boundaries).

### Formal Character
- IA is described as "a concurrent spin calculus applied to the living environment with
  strict topological constraints."
- Pask defined concepts as **persisting, countably infinite, recursively packed spin
  processes** in any medium (stars, liquids, gases, solids, machines, brains) that produce
  relations.
- Concepts exert **parity** — like or unlike, clockwise or anticlockwise — for a given
  observer in a given context.

### Spin-Spin Forces
- Pask introduced **spin-spin forces** as the agents of self-organization, learning,
  and evolution.
- **Like concepts repel** (unfold, differentiate).
- **Unlike concepts attract** (coalesce, combine).
- After sufficient interaction ("faith"), like-seeming concepts always produce a difference
  and thus an attraction — this is the engine of novelty.

### Many-Worlds Analogy
Pask on the many-worlds interpretation of quantum mechanics:
> "Theories of many universes, one at least for each participant — one to participant A
> and one to participant B — are bridged by an analogy. As before, this is the truth value
> of any interaction: the metaphor for which is culture itself."

---

## Key References

### Primary Sources
- Pask, G. (1975). *Conversation, Cognition and Learning*. Elsevier.
- Pask, G. (1976). *Conversation Theory: Applications in Education and Epistemology*. Elsevier.
- Pask, G. (1984). "Review of conversation theory and a protologic (or protolanguage), Lp."
  *ECTJ* 32, 3-40.
- Pask, G. (1996). "Heinz von Foerster's Self-Organization, the Progenitor of Conversation
  and Interaction Theories." (Final paper, posthumous.)

### Secondary Sources
- Scott, B.C.E. (2001). "Gordon Pask's Conversation Theory: A Domain Independent
  Constructivist Model of Human Knowing." *Foundations of Science* 6, 343-360.
- Scott, B.C.E. (2009). "Conversation, Individuals and Concepts: Some Key Concepts in
  Gordon Pask's Interaction of Actors and Conversation Theories." *Constructivist
  Foundations* 4(3), 151-158. https://constructivist.info/4/3/151.scott
- Tilak, S., Manning, T., Glassman, M., Pangaro, P. & Scott, B.C.E. (2024). "Gordon Pask's
  Conversation Theory and Interaction of Actors Theory: Research to Practice." *Enacting
  Cybernetics*. https://enacting-cybernetics.org/articles/10.58695/ec.11
- Pangaro, P. (2001). "THOUGHTSTICKER 1986: A personal history of conversation theory in
  software, and its progenitor, Gordon Pask." *Kybernetes*.
  https://www.pangaro.com/history-conversation-theory.html
- Pangaro, P. Archive of Pask PDFs: https://pangaro.com/pask-pdfs.html

---

## Summary Table of Core CT Concepts

| Concept | Definition | Role in CT |
|---------|-----------|------------|
| **Lo** (Object Language) | Language for discussing subject matter | Enables descriptions and derivations of topics |
| **Lp** (Protolanguage) | Metalanguage governing conceptualization | Rules of inference for how concepts form |
| **Entailment Mesh** | Cyclic graph of topic relations | The "objective" knowledge structure (toroidal) |
| **Entailment Structure** | Pruned/directed view of the mesh | Individual learner's path through knowledge |
| **Teachback** | Role-reversal verification | How shared understanding is confirmed |
| **M-Individual** | Physical/mechanical substrate | The body, machine, or hardware |
| **P-Individual** | Psychological/conceptual operator | The perspective, role, or cognitive process |
| **No Doppelgangers** | Exclusion principle | No two interaction products can be identical |
| **Complementarity** | Process-product duality | Processes produce products; products imply processes |
| **Cognitive Reflector** | Virtual machine for conversation | Manages concept selection and agreement tracking |
| **Agreement** | Shared public concept | Product of successful teachback |
| **Comprehension Learning** | Understanding "what may be known" | Navigating entailment structures |
| **Operation Learning** | Mastering "what may be done" | Navigating task structures |

---

*Notes compiled 2026-03-12. Sources accessed via web search and direct URL retrieval.
Primary texts (Pask 1975, 1976) referenced through secondary scholarly analyses.*
