# Powers (1973/2005) — Behavior: The Control of Perception

## Citation
- Powers, W.T. (1973). *Behavior: The Control of Perception*. Chicago: Aldine de Gruyter.
- Powers, W.T. (2005). *Behavior: The Control of Perception*, 2nd edition. New Canaan: Benchmark Publications.

## Access
- Book: Available from Benchmark Publications and Amazon.
- IAPCT page: https://www.iapct.org/publications/books/behavior-the-control-of-perception/

## Overview
The magnum opus. 296 pages. The culmination of 20 years of study (1953-1973). This book is where PCT is fully articulated for the first time as a comprehensive theory of behavior.

## Structure of the Book
The book covers:
1. Simple control systems
2. Multi-leveled hierarchical control systems
3. Learning and reorganization
4. Memory
5. Biological bases of control processes
6. Social aspects: conflict and interpersonal control

## The Hierarchy of Perceptual Control (as refined)

### Original 1973 Version: 9 Levels
The original hierarchy proposed in the book:
1. Intensity
2. Sensation
3. Configuration
4. Transition
5. Event
6. Relationship
7. Sequence (later revised position)
8. Program
9. System Concept

### Later Revision: 11 Levels
Powers later added Category and Principle levels and reordered slightly:

| Level | Name | What Is Controlled | Timescale |
|-------|------|-------------------|-----------|
| 1 | Intensity | Magnitudes of sensory signals | Milliseconds |
| 2 | Sensation | Combinations of intensities (color, warmth, texture) | Milliseconds |
| 3 | Configuration | Spatial patterns, shapes, objects | ~100ms |
| 4 | Transition | Rates of change (motion, acceleration) | ~100ms-1s |
| 5 | Event | Sequences of transitions with beginning/end | Seconds |
| 6 | Relationship | Contingencies, spatial/causal connections | Seconds-minutes |
| 7 | Category | Classifications, type assignments | Minutes |
| 8 | Sequence | Ordered series of perceptions | Minutes |
| 9 | Program | Contingent sequences with decision points (if-then) | Minutes-hours |
| 10 | Principle | Abstract rules, values, heuristics | Hours-lifetime |
| 11 | System Concept | Self-models, worldviews, ideologies | Lifetime |

**Critical caveat** (from Powers himself): These specific levels are hypotheses, not established fact. The principle of hierarchical organization is what matters. The particular number and naming of levels requires empirical validation.

### Processing Time
With each step up the hierarchy, the processing time for perceptual input slows down. Intensity-level control operates in milliseconds; system-concept-level control operates over lifetimes.

## Mathematical Formulation

### The Basic Loop
```
p = I(q_i)           # perception = input function of environmental quantity
e = r - p             # error = reference minus perception
o = G * integral(e dt) # output = gain times integral of error
q_i = f(o, d)         # environmental state = function of output and disturbance
```

Where:
- `p` = perceptual signal
- `r` = reference signal (set by higher-level system or intrinsic)
- `e` = error signal
- `o` = output signal
- `q_i` = environmental input quantity
- `d` = disturbance
- `G` = loop gain
- `I` = input (perceptual) function
- `f` = environmental feedback function

### Key Property: High-Gain Control
When loop gain G is high:
- `p ≈ r` (perception tracks reference closely)
- Output varies freely to compensate for disturbances
- The controlled variable (p) is stable; the means (o) is variable

### Neural Implementation
Powers (1973) proposed specific neural mechanisms:
- **Comparator (subtraction):** Convergence of excitatory and inhibitory neural connections at the pre-synaptic membrane.
- **Addition, multiplication:** Other known neural structural arrangements.
- **Integration:** Neural integrators (as found in oculomotor system, etc.)

## Empirical Validation
The correlation between behavior of human subjects and PCT models in tracking experiments approached **r = 0.99**. This is extraordinarily high — essentially perfect prediction of individual behavior.

## The 2005 Second Edition
The second edition updated the hierarchy, refined the mathematical treatment, and incorporated 30+ years of subsequent research. It includes a more detailed discussion of reorganization.

## Mapping to Agent Architectures

### PCT Hierarchy → Agent Goal Stack
| PCT Level | Agent Architecture Analogue |
|-----------|----------------------------|
| Intensity/Sensation | Raw sensor processing, embedding layers |
| Configuration | Object detection, state representation |
| Transition | Change detection, temporal difference |
| Event | Action recognition, episode boundaries |
| Relationship | Relational reasoning, causal models |
| Category | Classification, concept formation |
| Sequence | Sequential planning, chain-of-thought |
| Program | Conditional execution, if-then planning |
| Principle | Policy constraints, ethical guidelines |
| System Concept | Agent identity, meta-cognition |

### Key Insight for Agent Design
The PCT hierarchy is NOT a planning hierarchy (top-down decomposition of goals into subgoals into actions). It is a **perceptual** hierarchy — each level perceives a different kind of pattern in the world, and controls that perception. The planning falls out as a side effect.

This is fundamentally different from hierarchical RL, where the hierarchy is over *policies* (actions), not *perceptions* (states). PCT would predict that hierarchical RL architectures that organize around what the agent *perceives* (what state features it tracks) rather than what it *does* (which sub-policy to invoke) will be more robust.
