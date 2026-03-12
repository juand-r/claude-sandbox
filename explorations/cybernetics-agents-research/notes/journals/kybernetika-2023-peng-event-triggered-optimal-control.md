# Event-Triggered Optimal Control of Completely Unknown Nonlinear Systems via Identifier-Critic Learning

**Authors:** Zhinan Peng, Zhiquan Zhang, Rui Luo, Yiqun Kuang, Jiangping Hu, Hong Cheng, Bijoy Kumar Ghosh
**Journal:** Kybernetika, Vol. 59, No. 3, pp. 365-391, 2023
**DOI:** 10.14736/kyb-2023-3-0365
**URL:** https://www.kybernetika.cz/content/2023/3/365
**PDF:** https://www.kybernetika.cz/content/2023/3/365/paper.pdf
**Keywords:** optimal control, event-triggered mechanism, unknown nonlinear system, adaptive dynamic programming, identifier-critic neural networks

## Summary

Proposes an online identifier-critic learning framework for event-triggered optimal control of
completely unknown nonlinear systems. Uses a filter-regression approach to reconstruct system
dynamics without requiring an accurate model. Neural network adaptive laws estimate parameters
using only measured state and input data.

## Architecture

Two neural networks:
1. **Identifier NN:** estimates unknown system dynamics from measured data
2. **Critic NN:** approximates the cost/value function for optimal control

Event-triggered mechanisms (both static and dynamic) reduce sampling frequency.

## Key Innovation

Unlike traditional actor-critic methods, no prior system model is needed. The identifier
reconstructs dynamics online, making this truly adaptive to unknown environments.

## Relevance to Cybernetics-Agents Research

- **Adaptive control:** This is a modern adaptive control paper in the Wiener/Ashby tradition --
  a system that learns to regulate itself without prior knowledge
- **Model-free learning:** The identifier-critic architecture is a cybernetic feedback loop:
  sense (identify) -> evaluate (critic) -> act (control)
- **Event-triggered = efficient regulation:** Only act when needed, a principle of good
  regulation (minimal intervention, maximum effect)
- **Adaptive dynamic programming:** Connects Bellman's dynamic programming to adaptive
  systems, bridging control theory and reinforcement learning
- **Completely unknown systems:** The "black box" problem is fundamental to cybernetics --
  how do you control what you don't understand?

## Access Status

Full text accessible (open access).
