# Kaplan & Friston (2018) - Planning and navigation as active inference

**Journal:** Biological Cybernetics, 112(4), 323-343
**Authors:** Raphael Kaplan, Karl J. Friston
**DOI:** 10.1007/s00422-018-0753-2
**Year:** 2018
**License:** CC BY 4.0 (open access)
**Access:** Should be freely available via Springer. Fetch failed due to redirect.

## Summary

Formulates planning and navigation as active inference using Markov decision processes.
Demonstrates how the exploitation-exploration dilemma is dissolved by acting to minimize
uncertainty (expected surprise / free energy).

## Key Arguments

- **Exploration-exploitation dissolved:** Under active inference, there is no dilemma.
  Epistemic behavior (reducing uncertainty) and pragmatic behavior (achieving goals)
  are both driven by the same objective -- minimizing expected free energy.
- **Epistemic foraging:** Agents are driven by novelty and the imperative to reduce
  uncertainty about the world. This contextualizes goal-directed behavior.
- **Subgoals from context-sensitive priors:** Agents solve complicated planning problems
  using context-sensitive prior preferences to form subgoals.
- **Planning as inference:** Planning is not a separate process but emerges from the
  same inference machinery used for perception and action.

## Methods

- Maze navigation as test problem
- Markov decision process (MDP) framework
- Simulated behavioral and electrophysiological responses
- Active inference scheme for navigation under uncertainty about maze structure

## Key Results

- Agent must explore the maze visually, then use information to navigate to target
- The model produces synthetic reaction times, saccadic eye movements, and
  neurophysiological responses that can be compared to empirical data
- Context-sensitive priors enable flexible subgoal formation

## Relevance to Our Research

Directly relevant to how cybernetic agents can plan. The dissolution of the
exploration-exploitation trade-off is a key insight -- in a properly formulated
active inference agent, curiosity and goal-pursuit are unified under one principle.
This has implications for agent architecture design:

- No separate exploration strategy needed
- Planning emerges from inference, not from a separate planning module
- Epistemic value (information gain) is naturally balanced against pragmatic value

## Tags
`active-inference` `planning` `navigation` `exploration-exploitation` `markov-decision-process`
