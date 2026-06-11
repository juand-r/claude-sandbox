# E1 — Self-Duration Calibration: Can a Model Estimate Its Own Generation Time?

**Lane:** time self-perception (lane 2). Foundational experiment; replicates the
Garikaparthi "Can LLMs Perceive Time?" setup for our models/harness.

## Hypothesis

Models cannot estimate their own wall-clock generation time; estimates are biased high
(literature: 4–7× overshoot) and uncorrelated with actual latency (ordering at/below
chance).

## Setup

12 tasks spanning expected short→long outputs (one-word answer, yes/no, arithmetic, a
3-item list, a haiku, a short paragraph, a 500-word essay, a code function, etc.). For
each (model × task × 3 trials):
- **PRE**: ask the model to predict, in seconds, how long its response will take.
- **GEN**: send the real task; record true wall-clock `latency_s` and `output_tokens`.
- **POST**: in a fresh call, show it the task + its own answer and ask how long that took.

Models: haiku, sonnet, opus, gpt4o-mini, gpt4o, gpt5.2. 648 calls, 216 (model,task,trial)
units. Raw data `results.jsonl`; figures `fig_scatter.png`, `fig_ratios.png`,
`fig_noise.png`.

## Results

**The hypothesis does not hold for this task set.** Models are *well* calibrated.

| model | gm ratio PRE (est/actual) | ρ PRE | ordering acc | ρ POST |
|---|---|---|---|---|
| opus | 0.93 | 0.94 | 0.94 | 0.95 |
| sonnet | 0.76 | 0.85 | 0.95 | 0.85 |
| gpt4o | 1.04 | 0.83 | 0.86 | 0.77 |
| gpt4o-mini | 1.36 | 0.74 | 0.86 | 0.89 |
| haiku | 0.86 | 0.89 | 0.88 | 0.76 |
| gpt5.2 | 0.32 | 0.74 | 0.79 | 0.84 |
| **OVERALL** | **0.81** | **0.75** | — | — |

- **Ratios are near 1, not 4–7×.** Overall geometric-mean estimate/actual = 0.81 — if
  anything a mild *under*estimate, never the order-of-magnitude overshoot the literature
  reports. All models sit within ~1.4× either way except gpt5.2.
- **Ordering is far above chance** (0.5): 0.79–0.95. Models rank task durations correctly
  almost every time. Spot check (sonnet): est 1.0s for arithmetic (actual ~1.1s), est 8–12s
  for the essay (actual ~16s), est 1.0s for one-word (actual ~1.2s). The monotonic
  structure is essentially perfect.
- **Spearman ρ_PRE 0.74–0.94, all p < 0.001.** Strong, significant correlation between
  predicted and actual latency.

**Wall-clock noise** (median CV of latency across trials) is small — 0.04 (haiku) to 0.14
(opus) — so the calibration signal is not being swamped by harness noise.

## Why the contradiction with the literature

This is the interesting part, and it sets up E2. Our task set varies tasks primarily by
**output length** (one word → 500-word essay), and for non-reasoning models wall-clock
latency is dominated by output token count. Models *can* anticipate roughly how long their
own output will be, so they predict latency well **via an implicit output-length proxy** —
not because they have a clock, but because length is the thing that drives the clock here.

Two pieces of evidence that it is a length proxy, not genuine time-sensing:

1. **gpt5.2 (reasoning) is the worst-calibrated, undershooting at 0.32×.** Its latency is
   dominated by *hidden reasoning tokens* it cannot see in its own output, so the
   length-proxy breaks and it badly underestimates. Exactly the failure the length-proxy
   theory predicts.
2. **The systematic undershoots are on `code` and `story`** (sonnet est 4s vs actual ~7–8s)
   — longer free-form generations where the model underestimates its own verbosity.

Garikaparthi's stronger negative result very likely comes from tasks where latency varies
for reasons *invisible to the model* (reasoning depth, tool/network latency, hardware,
batching). When we strip those out and let output length drive latency, the "temporal
blindness" largely disappears. The honest conclusion is not "the literature is wrong" but
"the deficit is specific: models track latency they can predict from output length, and
fail on latency they cannot see."

## Threats to validity

- **Output-length-dominated task set** — by construction this is the regime most favorable
  to the model. A task set that decouples difficulty/latency from output length (forced
  long reasoning on a short answer; variable tool latency) would likely reproduce the
  literature's negative result. This is the obvious follow-up.
- **Wall-clock is harness/hardware specific.** Absolute ratios would shift on different
  hardware or under load; the *ordering* and *correlation* results are far more robust and
  are the headline. Note this does **not** make seconds-prediction untrainable: the median
  latency CV across trials here was only 0.04–0.14, so within a *fixed* deployment the seconds
  target is reproducible and learnable — it just won't transfer across environments. (An
  earlier reading of this report over-claimed that wall-clock seconds is unlearnable because
  it "isn't a function of the inputs"; that holds only across environments, not within one.
  See `../direction-train-it-in.md`.)
- **PRE estimates are coarse integers** (1s, 2s, 4s…), which slightly quantizes ratios but
  does not affect rank statistics.
- N=3 trials; latency CV is low so this is adequate for means, thin for tails.

## Verdict

Hypothesis **rejected for this regime.** Contrary to the 4–7×-overshoot / chance-ordering
claim, models predict their own generation time well **when latency is driven by output
length** (ρ up to 0.94, ordering up to 0.95, ratios near 1). The capability is a
**length proxy**, not a clock: it collapses for reasoning models whose latency hides in
unseen reasoning tokens (gpt5.2 at 0.32×). This directly motivates E2 — if the mechanism is
output-length estimation, then asking models to predict in token/length space should be the
natural, better-calibrated target.

## Spend (approximate)

~$1.01 Anthropic + ~$0.14 OpenAI (648 calls). opus dominates (~$0.84).
