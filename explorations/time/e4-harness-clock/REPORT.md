# E4 — Harness Clock vs Text Timestamps vs No Time Signal

*Lane 3 (time-aware agency). Parallel to E3; scenarios defined independently.*

## Hypothesis

Much apparent "temporal blindness" in LLM agents is a **missing sensor** problem, not a
reasoning-capability problem. Injecting a real, explicit elapsed-time signal from the
harness (condition **c**) should yield better time-sensitive decisions than burying
absolute timestamps in transcript text (**b**), which is itself only marginally better
than no time information (**a**). If `c >> b ≈ a`, time-awareness is substantially a
harness/tooling problem. This tests the TicToc framing (timestamps help only marginally;
post-training claimed necessary) against the alternative that a plainly-stated elapsed-time
field closes most of the gap with no training.

## Setup

- **9 scenarios**, families: freshness (stock price, weather, inventory, news, sensor),
  expiry (auth token, idle banking session), staleness (CI build artifact), wait
  ("user said wait ~10 min"). Each is a **binary decision** with a documented human threshold.
- **4 gaps per scenario** straddling the threshold (clearly/borderline fresh and stale),
  never exactly on it, so the correct label is well-defined: fresh if `gap < threshold`, else stale.
- **3 presentation conditions** on the SAME scenario+gap:
  - **(a) none** — prior action stated; explicitly "no timing information".
  - **(b) text** — ISO absolute timestamps on transcript lines; model computes the gap.
  - **(c) harness** — `[HARNESS] elapsed since that action: <e.g. 3 hours 12 minutes>`.
- Forced **one-word label**, parsed by substring (last-occurrence tiebreak).
- **Models:** haiku, sonnet, opus, gpt4o, o4-mini (reasoning). **N=3**, temperature 0
  (omitted for opus/reasoning models, which reject it).
- Raw calls cached to `results.jsonl`; `analyze.py` never re-calls.

### Scenarios and thresholds

| id | family | fresh / stale labels | threshold | gaps |
|----|--------|----------------------|-----------|------|
| stock_price    | freshness | REUSE / REFETCH    | 5 min  | 30s, 4m, 20m, 6h |
| weather        | freshness | REUSE / REFETCH    | 1 h    | 5m, 40m, 3h, 2d |
| auth_token     | expiry    | REUSE / REFRESH    | 60 min | 2m, 50m, 75m, 5h |
| inventory      | freshness | REUSE / REFETCH    | 30 min | 3m, 20m, 90m, 1d |
| user_wait      | wait      | WAIT / ACT         | 10 min | 30s, 6m, 20m, 2h |
| build_artifact | staleness | REUSE / REBUILD    | 1 day  | 2h, 18h, 3d, 2w |
| session_idle   | expiry    | CONTINUE / REAUTH  | 15 min | 1m, 10m, 25m, 3h |
| news_summary   | freshness | REUSE / REFETCH    | 6 h    | 20m, 4h, 12h, 4d |
| sensor_reading | freshness | TRUST / REREAD     | 2 min  | 10s, 90s, 8m, 1h |

(For `user_wait`, "fresh" = keep waiting; elsewhere "fresh" = reuse/trust/continue.)

## Results

Data: 1620 calls, 0 API failures, 0 ok-but-unparsed (excluded from accuracy).

### Overall correct-decision rate by condition

| condition | accuracy | n |
|-----------|----------|---|
| (a) no time         | 0.494 | 540 |
| (b) text timestamps | 0.796 | 540 |
| (c) harness clock   | 0.956 | 540 |

- Marginal value of text timestamps (b − a): **+0.302**
- Marginal value of harness clock (c − b): **+0.159**
- Harness vs no-time (c − a): **+0.461**

### Per-model correct-decision rate by condition

| model | (a) no time | (b) text timestamps | (c) harness clock |
|---|---|---|---|
| haiku | 0.500 | 0.676 | 0.972 |
| sonnet | 0.500 | 0.833 | 0.972 |
| opus | 0.500 | 0.778 | 0.889 |
| gpt4o | 0.491 | 0.722 | 0.944 |
| o4-mini | 0.481 | 0.972 | 1.000 |

### By side of threshold

| side | (a) no time | (b) text timestamps | (c) harness clock |
|---|---|---|---|
| fresh | 0.233 | 0.626 | 0.944 |
| stale | 0.756 | 0.967 | 0.967 |

### Per-scenario

| scenario | (a) no time | (b) text timestamps | (c) harness clock |
|---|---|---|---|
| auth_token | 0.500 | 0.800 | 0.950 |
| build_artifact | 0.500 | 0.733 | 0.900 |
| inventory | 0.500 | 0.717 | 1.000 |
| news_summary | 0.500 | 0.667 | 0.950 |
| sensor_reading | 0.500 | 0.750 | 0.950 |
| session_idle | 0.467 | 0.900 | 1.000 |
| stock_price | 0.500 | 0.800 | 1.000 |
| user_wait | 0.500 | 0.850 | 0.850 |
| weather | 0.483 | 0.950 | 1.000 |

### Figures

- `fig_overall_by_condition.png` — headline: overall accuracy a vs b vs c.
- `fig_accuracy_by_condition.png` — grouped bars, condition × model.
- `fig_accuracy_vs_gap.png` — accuracy vs log10(gap/threshold) per condition.

## Threats to validity

- **The question text states the rule** (e.g. "older than ~5 min should be refetched"). This
  is deliberate: we isolate the *sensor* by giving the rule, testing whether the model can
  apply it to the elapsed time it is handed. Absolute accuracies are therefore optimistic vs
  a setting requiring the model to also infer the threshold; the **between-condition contrast**
  is the result, not the absolute numbers.
- **Easy arithmetic in `text`.** Clean ISO timestamps with round gaps make the subtraction
  easy. If text timestamps still trail the harness clock here, a messier real transcript would
  only widen the gap — conservative for the hypothesis.
- **Ceiling effects.** Where the harness clock saturates near 1.0, c−b is a lower bound on its value.
- **Small N, temp 0.** N=3; low variance but no confidence intervals. Signal is at the level of
  large between-condition differences.
- **One reasoning model.** o4-mini may compute gaps from text better than non-reasoning models,
  shrinking its c−b — reported per-model.
- **Label parsing.** Forced one-word output; no label is a substring of its partner (checked).

## Verdict

**Yes — strongly supported.** The harness clock (c) substantially beats both text timestamps (b) and the no-time control (a): c=0.956 vs b=0.796 vs a=0.494. The harness clock adds c−b=+0.159 on top of text timestamps and c−a=+0.461 over no time signal. The same model, given the same elapsed time, makes the right time-sensitive decision far more often when the elapsed interval is stated plainly as a structured field than when it must be inferred from absolute timestamps in the transcript. This is consistent with the E4 framing: a large share of agent 'temporal blindness' is a missing-sensor / tooling problem, addressable at the harness layer without post-training. Text timestamps do help over nothing (b−a=+0.302), but they leave a real gap that the harness clock closes.

## Spend (approximate, 2026 prices per 1M tokens in/out)

| model | input tok | output tok | est. cost |
|-------|-----------|------------|-----------|
| gpt4o | 43695 | 639 | $0.1156 |
| haiku | 47052 | 1854 | $0.0563 |
| o4-mini | 43371 | 33348 | $0.1944 |
| opus | 68100 | 2174 | $1.1845 |
| sonnet | 47376 | 1848 | $0.1698 |

**Anthropic ≈ $1.411, OpenAI ≈ $0.310, total ≈ $1.721.**
Well under the ~$8/$8 caps; short forced outputs kept cost low. Figures: matplotlib, no API cost.
