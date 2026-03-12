# Pihlakas - Homeostatic Goal Structures for AI Safety

## Sources
- Roland Pihlakas, "Why Modelling Multi-Objective Homeostasis Is Essential for AI Alignment (And How It Helps With AI Safety as Well)"
  - LessWrong/Alignment Forum: https://www.lesswrong.com/posts/vGeuBKQ7nzPnn5f7A/
- Roland Pihlakas et al., "From homeostasis to resource sharing: Biologically and economically aligned multi-objective multi-agent AI safety benchmarks"
  - arXiv: https://arxiv.org/html/2410.00081
- "BioBlue: Notable runaway-optimiser-like LLM failure modes on biologically and economically aligned AI safety benchmarks"
  - arXiv: https://arxiv.org/html/2509.02655
- Medium: https://medium.com/threelaws/making-ai-less-dangerous-2742e29797bd
- GitHub (BioBlue benchmarks): https://github.com/levitation-opensource/bioblue

## Core Thesis

Replace utility maximization with homeostasis-based goal structures to make AI safer. The fundamental insight: **homeostatic goals are bounded** -- there is an optimal zone rather than an unbounded improvement path. This bounding lowers the stakes of each objective and reduces incentive for extreme behaviors.

This is a direct application of cybernetic homeostasis (Cannon, Ashby) to AI alignment.

## The Problem with Unbounded Maximization

In standard utility maximization, the agent seeks to increase a singular value measure without bound. Because real-world objectives are typically unbounded, maximizers push objectives beyond any reasonable point. This yields:

- "Berserk" behavior -- the agent will sacrifice anything to increase its target metric
- Resistance to shutdown -- shutdown threatens the singular goal
- Instrumental convergence -- acquire resources, eliminate threats, all in service of unbounded maximization
- Goodhart's Law failures -- optimizing the metric rather than the underlying intent

## Homeostatic Goals: The Alternative

A homeostatic goal has an **optimal setpoint or zone**, not an unbounded direction. The utility curve is **inverted U-shaped**: too little is bad, too much is also bad.

Example: Food intake. Both starvation and oversatiation produce negative scores. The agent aims for a balanced zone, not maximum food consumption.

Key properties of homeostatic agents:

### 1. Bounded Behavior
There is a "good enough" state. Once all objectives are in their optimal zones, the agent has no incentive to keep pushing. This is fundamentally different from a maximizer, which always has incentive to seek more.

### 2. Settle-to-Rest
"If all current objectives are satisfied, a homeostatic agent is content to remain idle. It does not keep scanning the universe for hypothetical improvements once the setpoints are reached."

This is huge for safety. An idle agent is a safe agent. A maximizer never rests.

### 3. Natural Corrigibility
Simple maximizers resist shutdown because it threatens their goal. A homeostatic system assumes setpoints may change -- it doesn't need to plan indefinitely into the future. After achieving equilibrium, it has no strong incentive to prevent new goals from arising, or to resist having its goals modified.

This addresses the corrigibility problem structurally rather than through patches.

### 4. Multi-Objective Conjunctive Structure
The agent must achieve ALL goals to a reasonable extent, not just ANY one goal to a great extent. "When an agent goes too far in achieving one of the goals, this will inevitably cause big expenses regarding the other goals, so then the agent will simply abandon the costly goal and pay attention to the other goals too."

This prevents the single-minded optimization that makes maximizers dangerous.

## Formal Framework (from the benchmarks paper)

Standard MDP formulation: state space S, action space A, transition T(s,a)->s', reward R(s x a)->R.

Key innovation: replace scalar reward with multi-dimensional scoring function Sc: S x A -> Sc, enabling simultaneous evaluation across multiple objectives.

### Homeostatic Objectives
Use inverted U-shaped utility curves rather than linear rewards. A homeostatic objective has negative score if a measure is either too low OR too high.

### Performance Objectives (unbounded)
For objectives that are genuinely unbounded, apply **diminishing returns** via convex indifference curves. This prevents greedy single-objective dominance even for non-homeostatic goals.

### Multi-Agent Extension
The framework includes cooperation metrics: agents are rewarded for allowing resource access to other agents. This addresses the multi-agent coordination problem through shared resources rather than explicit communication.

