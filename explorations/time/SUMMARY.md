# Time Project — Cross-Experiment Synthesis

Four scoping experiments, run on a shared roster (haiku, sonnet, opus, gpt4o-mini, gpt4o,
and a reasoning model gpt5.2/o4-mini), API-only, no training. Full method/results per
experiment in each `eN-*/REPORT.md`. This is the synthesis and the recommendation.

## One-line findings

| Exp | Question | Result |
|---|---|---|
| **E1** | Can a model estimate its own wall-clock generation time? | **It has no clock — it has an output-length estimator.** Predicts latency well *when latency is length-driven* (ρ up to 0.94, ordering up to 0.95), contradicting the "4–7× overshoot / chance" literature *for this regime*. Breaks for reasoning models (gpt5.2 ratio 0.32×, hidden tokens). |
| **E2** | Is length-space better than second-space? | **Yes.** Token-space estimates beat seconds (pooled ρ 0.889 vs 0.657, Δ+0.231) and are far more consistent across models. Confirms E1's mechanism. Caveat: models under-predict their own length ~2×; reasoning first does not help. |
| **E3** | Are agents blind to timestamp gaps in a transcript? | **Graded, not blind.** Sensitivity scales with model strength (opus 9/9 scenarios → haiku 5/9); when models *do* read the clock they are well-calibrated (0.80–0.93). The deficit is **inconsistent attention**, not bad judgment. |
| **E4** | Does a harness-injected elapsed-time field beat text timestamps? | **Yes, decisively.** Correct decisions: no-signal **0.49** → text timestamps **0.80** → harness clock **0.96**. Biggest lift on weaker models. |

## The unifying story

The four experiments split cleanly into two lanes, and they tell **one coherent story**:

> **LLMs do not have an internal clock. They have a length estimator and they respond to
> time only when it is handed to them explicitly.**

- **Lane 2 (self-perception, E1+E2):** what looks like temporal self-awareness is really
  *output-length anticipation*. Models rank and roughly size their own generations, and that
  proxies wall-clock latency whenever latency is length-dominated. There is no clock
  underneath — the moment latency hides in unseen reasoning tokens (reasoning models), the
  proxy collapses. The literature's "temporal blindness" is real but **regime-specific**: it
  shows up exactly where output length stops predicting time.

- **Lane 3 (agency, E3+E4):** in multi-turn settings the same absence of an internal clock
  means agents only act on elapsed time when it is **explicit and loud**. Burying timestamps
  in text gets you partway (0.80) because strong models can do the arithmetic; a plainly
  stated elapsed-time field from the harness gets you almost all the way (0.96). The gap
  between 0.49 and 0.96 is almost entirely a **missing-sensor problem**, not a
  missing-capability problem.

The two lanes agree: **don't try to train a clock into the model — give it one.**

## Recommendation: which lane to commit to

**Commit to Lane 3 (time-aware agency).** Rationale:

1. **It has the actionable lever.** E4 shows a large, cheap win (≈+0.46 absolute decision
   accuracy) from a harness-layer change — no fine-tuning, no post-training. That is a
   deployable result, and it directly challenges TicToc's "post-training alignment is needed"
   conclusion: a lot of the gap is closable with a sensor.
2. **E3 is a clean, novel diagnostic.** The single-variable gap manipulation (hold transcript
   fixed, vary only the gap) cleanly separates *reading the clock* from *reasoning about it* —
   something the existing benchmarks (TicToc, TimeBench) conflate. It is publishable as-is and
   extends naturally (more scenarios, multi-turn, tool-latency).
3. **Lane 2 is the scientific framing, not the product.** E1+E2 are the better *paper*
   (they reframe a published negative result and explain it mechanistically), but the
   practical knob is small — you cannot easily make a model's wall-clock self-estimate useful
   because wall-clock isn't a function of its inputs. Keep E1/E2 as the motivating "why":
   *models have no clock, so the agency fix must supply one externally.*

**Concrete next step.** Merge E3 + E4 into one harness study: take E3's low-sensitivity
models and scenarios, add E4's explicit elapsed-time field, and measure how much of the
sensitivity gap the sensor closes per model. Hypothesis from the current data: the harness
clock should lift the weak models (haiku, gpt4o) the most — i.e., the sensor substitutes for
the capability the strong models already have. If that holds, the project's thesis is settled:
**temporal awareness in agents is a tooling problem with a one-line fix, and the residual is
the part worth post-training.**

## Correction: wall-clock seconds *is* trainable in a fixed environment

An earlier draft of this doc claimed wall-clock self-prediction is ill-posed because latency
"isn't a function of the inputs." **That was overstated.** It only holds if you marginalize
over all hardware/load/batch states. Condition on a *fixed deployment* (this model, this
hardware, typical load) and `P(seconds | prompt, environment)` is tight with a learnable
mean — the environment is just a constant that post-training absorbs into the weights. This
is how a human develops "a sense of how long things take here."

E1's own data supports the corrected view: the median CV of actual latency across trials was
only **0.04–0.14** in this sandbox — i.e., the seconds target was already highly reproducible.
What wrecked pooled calibration in E2 was cross-model scale error and the model's own
miscalibration, **not** environmental noise. So the decomposition is
`latency ≈ length(prompt) × sec_per_token_here + overhead_here`: E2 shows the model can
estimate `length`; in-environment post-training pins the two constants. The real (narrower)
caveats: the predictor is **deployment-specific** (re-calibrate on drift), the achievable
floor equals the per-prompt latency variance in that environment (measurable — it's the CV),
and **reasoning models** add stochastic hidden-token variance a fixed constant can't absorb.
The full alternative direction is written up in `direction-train-it-in.md`.

## What NOT to chase (yet)

- Training a model to predict wall-clock seconds in a way that **transfers across
  environments** from the prompt alone — *that* is ill-posed (the cross-environment target
  isn't a function of the inputs). The fixed-environment version above is fine.
- Extending TimeBench-style *text* temporal reasoning — saturated, and orthogonal to the
  agency deficit that actually bites in deployment.

## Caveats spanning all four

- Small N (3 trials), modest scenario/task counts — trends are clear, tails are thin.
- Forced one-word decisions (E3/E4) and integer-second estimates (E1) are lower bounds on
  capability; real agents reason more.
- Absolute wall-clock numbers (E1) are harness/hardware specific; the rank/correlation and
  between-condition contrasts (E2/E3/E4) are the robust results.
- Prompts in E3/E4 state the staleness rule, isolating the *sensor* from threshold
  *knowledge* — between-condition deltas are the result, not absolute accuracies.

## Spend

Approx final-data estimates: **~$4–5 Anthropic + ~$1 OpenAI** total across all four (opus and
the reasoning models dominate). Actual spend was somewhat higher due to re-runs and a
concurrent-writer bug that produced duplicate rows (deduped out before analysis), but still
well within the $50/$50 budget.

## Process note

The four data-collection agents each bailed early (launched collection in the background,
ended their turns expecting to be re-woken), leaving orphaned `run.py` processes that the
orchestrator's resumes then raced — producing duplicate rows in E4 and E2. Root cause: the
append-only + `load_done()` resume scheme is **not safe against concurrent writers**. Fixed
by killing all writers, deduping on the logical key, and finishing each model as a single
writer. Documented here so the next run uses a file lock or a single coordinator process.
