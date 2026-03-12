# Rosen (1991) — Life Itself

**Citation:** Rosen, R. (1991). *Life Itself: A Comprehensive Inquiry into the Nature, Origin, and Fabrication of Life*. Columbia University Press, New York. ISBN 978-0-231-07565-7.
**Access:** Available from Columbia University Press and Amazon. Some chapters on JSTOR.

## Summary

Rosen's magnum opus. Thirty years of work distilled into a single argument: living systems are fundamentally different from machines, and this difference can be stated precisely using category theory and the concept of closure to efficient causation.

## The Central Thesis

**"A material system is an organism if, and only if, it is closed to efficient causation."**

This appears in Section 10A and is the book's key result.

## Aristotle's Four Causes (Rosen's Framework)

Rosen returns to Aristotle to build his causal framework:

1. **Material cause** — what something is made of (the substrate)
2. **Formal cause** — the pattern, form, or blueprint
3. **Efficient cause** — the agent or process that brings something about (the "maker")
4. **Final cause** — the purpose or function (the "why")

Modern science reduced all causation to material and efficient cause, dismissing formal and final cause. Rosen argues this was a mistake for biology.

## Closure to Efficient Causation — What It Means

In a machine:
- Every component has an efficient cause
- That efficient cause is either external to the machine or is another component
- But you can always trace the chain of efficient causes to something *outside* the machine
- There is NO closed path of efficient causation

In an organism:
- Every component has an efficient cause
- But those efficient causes are themselves components of the organism
- The chain of efficient causes *closes upon itself*
- The organism produces all the efficient causes it needs internally

### Formal Statement via (M,R)-Systems

- f: A -> B (metabolism: f is the efficient cause of B)
- Phi: B -> Hom(A,B) such that Phi(b) = f (repair: b is the efficient cause of f)
- beta: Hom(A,B) -> Hom(B, Hom(A,B)) such that beta(f) = Phi (replication: f is the efficient cause of Phi)

The closure: every mapping in the system is entailed by some other mapping in the system.

## Simple vs. Complex Systems

Rosen's definitions are precise and unconventional:

- **Simple system:** A system for which ALL models are simulable (computable). Equivalently: a mechanism.
- **Complex system:** A system that has at least ONE non-simulable model. Not a mechanism.

This is not "complex" in the colloquial sense (complicated, many parts). A system with billions of parts can be simple (a computer). A system with few parts can be complex (a minimal organism).

## The Non-Computability Argument

The argument chain:
1. Living organisms are closed to efficient causation
2. This closure creates impredicative loops (self-referential structures)
3. Impredicative structures cannot be fully captured by any algorithm
4. Therefore, no Turing machine can simulate all aspects of a living organism
5. Therefore, the Church-Turing thesis (that all effectively computable functions are Turing-computable) cannot apply to biology

### The Impredicativity

An impredicative definition is one where the thing being defined participates in its own definition. In (M,R)-systems, f is defined in terms of Phi, Phi is defined in terms of beta, and beta is defined in terms of f. The mappings are members of sets that contain themselves.

Rosen claims: "there is no algorithm for building something that is impredicative."

### Status of This Argument

This is the most contested part of Rosen's work:
- **Chu & Ho** argued the central proof is wrong
- **Louie** defended and restated the logic
- **Cardenas et al.** showed closure to efficient causation can be expressed in lambda-calculus, suggesting computability may be possible
- **Mossio, Longo & Stewart** proposed computable expressions of the closure
- The debate is ongoing and unresolved

## Mechanism vs. Organism (The Table)

| Property | Mechanism (Simple) | Organism (Complex) |
|----------|-------------------|-------------------|
| Models | All simulable | Some non-simulable |
| Efficient causation | Open chain | Closed loop |
| Fractionability | Can be decomposed into parts | Loses essential properties when decomposed |
| State space | Fully describable | Cannot be fully captured in any single description |
| Prediction | Fully predictable in principle | Inherently unpredictable aspects |

## Relevance to Agent Architectures

### The Hard Question

If Rosen is right that true organisms are non-computable, what does this mean for AI agents running on Turing machines?

Possible interpretations:
1. **Strong Rosen:** AI agents on digital computers can never be truly alive/autonomous in the Rosennean sense. They will always be mechanisms, not organisms.
2. **Weak Rosen:** Current AI agents are mechanisms, but the gap between mechanism and organism points to what they *lack* — namely, closure to efficient causation. We can use this to identify what needs to be added.
3. **Pragmatic Rosen:** Even if full closure is non-computable, *approximate* closure to efficient causation is useful and achievable. An agent that mostly maintains its own catalysts is more autonomous than one that does not.

### What "Closure to Efficient Causation" Means for Agents

An agent is "closed to efficient causation" if it produces all the processes it needs to maintain itself:
- Its inference engine (metabolism) produces outputs
- Those outputs are used to maintain the inference engine (repair)
- The maintenance process itself is maintained by the system (replication)

Current AI agents fail this test because:
- Their model weights require external training (not self-produced)
- Their code requires external developers
- Their infrastructure requires external maintenance
- Their reward signals often come from external sources

The question is whether these failures are *fundamental* or *engineering challenges*.
