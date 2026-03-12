# Parr, Pezzulo & Friston (2022) — Active Inference (Textbook)

**Book:** Parr, T., Pezzulo, G., & Friston, K.J. (2022). *Active Inference:
The Free Energy Principle in Mind, Brain, and Behavior.* MIT Press.
**URL:** https://mitpress.mit.edu/9780262045353/active-inference/
**Open Access PDF:** https://direct.mit.edu/books/oa-monograph-pdf/2246566/book_9780262369978.pdf

---

## Summary

This is the definitive textbook on active inference, providing the first
comprehensive treatment of the theory, its mathematical foundations, applications
to cognition, and implementation recipes. It is open-access (CC BY-NC-ND).

## Chapter Structure

1. **Overview** — Motivation and scope
2. **The Low Road to Active Inference** — Intuitive, conceptual introduction
3. **The High Road to Active Inference** — Formal mathematical treatment
4. **The Generative Models of Active Inference** — Model structures
5. **Message Passing and Neurobiology** — Neural implementation
6. **A Recipe for Designing Active Inference Models** — Practical guide
7. **Active Inference in Discrete Time** — POMDP formulation
8. **Active Inference in Continuous Time** — Differential equations
9. **Model-based Data Analysis** — Fitting to empirical data
10. **Active Inference as a Unified Theory of Sentient Behavior** — Synthesis

Plus: Appendix A (Mathematical Background), Appendix B (Equations of Active
Inference).

## Key Ideas

### The "Low Road" (Chapter 2)

Active inference begins with a simple insight: biological systems must resist
the tendency toward disorder. To do so, they must occupy a limited set of states
(their "phenotypic states"). This requires minimizing surprise — being where
you expect to be.

Two routes to minimize surprise:
1. Change your beliefs to match the world (perception)
2. Change the world to match your beliefs (action)

### The "High Road" (Chapter 3)

The formal derivation from first principles:

1. Start with the nonequilibrium steady-state assumption
2. Identify Markov blanket structure
3. Show that internal states must parameterize a probability distribution over
   external states
4. Derive that internal and active states must minimize variational free energy
5. Show this is equivalent to approximate Bayesian inference

### Generative Models (Chapter 4)

The generative model is the core data structure. It specifies:
- What the agent thinks generates its observations (likelihood model)
- How states evolve over time (transition model)
- What the agent prefers to observe (prior preferences)
- Initial beliefs (prior over initial states)

Different model structures support different cognitive functions:
- Simple models → reactive behavior
- Hierarchical models → abstraction, context sensitivity
- Temporal models → planning, prediction
- Deep models → multi-scale inference

### Message Passing and Neurobiology (Chapter 5)

Active inference provides a process theory for how inference is implemented
in neural circuits:

- **Predictive coding:** Forward connections carry prediction errors, backward
  connections carry predictions
- **Precision weighting:** Attention modulates the gain on prediction error
  signals (mapped to neuromodulation)
- **Basal ganglia:** Evaluate expected free energy of policies (value signals)
- **Prefrontal cortex:** Maintains beliefs about policies
- **Dopamine:** Encodes precision of policy-related predictions

### The Recipe (Chapter 6)

Step-by-step guide to designing active inference models:

1. Define the problem (what observations, what actions, what goals)
2. Specify the generative model (A, B, C, D matrices or their continuous
   equivalents)
3. Choose inference algorithm (variational message passing, belief propagation)
4. Implement the perception-action loop
5. Optionally add learning (parameter updates)

### Discrete Time (Chapter 7)

Full POMDP formulation:
- Observations, states, actions in discrete spaces
- Expected free energy for policy evaluation
- Softmax policy selection
- Belief updating via message passing

This is the framework implemented by pymdp.

### Continuous Time (Chapter 8)

Differential equation formulation:
- States and observations in continuous spaces
- Gradient descent on free energy (generalized filtering)
- Generalised coordinates of motion
- Active inference for motor control

This connects to classical control theory: continuous active inference is
formally related to PID control with a Bayesian twist.

## Cybernetic Connections in the Book

### Chapter 2: Homeostasis

The book begins with the cybernetic insight: biological systems must maintain
homeostasis. Active inference formalizes this as free energy minimization.
Prior preferences encode "what the agent expects to observe" — its homeostatic
setpoints.

### Chapter 5: Error Correction

The message passing framework implements error-driven control at every level
of the hierarchy. Prediction errors drive updates — this is Ashby's "error
correction" formalized as variational inference.

### Chapter 10: Unified Theory

The final chapter positions active inference as a modern realization of
cybernetic ambitions: a unified theory of sentient behavior that encompasses
perception, action, learning, and planning.

## Connection to PCT and Classical Control Theory

Continuous active inference has close formal links to classical control theory:
- Prior preferences = setpoints
- Prediction errors = error signals
- Action = control signals that minimize error
- The perception-action loop = negative feedback

The book acknowledges Powers' PCT as a predecessor. Active inference can be
seen as PCT with:
1. Bayesian uncertainty handling
2. Hierarchical model structure
3. Formal learning mechanisms
4. Epistemic action (exploration)

## Significance for Agent Design

This textbook provides everything needed to implement active inference agents:
- Mathematical foundations
- Model design methodology
- Implementation recipes
- Connections to neurobiology
- Discrete and continuous formulations

It is the primary reference for anyone building active inference systems.

## Status

Freely available as open-access PDF from MIT Press.
