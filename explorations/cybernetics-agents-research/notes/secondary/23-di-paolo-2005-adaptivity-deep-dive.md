# Di Paolo (2005) — Autopoiesis, Adaptivity, Teleology, Agency (Deep Dive)

**Full Citation:** Di Paolo, E.A. (2005). "Autopoiesis, Adaptivity, Teleology, Agency." *Phenomenology and the Cognitive Sciences*, 4, 429-452.

**Existing notes:** See `notes/citations/di-paolo-2005-autopoiesis-adaptivity.md` for the primary analysis. This note goes deeper on implications for artificial agent design.

**Source:** Springer abstract, PhilPapers, Academia.edu, SciSpace, Di Paolo's website, secondary analyses, and downstream citations.

---

## 1. Recap: The Central Move

Di Paolo identifies a gap in autopoiesis: an autopoietic system can be merely robust (passively withstanding perturbations) without being adaptive (actively regulating its distance from viability boundaries). He introduces **adaptivity** — the capacity to evaluate one's position relative to viability conditions and act to improve it.

The chain: Autopoiesis (identity) + Adaptivity (graded evaluation) = Sense-making (intrinsic generation of significance).

## 2. Deeper Analysis: What Adaptivity Formally Requires

The key formal structure of adaptivity:

1. **Viability space**: The set of all states in which the system maintains its organization. Not a point but a region with boundaries.
2. **Graded distance from boundaries**: The system must have some internal indicator of how close it is to losing viability. This is not binary (alive/dead) but continuous.
3. **Directional evaluation**: The system must detect not just distance but **direction** — whether its trajectory is moving toward or away from viability boundaries.
4. **Regulatory capacity**: The system must be able to modify its own dynamics (behavior, structure, coupling) in response to viability assessments.

This is more demanding than Ashby's ultrastability, which triggers only when essential variables actually exceed bounds. Di Paolo's adaptive system acts **before** reaching bounds, based on trajectory evaluation.

## 3. The Spectrum of Adaptivity

Di Paolo describes adaptivity as "many-layered" — it is not a single property but a spectrum:

- **Metabolic adaptivity**: Adjusting internal biochemical processes to maintain viability (e.g., enzyme regulation)
- **Behavioral adaptivity**: Modifying sensorimotor patterns to change environmental coupling (e.g., chemotaxis)
- **Developmental adaptivity**: Structural changes over longer timescales that alter the organism's capacities (e.g., phenotypic plasticity)
- **Evolutionary adaptivity**: Population-level changes in organizational patterns (not individual but lineage)

Each layer operates at a different timescale and modifies a different aspect of the organism's organization.

## 4. Implications for Artificial Agents — Going Deeper

### 4.1 The Graded Viability Problem

Current AI agents have binary success/failure criteria: the task is either completed or not. Di Paolo's framework suggests a richer evaluative architecture:

**What "viability" could mean for an AI agent:**
- Token budget remaining (resource viability)
- Context window utilization (information viability)
- Confidence in current world model (epistemic viability)
- Coherence of action plan (operational viability)
- Consistency with user intent (alignment viability)

Each of these defines a viability dimension. The agent's state is a point in a multi-dimensional viability space. Adaptivity means monitoring distance from boundaries in all dimensions simultaneously.

### 4.2 Trajectory Evaluation vs. State Evaluation

Most current agent evaluation is state-based: "Did the current action succeed?" Di Paolo's adaptivity requires **trajectory evaluation**: "Am I heading toward failure?"

This implies:
- Agents should track not just current state but rate of change of viability indicators
- An agent burning through its token budget at an accelerating rate should notice this trend and adjust, even if current output is acceptable
- Declining confidence in successive actions should trigger strategic reassessment, not just local retry

### 4.3 The Norm-Generation Problem

The deepest challenge Di Paolo poses for AI: genuine adaptivity requires **self-generated norms**. The organism's norms arise from its autopoietic organization — what counts as "good" or "bad" is determined by the organism's own conditions of continued existence.

