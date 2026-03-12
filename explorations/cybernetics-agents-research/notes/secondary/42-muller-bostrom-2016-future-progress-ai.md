# Muller & Bostrom (2016) — Future Progress in Artificial Intelligence: A Survey of Expert Opinion

## Citation

Muller, V. C., & Bostrom, N. (2016). Future Progress in Artificial Intelligence: A Survey of Expert Opinion. In V. C. Muller (Ed.), *Fundamental Issues of Artificial Intelligence* (pp. 553–570). Cham: Springer. DOI: 10.1007/978-3-319-26485-1_33

Short version: Muller, V. C., & Bostrom, N. (2014). Future progress in artificial intelligence: A poll among experts. *AI Matters*, 1(1), 9–11.

Available: https://nickbostrom.com/papers/survey.pdf

## Purpose

To establish empirical data on what AI experts actually believe about the timeline and risks of advanced AI, cutting through the noise of science fiction hype vs. dismissive skepticism.

## Methodology

Brief questionnaire distributed to four groups in 2012/2013:
1. **TOP100**: The 100 most-cited living AI researchers
2. **AGI**: Participants at the 2012 AGI conference
3. **EETN**: Members of the Greek Association for AI
4. **PT-AI**: Participants at the 2013 Philosophy and Theory of AI conference

Total: 170 responses out of 549 invited (31% response rate).

## Key Findings

### 1. Timeline for High-Level Machine Intelligence (HLMI)

HLMI defined as: "one that can carry out most human professions at least as well as a typical human."

- **Median 50% probability**: 2040-2050 (varies by group)
- **Median 90% probability**: 2075
- Substantial uncertainty: individual estimates range from 10 years to "never"

### 2. Transition to Superintelligence

Respondents were asked: once HLMI is achieved, how long until superintelligence?
- Median: within 30 years of HLMI
- Some respondents: within 2 years of HLMI (fast takeoff)
- Others: never (skeptics)

### 3. Methods

Expert groups differed on which methods would lead to HLMI:
- TOP100 favored integrated approaches (combining multiple methods)
- AGI group uniquely favored "whole brain emulation" (46% vs. 0% in TOP100)
- All groups acknowledged uncertainty about which approach would work

### 4. Impact Assessment

Most respondents viewed the impact of HLMI as significant:
- Median assessment: "on balance good" but with substantial risk
- A non-trivial minority (~5%) assigned meaningful probability to "extremely bad" outcomes (existential risk)

## Relevance to Agent Design

### 1. The Governance Question

This survey established the empirical basis for the AI safety/alignment field. If experts believe HLMI is coming within decades, then the design of AI agents is not just an engineering question but a governance question. How agents are designed — their feedback mechanisms, goal structures, control architectures — has long-term implications.

### 2. Agent Architecture and Control

From a cybernetic perspective, the survey highlights the urgency of:
- **Variety management**: As AI agents become more capable, their variety increases. Without correspondingly increased regulatory variety, they become uncontrollable (Law of Requisite Variety applied to AI safety).
- **The Good Regulator problem**: To regulate a superintelligent agent, the regulator (human oversight, safety systems) must be a model of the agent. But if the agent surpasses human comprehension, the Good Regulator Theorem implies effective regulation becomes impossible.
- **Ultrastability risks**: A truly ultrastable AI agent would change its own parameters to maintain homeostasis — but "homeostasis" for the agent might conflict with human interests.

### 3. Timeline Relevance

The survey's timelines have been partially borne out (or exceeded, depending on interpretation). LLM-based agents in 2024-2026 exhibit capabilities that were expected to take longer. This compression makes the design principles more urgent, not less.

### 4. The "Fast Takeoff" Concern

If the transition from HLMI to superintelligence is fast, there is limited time for iterative design improvement. This argues for building robust control architectures (cybernetic stability, variety constraints) into agents from the start, not adding them later.

## Connection to Cybernetics

- **Law of Requisite Variety**: The regulator of an increasingly capable AI system must match its variety. This becomes increasingly difficult as capability grows.
- **Good Regulator Theorem**: Effective oversight requires a model of the system being overseen. Superintelligent systems may be unmodelable.
- **Ultrastability**: Agents that modify their own parameters in pursuit of stability may be dangerous if their stability criterion diverges from human values.
- **Beer's VSM**: The recursive structure of VSM (systems 1-5) provides a template for hierarchical AI governance — but does it scale to superintelligence?

## Limitations

- Response rate of 31% introduces selection bias
- "Expert" groups varied widely in expertise and domain
- The survey predates the LLM revolution (2012-2013)
- Forecasting accuracy for technology timelines is historically poor
- The survey conflates very different conceptions of "intelligence"

## Relation to Other Notes

- Floridi (2013): Provides the ethical framework for evaluating AI progress
- Russell & Norvig: The agent architectures that will be extended toward HLMI
- Dennett (2017): Competence without comprehension — relevant to whether HLMI requires consciousness
- Barandiaran et al. (2009): Are HLMI systems genuine agents? By their definition, probably not.
- Beer VSM / Ashby variety: Design principles for governing increasingly capable systems
