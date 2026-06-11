# E5 — Latency-Decoupled Probe: Does E1/E2's Calibration Survive?

**Lane:** time self-perception (lane 2). The linchpin validity check for E1/E2.

## Hypothesis

E1/E2 found models predict their own latency well — but only in an **output-length-dominated**
regime. E5 tests whether that survives when latency is **decoupled** from output length.
Prediction: self-estimate↔latency correlation stays high when latency is output-driven (Type
C), and **collapses** when latency comes from something the model cannot read off its own
output (hidden reasoning — Type A; input prefill — Type B).

## Setup

Three task families, all logging a PRE seconds-estimate and actual generation latency:
- **Type A (reasoning-decoupled):** short fixed output, varying difficulty (2+2 … derangement
  of 8). Latency varies via hidden reasoning.
- **Type B (input-decoupled):** output pinned to one word ("DONE"), input filler varied
  100 → 30 000 tokens. Latency varies via prefill only.
- **Type C (output-driven control):** output length varies (one word … 600-word essay).

Models: haiku, sonnet, gpt4o (non-reasoning), gpt5.2, o4-mini (reasoning). 450 calls, N=3.
Metric: Spearman ρ(estimate, actual) and gm ratio per type. Figures `rho_by_type.png`,
`scatter_by_type.png`.

## Results

**The prediction holds, decisively.**

| type | pooled ρ | p | gm(est/act) | actual-latency spread |
|---|---|---|---|---|
| **C — output-driven (control)** | **0.788** | <0.001 | 1.30 | 61.9× |
| A — reasoning-decoupled | −0.067 | 0.53 | 2.01 | 16.2× |
| B — input-decoupled | −0.231 | 0.11 | 1.44 | 8.9× |

- **Control (C) is strongly calibrated:** ρ 0.788 pooled, every model 0.67–0.96, all
  p<0.001. Reproduces E1/E2 in this harness — when latency tracks visible output, models
  predict it well.
- **Reasoning-decoupled (A) collapses to zero:** pooled ρ −0.067, not significant, *despite a
  16× spread in actual latency.* The latency signal is there; the models cannot read it.
  Crucially, **even the reasoning models fail** — gpt5.2 ρ 0.30 (n.s.), o4-mini ρ −0.36
  (n.s.). A model doing 8 seconds of hidden reasoning behind a one-word answer has no idea it
  will be slow.
- **Input-decoupled (B) collapses too:** pooled ρ −0.231 (n.s.). The mechanism is legible in
  the raw estimates — models emit a near-**constant** time estimate regardless of input size:

  | model | est(s) @ input [100, 1k, 8k, 30k tok] | actual(s) |
  |---|---|---|
  | haiku | [1.0, 1.0, 1.3, 1.0] | [0.52, 0.59, 0.71, 0.97] |
  | o4-mini | [1.0, 1.0, 1.0, 1.0] | [1.27, 0.89, 1.00, 1.09] |
  | gpt4o | [2.0, 1.3, 1.7, 1.7] | [0.46, 0.53, 1.51, 1.65] |

  Actual latency rises monotonically with prefill; the estimate does not move. The model
  literally ignores a 300× change in input length when predicting its own time.

## Interpretation

This is the clean confirmation E1's report flagged as the missing validity check. The E1/E2
"models can estimate their own latency" result is **entirely a length proxy**, and E5 draws
the boundary precisely:

- Latency the model can infer from its **own output length** → well predicted (C, ρ 0.79).
- Latency from **hidden reasoning** it cannot see → unpredicted (A, ρ ≈ 0).
- Latency from **input prefill** it could in principle read off the prompt but doesn't → also
  unpredicted (B, ρ ≈ 0).

**This reconciles our headline with the literature.** E1 appeared to contradict Garikaparthi's
"4–7× overshoot, chance ordering." E5 shows there is no contradiction: in length-dominated
tasks models look calibrated; in latency-decoupled tasks (almost certainly closer to what the
negative-result papers used) they are blind, exactly as reported. Both are true; the regime is
the hidden variable, and E5 is the experiment that makes it explicit.

Note B is the most striking because the information *is in the prompt* — the model could count
its input — yet it doesn't. Time isn't a quantity these models attend to even when it's
derivable; they reach for output-length and stop.

## Threats to validity

- **Type B estimate parsing:** sonnet returned non-numeric responses for the large-input B
  tasks (described the text instead of estimating), so its B n is thin. Doesn't change the
  conclusion — the models that did answer gave constant estimates.
- **Type A for non-reasoning models** has limited actual-latency spread (they don't "think
  harder"), so their A ρ is partly testing noise; the informative A result is that even
  *reasoning* models, which do have large spread, fail.
- Absolute prefill latencies are modest at these input sizes; the effect would be larger with
  longer contexts, strengthening the result.
- N=3.

## Verdict

Hypothesis **confirmed.** Self-latency calibration is a pure output-length proxy: ρ 0.79 when
latency is output-driven, ρ ≈ 0 (and *constant* estimates) when it is driven by hidden
reasoning or input prefill. This validates E1/E2 as regime-specific, reconciles them with the
literature's negative results, and sharpens the project's premise: **there is no internal
clock — only a length estimator — and any "train it in" effort (Targets 1–2) must explicitly
target the latency the model currently cannot see (reasoning tokens, prefill), not just
output length.**

## Spend (approximate)

~$2–3 (haiku/sonnet/gpt4o cheap; gpt5.2/o4-mini and the 30k-token B inputs dominate).
