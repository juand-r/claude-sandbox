# Boden (2006) — Mind as Machine: A History of Cognitive Science

**Full Citation:** Boden, M.A. (2006). *Mind as Machine: A History of Cognitive Science*. 2 volumes. Oxford: Oxford University Press. ~1700 pages.

**Source:** OUP catalog, PMC book review, PhilPapers, ResearchGate reviews, Amazon, Archive.org, Google Books.

---

## 1. Overview

The first and most comprehensive full-scale history of cognitive science. Nearly a million words across two volumes, with a 130-page bibliography of over 4000 entries. Ten years in the making. Boden (Professor of Cognitive Science, University of Sussex) has firsthand knowledge of most of the developments she describes.

The book's aim is twofold: to provide a historical account of cognitive science and to clarify what cognitive science actually is. Boden argues these are inseparable — you cannot understand cognitive science without understanding its history.

## 2. Structure

### Volume 1: Origins and Core Disciplines
- **Man as Machine: Origins of the Idea** — Tracing the metaphor from Descartes through La Mettrie to the 20th century. Boden notes that "mind as machine," contrary to appearances, is a recent idea in its current computational sense.
- **Anticipatory Engines** — Babbage, Turing, and the theoretical foundations
- **Cognitive Science Comes Together** — The 1950s convergence of AI, linguistics, psychology, neuroscience, and philosophy
- **Transforming Linguistics** — Chomsky's revolution and its impact
- **Cognitive Psychology** — From behaviorism to information processing
- **Cognitive Anthropology** — Culture and cognition
- Additional chapters on symbolic representation and reasoning

### Volume 2: AI and Beyond
- **Classical AI** (Chapters 10-11) — GOFAI: symbol manipulation, knowledge representation, expert systems, planning. The promises and failures.
- **Connectionism** (Chapters 12-13) — Neural networks, distributed representations, learning. The "new AI" challenge to symbolic approaches.
- **Neuroscience** (Chapter 14) — The brain sciences and their uneasy relationship with cognitive science
- **Artificial Life** (Chapter 15) — Self-organization, emergence, evolutionary computation
- **Philosophy of Cognitive Science** (Chapter 16) — Functionalism, eliminativism, consciousness, intentionality
- **Outlook** — Where cognitive science is heading (as of 2006)

## 3. Key Arguments

### 3.1 The Computer Metaphor
Boden uses a "wider notion" of computation that encompasses not just classical symbol manipulation but also connectionism and even cybernetics. The computer metaphor is the unifying thread of cognitive science — but Boden acknowledges its limits.

Reviewer Vincent Muller's critique: the wider notion of computation may be too wide to be meaningful. If everything from symbolic logic to neural networks to cybernetic feedback counts as "computation," the metaphor has lost its explanatory power.

### 3.2 AI: Not a Failed Program
Against those who pronounced AI dead after its failed promises (1970s "AI winter"), Boden argues that AI enormously advanced both itself and the cognitive sciences. The failures were failures of specific approaches and specific claims, not of the enterprise itself. Classical AI revealed the complexity of common sense reasoning; connectionism revealed the power of distributed representation and learning.

### 3.3 Cybernetics in the History
This is directly relevant to our research. Boden situates cybernetics as a precursor to cognitive science that was largely displaced by the computational approach. Key observations:
- Cybernetics explored many concepts (self-organization, feedback, adaptation) that cognitive science later rediscovered
- The "standard notion of computation doesn't cover cybernetics, nor even connectionist AI"
- The displacement of cybernetics by computationalism was partly sociological (funding, institutional power) not just intellectual
- Cybernetic ideas survived in specific niches: robotics, artificial life, complex systems, enactivism

### 3.4 The Divide Between Approaches
Cognitive science is "riddled with intellectual divides":
- Symbolic vs. connectionist
- Computational vs. dynamical
- Representational vs. embodied/enacted
- Individual vs. situated/distributed

Boden traces these divides historically and shows they are not merely technical disagreements but reflect fundamentally different conceptions of what mind is.

