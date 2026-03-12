# Von Foerster (1976) — Objects: Tokens for (Eigen-)Behaviors

## Citation
Von Foerster, H. (1976). "Objects: Tokens for (Eigen-)Behaviors." Presented at the University of Geneva, June 29, 1976, for Jean Piaget's 80th birthday. French version in *Hommage a Jean Piaget: Epistemologie genetique et equilibration*, Delachaux et Niestle, Neuchatel (1977). Reprinted in *Observing Systems* (1981), pp. 274-285, and *Understanding Understanding* (Springer, 2003), pp. 261-271.

## Source Status
Full text available as PDF:
- Monoskop: https://monoskop.org/images/b/bf/Von_Foerster_Heinz_2003_Objects_Tokens_for_Eigen-Behaviors.pdf
- ResearchGate: https://www.researchgate.net/publication/319818470_Objects_Tokens_for_Eigen-Behaviors

Dedicated to Piaget: "A seed, alas, not yet a flower, for Jean Piaget to his 80th birthday from Heinz von Foerster with admiration and affection."

## Core Argument

### The Central Thesis

Objects are not pre-given features of an external reality that we passively discover. Objects are **tokens for eigenbehaviors** — they are the stable outcomes (fixed points) of recursive processes of interaction between an observer and its environment.

### The Mathematical Framework

Given an operator O (representing an observer, a process, a transformation), an **eigenform** is an entity X such that:

```
O(X) = X
```

This is the fixed-point equation. X is invariant under the operation O.

### The Recursive Construction

How to find such a fixed point — by recursive iteration:

```
x_0 = anything (arbitrary starting point)
x_1 = O(x_0)
x_2 = O(x_1) = O(O(x_0))
x_3 = O(x_2) = O(O(O(x_0)))
...
x_inf = O(O(O(...)))
```

If this process converges (in some appropriate sense), the limit x_inf satisfies O(x_inf) = x_inf. The limit is the eigenform.

Key insight: **the starting point x_0 does not matter.** If the operator O is sufficiently "contractive" (in the Banach fixed-point sense), all initial conditions converge to the same fixed point. The eigenform is determined by the operator, not by the initial state.

### The Nested Boxes Example

Begin with an empty box. Apply the operation "put a box around it":

```
[] -> [[]] -> [[[]]] -> [[[[]]]] -> ...
```

The limit is an infinitely nested structure: [[[...]]]

This infinite nesting is invariant under the operation of adding one more surrounding box. Hence it is a fixed point / eigenform.

This object does not "exist" in any naive physical sense. It requires what Kauffman later calls "imaginative completion" — the mind posits the limit of an infinite process. The eigenform is a cognitive construction.

### Connection to Piaget

Von Foerster's choice to present this at Piaget's birthday was deliberate. Piaget's developmental psychology describes how children construct stable "objects" through repeated sensorimotor interactions. The infant does not start with objects — it constructs them through recursive interaction. Von Foerster formalizes this: the child's cognitive operator O, applied recursively to environmental stimulation, converges on stable eigenforms that the child experiences as "objects."

Object permanence (Piaget's stage 4) is the stabilization of an eigenform — the child's recursive process has converged to a fixed point that persists even when the sensory input is removed.

### Mathematical Context: Fixed-Point Theorems

Von Foerster's construction connects to:

1. **Banach Fixed-Point Theorem**: In a complete metric space, a contraction mapping has a unique fixed point, obtainable by iteration.
2. **Brouwer Fixed-Point Theorem**: Every continuous function from a compact convex set to itself has a fixed point.
3. **Lawvere's Fixed-Point Theorem** (category theory): In any cartesian closed category, if there is a point-surjective map from A to A^A, then every endomorphism has a fixed point. This unifies Godel, Turing, Cantor, and eigenforms.

### Eigenforms as Attractors

Von Foerster's eigenforms correspond to attractors in dynamical systems:
- Single fixed points (eigenstates)
- Periodic orbits (oscillatory eigenbehaviors)
- Strange attractors (bounded but non-repeating eigenbehaviors)

Note: Von Foerster himself objected to the term "attractor" because it implies causation from the future or from an external structure — which contradicts the constructivist epistemology. The eigenform is not something that "attracts" the system; it is something that *emerges from* the recursive process.

## Relevance to Agent Architectures

### Training as Eigenform Discovery

Neural network training is precisely the recursive construction von Foerster describes:
- The operator O = one step of gradient descent
- x_0 = random initialization (arbitrary starting point)
- x_n = the model parameters after n training steps
- The "eigenform" = the converged model

The fact that x_0 doesn't matter (much) for well-behaved optimization landscapes is exactly the Banach contraction property. Different random seeds converge to similar solutions because the operator (training process) determines the eigenform, not the initial state.

### Concepts as Eigenbehaviors

What a trained model "knows" can be understood as eigenbehaviors — stable patterns of response that are invariant under the model's processing. A concept like "dog" in a vision model is an eigenform: when the model processes images of dogs, it converges on a stable internal representation that is invariant across different dog images.

### Agent-Environment Eigenforms

In an RL agent, the learned policy is an eigenform of the agent-environment interaction. The policy converges to a fixed point where the agent's behavior produces environmental responses that reinforce the behavior. This is circular causality producing stability — exactly von Foerster's framework.

### LLM Eigenbehaviors

Recent work (Lehrheuer, 2026) has applied von Foerster's eigenbehavior concept to transformer models. The argument: LLM responses are "dynamically stable response patterns that emerge from recursive optimization and forward-pass dynamics." Hallucinations are described as "eigen-collapse" — the failure of dynamically stabilized semantic eigenbehaviors under recursive self-generation.

## Key Formulations

- O(X) = X — the eigenform equation
- Objects are tokens for eigenbehaviors, not pre-given features of reality
- The starting point is irrelevant; the operator determines the eigenform
- The eigenform requires "imaginative completion" — it is a cognitive construction
- Connection to Piaget: object permanence = convergence of recursive sensorimotor process

## Related Work
- Kauffman, L.H. (2005). "Eigenforms — Objects as Tokens for Eigenbehaviors." *Kybernetes* 34(1-2), 129-150. CEPA fulltext: https://cepa.info/fulltexts/1817.pdf
- Kauffman, L.H. (2009). "Reflexivity and Eigenform: The Shape of Process." *Constructivist Foundations* 4(3), 121-137.