For AI agents, norms are always externally imposed: by the programmer, the user, the reward function. Can an AI system generate its own norms?

**Possible approaches:**
1. **Derived norms**: The agent's operational requirements generate secondary norms. If the agent must maintain context coherence to function, then coherence becomes an internally generated norm — not because anyone programmed "maintain coherence" but because incoherence causes operational failure.
2. **Emergent norms**: In multi-agent systems, interaction dynamics might generate norms that no individual agent was programmed to follow. (Cf. Thompson's participatory sense-making.)
3. **Metabolic analogy**: Give the agent a "metabolism" — ongoing processes that must be maintained for continued operation. Resource management, memory management, model updating. These create intrinsic norms.

### 4.4 Adaptivity at Multiple Timescales

Following Di Paolo's multi-layered adaptivity, AI agents could implement:

1. **Immediate adaptivity** (within-task): Adjusting strategy based on current feedback. This is what ReAct and Reflexion do.
2. **Session adaptivity** (across-tasks): Learning from accumulated experience within a session to modify general approach. Current agents partially do this via context accumulation.
3. **Developmental adaptivity** (across-sessions): Structural changes to the agent's architecture or prompts based on long-term performance patterns. This is mostly absent from current designs.
4. **Population adaptivity** (across-agents): Evolutionary optimization of agent designs based on population-level performance. This corresponds to prompt optimization and fine-tuning.

## 5. The Conservation vs. Homeostasis Distinction

One of Di Paolo's most subtle points: autopoiesis entails **conservation** (the organization is maintained) but not **homeostasis** (the organization is actively maintained against perturbation). Conservation admits "fortuitous self-maintenance" — the system persists simply because nothing disrupts it. Homeostasis requires active regulation.

For agents: an LLM agent that produces correct outputs because its training data happened to cover the current task is "fortuitously self-maintaining." An agent that monitors its own performance and adjusts its strategy when it detects degradation is genuinely homeostatic.

The difference matters because fortuitous self-maintenance is brittle — it fails as soon as the environment changes beyond what was anticipated. Active homeostasis is robust because it responds to the novel.

## 6. Connection to Hans Jonas's Existential Biology

Di Paolo draws on Jonas to ground the philosophical argument. Jonas's insight: the living being's existence is not a given but a constant achievement. The organism must continuously work to maintain itself against entropic dissolution. This creates:

1. **A self** that is its own doing — identity through activity, not through substance
2. **Needfulness** — the organism is always in need, always dependent on exchanges with the environment
3. **Freedom** — because the organism can succeed or fail at self-maintenance, it has a minimal form of freedom

For AI: an agent with no genuine precariousness has no genuine freedom. Its "choices" are not real choices because nothing is at stake for the agent itself.

## 7. Downstream Influence

Di Paolo's adaptivity concept has been foundational for:
- **Froese & Ziemke (2009)**: Adaptivity as one of two design principles for enactive AI
- **Thompson (2007)**: Adopts adaptivity as central to the enactive approach
- **Barandiaran, Di Paolo & Rohde (2009)**: Defining agency as autonomous adaptive regulation
- **De Jaegher & Di Paolo (2007)**: Participatory sense-making in social cognition
- **The broader 4E cognition movement**: Embodied, embedded, enacted, extended

## 8. Critical Appraisal

Di Paolo's paper is one of the most important works bridging cybernetics and the philosophy of mind in the 2000s. Its main contribution — adaptivity as graded viability regulation — is both philosophically rigorous and operationally suggestive. The main limitation is that it remains largely at the conceptual level; there is no mathematical formalism for adaptivity comparable to Ashby's variety calculus or Friston's free energy. This formalization gap is an open research problem.

---

*Notes compiled 2026-03-12 from Springer, PhilPapers, Academia.edu, Di Paolo's website, and downstream citations.*