## 4. Relevance to Agent Design

### 4.1 The Historical Arc from Cybernetics to Agents
Boden's history reveals the intellectual genealogy of current AI agent design:
1. **Cybernetics (1940s-60s)**: Feedback, control, adaptation, self-organization
2. **Classical AI (1960s-80s)**: Symbolic planning, knowledge representation, reasoning
3. **Connectionism (1980s-90s)**: Learning, pattern recognition, distributed processing
4. **Embodied/Situated AI (1990s-00s)**: Behavior-based robotics, environmental coupling
5. **LLM-based agents (2020s)**: Language as the medium of reasoning and action

Modern LLM agents inherit primarily from strand 2 (symbolic reasoning about the world via language) with elements of strand 3 (learned representations). They largely skip strands 1 and 4 — cybernetic control and embodied interaction.

### 4.2 Lessons from AI's History of Failure
Boden's account of AI failures is instructive for current agent design:
- **Frame problem**: Classical AI could not determine what was relevant in a changing situation. Current LLM agents face a version of this: which parts of the context are relevant to the current task?
- **Brittleness**: Expert systems worked in narrow domains but failed at boundaries. Current agents similarly fail when tasks exceed their training distribution.
- **Common sense**: The most persistent problem. LLMs appear to have common sense but fail in subtle, unpredictable ways — the same problem Boden documents for GOFAI.

### 4.3 The Recurring Pattern
Boden's history reveals a recurring pattern: each new approach to AI begins with bold claims, achieves impressive initial results, hits fundamental limitations, and is partially displaced by a new approach that inherits some ideas and rejects others.

Cybernetics → GOFAI → Connectionism → Embodied AI → LLM Agents

If the pattern holds, current LLM-based agents will hit fundamental limitations and be partially displaced by an approach that inherits some elements (language capability, world knowledge) and rejects others (disembodiment, lack of genuine autonomy, purely representational reasoning).

The cybernetics-enactivism tradition suggests what that next approach might emphasize: embodiment, genuine autonomy, adaptive self-organization, and performative engagement with the world.

### 4.4 What Cognitive Science Reveals About Agent Limitations
Boden's survey shows that cognitive science has identified capabilities that current AI approaches cannot replicate:
- **Genuine understanding** (vs. behavioral mimicry)
- **Creative insight** (vs. combinatorial search)
- **Common sense reasoning** (vs. pattern matching)
- **Motivated action** (vs. programmed goal pursuit)
- **Social cognition** (vs. protocol-based interaction)

Each of these gaps corresponds to a cybernetic concept: genuine understanding = Good Regulator (having an internal model), creative insight = exploration of variety space, common sense = requisite variety in world model, motivated action = autopoietic normativity, social cognition = Pask's conversation theory.

## 5. Connections to Other Sources

- **Pickering (2010)**: Covers the cybernetics history that Boden treats as a precursor. Pickering is deeper on cybernetics; Boden is broader on cognitive science.
- **Ashby, Wiener, Beer, Pask**: All appear in Boden's history as precursors to cognitive science proper.
- **Thompson (2007)**: The enactive approach that Boden discusses as one of the "divides" in cognitive science.
- **Brooks**: The subsumption architecture appears in Boden's coverage of embodied/situated AI.
- **Wooldridge**: Agent-based AI appears as one of the more recent developments.

## 6. Assessment

This is an indispensable reference work. No other source provides such a comprehensive view of the intellectual landscape in which cybernetics, AI, and cognitive science intersect. For our research, its main value is contextual: it shows how cybernetic ideas were marginalized, how their competitors fared, and where the gaps remain that cybernetics might fill.

The main limitation for our purposes is temporal: the book was written before LLMs and the current agent revolution. Boden could not have anticipated how dramatically the landscape would change. But her analysis of recurring patterns (bold claims, initial success, fundamental limitations, partial displacement) is eerily predictive of the current situation.

---

*Notes compiled 2026-03-12 from OUP, PMC review, PhilPapers, and secondary analyses.*
