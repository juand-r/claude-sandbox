# Conant & Ashby (1970) — Every Good Regulator of a System Must Be a Model of That System

**Full Citation:** Conant, R.C. & Ashby, W.R. (1970). "Every Good Regulator of a System Must Be a Model of That System." *International Journal of Systems Science*, 1(2), 89-97.

**Cited in our notes:** good-regulator-theorem.md, ashby-intro-cybernetics.md, beer-vsm.md

**Source:** Full text obtained via [pespmc1.vub.ac.be PDF](https://pespmc1.vub.ac.be/books/Conant_Ashby.pdf); extracted via pdftotext.

---

## 1. Setup

The theorem operates on a regulation scenario with five sets and three mappings, following Sommerhoff (1950):

**Sets:**
- **Z** — total set of events (outcomes), regulated and unregulated
- **G ⊆ Z** — "good" outcomes (the goal set)
- **R** — events in the regulator H
- **S** — events in the rest of the system (the "reguland")
- **D** — primary disturbers (Sommerhoff's "coenetic variable")

**Mappings:**
- φ: D → S (disturbance determines system state)
- ρ: D → R (disturbance determines regulator state)
- ψ: S × R → Z (system and regulator jointly determine outcome)

Regulation is successful when H(Z) (Shannon entropy of outcomes) is minimal.

## 2. Error-Controlled vs. Cause-Controlled Regulation

A key preliminary distinction (Section 3): error-controlled regulation (where R gets information about D indirectly, through deviation in Z) is "a primitive and demonstrably inferior method." In cause-controlled regulation, R observes D directly and can achieve H(Z) = 0 (perfect regulation). The theorem addresses the more advanced cause-controlled case.

This connects to Ashby's treatment in *Introduction to Cybernetics* (S.12/14) where error-based regulation "cannot be perfect."

## 3. The Formal Theorem

**Theorem:** The simplest optimal regulator R of a reguland S produces events R which are related to the events S by a mapping h: S → R.

"The best regulator of a system is one which is a model of that system in the sense that the regulator's actions are merely the system's actions as seen through a mapping h."

### Proof

Given:
- Sets R, S, Z and mapping ψ: R × S → Z
- A probability distribution p(S) over system states
- Regulator behavior specified by conditional distribution p(R|S)
- p(S) and p(R|S) jointly determine p(Z) and H(Z)
- Class π = all optimal distributions p(R|S) minimizing H(Z)

**Lemma:** For any optimal p(R|S) and any sⱼ ∈ S, all rᵢ with positive probability p(rᵢ|sⱼ) map (with sⱼ under ψ) to the same zₖ.

*Proof of lemma:* Suppose two rᵢ with positive probability mapped to different zₖ. Then we could shift probability between them to make p(Z) more unequal, which necessarily decreases H(Z) — contradicting optimality.

**Main proof:** Given the lemma, for any sⱼ, all rᵢ with positive probability produce the same outcome. We can select one such rᵢ, set its probability to 1 and others to 0, without affecting H(Z). Repeating for all sⱼ yields a deterministic mapping h: S → R. This is the "simplest optimal" regulator. QED.

## 4. What "Model" Means (Critical Point)

The isomorphism is of the form:

∃h : ∀i : ρ(i) = h[σ(i)]

where ρ and σ are the mappings that R and S impose on their common input. This is a **Black Box homomorphism** — the regulator's behavior mirrors the system's behavior through a mapping.

This is what RL calls a **policy** (state-to-action mapping), NOT a predictive world model. The "model" is functional, not representational.

## 5. Key Qualifications

1. "Not all optimal regulators are models of their regulands" — only the simplest ones are. Others are "unnecessarily complex."
2. The theorem "leaves open the question of how R, S, and Z are interrelated" — it applies to both cause-controlled (fig. 1) and error-controlled (fig. 2) configurations.
3. The assumption p(S) is constant can be weakened: for slowly varying p(S), a time-varying model is needed.
4. The theorem says nothing about how the model is built or learned.

## 6. Relation to Our Cybernetics-Agents Research

### What the theorem actually proves
Stripped of rhetoric: the simplest optimal policy is a deterministic function of the state. As Erdogan (2021) noted, this is "almost trivial."

### Why it matters anyway
- It was the first formal attempt to prove the necessity of modeling in regulation.
- It directly extends Ashby's Law of Requisite Variety: the regulator's variety (number of distinct responses) must match the system's variety.
- It launched a research program culminating in Francis & Wonham's Internal Model Principle (1976) and Richens et al.'s (2025) proof that general agents contain world models.

### Bridge to agent design
- The theorem establishes a minimum: any good agent policy must be a deterministic function of the state.
- But it does NOT establish whether agents need internal predictive models — that requires the stronger results of Francis & Wonham (for linear systems) or Richens et al. (for multi-goal agents).
- The distinction between "model as policy" and "model as world model" is critical for understanding modern agent architectures.

## 7. Key References Cited in This Paper

- **Sommerhoff, G. (1950). *Analytical Biology*.** — The five-variable framework for regulation that Conant & Ashby build on.
- **Ashby, W.R. (1967). "The Set Theory of Mechanism and Homeostasis."** In Stewart (ed.), *Automaton Theory and Learning Systems*. — Ashby's set-theoretic reformulation of regulation.
- **Conant, R.C. (1969). IEEE Trans. Systems Sci., 5, 334.** — Conant's earlier work showing regulation and modeling are closely related. Distinguishes information-conserving vs. lossy channels.
- **Hartmanis, J. & Stearns, R.E. (1966). *Algebraic Structure Theory of Sequential Machines*.** — Formal definition of machine homomorphism used in the proof.

---

*Notes compiled 2026-03-12 from full text of the original paper.*