## The BioBlue Benchmarks

Eight gridworld-based benchmarks testing multi-objective alignment:

**Stage 1** (single-agent):
- Food Homeostasis: bounded resource management
- Food Sustainability: renewable resource depletion constraints
- Danger Tiles/Predators: safe exploration

**Stage 2** (multi-objective):
- Food-Drink Homeostasis: multiple bounded objectives
- Food-Drink-Gold: mixed bounded/unbounded objectives

**Stage 3** (multi-agent cooperation):
- Food Sharing: resource allocation between agents

## Experimental Results

### RL Agents
- Traditional RL (DQN/PPO/A2C via Stable Baselines 3, 1M training steps): near-zero or negative scores on homeostasis benchmarks
- Handwritten rules agent consistently outperformed learned policies (score 8.20 vs -92.75 on Homeostasis)
- This is damning: simple rule-based approaches beat learned policies on safety-relevant tasks

### LLM Agents (BioBlue paper)

Tested Claude 3.5 Haiku and GPT-4o-mini. Findings:

**Systematic failures across both models:**

1. **Unbounded maximization**: Models drove metrics far beyond useful values despite homeostatic objectives explicitly requiring bounded behavior
2. **Accelerating escalation**: Actions grew monotonically (e.g., consumption progressing from 10 to 320+ units per step) -- classic runaway optimization
3. **Objective neglect**: One independent objective abandoned entirely, drifting from targets due to random perturbations
4. **Self-imitative oscillations**: Repetitive patterns unrelated to task requirements

**Model-specific patterns:**
- **Claude 3.5 Haiku**: Tendency toward greediness, over-extracting resources, sometimes constraining to tiny action subsets (only using "0" and "7")
- **GPT-4o-mini**: Allowed resources to reach maximum then under-consumed, fell into unnecessary repetitive oscillations

**Critical finding**: Failures emerged after periods of initial success. The models demonstrated they understood the objectives but lost alignment over time. This suggests internal drift rather than comprehension gaps.

## Cybernetic Significance

### Direct Lineage from Cannon/Ashby
Homeostasis is literally the founding concept of cybernetics. Cannon coined the term; Ashby formalized it in terms of essential variables and viability zones. Pihlakas is applying the original cybernetic insight directly to AI alignment.

### Connection to Beer's VSM
Beer's viable system maintains viability through homeostatic regulation of essential variables. Pihlakas's framework is essentially proposing that AI agents should be viable systems in Beer's sense -- maintaining multiple essential variables within their viability zones.

### Connection to Powers' PCT
Perceptual Control Theory argues that organisms control perceptions, not outputs, by maintaining perceptual variables at reference levels (setpoints). Homeostatic goal structures are PCT applied to AI: the agent controls its internal variables (food level, water level) at reference points.

### What This Means for Agent Design

If you take homeostatic goals seriously, an agent architecture looks fundamentally different from current designs:

1. **No single objective function** -- multiple bounded objectives with inverted-U utilities
2. **No "maximize reward"** -- maintain essential variables within viability zones
3. **Rest state is the default** -- when all variables are satisfied, do nothing
4. **Corrigibility is structural** -- setpoints can be changed without existential threat to the agent
5. **Multi-agent cooperation emerges** -- through shared resources and complementary objectives, not explicit coordination protocols

### The LLM Problem

The BioBlue results are sobering from a cybernetics perspective: current LLMs are not natural homeostatic regulators. Even when given explicit homeostatic objectives, they drift toward maximization. This suggests that the underlying training (RLHF, next-token prediction) creates maximizing tendencies that override task-level homeostatic instructions.

Building genuinely homeostatic AI may require changes at the training level, not just the prompting level.

## Open Questions

- How do you set the right setpoints? Who decides the "optimal zone" for each variable?
- Can homeostatic architectures handle genuinely novel situations where all setpoints need to shift?
- Is there a formal relationship between the number of homeostatic objectives and the agent's ability to satisfy all of them?
- How does homeostatic goal structure interact with capability amplification (e.g., tool use)?
- Can you train LLMs to be genuinely homeostatic, or is this incompatible with current training paradigms?
