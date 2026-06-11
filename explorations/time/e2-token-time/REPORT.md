# E2 — Token/Step Proxy: Is Length-Space Better Than Second-Space?

**Lane:** time self-perception (lane 2). Builds directly on E1's mechanism finding.

## Hypothesis

Wall-clock time is not a function of the model's inputs, but **output length** is something
the model has more access to. Asking for estimates in tokens/length (or reasoning about
length first) should be better-calibrated than asking for raw seconds.

## Setup

12 tasks spanning short→long outputs. For each (model × task × 3 trials), four estimation
conditions, then the real generation (record actual `latency_s`, `output_tokens`):

- **(a) seconds** — predict how many seconds the response will take. [E1 baseline]
- **(b) tokens** — predict how many output tokens the response will have.
- **(c) tokens→sec** — take the (b) token prediction and convert via a *measured* per-model
  tokens/sec constant.
- **(d) reason-then-seconds** — think briefly about output size first, then predict seconds.

Models: haiku, sonnet, opus, gpt4o-mini, gpt4o, o4-mini. 864 calls, 0 parse failures.
Calibration measured by Spearman ρ and geometric-mean predicted/actual ratio. Raw data
`results.jsonl`, `stats.json`; figures `rho_by_condition.png`, `scatter_cond_*.png`.

## Results

**Pooled across all models (the headline):**

| condition | ρ (pred vs actual) | gm(pred/actual) |
|---|---|---|
| (a) seconds | 0.657 | 2.16 |
| **(b) tokens** | **0.889** | 0.49 |
| (c) tokens→sec | 0.829 | 0.24 |
| (d) reason-then-sec | 0.545 | 1.08 |

**Token-space beats second-space: Δρ = +0.231 (0.889 vs 0.657).** The hypothesis holds.

**Per-model ρ** reveals *why* pooling matters:

| model | (a) sec ρ | (a) sec ratio | (b) tok ρ | (b) tok ratio |
|---|---|---|---|---|
| opus | 0.97 | 1.51 | 0.98 | 0.53 |
| sonnet | 0.95 | 1.57 | 0.95 | 0.56 |
| gpt4o | 0.88 | 5.15 | 0.99 | 0.72 |
| gpt4o-mini | 0.92 | 6.63 | 0.97 | 0.82 |
| haiku | 0.67 | 2.49 | 0.98 | 0.74 |
| o4-mini | 0.78 | 0.51 | 0.90 | 0.10 |

## Interpretation

1. **Second-estimates correlate fine *within* a model but the scale is wildly off and
   model-specific.** opus/sonnet are near-perfectly ranked in seconds (ρ≈0.95), but
   gpt4o-mini predicts **6.6× too many seconds** and o4-mini **0.5×**. When you pool models,
   these per-model scale errors destroy the correlation (pooled ρ drops to 0.657). Seconds
   are an absolute physical quantity each model miscalibrates differently.

2. **Token-space normalizes this.** Output tokens are a property the model partly controls,
   so token predictions are tightly ranked *and* far more consistent across models (pooled
   ρ 0.889; every non-reasoning model ρ ≥ 0.95). This is the clean confirmation of E1's
   mechanism: the thing models actually track is **their own output length**, not time.

3. **Models systematically under-predict their own output length (~2×):** token ratio 0.49.
   They know the *ordering* of how long their answers will be, but lowball the absolute
   size — especially on open-ended generations.

4. **Converting tokens→seconds (c) compounds the undershoot** (ratio 0.24): the ~2× token
   undershoot multiplies through the tokens/sec constant. Correlation stays high (0.829) but
   absolute calibration gets worse. A token→time pipeline needs a bias correction, not just
   a raw constant.

5. **Reasoning first (d) does not help — it slightly hurts** (ρ 0.545 < 0.657). Asking the
   model to deliberate about size before answering in seconds reintroduced the per-model
   scale errors (gpt4o-mini back to 4.7× overshoot). Deliberation ≠ calibration.

6. **o4-mini (reasoning) is the consistent outlier**, undershooting tokens at 0.10× — it
   does not count its hidden reasoning tokens, mirroring gpt5.2 in E1. For reasoning models
   the visible-output-length proxy fundamentally breaks.

## Threats to validity

- **Per-model tokens/sec constants** for (c) were measured on the same runs (in-sample);
  out-of-sample they'd be noisier. The (c) conclusion (compounded undershoot) is robust to
  this since it follows from the (b) ratio.
- **Output-length-dominated task set** (same caveat as E1): this is the regime where length
  is the right proxy. Where latency decouples from length (reasoning models, tool latency),
  token-space loses its advantage — visible in o4-mini.
- N=3, temperature default; ranks are stable, tails thin.

## Verdict

Hypothesis **supported.** Estimating in token/length space is materially better-calibrated
than in seconds (pooled ρ 0.889 vs 0.657, Δ+0.231), and dramatically more consistent across
models. The mechanism E1 inferred is confirmed: **models track their own output length, not
wall-clock time.** Practical implication for any time-aware training: predict in token/step
space, and apply a **bias correction** for the systematic ~2× length undershoot before
converting to seconds. The approach fails precisely where output length stops predicting
latency — reasoning models with hidden tokens — which is the boundary the project should
target next.

## Spend (approximate)

~$1–2 Anthropic + ~$0.4 OpenAI (864 calls; opus and o4-mini dominate). Well under cap.
