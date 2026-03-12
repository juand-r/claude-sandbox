# Closure to Efficient Causation

**Key sources:**
- Rosen (1991). *Life Itself*, Section 10A.
- Cardenas, Letelier et al. (2010). "Closure to efficient causation, computability and artificial life." *J. Theor. Biol.* 263(1):79-92.
- Chemero & Turvey (2006/2008). "Complexity and Closure to Efficient Cause."
- Mossio, Longo & Stewart (2009). "A computable expression of closure to efficient causation." *J. Theor. Biol.*
- Piedrafita et al. (2010). "A Simple Self-Maintaining Metabolic System." *PLOS Computational Biology*.
- Siekmann (2020). "An applied mathematician's perspective on Rosennean Complexity." *Ecological Complexity*.

## The Concept

### Rosen's Fundamental Theorem of Relational Biology

"A natural system is an organism if and only if it is closed to efficient causation."

### What "Efficient Cause" Means

Aristotle's efficient cause is the agent or process that brings something about — the "maker." In modern terms, it is closest to the standard notion of causality.

In the context of (M,R)-systems, each component is the efficient cause of the transformation of elements in its domain to elements in its range:
- f is the efficient cause of the transformation A -> B
- Phi is the efficient cause of the production of f
- beta is the efficient cause of the production of Phi

### What "Closure" Means

**Closed to efficient causation:** All the specific catalysts/efficient causes needed for the system to maintain itself must be produced by the system itself.

**Not closed to material causation:** The system is open to matter and energy flows. It needs environmental inputs (food, energy). But it produces its own machinery.

Analogy: A factory that imports raw materials (open to material cause) but manufactures all of its own machines, tools, and robots (closed to efficient cause).

### What Closure is NOT

- It is NOT thermodynamic closure (organisms are open thermodynamic systems)
- It is NOT informational closure (organisms receive information from environment)
- It is NOT physical closure (organisms exchange matter with environment)
- It IS organizational closure — the organization maintains itself

## The Computability Debate

### Rosen's Claim
Closure to efficient causation creates impredicative loops. Impredicative structures are not Turing-computable. Therefore, organisms cannot be simulated by Turing machines.

### Challenges to This Claim

**Cardenas et al. (2010):**
- Closure to efficient causation should be regarded as a *hypothesis* to be tested, not a proven theorem
- Proposed mathematical models for how it could be implemented
- The "closure" is not a result that follows automatically from the construction of (M,R)-systems

**Mossio, Longo & Stewart (2009):**
- Expressed closure to efficient causation in lambda-calculus
- Used a fixed-point operator to identify functions for f, B, and Phi
- Argued that "Rosen's definitional infinite regress is perfectly handled by recursion, in particular as formalized in the lambda-calculus"

**Counter-counter-argument (Cardenas et al.):**
- Mossio et al. do not accurately represent (M,R) systems
- Specifically, they fail to capture the difference between B as product and b as catalyst

### The Current State

The computability question remains genuinely open. The mathematical arguments on both sides have significant subtleties. What is clear:
- The *concept* of closure to efficient causation is well-defined and biologically meaningful
- Whether it implies non-computability depends on contested mathematical arguments
- Even if computable, the closure property is still a useful design principle

## Minimal Self-Maintaining Systems

Piedrafita et al. (2010) showed that a small system with three catalytic cycles, all catalysts produced internally, can:
- Establish and maintain a non-trivial steady state
- Resist degradation of catalysts (as long as degradation is not too fast)
- Recover from large perturbations, including complete loss of a catalyst
- There exists a minimum volume below which self-organization cannot be maintained

This is the closest thing to an experimental/computational realization of closure to efficient causation.

## Relationship to Other Closure Concepts

| Framework | Closure Type | Key Difference from Rosen |
|-----------|-------------|--------------------------|
| Autopoiesis (Maturana/Varela) | Organizational + boundary | Emphasizes self-production of boundary (membrane) |
| Chemoton (Ganti) | Metabolic + template + membrane | Three subsystem model, more concrete |
| Autocatalytic sets (Kauffman) | Catalytic closure | Each catalyst produced by some reaction in the set |
| Operational closure (Luhmann) | Communication closure | Applied to social systems |
| Rosen's (M,R) | Efficient causal closure | Most abstract; category-theoretic; includes replication |

Letelier et al. (2003) showed that autopoietic systems are a *subset* of (M,R)-systems. What autopoiesis adds is the requirement for boundary generation and internal topology.

## Relevance to Agent Architectures

### Testing AI Agents for Closure

An agent is closed to efficient causation if:

1. Its processing pipeline (metabolism) is maintained by its own outputs
2. The maintenance process (repair) is itself maintained by the system
3. No essential "catalyst" requires external provision

Current AI agents typically fail because:
- Model weights: produced by external training, not self-generated
- Code/architecture: written by external developers
- Reward/objective: often externally specified
- Infrastructure: external compute, networking, storage

### Degrees of Closure

Rather than binary (closed/not closed), we might think of *degree of closure*:
- **Zero closure:** Pure tool (requires external everything)
- **Partial closure:** Self-modifying agent (can update some of its own processes)
- **Near-complete closure:** Self-training agent on self-generated objectives with self-maintained infrastructure
- **Full closure:** Rosen's ideal — the agent produces ALL its own efficient causes

### The Fabrication-Assembly (F,A)-System Alternative

Palmer & Cloete proposed (F,A)-systems as an alternative to (M,R)-systems, specifically because (M,R) has been "notoriously problematic to realise in terms of real biochemical processes." The (F,A)-system separates fabrication from assembly, which may map better onto engineering architectures.
