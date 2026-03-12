# Bateson — "The Role of Somatic Change in Evolution" (1963)

## Publication
- *Evolution*, Vol. 17, No. 4, pp. 529-539, December 1963
- Reprinted in *Steps to an Ecology of Mind* (1972)

## Core Framework

Bateson examines evolution through three interconnected factors:
1. **Genotypic change** — fundamental structural change (mutation)
2. **Somatic change** — adaptive response to environment (phenotypic flexibility)
3. **Environmental change** — shifts in conditions

Evolution is the interplay among these three under natural selection.

## The Economics of Flexibility

### Flexibility Has Finite Limits
Adaptation is more surface-level and reversible than structural (genotypic) change. But
flexibility is not free. We can only do so much adapting before its possibilities and
resources are exhausted.

### The Flexibility Paradox
"The more flexibility there is, the less real (new) difference the system can support."

Bateson argues that excessive flexibility *at one level* consumes the resources needed
for flexibility *at other levels*. A system that spends all its adaptive capacity
responding to short-term perturbations has none left for fundamental restructuring.

This is a deep insight: **adaptation and innovation compete for the same resources.**

### Implications for Rate of Change
Bateson stresses that "fast change" is not a good thing. Control or identity and
continuity lag behind what is controlled. In fast change, control will fail and
pressures on the organism escalate.

## Three Control Strategies: Regulators, Adjustors, Extraregulators

### Adjustors
- Let environmental variables enter the organism, which must then cope internally
- The organism's internal state tracks environmental fluctuation
- High metabolic cost; flexibility consumed on tracking the environment

### Regulators
- Negotiate relationships with environment at their boundaries
- Keep internal conditions stable regardless of external fluctuation
- Classic homeostasis: the thermostat model

### Extraregulators
- Project control mechanisms *into* the environment
- Modify the environment to suit the organism rather than adapting to it
- Organizations and cultures serve as means of controlling the self/environment
  relationship
- The evolutionary trend appears to favor extraregulation

## The Waddington Connection

Bateson's paper engages with C.H. Waddington's concept of **genetic assimilation** —
the process by which an environmentally-induced phenotypic change can become genetically
fixed over evolutionary time. This is not Lamarckism (inheritance of acquired
characteristics) but a more subtle process:

1. Environmental stress induces a somatic (phenotypic) adaptation
2. This adaptation has selective value
3. Natural selection favors genotypes that produce the same adaptation more cheaply
   (with less flexibility expenditure)
4. Over time, the adaptation becomes "assimilated" into the genotype

Bateson frames this cybernetically: the somatic change is the *flexible* response; the
genotypic assimilation is the system's way of *economizing flexibility* by hardwiring
what was previously soft-coded.

## Application to Agent Architectures

### The Economics of Flexibility in Agent Design
This paper offers a formal framework for understanding the tradeoffs agents face:

**In-context learning (prompting) = somatic adaptation:**
- Flexible, reversible, context-dependent
- Consumes context window (finite resource)
- Every token spent on adaptation is a token not available for reasoning

**Fine-tuning = genotypic change:**
- Less flexible, more permanent
- Frees up context window for other purposes
- But reduces adaptability to novel situations

**The Bateson prediction:** an agent that relies entirely on in-context learning will
exhaust its flexibility budget (context window) and fail on complex tasks. An agent that
is entirely fine-tuned will be rigid. The optimal design uses **both levels** — fine-tuning
for stable patterns, in-context learning for novel situations.

### Regulators vs. Adjustors vs. Extraregulators in Agent Design

**Adjustor agents:**
- Directly track environmental state (user requests, tool outputs)
- Internal state fluctuates with every new input
- High computational cost; brittle under noise
- Example: naive ReAct loops that fully reprocess every observation

**Regulator agents:**
- Maintain stable internal models; respond only to deviations
- Don't track every environmental fluctuation, only violations of expectations
- More efficient, more robust
- Example: agents with persistent world models that update incrementally

**Extraregulator agents:**
- Modify their environment to suit their processing
- Structure tool outputs, request specific formats, create scaffolding
- Example: agents that set up databases, create structured outputs for future queries,
  or modify their own prompts
- This is the most sophisticated and, per Bateson, the evolutionary trend

### The Genetic Assimilation Parallel
In agent development:
1. A prompting technique works well (somatic adaptation)
2. It's discovered to be broadly useful (selective value)
3. It gets incorporated into training data or model architecture (genetic assimilation)
4. This frees up prompt space for new adaptations

Chain-of-thought is a perfect example: originally a prompting technique (somatic), now
being trained into models directly (genotypic assimilation), freeing prompt space for
task-specific adaptation.

## Key Quotation

"The economics of flexibility are to the theory of evolution as the theory of money
is to economics. In a society bent on rapid change, the individuals of the group have
problems not unlike the problems of organisms rapidly evolving."

## Sources
- Bateson, G. (1963). "The Role of Somatic Change in Evolution." *Evolution*, 17(4),
  529-539.
  [Wiley](https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1558-5646.1963.tb03310.x)
  [Oxford Academic](https://academic.oup.com/evolut/article-abstract/17/4/529/6868053)
- [Introduction to the paper — Emergent Publications](https://eco.emergentpublications.com/Article/260df2e9-a84e-4c13-89b2-5b8e4e98eaa8/academic)
