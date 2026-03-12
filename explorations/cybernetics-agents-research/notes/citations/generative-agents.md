# Generative Agents: Interactive Simulacra of Human Behavior

**Citation:** Park, J.S., O'Brien, J.C., Cai, C.J., Morris, M.R., Liang, P., & Bernstein, M.S. (2023). "Generative Agents: Interactive Simulacra of Human Behavior." UIST 2023. arXiv:2304.03442. Stanford University, Google DeepMind.

**Cited in our notes:** wang-agent-survey.md (most cited example architecture), reflexion-paper.md (related memory architecture)

**Date:** 2026-03-12

---

## Key Findings

### Architecture
Three-component cognitive architecture for 25 agents in a sandbox world (Smallville):

**1. Memory Stream**
- Comprehensive natural language record of all agent experiences with timestamps
- Retrieval function combines three scores: recency (exponential decay), importance (LLM-rated poignancy), and relevance (embedding similarity)
- This retrieval formula is functionally similar to ACT-R's activation equation

**2. Reflection**
- Generates higher-level abstractions from accumulated observations
- Process: prompt LLM with 100 most recent records -> generate 3 salient questions -> retrieve relevant memories -> extract insights with evidence citations
- Creates hierarchical reflection trees (reflections on reflections)
- Triggered periodically, not continuously

**3. Planning**
- Recursive temporal decomposition: broad daily plan -> hourly chunks -> 5-15 minute actions
- Plans are reactive: new observations can override current plans
- Agents re-plan when encountering significant events

### Results
- Controlled evaluation (100 participants): full architecture scored highest believability (TrueSkill mu=29.89)
- Each ablation degraded performance: no reflection (26.88), no reflection+planning (25.64), no memory (21.21)
- Effect size vs. prior work: d=8.16 (massive)
- Emergent social behaviors: information diffusion (4% -> 52% for party), Valentine's Day party coordination with 5/12 invited agents attending
- Low hallucination rate: 1.3% (6/453 responses)
- Network density increased from 0.167 to 0.74 over 2 game days

---

## Relevance to Cybernetics-Agents Bridge

### Reflection as Second-Order Cybernetics
The reflection mechanism is a clear implementation of second-order observation: the agent observes its own observations and generates meta-level descriptions. Von Foerster would recognize this as a self-referential loop producing eigenforms — stable abstractions ("Klaus is dedicated to research") emerge as fixed points of recursive self-observation.

The hierarchical reflection trees (reflections on reflections) implement multiple orders of self-reference. This is the computational instantiation of second-order cybernetics: the observer observing itself.

### Memory Retrieval as Selective Perception
The retrieval function (recency + relevance + importance) determines what the agent "perceives" from its history. This is a **perceptual filter** — it constructs the agent's current experience from stored records. In cybernetic terms, this is the agent's **sensory apparatus**, and its parameters (alpha, beta, gamma weights) determine what the agent can regulate.

Ashby's insight applies: you can only regulate what you can sense. If the retrieval function cannot surface a relevant memory, the agent cannot act on that information, regardless of whether it was stored.

### Emergent Coordination Without Explicit Protocol
The Valentine's Day party coordination is striking: no explicit coordination mechanism exists. Agents coordinate through natural language interaction and shared observation. This is an emergent phenomenon from individual feedback loops — each agent acts on its own observations and reflections, and coordination emerges from the overlap of their perceptual fields.

This is consistent with Maturana & Varela's structural coupling: agents that share an environment co-determine each other's behavior through repeated interaction, without requiring a centralized coordinator.

### What Is Missing (Cybernetically)
- No explicit comparator or error signal
- No homeostatic variables — agents have no concept of viability bounds
- No stability analysis — the simulation runs for a fixed period, not indefinitely
- Reflection is batch, not continuous — triggered periodically rather than driven by error signals
- No variety analysis — do agents have sufficient behavioral variety for their environment?

---

## Most Important Cited References

1. **Bates, J. (1994).** "The Role of Emotion in Believable Agents" — foundational work on believable agent design
2. **Laird, J. & VanLent, M. (2001).** Cognitive architectures for believable agents
3. **Newell, A. (1990).** *Unified Theories of Cognition* — cognitive architecture foundations
4. **Park et al. (2022).** Social Simulacra — prior work on LLM-based persona generation
5. **Card, Moran & Newell (1983).** GOMS model — cognitive models for HCI
