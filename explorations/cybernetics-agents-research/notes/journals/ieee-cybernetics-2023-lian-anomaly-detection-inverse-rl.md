# Anomaly Detection and Correction of Optimizing Autonomous Systems With Inverse Reinforcement Learning

## Citation
Lian, B., Kartal, Y., Lewis, F.L., Mikulski, D., Hudas, G., Wan, Y., & Davoudi, A. (2023). Anomaly Detection and Correction of Optimizing Autonomous Systems With Inverse Reinforcement Learning. *IEEE Transactions on Cybernetics*, 53(7), 4555-4566.

## Access
- ResearchGate (PDF available): https://www.researchgate.net/publication/364606380
- PubMed: https://pubmed.ncbi.nlm.nih.gov/36264741/
- IEEE Xplore: (subscription required)
- ResearchGate PDF returned 403 when fetched directly.

## Summary

Addresses anomaly detection for autonomous systems that are *optimizing* an objective function. Goes beyond standard condition-based maintenance (which detects faults in non-optimizing systems) to detect when an optimizing agent has deviated from its intended objective. Uses inverse RL to recover the objective function from observed behavior, then detects anomalies as deviations from that recovered objective.

## Key Contributions

1. **Inverse RL for objective recovery**: Given observed behavior of an autonomous system, uses inverse RL to infer what objective function the system is (implicitly) optimizing.

2. **Anomaly detection via objective comparison**: Once the "intended" objective is known and the "actual" objective (inferred from current behavior) is recovered, discrepancies indicate anomalies -- the system is no longer optimizing what it should be.

3. **Correction via apprentice learning**: After detecting anomaly, uses a data-driven off-policy inverse RL apprentice learning algorithm to correct the behavior back toward the intended objective.

4. **Quadrotor UAV validation**: Demonstrates the approach on a nonlinear quadrotor model.

## Relevance to Cybernetics-Agents Research

**VERY HIGH RELEVANCE.** This paper addresses a deeply cybernetic problem with direct implications for AI agent design:

1. **Monitoring the regulator itself**: This is second-order cybernetics applied to engineering. The system doesn't just regulate its environment -- it monitors whether *its own regulation* is correct. This is von Foerster's observing system: a system that observes its own observation process.

2. **Inverse RL as model recovery = Good Regulator Theorem in reverse**: The Good Regulator says a controller must be a model of the system. This paper asks: given a controller's behavior, can we recover its model? And if that model diverges from the intended one, something is wrong. This is the diagnostic inverse of Conant-Ashby.

3. **Self-correction as ultrastability**: The anomaly detection and correction loop is Ashby's ultrastability mechanism. The system operates normally (stability at one level), but when essential variables drift outside acceptable bounds (the detected anomaly), a higher-level mechanism (the correction algorithm) intervenes to restore proper behavior.

4. **Direct relevance to LLM agent failure modes**: LLM-based agents can "drift" from their intended objectives through prompt injection, reward hacking, or accumulated context errors. The framework here -- monitor the agent's implicit objective, detect when it deviates from the intended one, and correct -- is exactly what's needed for robust agent architectures.

5. **Optimizing vs. non-optimizing systems**: The paper's distinction between systems that merely function and systems that optimize is relevant to the difference between simple tool-using LLM agents (reactive) and planning/optimizing agents (ReAct, Tree of Thoughts).

## Key Insight for Our Research

This paper provides a formal framework for one of the most critical problems in AI agent design: **how do you detect when an agent has gone off the rails, if the agent itself doesn't know it has?** The cybernetic answer is: you need a meta-level monitor (System 4/5 in VSM) that models the agent's intended behavior and compares it against observed behavior. This paper operationalizes that idea with inverse RL.

## Gaps

- Assumes the "intended" objective is known a priori. For LLM agents, defining the intended objective precisely is itself the hard problem.
- Linear/quadrotor validation -- unclear how this scales to the high-dimensional, discrete action spaces of LLM agents.
- No discussion of adversarial scenarios where the anomaly is deliberately introduced (e.g., prompt injection).

## Status: PARTIALLY ACCESSIBLE
Detailed information from PubMed abstract, ResearchGate metadata, and search results. Full PDF not directly accessible.
