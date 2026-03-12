# Sajid et al. (2021) — Active Inference: Demystified and Compared

**Paper:** Sajid, N., Ball, P.J., Parr, T., & Friston, K.J. (2021). "Active
inference: demystified and compared." *Neural Computation*, 33(3), 674-712.
**URL:** https://arxiv.org/abs/1909.10863

---

## Summary

This paper provides a systematic comparison of active inference with reinforcement
learning on the same discrete-state environments. It demonstrates that active
inference agents can perform epistemic exploration and handle uncertainty in a
Bayes-optimal fashion, without requiring an explicit reward signal.

## Core Contributions

### 1. Demystification

The paper walks through the active inference framework step by step, making
the mathematics accessible. Key clarifications:

- Active inference operates entirely in **belief space** (beliefs about states,
  not states themselves)
- Reward is treated as "just another observation" — preferences over observations
  replace external reward signals
- Policy selection uses expected free energy, which naturally balances exploration
  and exploitation

### 2. Comparison with RL

The paper compares active inference agents with standard RL agents on the same
environments:

| Feature | Active Inference | RL |
|---------|-----------------|-----|
| Objective | Minimize expected free energy | Maximize expected reward |
| Reward signal | Prior preferences (no external reward needed) | External reward function |
| Exploration | Epistemic value (information gain) emerges naturally | Must be added (epsilon-greedy, UCB, etc.) |
| State estimation | Integrated (belief updating) | Separate or assumed known |
| Model | Always model-based (generative model) | Model-free or model-based |

### 3. Reward-Free Learning

A key demonstration: active inference agents can learn meaningful behaviors
in environments with **no reward signal at all**. They explore systematically
(driven by epistemic value) and form useful models of the environment. RL agents,
by contrast, cannot learn without reward.

This is because epistemic value — the drive to reduce uncertainty about hidden
states — is intrinsic to the expected free energy objective. The agent seeks
informative observations even when there is no pragmatic incentive.

### 4. Epistemic Exploration

The paper shows active inference agents engaging in principled exploration:
- They seek out observations that resolve uncertainty about hidden states
- They avoid ambiguous observations that do not disambiguate hypotheses
- They balance exploration (epistemic value) with exploitation (pragmatic value)
  without hyperparameters

## Formal Comparison

### Expected Free Energy vs. Expected Reward

The expected free energy can be decomposed as:

```
G(π) = -E[ln p(o)] - I(o; s | π)
        ^^^^^^^^^^   ^^^^^^^^^^^^
        Pragmatic    Epistemic
        (exploit)    (explore)
```

Expected reward in RL:

```
V(π) = E[r(s, a)]
```

The key difference: G(π) includes an epistemic term that has no counterpart in
standard RL. This term drives exploration without requiring any add-on mechanism.

### When They Converge

In fully observable environments with known dynamics and only pragmatic
considerations, active inference reduces to standard Bayesian decision theory
(and hence to RL with a Bayesian model). The frameworks diverge when:
- The environment is partially observable
- There is genuine uncertainty about hidden states
- Exploration is valuable

## Cybernetic Connections

### Error-Driven Control

Active inference updates beliefs through prediction errors — the difference
between predicted and actual observations. This is the same error-correction
mechanism that Ashby identified as fundamental.

### Goals as Setpoints

Prior preferences (the C vector) function as cybernetic setpoints: the agent
acts to make observations match its preferences, just as a thermostat acts to
make temperature match its setpoint.

### Model-Based Regulation

The requirement for a generative model echoes the Good Regulator Theorem: the
agent must model its environment to regulate it effectively.

## Significance for Agent Design

1. Active inference provides a principled framework for agents in partially
   observable environments
2. Exploration arises naturally without hyperparameter tuning
3. Goals can be specified as preferences over observations rather than reward
   functions
4. The framework is inherently model-based, which may be advantageous for
   sample efficiency but costly for complex environments
5. The comparison clarifies when active inference offers advantages over RL
   and when it does not

## Limitations Noted

1. Active inference has not been scaled to high-dimensional problems
2. The generative model must be specified or learned — this is the hard part
3. In simple, fully observable environments, active inference offers no
   advantage over RL
4. The computational cost of policy evaluation grows with planning depth

## Status

Freely available on arXiv.
