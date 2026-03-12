# Powers, Clark & McFarland (1960) — A General Feedback Theory of Human Behavior

## Citation
Powers, W.T., Clark, R.K., & McFarland, R.L. (1960). A general feedback theory of human behavior. *Perceptual and Motor Skills*, 11.
- Part I: Monograph Supplement 7(1), pp. 71-88.
- Part II: Monograph Supplement 7(3), pp. 309-323.

## Affiliation
Veterans Administration Research Hospital, Chicago; Northwestern University Medical School.

## Access
- PDFs available via IAPCT: https://www.iapct.org/publications/other/a-general-feedback-theory-of-human-behavior-part-i-and-part-ii/
- SAGE Journals (subscription): https://journals.sagepub.com/doi/10.2466/pms.1960.11.1.71

## Historical Context
- Work began in 1953 when Powers, Clark, and McFarland started collaborating.
- An earlier 1957 manuscript version exists in the William T. Powers Papers at Northwestern University Archives (Box 8, Folder 14).
- Powers described this as "the beginnings of my contributions to applying control theory to behavior."
- This is the foundational PCT paper. Everything else builds from here.

## Core Arguments

### Part I: The Basic Control Loop
The paper applies control engineering principles to human behavior. The central claim: organisms are negative feedback control systems that control their sensory inputs, not their behavioral outputs.

Key structural elements introduced:
1. **The negative feedback loop** as the fundamental unit of behavioral organization.
2. **The comparator** — computes discrepancy between reference signal (desired state) and perceptual signal (current sensed state).
3. **The error signal** — drives output to reduce the discrepancy.
4. **The output function** — converts error into behavioral action.
5. **The feedback path** — the physics of the environment through which output affects input.

### Part II: The Hierarchy
Part II introduced the hierarchical organization of control systems. The original 1960 formulation proposed fewer than the eventual 11 levels (the hierarchy was refined through 1973 and later). The key principle:
- Each level constructs its perceptions by combining signals from the level below.
- Each level controls by setting reference signals for the level below.
- Only the lowest level acts directly on the environment.
- Higher levels act indirectly, by specifying *what to perceive*, not *what to do*.

### Intellectual Debts
- Credits to Norbert Wiener (cybernetics) and W. Ross Ashby (homeostasis, ultrastability).
- Builds on Rosenblueth, Wiener & Bigelow (1943) "Behavior, Purpose and Teleology" — the paper that brought teleology back into science via feedback.

## Significance for Agent Architectures

### The 1960 paper establishes three principles that map directly to agent design:

1. **Control of inputs, not outputs.** An agent should define success in terms of perceived states matching desired states, not in terms of specific action sequences. This is the difference between "navigate to the kitchen" (specifying a desired perception) and "turn left, walk 10 steps, turn right" (specifying outputs).

2. **Hierarchical goal decomposition is automatic.** Higher levels don't need to know how lower levels work. They just set reference signals. This is a clean separation of concerns — analogous to how a manager sets objectives without specifying implementation details.

3. **Disturbance rejection is inherent.** The closed-loop structure means the system automatically compensates for unexpected perturbations without explicit exception handling or replanning. This is the most underappreciated advantage over plan-execute architectures.

## Relation to Later Work
- The 1960 paper is the seed. The 1973 book *Behavior: The Control of Perception* is the full elaboration.
- The hierarchy was later expanded to 11 levels (intensity through system concept).
- The reorganization mechanism (PCT's theory of learning) was not yet fully developed here; that came later, drawing on Ashby's ultrastability.
