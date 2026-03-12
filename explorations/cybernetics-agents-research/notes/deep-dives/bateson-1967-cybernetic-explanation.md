# Bateson — "Cybernetic Explanation" (1967)

## Publication
- *American Behavioral Scientist*, Vol. 10, No. 8, pp. 29-32, April 1967
- Reprinted in *Steps to an Ecology of Mind* (1972), Part V

## Core Argument: Negative vs. Positive Explanation

Bateson draws a fundamental distinction between two modes of scientific explanation:

**Causal (positive) explanation:** "Billiard ball B moved in direction X because ball A
hit it at angle Y." Effects explained by forces, impacts, energy transfer. This is
Newtonian physics.

**Cybernetic (negative) explanation:** "The course of events is said to be subject to
*restraints*, and it is assumed that, apart from such restraints, the pathways of change
would be governed only by *equality of probability*."

Cybernetic explanation asks: why didn't all the other things happen? What constrained the
system so that *this* outcome occurred, out of the full possibility space?

## Formal Structure of Negative Explanation

1. Identify the full set of possible outcomes (the possibility space)
2. Identify the restraints (constraints) that eliminate most possibilities
3. The event that occurred is explained as one of the few not eliminated by constraints

This inverts causal logic. Instead of "A caused B," we get "Everything except B (and a
few others) was prevented by constraints C1, C2, ... Cn."

## The Monkey at the Typewriter

Bateson's key illustration: if we find a monkey typing coherent prose, we do not look for
a positive force that *makes* the monkey type correctly. We look for **restraints** —
mechanisms that identify error and eliminate it. Somewhere in the system is a circuit that
selects against incorrect keystrokes. The prose is explained not by what produced it but
by what was *excluded*.

## The Thermostat Example

The thermostat does not "aim for" 70°F. It activates when temperature deviates beyond a
threshold. It moves *away from* an undesired state, not *toward* a desired one. Purpose
is an artifact of constraint, not a positive cause.

## The Stone vs. the Dog

- Kick a stone: it moves with the energy from the kick (Newtonian)
- Kick a dog: it responds with energy from its own metabolism (cybernetic)

In mental/living systems, the input is *information* (difference), and the response is
powered by *collateral energy* already available in the system. The "cause" is a
difference (a piece of news), not an energy transfer.

## Restraints as Inequalities of Probability

"The restraints upon which cybernetic explanation depends can in all cases be regarded as
factors which determine *inequality of probability*."

- Without restraints: all outcomes equally probable (maximum entropy, randomness)
- With restraints: certain outcomes far more probable than others
- The restraints *are* the explanation

## Application to Agent Architectures

This essay is foundational for understanding AI agent design:

### Agents as Constraint-Based Systems
Modern AI agents don't operate by "positive" force toward goals. They operate through
layers of constraints:
- The LLM's training constrains possible outputs (learned restraints)
- System prompts add further constraints (narrowing the possibility space)
- Tool availability constrains possible actions
- Guardrails and safety filters eliminate undesirable outputs
- ReAct-style loops provide error-detection circuits

### The Agent's "Prose" Is Explained by Its Constraints
Like Bateson's monkey, an agent's coherent output is explained not by a force that
produces correct tokens, but by the training process that selected against incorrect
ones. The entire transformer architecture operates via attention mechanisms that
*constrain* which information flows where — pure negative explanation.

### Error Correction vs. Goal-Seeking
Bateson's thermostat model maps directly onto agent feedback loops:
- ReAct: the agent observes an outcome, compares it to expectations, and corrects
  deviations — it doesn't "aim for" the goal positively, it moves away from error states
- Reflexion: explicit self-evaluation constrains future attempts by eliminating failed
  strategies
- The crucial insight: effective agent design is about designing the *right constraints*,
  not the right "drives"

### The Information-Energy Distinction
Agents, like dogs, respond with their own computational energy (GPU cycles, API calls)
to informational inputs (prompts, observations). The prompt doesn't "force" the output
through energy transfer — it provides differences that the system's own energy processes.
This is why prompt engineering works through nuance and framing (information), not
through "force."

## Key Quotation

"The course of events is said to be subject to restraints, and it is assumed that,
apart from such restraints, the pathways of change would be governed only by equality
of probability." — Bateson, "Cybernetic Explanation" (1967)

## Sources
- Bateson, G. (1967). "Cybernetic Explanation." *American Behavioral Scientist*, 10(8), 29-32.
- [PDF at convergentemergence.pbworks.com](http://convergentemergence.pbworks.com/f/Bateson+Cybernetic+Explanation.pdf)
- [SAGE Journals entry](https://journals.sagepub.com/doi/10.1177/0002764201000808)
- [Semantic Scholar](https://www.semanticscholar.org/paper/Cybernetic-Explanation-Bateson/1237a84d13a47003948ba7f6bd9efd2ca6d28037)
- [Harish's Notebook analysis](https://harishsnotebook.wordpress.com/2020/07/19/the-monkeys-prose-cybernetic-explanation/)
