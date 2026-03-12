# Nadin on Anticipation and Computing (2003-2010+)

**Key sources:**
- Nadin, M. (2003). *Anticipation: The End Is Where We Start From*. Lars Muller Publishers.
- Nadin, M. (2010). "Anticipatory Computing: from a High-Level Theory to Hybrid Computing Implementations." *IJARITAC* Vol. 1, No. 1.
- Nadin, M. (2010). "Anticipation and dynamics: Rosen's anticipation in the perspective of time." *International Journal of General Systems* 39:1, 3-33.
- Nadin, M. (2012). Prolegomena to the 2nd edition of Rosen's *Anticipatory Systems* (Springer).
- Nadin, M. (earlier). *MIND — Anticipation and Chaos*.
**Access:** The 2010 IJARITAC paper was at anteinstitute.org but returned 503. The IJGS paper is paywalled at Taylor & Francis.

## Who Is Nadin?

Mihai Nadin is Ashbel Smith Endowed University Professor and Director of the Institute for Research in Anticipatory Systems at UT Dallas. Co-founder of the field of anticipatory systems. Background spans electrical engineering, computer science, aesthetics, semiotics, computational design, and HCI.

He wrote the Prolegomena for the 2012 Springer edition of Rosen's *Anticipatory Systems*, providing an historical survey of the field's development since 1985.

## Nadin's Definition of Anticipation

"An anticipatory system is a system whose current state depends not only on previous states, but also on possible future states." (Nadin 2003)

Key aspects:
- Anticipation implies awareness of past, present, and future (i.e., of time)
- It implies observation capability, processing of what is observed, and ability to effect change
- Anticipation is expressed in *action* — it is not merely prediction

## Anticipatory vs. Predictive Computation

Nadin makes a crucial distinction:

### Predictive Computation
- Extrapolates from past data to estimate future states
- Fundamentally reactive: uses past to compute future
- Algorithmic, deterministic (or probabilistic)
- Standard machine learning, time series forecasting

### Anticipatory Computation
- Uses possible futures to determine present action
- Two concurrent processes:
  1. A reactive process at the object level (system controlled)
  2. A predictive-anticipatory process at the meta-level (pertaining to the model)
- The living is defined by its anticipation; once anticipation ceases, the living returns to the physical

### The Key Difference
Prediction: past -> model -> future estimate
Anticipation: possible future -> model -> present action that may change the future

Anticipation is *interventionist*. It does not just forecast; it acts to bring about or prevent the forecast.

## Anticipatory Computing

Nadin proposes that anticipatory computing requires hybrid architectures — not purely digital/algorithmic:

"Autonomic processing is the prerequisite for anticipatory expression. In the physical, processing is reactive; in the living it is autonomic."

This connects to Rosen's non-computability argument: if anticipation requires autonomic (self-organizing) processes, and these are not fully capturable by algorithms, then anticipatory computing may require non-standard computing substrates.

## Anticipation as a Prerequisite for Evolution

Nadin argues: "It turns out that anticipation is a premise for evolution in its broadest sense. In other words, the living is defined by its anticipation."

This is stronger than Rosen's claim. Rosen said all organisms are anticipatory. Nadin says anticipation is what *makes* something living in the first place.

## Relevance to Agent Architectures

### Two-Level Architecture

Nadin's two-concurrent-processes model maps well to agent design:

1. **Object level (reactive):** The agent's direct interaction with the environment. Stimulus-response. The "fast path."
2. **Meta level (anticipatory):** The agent's model of itself and its environment, running ahead of real time. The "slow path" that generates feedforward commands.

Both are needed. Pure reactive = no anticipation. Pure anticipatory = disconnected from reality.

### The Anticipatory Computing Challenge

Nadin's work raises the question: can standard digital computing implement genuine anticipation, or does it only implement prediction (which is different)?

If Nadin is right that anticipation requires autonomic processing, then current LLM-based agents are doing sophisticated *prediction* but not true *anticipation*. The difference is subtle but important:
- LLM predicts next token (prediction)
- LLM-agent plans actions based on predicted outcomes (closer to anticipation)
- But the agent does not autonomically generate its own models (not full anticipation)

### Design Principle
An anticipatory agent needs:
1. An explicit internal model of its environment
2. The ability to run this model faster than real time
3. The coupling of model predictions to present actions
4. The ability to update the model based on reality
5. (Strong version) The ability to generate and maintain its own models autonomically
