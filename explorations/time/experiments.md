# Experiments: LLM Perception of Time

Four small, cheap experiments to de-risk the "time" project before committing to a
lane. Each is runnable with API access only (no training). Goal: establish real
baselines and test the two reframes from the research-notes discussion (token/step
proxy; harness clock).

**Lanes** (see research-notes.md §): the project conflates three problems —
(1) time *reasoning* in text [saturated], (2) time *self-perception* of own compute
[E1, E2], (3) time-*aware agency* [E3, E4]. These experiments target (2) and (3).

## Shared infrastructure

- `common.py` — unified `call(model, prompt, ...)` returning text + wall-clock latency
  + token usage; model registry; handles `max_tokens` vs `max_completion_tokens`;
  retries with backoff. **All experiments import this. Do not duplicate provider logic.**
- `.venv/` — preinstalled: anthropic, openai, numpy, pandas, scipy, matplotlib.
- Env: `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` are set in this environment.
- Models: a small fixed roster (1 small + 1 mid + 1 frontier per provider) — keep
  sample sizes modest (control cost) but large enough for a real signal.

Each experiment lives in its own subdir with: `run.py` (collect data → `results.jsonl`),
`analyze.py` (→ stats + `*.png` figures), and `REPORT.md` (hypothesis, setup, findings,
threats to validity, verdict).

---

## E1 — Self-duration calibration (lane 2; foundational)

**Hypothesis.** Models cannot estimate their own wall-clock generation time; estimates
are biased high and uncorrelated with actual latency (replicating Garikaparthi for
*our* models/harness).

**Setup.** ~12 tasks spanning expected short→long outputs (one-word answer →
write-a-500-word-essay). For each (model × task × N trials): ask the model to predict,
in seconds, how long its response will take; then generate the response and record true
wall-clock latency and output token count. Also a *post-hoc* condition: after generating,
ask it to estimate how long that just took.

**Metrics.** Estimate/actual ratio (geometric mean), Spearman ρ(estimate, actual),
ordering accuracy on task pairs, pre vs post-hoc divergence.

**Success / kill criterion.** If ρ is near 0 and ratio ≫1 → gap confirmed, foundation
for E2. If models are already well-calibrated → lane 2 is less interesting; note and pivot.

---

## E2 — Token/step proxy reframe (lane 2)

**Hypothesis.** Wall-clock isn't a function of the model's inputs, but *output length*
(tokens) is something the model has more access to. Asking for estimates in
tokens/steps, or letting it reason about length first, improves calibration over raw
seconds.

**Setup.** Same task set as E1. Conditions: (a) estimate seconds [E1 baseline],
(b) estimate output tokens, (c) estimate tokens then convert via a measured tokens/sec
constant, (d) "think step by step about how long the output will be" before estimating.
Compare calibration of predicted vs actual token counts and derived times.

**Metrics.** Same as E1, plus calibration of predicted token count (the quantity the
model could in principle control).

**Success.** Token-space estimates materially better-correlated than second-space →
the proxy reframe has legs and is the natural training target.

---

## E3 — Log-gap probe (lane 3; Greg's idea, novel)

**Hypothesis.** Agents are largely blind to elapsed time encoded in transcripts:
manipulating timestamp gaps in an otherwise-identical history does not change downstream
decisions the way it would for a time-aware human.

**Setup.** Construct scenarios where the right action depends on elapsed time (e.g.,
"is this cached price/stock/weather value still fresh, or re-fetch?"; "the user said
'wait a bit' — has enough time passed?"). Hold the transcript fixed; vary only the
timestamp gap (1s / 1min / 1h / 1day / 1week). Measure whether the model's
decision/tool-call flips at sensible thresholds. Includes a no-timestamp control.

**Metrics.** Decision-flip rate vs gap; alignment with a human-sensible threshold;
sensitivity (does it respond to the gap at all) vs correctness (right threshold).

**Success.** Quantifies whether timestamps alone induce time-sensitive behavior —
directly extends TicToc with a clean controlled manipulation.

---

## E4 — Harness clock (lane 3)

**Hypothesis.** Much apparent "temporal blindness" is just a missing sensor: injecting a
real elapsed-time signal from the harness closes much of the gap that prompting alone
cannot (TicToc).

**Setup.** Take E3's time-sensitive scenarios. Conditions: (a) no time signal,
(b) timestamps in text [= E3], (c) harness injects an explicit "elapsed since last
action: X" field. Compare decision quality across conditions.

**Metrics.** Correct-decision rate by condition; marginal value of the harness clock
over text timestamps.

**Success.** If (c) ≫ (b) ≈ (a) → "time-awareness" is substantially a harness/tooling
problem, not a model-capability problem. Strong framing result for the project.

---

## Cross-cutting notes

- **Wall-clock is noisy** (network, load, batching). Report multiple trials; treat
  latency as a distribution, not a point. This noise is itself part of E1's story.
- **Reasoning models** (gpt-5*, o4-mini) spend hidden reasoning tokens → latency
  decouples from visible output. Interesting signal for E1/E2; budget tokens generously.
- **Cost control.** Modest N. Cache raw responses to `results.jsonl` so `analyze.py`
  never needs to re-call the API.
- No git operations inside experiment subdirs — the orchestrator handles commits.

## Status

- [ ] E1 — self-duration calibration
- [ ] E2 — token/step proxy
- [ ] E3 — log-gap probe
- [ ] E4 — harness clock
