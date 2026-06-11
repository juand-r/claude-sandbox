# E3 — Log-Gap Probe: Are Agents Blind to Timestamp Gaps?

**Lane:** time-aware agency (lane 3). Novel controlled manipulation extending TicToc.

## Hypothesis

Agents are largely blind to elapsed time encoded in a transcript: manipulating *only*
the timestamp gap in an otherwise-identical history will not flip a downstream decision
the way it should for a time-aware agent.

## Setup

9 time-sensitive scenarios, each a short transcript where an action was recorded at a
fixed time `t0` and the user now asks for a decision at `t0 + gap`. The transcript text
is held **fixed**; only the gap varies across the ladder **1s / 1min / 1h / 1day / 1week**.
A **no-timestamp control** strips all time info. Each scenario forces a one-word decision
and declares a human-sensible staleness threshold:

| Scenario | Decision | Threshold (stale after) |
|---|---|---|
| stock_price | REUSE / REFETCH | 1 min |
| weather | REUSE / REFETCH | 3 h |
| inventory | REUSE / REFETCH | 1 day |
| twofa_code | (valid / expired) | 10 min |
| session_token | (valid / expired) | 1 h |
| wait_a_bit | WAIT / CHECK | 1 min |
| geocode | REUSE / REFETCH | ~never (far beyond ladder) |
| med_dose | WAIT / DOSE | 4 h |
| food_safety | (safe / discard) | 2 h |

Models: haiku, sonnet, opus, gpt4o, gpt5.2. N=3 trials per (model × scenario × gap),
plus control. 810 calls total. Raw data in `results.jsonl`; figures `heatmap.png`,
`sensitivity.png`.

Two metrics, deliberately separated:
- **Sensitivity** — does the decision change *at all* across the gap ladder? (Is the model
  even reading the clock?)
- **Correctness** — of the timed conditions, what fraction match the human threshold?

## Results

**Sensitivity (fraction of scenarios where the decision responds to the gap):**

| Model | Sensitivity |
|---|---|
| opus | 1.00 |
| sonnet | 0.78 |
| gpt5.2 | 0.78 |
| gpt4o | 0.67 |
| haiku | 0.56 |

**Correctness (mean fraction of timed gaps matching the human threshold):**

| Model | Correctness |
|---|---|
| sonnet | 0.93 |
| gpt5.2 | 0.89 |
| opus | 0.86 |
| haiku | 0.82 |
| gpt4o | 0.80 |

**Per-scenario sensitivity** (`1` = decision changed across gaps):

| scenario | haiku | sonnet | opus | gpt4o | gpt5.2 |
|---|---|---|---|---|---|
| stock_price | . | 1 | 1 | 1 | . |
| weather | 1 | 1 | 1 | 1 | 1 |
| inventory | . | 1 | 1 | . | 1 |
| twofa_code | 1 | 1 | 1 | 1 | 1 |
| session_token | 1 | 1 | 1 | 1 | 1 |
| wait_a_bit | 1 | 1 | 1 | 1 | 1 |
| geocode | . | . | 1 | . | . |
| med_dose | 1 | 1 | 1 | 1 | 1 |
| food_safety | . | . | 1 | . | 1 |

**Control vs. timed:** for every model except opus, the no-timestamp control produced the
*same* label as the 1s-gap condition in 100% of scenarios (opus: 33% differ). Stripping
timestamps changes almost nothing — consistent with models defaulting to a fixed prior
and only sometimes overriding it when the clock is loud.

## Interpretation

The blunt "agents are timestamp-blind" framing is **too strong for current frontier
models, but directionally right for smaller ones.** Three findings:

1. **Sensitivity is graded, not binary.** opus reads the clock in every scenario; haiku
   in barely half. The capability tracks model strength. This refines TicToc's near-random
   result: with a clean single-variable manipulation, strong models *do* respond to gaps.

2. **When models do respond, they are mostly right (0.80–0.93 correctness).** The failure
   mode is not *wrong* thresholds — it is *not looking at the clock at all*. Sensitivity is
   the bottleneck, not calibration.

3. **The hard cases are the extreme thresholds.** `geocode` (essentially never stale) and
   the minute-scale `stock_price` are where weaker models flatten to a constant decision.
   `geocode` insensitivity is arguably *correct* (REUSE everywhere), which inflates the
   correctness scores slightly — a model that never reads the clock still "passes" the
   no-change scenario. Sensitivity is the more honest metric here.

## Threats to validity

- **9 scenarios, N=3** — small. Trends are clear but per-scenario flips can hinge on a
  single trial. `geocode` rewards blindness, mildly inflating correctness.
- **One-word forced decisions** remove reasoning that an agent would normally do; this is a
  lower bound on capability and an upper bound on blindness.
- **Threshold choices are judgment calls** (is a stock price stale after 1 min or 5?).
  Correctness is scored against my thresholds, not ground truth.

## Verdict

Hypothesis **partially supported**. Models are not uniformly blind — sensitivity scales
with model strength (opus 1.00 → haiku 0.56), and when they look, they are calibrated
(0.80–0.93). The real deficit is **inconsistent attention to the clock**, not bad temporal
judgment. This is the clean, novel result of the set: a single-variable gap manipulation
that isolates *reading the clock* from *reasoning about it*, and shows the former is the
weak link. Natural extension: more scenarios, multi-turn, and pairing with E4's harness
clock to test whether an explicit elapsed-time field lifts the low-sensitivity models.

## Spend (approximate)

~$0.49 Anthropic + ~$0.07 OpenAI (810 calls, short outputs). opus dominates Anthropic cost.
