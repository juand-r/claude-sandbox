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

- [x] E1 — self-duration calibration — **done** (hypothesis rejected for this regime; models track latency via output-length proxy)
- [x] E2 — token/step proxy — **done** (hypothesis supported; token-space Δρ +0.231 over seconds)
- [x] E3 — log-gap probe — **done** (sensitivity scales with model strength; deficit is attention, not calibration)
- [x] E4 — harness clock — **done** (hypothesis supported; harness clock 0.96 vs text 0.80 vs none 0.49)

See `SUMMARY.md` for the cross-experiment synthesis and recommendation, and
`direction-train-it-in.md` for the counterpoint research direction.

---

# Next experiments (E5–E10)

Guiding principle: before building a research program on the scoping findings, the next
experiments should first try to **break** them, then invest in the flagship. Tiers are
ordered by information-per-dollar.

## Tier 1 — Validate the headline (cheap, do first)

### E5 — Latency-decoupled probe (the linchpin)
**Why.** Our entire "models track length, not time" story (E1/E2) only holds in an
**output-length-dominated** regime — the main threat to validity in E1's report. E5 tests
whether the finding survives when latency is decoupled from output length.

**Setup.** Three task families, all logging pre-estimate + actual latency + output tokens:
- **Type A (reasoning-decoupled):** matched *short* output, varying difficulty (easy
  arithmetic vs hard combinatorics, both "answer with just the number"). Latency varies via
  hidden reasoning, not output length. Most meaningful for reasoning models.
- **Type B (input-decoupled):** fixed short output, varying *input/context* length (short vs
  ~2k vs ~8k tokens of filler, then a one-word task). Latency varies via prefill.
- **Type C (output-driven control):** E1-style length-varying tasks, as a positive control
  that calibration still holds in this harness.

**Metric.** Spearman ρ(estimate, actual) and gm ratio *within each type*. **Prediction:** ρ
stays high in C, drops in A and B. That would *confirm* "models track length they can see,
not latency they can't" — strengthening E1/E2. If ρ stays high in A/B, the self-estimation
story is richer than a pure length proxy (models have some genuine latency sense), and the
literature's negative result is the artifact.

**Cost.** ~$2–5, API-only, reuses E1 infra. Roster leans on reasoning models for Type A.

### E6 — Length-estimation bias correction (cheap Target 1 test)
**Why.** E2 found a systematic ~2× output-length undershoot. Before anyone fine-tunes, test
whether it closes with **in-context** calibration.

**Setup.** Predict output tokens under conditions: (a) bare [E2 baseline], (b) few-shot
anchors ("one word ≈ 3 tokens, a haiku ≈ 30, a 500-word essay ≈ 700"), (c) predict-then-
self-revise. Measure gm(predicted/actual tokens) → does it move toward 1.0? Plus ρ.

**Prediction / payoff.** If few-shot fixes the bias, Target 1 (length self-estimation) needs
**no training at all** — a cheap, decision-relevant result for `direction-train-it-in.md`.

**Cost.** ~$1–2, short outputs, E2 roster.

## Tier 2 — The flagship (only after Tier 1 confirms the premise)

### E7 — Harden + scale E3 (prerequisite for E8)
Remove E3/E4's biggest caveat: the prompt currently **states** the staleness rule, so we test
the sensor, not threshold knowledge. Drop the stated rule; add multi-turn transcripts and
real elapsed-time consequences; scale 9 → ~200 scenarios; hold out whole scenario families and
threshold regimes. This is the training/eval substrate for E8.

### E8 — Internalization experiment (the "train it in" flagship)
SFT (LoRA; OpenAI FT API available) one weak + one strong model on text-timestamp transcripts
→ correct decision. Report **internalization fraction = (trained − base)/(E4 ceiling − base)**
per model. Prediction: highest for weak models (the sensor substitutes for capability strong
models already have). Decides whether the project's thesis is "give it a sensor" or "a clock
is learnable — here's how much." See `direction-train-it-in.md`. Higher cost (fine-tune +
eval) — do not start before E5 confirms the self-perception premise.

## Tier 3 — Refinements (opportunistic)

### E9 — Sensor-format ablation (extends E4)
Absolute timestamp vs elapsed field vs relative ("3h ago") vs countdown-to-deadline. Which
representation carries the 0.80 → 0.96 lift? Cheap, sharpens the deployable result.

### E10 — Reasoning-model hidden-token probe
Can o4-mini/gpt5.2 estimate their *own reasoning length*? This is the boundary case that
breaks Targets 1–2 (self-estimation). Probe-first before assuming it's trainable.

## Recommendation

Run **E5 + E6 first** (~$3 together): they either harden the foundation or save us from
building on sand. Do **not** start E8 (fine-tuning) until E5 confirms the premise survives
latency-decoupling — if it doesn't, the self-perception lane changes shape entirely.

## Status (next batch)

- [x] E5 — latency-decoupled probe — **done** (prediction confirmed: control ρ 0.79, but
  reasoning-decoupled ρ ≈ 0 and input-decoupled ρ ≈ 0 — calibration is a pure output-length
  proxy; reconciles E1/E2 with the literature)
- [x] E6 — length-estimation bias correction — **done** (self-revision closes the undershoot
  0.37 → 0.76 gm for non-reasoning models; reasoning models stay stuck → Target 1 nearly free
  except for the hidden-token case)
- [ ] E7 — harden + scale E3
- [ ] E8 — internalization experiment
- [ ] E9 — sensor-format ablation
- [ ] E10 — reasoning-model hidden-token probe — **now higher priority** (E5+E6 both isolate
  reasoning-model hidden tokens as *the* boundary where in-context fixes fail)
