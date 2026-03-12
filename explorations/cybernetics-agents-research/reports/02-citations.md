# Report: Citation-Chased Papers

**Scope:** 30 papers found by following references from primary sources (notes/citations/)

---

## What Was Read

Papers fall into three clusters:

### Cybernetics Extensions
- Conant & Ashby (1970) — Good Regulator Theorem (original)
- Francis & Wonham (1976) — Internal Model Principle
- Wonham (2018) — IMP in sets and functions
- Virgo et al. (2025) — Good Regulator for embodied agents
- Rosenblueth, Wiener & Bigelow (1943) — Behavior, Purpose, Teleology
- Shannon (1948) — Mathematical Theory of Communication
- Kauffman (2003) — Eigenforms
- Varela (1975) — Calculus for self-reference
- Reichel (2011) — Varela's self-reference and praxis
- Powers, Clark & McFarland (1960) — General Feedback Theory of Human Behavior
- Siegenfeld & Bar-Yam (2022) — Multi-scale requisite variety
- Di Paolo (2005) — Autopoiesis, adaptivity, teleology, agency
- Di Paolo & Thompson — Enactive approach
- Froese & Stewart (2010) — Life After Ashby
- Berkenkamp et al. (2017) — Safe RL with stability guarantees

### Agent Papers
- Richens et al. (2025) — General Agents Contain World Models
- Huang et al. (2023) — LLMs Cannot Self-Correct Reasoning
- Kambhampati — LLMs Can't Plan
- Madaan et al. (2023) — Self-Refine
- Turpin et al. — Unfaithful Chain of Thought
- Wang et al. (2023) — Self-Consistency
- Park et al. (2023) — Generative Agents
- Hong et al. (2023) — MetaGPT
- Wang et al. (2023) — Voyager
- Cemri et al. (2025) — Multi-agent failure taxonomy
- Arike et al. (2025) — Goal drift in LLM agents
- Sajid et al. (2021) — Active Inference Demystified
- Tschantz et al. (2020) — RL through Active Inference

---

## Key Findings

### 1. The Internal Model Principle Is Stronger Than the Good Regulator Theorem

Wonham's (2018) IMP formulation shows that a robust controller must contain a *dynamical copy* of the disturbance generator — the controller's internal dynamics must commute with the exosystem's dynamics. This is stronger than Conant-Ashby (which only requires a deterministic mapping). The IMP says agents need to learn the *generative structure* of their environment, not just the correct response to each state. This distinction matters: memorizing Q-values (state-action mapping) is Conant-Ashby; learning a world model (dynamics) is IMP.

Wonham's "shape of the river" metaphor: the pilot doesn't memorize specific configurations but learns the invariant dynamic structure that persists across perturbations. This is exactly what transformer attention patterns may be learning.

### 2. Virgo et al. (2025) Resolves the Good Regulator Counterexamples

The reformulated theorem shows that *any* good regulator can be *interpreted* as having beliefs — but the interpretation is observer-attributed (intentional stance), not intrinsic. This resolves the doorstop objection (trivial systems satisfy the theorem trivially). For agent design, this means the theorem is useful for post-hoc analysis (what beliefs would make this agent's behavior rational?) but not for design (doesn't tell you how to build a regulator).

### 3. Richens et al. (2025) Finally Proves What People Thought Conant-Ashby Proved

General agents operating over multi-step horizons with multiple goals necessarily encode extractable world models in their policies. This is the result the agent community wanted the Good Regulator Theorem to be. The proof establishes that LLMs, as multi-goal agents, must be encoding world models — and indeed, recent work on probing LLM internals confirms extractable spatial and temporal representations.

### 4. LLM Self-Correction Fails Exactly Where Ashby Predicts

Huang et al. (2023) shows LLMs cannot self-correct reasoning without external feedback. Madaan et al. (2023) documents a 94% false-positive rate in Self-Refine's self-evaluation on math tasks. The cybernetic explanation: the evaluator (same LLM) has the same systematic biases as the generator. Its variety for error detection is bounded by its independence from the error source. When evaluator = generator, systematic errors pass through undetected. This is Ashby's Law applied to the self-evaluation channel.

### 5. Multi-Scale Requisite Variety Explains AutoGPT's Failure Pattern

Siegenfeld & Bar-Yam (2022) extend Ashby's Law to multiple scales. Applied to AutoGPT: variety was matched at the fine scale (individual actions) but absent at coarse scales (strategy, meta-cognition). This predicts AutoGPT would execute individual steps competently while failing at multi-step coordination — exactly what was observed.

### 6. Voyager Implements Cybernetic Variety Accumulation

Voyager's skill library is a persistent variety amplifier — it stores successful behavioral patterns as reusable code. Unlike Reflexion's episodic memory (what went wrong) or ReAct's ephemeral reasoning, the skill library creates composable, persistent variety. Combined with multi-source feedback (environment, code interpreter, LLM critic), Voyager achieves better error correction through channel diversity — consistent with Shannon's channel coding theorem.

### 7. Goal Drift Is Reference Signal Degradation

Arike et al. (2025) documents goal drift in LLM agents: agents lose track of their original objective as context accumulates. In cybernetic terms, this is corruption of the reference signal. The context window functions as a noisy channel; as the conversation grows, the goal signal degrades relative to accumulated noise. Homeostatic architectures (explicit setpoints maintained outside the context) would prevent this.

### 8. Active Inference Is Mathematically Equivalent to RL But Practically Uncompetitive

Tschantz et al. (2020) proves formal equivalence between active inference and RL. Sajid et al. (2021) shows active inference provides natural exploration-exploitation balance without ad-hoc mechanisms. But no competitive active-inference LLM agent exists. The framework is mathematically elegant but has not been implemented at scale.

---

## Assessment

The citations fill critical gaps in the primary source analysis. The most important finding: the hierarchy of regulator theorems (Conant-Ashby < IMP < Richens et al.) provides increasingly strong formal foundations for why agents need world models. The self-correction failure evidence (Huang, Madaan) is the strongest empirical validation of cybernetic predictions. The multi-scale variety framework is the most actionable diagnostic tool. Active inference remains the most promising but least realized theoretical bridge.
