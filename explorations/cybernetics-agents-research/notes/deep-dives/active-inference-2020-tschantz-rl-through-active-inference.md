# Tschantz et al. (2020) — Reinforcement Learning through Active Inference

**Paper:** Tschantz, A., Millidge, B., Seth, A.K., & Buckley, C.L. (2020).
"Reinforcement Learning through Active Inference." arXiv:2002.12636.
**URL:** https://arxiv.org/abs/2002.12636

---

## Summary

This paper bridges active inference and reinforcement learning by proposing a
novel objective — the "free energy of the expected future" — that enables scaling
active inference to complex, high-dimensional environments using deep neural
networks. It demonstrates that the approach provides an inherent balance of
exploration and exploitation and handles sparse, well-shaped, and absent rewards.

## Core Contribution

### The Scaling Problem

Standard active inference on discrete state-spaces (Da Costa et al. 2020, pymdp)
requires explicit matrix representations of the generative model. This does not
scale to high-dimensional continuous environments (images, physics simulations).

Tschantz et al. propose using **deep neural networks** to parameterize the
generative model, enabling active inference to operate at the scale of modern RL
benchmarks.

### The Free Energy of the Expected Future

The paper introduces a new objective:

```
F_future = E_q(s_T) [ln q(s_T) - ln p̃(s_T)]
```

Where:
- q(s_T) is the expected future state distribution under a policy
- p̃(s_T) is a "biased" generative model encoding preferences

The key insight: agents act to maximize evidence for a **biased** generative
model — one that expects preferred outcomes. This naturally drives goal-directed
behavior while maintaining an exploration bonus.

### Exploration-Exploitation Balance

The objective inherently balances:
- **Exploitation:** Seeking states that match preferences (high p̃(s_T))
- **Exploration:** Seeking states where the model is uncertain (high entropy
  of q(s_T))

No epsilon-greedy, no UCB, no intrinsic motivation add-ons. The balance emerges
from the mathematics.

### Flexible Reward Conceptualization

The framework offers a more flexible notion of reward:
- Reward can be encoded as preferences in the generative model
- Reward-free exploration is naturally supported
- Sparse rewards are handled gracefully (exploration fills the gaps)

## Implementation

### Deep Active Inference Architecture

The agent uses neural networks for:
1. **World model:** Learns environment dynamics (transition model)
2. **Observation model:** Maps states to observations (encoder/decoder)
3. **Policy network:** Outputs actions

Training uses the variational free energy as a loss function, similar to
variational autoencoders (VAEs). The world model learns by minimizing free
energy on observed trajectories.

### Connection to Model-Based RL

The architecture is structurally similar to model-based RL methods like
World Models (Ha & Schmidhuber, 2018) and Dreamer (Hafner et al., 2019).
The difference is the objective function: free energy instead of reward
maximization.

## Experimental Results

The paper tests on challenging RL benchmarks:
- Mountain Car (sparse reward)
- Cart-Pole (well-shaped reward)
- Environments with no reward at all

Results show robust performance across all settings. Key findings:
- With sparse rewards: active inference explores systematically and finds
  the goal
- With well-shaped rewards: competitive with standard RL
- With no rewards: still explores meaningfully (unlike RL which stagnates)

## Cybernetic Connections

### From Setpoints to Biased Generative Models

The "biased generative model" p̃ is essentially a mathematical formalization
of cybernetic setpoints. The agent acts to make reality match its biased
model — to bring the world into conformity with its expectations. This is
precisely what a cybernetic controller does: acts to reduce the discrepancy
between setpoint and measured value.

### Model-Based Control

The requirement for a learned world model echoes the Good Regulator Theorem:
the agent must model its environment to control it. The deep neural network
learns to be a model of the environment through free energy minimization.

### Active vs. Passive

The distinction between exploring (active, epistemic) and exploiting (passive,
pragmatic) maps onto the cybernetic distinction between search behavior
(exploring the environment to build a model) and regulatory behavior
(acting to maintain essential variables).

## Significance for Agent Design

This paper is important because it shows that active inference can be made
practical at scale:

1. **Neural network parameterization** overcomes the scalability limitations
   of discrete active inference
2. **Compatible with modern deep learning infrastructure** (gradient descent,
   backpropagation, GPUs)
3. **Unified exploration-exploitation** without hyperparameters
4. **Robust across reward conditions** (sparse, shaped, absent)

However, the honest assessment (per Millidge 2024): once you parameterize
with neural networks and train with gradient descent, the resulting algorithm
looks a lot like model-based RL with a different loss function. The "special
sauce" of active inference may not survive the translation to deep learning.

## Follow-Up

- Fountas et al. (2020): "Deep active inference agents using Monte-Carlo methods"
- Millidge (2020): "Deep active inference as variational policy gradients"
- Millidge (2024): Retrospective concluding the frameworks are "essentially
  isomorphic"

## Status

Freely available on arXiv.
