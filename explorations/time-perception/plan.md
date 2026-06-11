# Time Perception — Plan

Build a subjective sense of time out of **interacting oscillations**, as a
self-contained dynamical system. No LLM. If a language model ever uses this, it
just reads a few scalars off the engine.

## Core claim

One oscillator system, three read-outs. The three payoffs we care about are not
separate projects — they are different taps on the same state:

| Payoff               | Read-out off the oscillator state                                  |
|----------------------|--------------------------------------------------------------------|
| Temporal reasoning   | the multi-scale phase code; phase-stamp differences = durations     |
| Subjective illusions | prospective rate (gated self-clock) vs retrospective load disagree  |
| Self-regulation      | thresholds on those read-outs, fed back as events (nested loop)     |

## Vocabulary (kept concrete to avoid numerology)

- **Oscillator**: phase theta_i advancing at natural frequency omega_i,
  geometric spacing fast -> slow. The bank is the multi-scale clock.
- **Perception**: an event perturbs the phases (partial reset toward 0).
- **Attention**: a gate on the prospective clock. High when little is happening
  (idle), low when flooded. This is the prospective sign.
- **Read-outs**:
  - prospective `tau`   = gated integral of the self-clock (felt rate, in the moment)
  - retrospective `load`= accumulated perturbation magnitude (remembered duration)
  - recency/`coherence` = order parameter, decays as oscillators dephase after a reset

## The key phenomenology (got the sign right after correction)

Prospective (in the moment): idle **drags**, busy **flies**.
Retrospective (from memory): busy is remembered **long**, idle **short**.
The holiday paradox = these two disagree. Reproducing the disagreement is the
headline result, and it is why this is more than a timestamp counter.

## Skeptical constraints

1. Scalar property (Weber) does NOT emerge for free — inject frequency jitter.
2. Strong global coupling synchronizes everything and destroys the multi-scale
   code. Coupling must be weak or hierarchical. (Stage 2 concern.)
3. Coupling is not load-bearing for the dissociation or self-regulation, so do
   not front-load it.

## Stages

### Stage 1 — uncoupled bank (DONE)
- [x] Oscillator bank, geometric frequencies, event perturbations.
- [x] Attention gate driven by recent input activity.
- [x] Three read-outs: prospective tau, retrospective load, coherence.
- [x] Demo A: holiday-paradox dissociation (busy vs idle, same wall time).
- [x] Demo B: idle detection / self-regulation (felt-idle threshold -> check-in).
- [x] Validation: scalar property (CV ~ flat across durations with jitter).

### Stage 1b — back-end read-outs (later)
- [ ] Central tendency (Bayesian prior over the tested range).
- [ ] Bisection (detector training; geometric-mean crossover with log-spaced omega).

### Stage 2 — interaction
- [ ] Weak / hierarchical coupling (Kuramoto and/or fast-ticks-slow cascade).
- [ ] Emergent coherence-decay recency; nested-scale loops.
- [ ] Check whether coupling buys anything Stage 1 did not.

## Notes log
- Stage 1 works. Dissociation reproduced: busy felt ~6s / idle felt ~43s over the
  same 60s window (prospective), while busy load >> idle load (retrospective).
- Scalar property CV is flat to 3 decimals — because it is injected as multiplicative
  rate jitter, not emergent. Honest, expected; do not oversell it.
- Coherence read-out exists but is not yet exercised by a demo; it becomes useful
  with coupling (Stage 2), where the decay rate is structured rather than just the
  free dephasing of the bank.
- Open question for Stage 2: does coupling earn its place, or does it mostly just
  risk synchronization collapse? Decide empirically.
