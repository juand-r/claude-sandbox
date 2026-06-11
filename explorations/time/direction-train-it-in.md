# Direction: Train the Clock In (the sensor is a ceiling, not the destination)

*Counterpoint to `SUMMARY.md`'s recommendation. This is a distinct research direction, not a
revision of the four scoping experiments.*

## Thesis

The scoping experiments concluded "LLMs have no internal clock, so give them one" (E4's
harness-injected elapsed-time field lifts time-sensitive decisions 0.49 → 0.96). That is the
cheap, deployable answer. But it answers the wrong question if the goal is understanding.

**The absence of an internal clock is the reason to train one in, not a reason to route
around it.** Reframe E4 not as the solution but as the **ceiling**: it tells us what a perfect
elapsed-time sensor buys (0.96). The research question is then:

> How much of that sensor's benefit can a model **internalize** through post-training, so it
> behaves time-aware *without* the explicit field?

This turns a plumbing result into a capability result. Both outcomes are informative:
- **Model reaches the ceiling without the sensor** → temporal awareness is a learnable skill;
  the sensor was a shortcut. Directly contradicts TicToc's "post-training alignment is needed,
  and prompting/timestamps are not enough" framing by *doing* the post-training.
- **Model plateaus below the ceiling** → you have **quantified the irreducible value of the
  sensor** — a precise, publishable claim about what tooling buys over training.

## Three trainable targets

In rough order of tractability. Targets 1–2 are lane-2 (self-perception); target 3 is lane-3
(agency) and is where the sensor/ceiling comparison is cleanest.

### Target 1 — Output-length / step-count self-estimation
The latent skill already exists (E2: token-space ρ 0.889) with a clean, fixable defect: a
systematic ~2× undershoot, and total collapse on reasoning models that don't count their
hidden tokens. **Train to remove the bias and to make reasoning models account for their own
reasoning length.** This is the most well-posed target — output length is a property of the
model's own policy, fully determined by what it does.

### Target 2 — Wall-clock seconds, in a fixed environment
Earlier dismissed as ill-posed; that was wrong (see `SUMMARY.md` correction). Within a fixed
deployment, `latency ≈ length(prompt) × sec_per_token_here + overhead_here`, and E1 measured
the residual noise floor at **CV 0.04–0.14** — the seconds target is reproducible enough to
fit. Post-training in-environment pins the two constants; Target 1 supplies `length`.
- **Caveat that defines the experiment:** the predictor is deployment-specific (re-calibrate
  on drift), and reasoning models add stochastic hidden-token variance a fixed constant can't
  absorb. Treat reasoning vs non-reasoning as separate regimes.
- **Success = approaching the CV floor on held-out tasks**, not zero error. The CV *is* the
  best-case RMSE-fraction; beating it is impossible by construction, so the floor is the
  target.

### Target 3 — Agentic time-attention (the sensor/ceiling comparison)
Train the model to attend to elapsed time encoded in a transcript (text timestamps) and make
correct stale/fresh / act-wait decisions **without** the explicit elapsed field. E3 shows the
raw capability is graded by model strength (opus 9/9 scenarios, haiku 5/9) and that when
models do attend they are calibrated (0.80–0.93) — so the deficit is *attention*, which is
exactly the kind of thing post-training fixes.

## Training / eval design

### Data
- **Self-estimation (Targets 1–2):** auto-generated. Run a task distribution, log
  `(prompt, output_tokens, latency_s)` triples in the target environment — this is literally
  what E1/E2's `run.py` already produces. Labels are free and exact; no human annotation. Hold
  out tasks by *type* (train on short/medium, test on long, and vice versa) to test
  generalization rather than memorization of specific prompts.
- **Time-attention (Target 3):** extend E3's generator — it already parameterizes
  `(scenario, gap, threshold)` and holds the transcript fixed while varying only the gap. Scale
  from 9 scenarios to a few hundred across more domains and threshold scales; this is the
  training set. **Critically, hold out whole scenario families and whole threshold regimes** so
  the eval tests transfer of "read the clock and compare to a learned rule," not memorized
  thresholds. E3's single-variable manipulation is the clean held-out probe.

### Method
- Start with the cheapest intervention that could work and escalate only if it doesn't:
  **few-shot / in-context calibration → LoRA/PEFT → full fine-tune.** Much of Target 1's bias
  may close with a calibration head or even few-shot anchors; don't reach for RL first.
- For Target 3, supervised fine-tuning on `(timestamped transcript → correct decision)` is the
  obvious baseline; only move to reward-model / RL (the doc's original "feedback loop" sketch,
  or RAGEN-style) if SFT plateaus below the ceiling.

### The headline comparison (per target, per model)
Three conditions, same held-out eval:
| condition | what it measures |
|---|---|
| **base** (no training, text timestamps) | starting point — E3's numbers |
| **trained** (post-trained, text timestamps, no sensor) | how much was internalized |
| **sensor ceiling** (no training, explicit elapsed field) | E4's numbers = the ceiling |

**Internalization fraction = (trained − base) / (ceiling − base).** This single number is the
deliverable. Report it per model — the prediction from current data is that it will be
*highest for weak models* (haiku, gpt4o), since the sensor substitutes for capability the
strong models already have, so there's more room to internalize.

### Metrics
- Targets 1–2: Spearman ρ and geometric-mean ratio vs actual (reuse E1/E2's `analyze.py`),
  plus distance-to-CV-floor for Target 2. Separate reasoning vs non-reasoning regimes.
- Target 3: correct-decision rate and E3's **sensitivity** (does the decision respond to the
  gap at all) vs **correctness** (right threshold) split — training should move sensitivity
  first.

## Risks and controls

- **Emergent misalignment** (flagged in the seed doc, arXiv 2502.17424): narrow fine-tuning
  can shift unrelated behavior. Budget a small general-capability + behavior eval before/after
  any fine-tune. Cheap, non-optional.
- **Environment drift (Target 2):** the wall-clock predictor is only valid for the deployment
  it was trained on. Monitor the live latency CV; re-calibrate when it moves. Don't ship a
  cross-environment claim.
- **Contamination / memorization:** hold out by task type and scenario family, not random
  split, or you measure memorization. (Cf. Test-of-Time's contamination-controlled design.)
- **Reasoning-model variance (Targets 1–2):** their latency depends on stochastic hidden
  reasoning length unknown at predict-time. Expect a wider achievable floor; predict a
  distribution, not a point, and score accordingly.

## First concrete step

Cheapest experiment that tests the thesis, reusing existing infra:
1. Take E3's generator, scale to ~200 scenarios, hold out 3 families + the extreme-threshold
   regime.
2. SFT (LoRA) one weak model (e.g. haiku-class) and one strong model on text-timestamp
   transcripts → correct decision.
3. Evaluate base / trained / sensor-ceiling on the held-out probe; report the internalization
   fraction per model.

If weak models internalize most of the sensor's gap from pure SFT, the project's thesis flips
from "give it a clock" to "**a clock is learnable, and here's how much**" — the more
interesting result, and the one this direction exists to get.
