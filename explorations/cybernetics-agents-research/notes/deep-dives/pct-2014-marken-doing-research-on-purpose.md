# Marken (2014) — Doing Research on Purpose

## Citation
Marken, R.S. (2014). *Doing Research on Purpose: A Control Theory Approach to Experimental Psychology*. St. Louis: New View Publications.

## Access
- Amazon: https://www.amazon.com/Doing-Research-Purpose-Experimental-Psychology/dp/0944337554
- New Books Network podcast interview: https://newbooksnetwork.com/richard-s-marken-doing-research-on-purpose

## Overview
A collection of six peer-reviewed papers by Marken, published over the preceding decade, explaining why PCT offers the most promising approach to understanding behavior. The book traces the accruing empirical validation of PCT and the evolution of a new experimental methodology.

## Key Themes

### 1. Behavior as Control
Research on purpose is based on the fact that the behavior of organisms is a control process. "Behavior" consists of controlled results — consistent outcomes produced in the face of disturbances that should prevent such consistency.

### 2. The Controlled Variable as the Unit of Study
The main goal of research on purpose is the discovery of the variables that organisms control — the controlled variables. This is what behavior IS: the process of keeping perceptual variables at reference values.

### 3. The Test for the Controlled Variable (TCV)
The TCV is the "bedrock" of PCT investigation. The book presents detailed applications of the TCV to:

**Fly-ball catching in baseball:**
- The "obvious" hypothesis: players control the perceived position of the ball.
- The PCT analysis (Marken 2005): players actually control the **optical trajectory** — specifically, the rate of change of the vertical optical angle to the ball. If this rate is kept constant (a controlled variable), the player will arrive at the right place at the right time.
- This was tested by comparing PCT simulation behavior to human behavior. The match was extremely close.

**Frisbee catching by dogs:**
- Same principle: the dog controls an optical variable, not the explicit trajectory.

### 4. The Reference Value Problem
A distinctive methodological challenge: the reference values for controlled perceptual variables exist only inside the minds of individual organisms. They cannot be directly observed. The experimenter must infer them from the pattern of disturbance rejection.

This is why standard experimental methods (manipulate IVs, measure DVs) are insufficient. You need the TCV, which looks for **invariance** in the face of disturbance, not **variance** in response to stimulation.

## Relation to the Cambridge Book
Marken later published a related work through Cambridge University Press:
- Marken, R.S. (2021). *The Study of Living Control Systems: A Guide to Doing Research on Purpose*. Cambridge University Press. https://www.cambridge.org/core/books/study-of-living-control-systems/

This is a more comprehensive and accessible version of the same ideas, updated for a new generation of researchers.

## Relevance to Agent Architectures

### The Optical Trajectory Finding
The fly-ball catching result is a perfect example of why the PCT approach matters for agent design. Two alternative agent architectures:

**Naive approach (plan-execute):**
1. Observe ball position
2. Predict trajectory using physics model
3. Compute interception point
4. Plan path to interception point
5. Execute path

**PCT approach (control perception):**
1. Perceive optical trajectory (rate of change of vertical angle)
2. Compare to reference (constant rate)
3. Output: run in the direction that reduces error
4. No physics model, no trajectory prediction, no path planning

The PCT approach is simpler, more robust, and matches what humans and dogs actually do. It degrades gracefully when conditions change (wind, uneven ground) because it continuously controls a perception rather than executing a plan.

### Implications for LLM Agent Design
Current LLM agents are plan-execute systems: they generate a plan (chain of thought, tool calls) and execute it. A PCT-inspired agent would instead:
1. Continuously monitor a perceptual variable (e.g., "how well does this response answer the query?")
2. Adjust its output to reduce error between perception and reference
3. Never commit to a fixed plan; instead, continuously adjust based on feedback
