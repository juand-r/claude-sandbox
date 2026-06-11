# E6 — Length-Estimation Bias Correction: Can In-Context Fixes Close the Undershoot?

**Lane:** time self-perception (lane 2). Cheap tractability test for Target 1 of
`direction-train-it-in.md`.

## Hypothesis

E2 found a systematic ~2× undershoot when models predict their own output-token count. E6
asks whether that bias closes with **in-context** interventions — no fine-tuning. If yes,
Target 1 (length self-estimation) is nearly free.

## Setup

10 output-length-varying tasks (one word → 600-word essay). For each (model × task × 3
trials): one generation (actual output tokens) plus three estimate conditions:
- **bare** — predict output tokens, no help. [E2 baseline]
- **anchors** — predict after a few-shot table of token-count calibration anchors.
- **self_revise** — predict, then "models under-estimate; adjust", then output `FINAL: <n>`.

Models: haiku, sonnet, opus, gpt4o-mini, gpt4o, o4-mini. 720 calls, N=3. Metric:
gm(predicted/actual tokens) — 1.0 is perfect, <1 undershoot — and Spearman ρ. Figure
`ratio_by_condition.png`.

## Results

**In-context calibration substantially closes the bias, while correlation stays high.**

| condition | pooled gm(pred/act) | vs bare | pooled ρ |
|---|---|---|---|
| bare | 0.37 | — | 0.842 |
| anchors | 0.55 | +0.18 | 0.861 |
| **self_revise** | **0.76** | **+0.39** | 0.825 |

- **bare confirms (and exceeds) the E2 undershoot:** gm 0.37 ≈ a 2.7× underestimate of own
  output length. The ordering is already good (ρ 0.84) — it is a *scale* error, not a ranking
  error, exactly as E1/E2 argued.
- **self-revision recovers most of the gap** (0.37 → 0.76) without hurting ρ. Just telling the
  model "you tend to under-count, reconsider" moves calibration ~2× closer to truth.
- **anchors help less** (0.55) — a static reference table is weaker than making the model
  reason about its own verbosity.

**Per-model is where the nuance lives** (self_revise gm):

| model | bare | self_revise |
|---|---|---|
| opus | 0.40 | 0.82 |
| sonnet | 0.46 | 0.78 |
| gpt4o | 0.46 | 0.69 |
| gpt4o-mini | 0.52 | 1.08 |
| haiku | 0.64 | **2.01 (overshoot)** |
| o4-mini | 0.08 | **0.19 (still stuck)** |

- **Strong models land near 1.0** under self-revision (opus 0.82, sonnet 0.78) — clean fix.
- **Weak models over-correct:** haiku swings from 0.64 undershoot to 2.0× *overshoot* — the
  "adjust upward" nudge is too blunt for it. A calibrated correction needs to be model-aware,
  not a one-size instruction.
- **o4-mini stays broken** (0.08 → 0.19): a reasoning model cannot count tokens it spends on
  hidden reasoning, and no prompt fixes that. Same boundary as E1/E2/E5.

## Interpretation

The output-length undershoot is **mostly an in-context-fixable calibration error for
non-reasoning models** — self-revision alone takes pooled calibration from 2.7× off to ~1.3×
off, keeping the already-good ranking. That is a meaningful, cheap result for the "train it
in" program: **Target 1 may not need training at all** for non-reasoning models; a
self-revision step (tuned per model to avoid overcorrection, e.g. a learned scalar rather than
"adjust up") gets most of the way.

Two boundaries remain, and they are the same boundary E5 drew:
1. **Reasoning models** (o4-mini) — hidden tokens are invisible to the model, so neither
   anchors nor self-revision help. This is the part that genuinely needs a different
   mechanism (train the model to predict its own reasoning budget, or read it from the
   harness).
2. **Overcorrection on weak models** — argues for a fitted correction (a per-model bias
   constant, trivially learned from a handful of calibration examples) rather than a verbal
   nudge.

## Threats to validity

- Same output-length-dominated task family as E1/E2 — by design (this is where the undershoot
  lives). Says nothing about latency the model can't see (that's E5's domain).
- `self_revise` parsing relies on a `FINAL:` line; fell back to last-number when absent
  (parsed cleanly here).
- gm pooled across heterogeneous models hides the over/under-correction split — hence the
  per-model table is the real result.
- N=3.

## Verdict

Hypothesis **largely supported.** A self-revision prompt closes most of the ~2.7× length
undershoot (pooled gm 0.37 → 0.76) while preserving ranking (ρ ≈ 0.83), and strong models land
near perfect calibration. Implication for `direction-train-it-in.md`: **Target 1 is nearly
free for non-reasoning models via a fitted in-context correction; fine-tuning effort should be
reserved for the reasoning-model hidden-token problem (the E10 probe) — the one place
in-context fixes fail.**

## Spend (approximate)

~$1–2 (short outputs; opus and o4-mini dominate).
