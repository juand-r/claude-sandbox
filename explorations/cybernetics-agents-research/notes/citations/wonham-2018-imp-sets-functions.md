# Wonham (2018) — The Internal Model Principle in Sets and Functions

**Full Citation:** Wonham, W.M. (2018). "The Internal Model Principle of Control Theory." Expository note, University of Toronto. Available at [utoronto.ca](https://www.control.utoronto.ca/~wonham/W.M.Wonham_IMP_20180617.pdf).

**Cited in our notes:** good-regulator-theorem.md (Section 5, as context for Francis & Wonham 1976)

**Source:** Full text extracted via pdftotext.

---

## 1. Purpose

This note develops the Internal Model Principle in "as elementary a setting as possible, namely just that of plain sets and functions" — removing the restriction to linear systems. This makes the IMP potentially universal, applicable to any dynamical system.

## 2. The Framework

### Total System
S = Exosystem (E) × Controller (C) × Plant (P)

State space X = X_E × X_C × X_P

One-step transition function α: X → X

### Key Definitions

**Internal stability:** The exosystem's embedded image X̃_E is a **global attractor** — all trajectories eventually converge to it.

**Error feedback:** The controller's dynamics are **autonomous** (self-contained, not externally driven) whenever regulation is perfect (state is on the target set K). External input reaches the controller ONLY when regulation fails.

**Perfect regulation:** The system reaches and remains on the target set K where tracking error is zero.

**Exosystem detectability:** The exosystem is observable by the controller during perfect regulation.

## 3. Theorem 1 (Assertion 1)

Under internal stability, perfect regulation, error feedback, and exosystem detectability:

1. There exists a unique mapping α_C: X_C → X_C (controller's autonomous dynamics)
2. α_C ∘ γ̃_E = γ̃_E ∘ α̃_E — the controller dynamics COMMUTE with the exosystem dynamics on the attractor
3. γ̃_E is injective — the copy is **faithful**

**Translation:** On the invariant set where regulation is perfect, the controller's internal dynamics are a faithful copy of the exosystem's dynamics. The controller literally simulates the disturbance generator.

The proof is constructive: it builds up the commutative diagram showing the isomorphism between controller and exosystem dynamics.

## 4. Assertion 2 (Structural Stability)

When parameter robustness is added:

Structurally stable perfect regulation ⇒ Error feedback + Internal Model

This is the stronger assertion: not only does the controller contain an internal model, but error feedback is ALSO necessary. You need both.

The parameter perturbation model: enlarge state structure with parameter set M. Internal stability, perfect regulation, and detectability must hold for EVERY parameter value μ ∈ M.

Result: a "small" perturbation merely shifts the current state to a "neighboring" trajectory of the SAME dynamics. The internal model captures the invariant dynamic structure that persists across perturbations.

## 5. The "Shape of the River"

Wonham quotes Mark Twain's riverboat pilot: "You only learn the shape of the river; and you learn it with such absolute certainty that you can always steer by the shape that's in your head, and never mind the one that's before your eyes."

What IS the "shape"? Wonham's answer: it is the equivalence class of trajectories under the exosystem dynamics — the invariant structural pattern that persists despite moment-to-moment changes. The pilot's internal model captures this invariant, not the specific configuration at any instant.

This is a beautiful illustration of what the IMP means concretely: the controller doesn't memorize specific states but learns the DYNAMICS — the generative structure that produces the reference/disturbance signals.

## 6. Relation to Good Regulator Theorem

Wonham's formulation makes the distinction sharp:

- **Conant-Ashby:** Optimal policy is a deterministic function of state. (State → Action mapping.)
- **IMP:** Controller dynamics must commute with exosystem dynamics. (Dynamic structure → Dynamic structure.)

The IMP is about DYNAMICS, not just mappings. The controller doesn't just respond correctly to each state — it internally reproduces the temporal evolution of the disturbance source.

## 7. Relation to Our Cybernetics-Agents Research

### Connection to Ashby
The IMP formalizes what Ashby's Law of Requisite Variety states qualitatively: the controller's variety must match the disturbance variety. The IMP specifies that this match must be STRUCTURAL — the dynamics must commute, not just the static variety.

### For agent architectures
This suggests that agents in environments with structured dynamics need to learn not just optimal responses but the GENERATIVE MODEL of the environment's temporal patterns. This is precisely what:
- World models in model-based RL do
- Transformer attention patterns learn (temporal structure of sequences)
- Beer's System 4 does (modeling the environment's dynamic structure)

### The autonomy condition
The error feedback requirement is noteworthy: the controller becomes autonomous (self-driven) during perfect regulation. It runs on its own internal model. External input arrives ONLY when regulation fails. This is exactly Beer's System 3-4 homeostat: the metasystem runs autonomously unless the 3-4 balance fails, at which point System 5 intervenes.

## 8. Key References Cited

- **Craik, K. (1943). *The Nature of Explanation*.** — The original statement that minds model reality.
- **Hobbes, T. (1651). *Leviathan*.** — "All automata have an artificial life."
- **Smith, O.J.M. (1958). *Feedback Control Systems*.** — Internal model in predictive control.

---

*Notes compiled 2026-03-12 from full text extracted via pdftotext.*
