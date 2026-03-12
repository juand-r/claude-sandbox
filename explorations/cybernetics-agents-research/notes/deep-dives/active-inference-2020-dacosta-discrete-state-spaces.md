# Da Costa et al. (2020) — Active Inference on Discrete State-Spaces

**Paper:** Da Costa, L., Parr, T., Sajid, N., Veselic, S., Neacsu, V., & Friston, K.
(2020). "Active inference on discrete state-spaces: A synthesis." *Journal of
Mathematical Psychology*, 99, 102447.
**URL:** https://arxiv.org/abs/2001.07203

---

## Summary

This paper provides the **complete mathematical synthesis** of active inference on
discrete state-space (POMDP) models. It is the definitive technical reference for
implementing active inference agents in discrete environments — the mathematical
foundation behind pymdp and similar implementations.

## Mathematical Framework

### Generative Model: POMDP Structure

The generative model is a Partially Observable Markov Decision Process specified by:

- **A matrix** (likelihood): P(o_t | s_t) — mapping from hidden states to observations
- **B matrix** (transitions): P(s_t | s_{t-1}, a_{t-1}) — state dynamics given actions
- **C vector** (preferences): log P(o) — prior preferences over observations
- **D vector** (initial state): P(s_0) — prior beliefs about initial state

The agent does not know the true hidden state, only observations. It must infer
states, select policies, and learn model parameters — all from the same variational
objective.

### Variational Free Energy (for Past/Present)

For current observations, the agent minimizes variational free energy:

```
F = E_q[ln q(s) - ln p(o, s)] = D_KL[q(s) || p(s|o)] - ln p(o)
```

This performs approximate Bayesian inference: the approximate posterior q(s)
converges toward the true posterior p(s|o).

### Expected Free Energy (for Future/Planning)

For evaluating policies (sequences of future actions), the agent minimizes
**Expected Free Energy** (EFE):

```
G(π) = Σ_τ G(π, τ)

G(π, τ) = E_q(o_τ, s_τ | π)[ln q(s_τ | π) - ln p(o_τ, s_τ)]
```

This decomposes into:

1. **Risk + Ambiguity:**
   ```
   G = D_KL[q(o_τ|π) || p(o_τ)] + E_q[H[p(o_τ|s_τ)]]
   ```
   - Risk: deviation from preferred observations
   - Ambiguity: expected observation uncertainty

2. **Pragmatic + Epistemic value:**
   ```
   G = -E[ln p(o_τ)] - I(o_τ; s_τ | π)
   ```
   - Pragmatic: expected preference satisfaction
   - Epistemic: expected information gain

### Policy Selection

Beliefs about policies use softmax over negative EFE:

```
Q(π) = σ(-γ · G(π))
```

Where γ is an inverse temperature parameter controlling exploration-exploitation
balance.

### Belief Updating (Message Passing)

State inference uses iterative message passing that combines:
- Bottom-up messages from observations (likelihood)
- Top-down messages from predictions (transition model)
- Policy-dependent expectations

The update equations have the form of gradient descent on free energy and can
be mapped onto known neurophysiological processes.

## Neuronal Dynamics

The paper derives neuronal dynamics from first principles:

- **State estimation** maps onto sensory cortex activity
- **Policy evaluation** maps onto prefrontal/striatal evaluation
- **Precision (γ)** maps onto dopaminergic modulation
- **Expected free energy** maps onto value signals in basal ganglia
- **Policy selection** maps onto action selection in motor cortex

## Mixed Generative Models

The paper extends the framework to **mixed models** where discrete hidden states
generate continuous observations. This bridges the gap between discrete planning
and continuous sensory processing — relevant for real-world agents that plan in
discrete action spaces but perceive continuous signals.

## Cybernetic Connections

### Homeostatic Goals as Priors

The C vector (preferences over observations) encodes what the agent *expects* to
observe — its homeostatic setpoints. The agent acts to make observations conform
to these priors, which is negative feedback control implemented via Bayesian
inference.

### Error-Driven Updates

All belief updating is driven by prediction errors — the difference between
predicted and actual observations/states. This is the same error-correction
principle that Ashby identified as fundamental to brain function.

### Good Regulator

The agent's generative model (A, B, C, D matrices) constitutes a model of its
environment. Through learning (updating these matrices), the agent becomes a
progressively better model of its environment — the Good Regulator Theorem in
action.

## Significance for Agent Design

This paper is the **implementation blueprint**. It specifies exactly:
1. What data structures are needed (A, B, C, D matrices)
2. How state inference works (variational message passing)
3. How policies are evaluated (expected free energy)
4. How actions are selected (softmax over negative EFE)
5. How learning updates model parameters

pymdp implements this directly. Any practical active inference agent on discrete
state-spaces starts here.

## Limitations

1. Scales poorly with state-space size (matrix operations grow combinatorially)
2. Policy evaluation requires enumerating all policies or using tree search
3. Planning depth is limited by computational cost
4. Continuous state-spaces require different formulation (continuous active inference)

## Status

Freely available on arXiv.
