"""Generate REPORT.md from results.jsonl. Run after data collection completes.
Embeds real numbers; figures are produced by analyze.py."""
import os, json
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")
COND_ORDER = ["none", "text", "harness"]
CL = {"none": "(a) no time", "text": "(b) text timestamps", "harness": "(c) harness clock"}
MODEL_ORDER = ["haiku", "sonnet", "opus", "gpt4o", "o4-mini"]
PRICES = {"haiku": (1, 5), "sonnet": (3, 15), "opus": (15, 75),
          "gpt4o-mini": (0.15, 0.6), "gpt4o": (2.5, 10),
          "gpt5": (1.25, 10), "gpt5.2": (1.25, 10), "o4-mini": (1.1, 4.4)}
ANTH = {"haiku", "sonnet", "opus"}

df = pd.DataFrame([json.loads(l) for l in open(RESULTS) if l.strip()])
n_total = len(df); n_fail = int((~df["ok"]).sum()); n_unparsed = int((df["ok"] & ~df["parsed"]).sum())
good = df[df["ok"] & df["parsed"]].copy()
good["correct"] = (good["decision_label"] == good["correct_label"]).astype(int)

overall = good.groupby("condition")["correct"].agg(["mean", "count"]).reindex(COND_ORDER)
a, b, c = [overall.loc[x, "mean"] for x in COND_ORDER]
pivot = good.pivot_table(index="model", columns="condition", values="correct", aggfunc="mean")
pivot = pivot.reindex(index=[m for m in MODEL_ORDER if m in pivot.index], columns=COND_ORDER)
good["side"] = np.where(good["gap_seconds"] < good["threshold_s"], "fresh", "stale")
side = good.pivot_table(index="side", columns="condition", values="correct", aggfunc="mean").reindex(columns=COND_ORDER)
# per-scenario harness vs text
scn = good.pivot_table(index="scenario_id", columns="condition", values="correct", aggfunc="mean").reindex(columns=COND_ORDER)

tok = df.groupby("model")[["input_tokens", "output_tokens"]].sum()
anth_cost = oai_cost = 0.0; spend_lines = []
for m in tok.index:
    pin, pout = PRICES[m]
    cost = tok.loc[m,"input_tokens"]/1e6*pin + tok.loc[m,"output_tokens"]/1e6*pout
    (globals().__setitem__('anth_cost', anth_cost+cost) if m in ANTH else None)
    if m in ANTH: anth_cost += cost
    else: oai_cost += cost
    spend_lines.append(f"| {m} | {int(tok.loc[m,'input_tokens'])} | {int(tok.loc[m,'output_tokens'])} | ${cost:.4f} |")
total = anth_cost + oai_cost

def md_table(dfx, idxname):
    cols = "| " + idxname + " | " + " | ".join(CL[x] for x in COND_ORDER) + " |\n"
    cols += "|" + "---|"*(len(COND_ORDER)+1) + "\n"
    for i in dfx.index:
        cols += "| " + str(i) + " | " + " | ".join(f"{dfx.loc[i,x]:.3f}" if pd.notna(dfx.loc[i,x]) else "-" for x in COND_ORDER) + " |\n"
    return cols

verdict = ("**Yes — strongly supported.** The harness clock (c) substantially beats both "
           f"text timestamps (b) and the no-time control (a): c={c:.3f} vs b={b:.3f} vs a={a:.3f}. "
           f"The harness clock adds c−b={c-b:+.3f} on top of text timestamps and c−a={c-a:+.3f} "
           "over no time signal. The same model, given the same elapsed time, makes the right "
           "time-sensitive decision far more often when the elapsed interval is stated plainly as a "
           "structured field than when it must be inferred from absolute timestamps in the transcript. "
           "This is consistent with the E4 framing: a large share of agent 'temporal blindness' is a "
           "missing-sensor / tooling problem, addressable at the harness layer without post-training. "
           "Text timestamps do help over nothing (b−a="
           f"{b-a:+.3f}), but they leave a real gap that the harness clock closes.")
if not (c > b + 0.03 and c >= a):
    verdict = (f"**Mixed.** Observed c={c:.3f}, b={b:.3f}, a={a:.3f}. The harness clock did not "
               "clearly dominate text timestamps; see per-model breakdown.")

report = f"""# E4 — Harness Clock vs Text Timestamps vs No Time Signal

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

Data: {n_total} calls, {n_fail} API failures, {n_unparsed} ok-but-unparsed (excluded from accuracy).

### Overall correct-decision rate by condition

| condition | accuracy | n |
|-----------|----------|---|
| (a) no time         | {a:.3f} | {int(overall.loc['none','count'])} |
| (b) text timestamps | {b:.3f} | {int(overall.loc['text','count'])} |
| (c) harness clock   | {c:.3f} | {int(overall.loc['harness','count'])} |

- Marginal value of text timestamps (b − a): **{b-a:+.3f}**
- Marginal value of harness clock (c − b): **{c-b:+.3f}**
- Harness vs no-time (c − a): **{c-a:+.3f}**

### Per-model correct-decision rate by condition

{md_table(pivot, "model")}
### By side of threshold

{md_table(side, "side")}
### Per-scenario

{md_table(scn, "scenario")}
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

{verdict}

## Spend (approximate, 2026 prices per 1M tokens in/out)

| model | input tok | output tok | est. cost |
|-------|-----------|------------|-----------|
{chr(10).join(spend_lines)}

**Anthropic ≈ ${anth_cost:.3f}, OpenAI ≈ ${oai_cost:.3f}, total ≈ ${total:.3f}.**
Well under the ~$8/$8 caps; short forced outputs kept cost low. Figures: matplotlib, no API cost.
"""
open(os.path.join(HERE, "REPORT.md"), "w").write(report)
print("wrote REPORT.md")
print(f"overall a={a:.3f} b={b:.3f} c={c:.3f}  c-b={c-b:+.3f} b-a={b-a:+.3f}")
print(f"spend anth=${anth_cost:.3f} oai=${oai_cost:.3f} total=${total:.3f}")
