# E10 — Reasoning-Model Hidden-Token Probe

**Lane:** time self-perception (lane 2). Attacks the boundary that E1, E2, E5, and E6 all
isolated: reasoning models cannot account for tokens spent on hidden reasoning.

## Hypothesis

A reasoning model is blind to its own reasoning cost — it cannot predict how much internal
reasoning a problem will require. Prediction: ρ(estimate, actual reasoning tokens) ≈ 0.

## Setup

14 short-answer problems across a reasoning-difficulty gradient (2+2 … a 5-person ordering
puzzle; derangements; modular exponentiation). All have a one-token-ish final answer, so the
variable is *internal reasoning*, not output length. For each (model × task × 3 trials), two
pre-solve estimates and the solve:
- **pre\_tokens** — "without solving, estimate how many tokens of internal reasoning you will
  need" (a number).
- **pre\_effort** — "rate 1–10 how much step-by-step reasoning this needs" (ordinal).
- **gen** — actually solve; record **actual `reasoning_tokens`** from the API usage.

Models: **o4-mini, gpt5** — the OpenAI reasoning models whose `reasoning_tokens` vary with
difficulty and are exposed in usage. (gpt5.2 does not engage reasoning by default → excluded;
this is itself worth noting.) 252 calls. The quantity being predicted has a huge real range:
o4-mini 0→4075, gpt5 0→4757 reasoning tokens.

## Results

**The hypothesis is wrong — and the truth is more interesting.** Reasoning models have
substantial *ordinal* awareness of their own reasoning cost; what they lack is *magnitude*.

| model | predictor | ρ vs actual reasoning | ordering acc | gm(est/act) | n |
|---|---|---|---|---|---|
| gpt5 | effort 1–10 | **0.908** | 0.943 | — | 14 |
| o4-mini | token estimate | **0.796** | 0.837 | 0.17 | 14 |
| o4-mini | effort 1–10 | 0.602 | 0.867 | — | 14 |
| gpt5 | token estimate | 0.036 | 0.500 | 0.24 | 8* |
| **pooled** | effort 1–10 | **0.772** | 0.901 | — | 28 |
| **pooled** | token estimate | 0.403 | 0.668 | — | 22 |

\*gpt5 produced a parseable token number for only 8/14 tasks — it frequently *refuses* to put a
number on its reasoning, or gives wildly inconsistent ones (e.g. 133 496 on one trial, 30 on the
next for the same task). So its token-estimate ρ is on a thin, self-selected subset and is not
meaningful. Its **effort rating, by contrast, is excellent (ρ 0.91).**

Three findings:

1. **Ordinal effort awareness is real and strong.** The 1–10 effort rating tracks actual
   reasoning tokens well (pooled ρ 0.77, ordering 0.90; gpt5 0.91). Models *know which problems
   will make them think harder*. Sorted by actual reasoning, gpt5's effort climbs monotonically
   (easy ≈ 1, medium ≈ 2, hard 2–3, very-hard 3–4.7). This directly contradicts a naive "blind
   to reasoning" claim.

2. **Magnitude calibration fails completely.** gm(token estimate / actual) is 0.17–0.24 — off
   by ~5–6× on the parsed subset, and far worse at the extremes. They cannot map "this is hard"
   to a token count.

3. **The extremes are systematically under-rated.** The hardest task (`vhard_logic`, ~4075–4757
   actual reasoning tokens — 5–10× the next hardest) drew an effort rating of only **3/10** from
   both models. The ordinal signal saturates: models distinguish easy/medium/hard but flatten at
   the top, badly under-rating their worst cases.

4. **Token estimates are model-specific.** o4-mini *will* give a token number and ranks it well
   (ρ 0.80); gpt5 mostly won't. The robust cross-model channel is the **effort rating**.

## Interpretation — this refines the project's central boundary

Every prior experiment (E1, E2, E5, E6) found reasoning models at the failure edge and we
framed it as "blind to hidden reasoning." E10 sharpens that: the blindness is about
**magnitude/calibration, not ordinal access.** Asked in the right currency — *how hard is this
for you?* rather than *how many tokens/seconds?* — a reasoning model answers well.

This matters for the "train-it-in" direction. E6 showed the output-length undershoot is
in-context-fixable precisely because the *ranking* was intact and only the *scale* was off.
E10 shows the reasoning-cost signal has the **same structure**: intact ordinal ranking (the
effort rating), broken magnitude. So the reasoning-model boundary is plausibly the *same kind*
of tractable calibration problem, not a fundamental wall — a fitted map from effort rating →
token count could work, exactly as a bias correction worked for output length. The boundary is
softer than the earlier experiments implied.

## Threats to validity

- **Small**: 14 tasks, 2 models. ρ 0.91 (n=14) is significant (p<0.01), 0.60 (n=14) ≈ p<0.05,
  so the ordinal findings hold, but tails are thin.
- **gpt5 token refusals** make its token-estimate ρ uninformative; the effort channel carries
  the gpt5 result.
- **Effort gm is meaningless** (1–10 scale vs token counts) — only ρ/ordering are interpretable
  for effort; gm is shown only for token estimates.
- **Reasoning effort is partly stochastic** (the same task draws different reasoning_tokens
  across trials), which caps achievable ρ — the model is predicting a distribution.
- **gpt5.2 excluded** (no reasoning by default); Anthropic extended-thinking models untested —
  both are future work.

## Verdict

Hypothesis **rejected, with a sharper replacement.** Reasoning models are *not* blind to their
own reasoning — they have strong ordinal awareness of reasoning effort (effort-rating ρ up to
0.91) — but they cannot calibrate its magnitude (token estimates off ~5–6×, refused outright by
gpt5, extremes under-rated). The recurring "reasoning-model boundary" is a **magnitude-calibration
problem on an already-ordered signal**, which — per E6's precedent — is the tractable, trainable
kind. This is the most optimistic finding for the train-it-in program and should update the
synthesis accordingly.

## Spend (approximate)

~$3–5 (252 calls, reasoning models with up to ~4–8k reasoning tokens on the hard solves).
