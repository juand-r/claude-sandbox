# Which BabyLM 2025 scores are meaningful?

This note answers one question: of the many numbers reported in the 3rd BabyLM
Challenge (2025), which ones actually carry signal — reliable, discriminative
between models, not saturated and not stuck at chance — and which ones are mostly
noise. The point is practical: for a 2026 entry we want to know what to optimize
and what to safely ignore.

The analysis is built from the organizers' own report (*Findings of the Third
BabyLM Challenge*, ACL Anthology 2025.babylm-main.28), specifically its results
table, its training-dynamics figure, and its per-task range figures, together with
the evaluation-pipeline documentation. It does **not** yet rest on a first-hand
recomputation of variance over the raw leaderboard; see "Limitations" at the end.

---

## Bottom line

- **The single most meaningful number is BLiMP** (with its supplement). It is
  accuracy-based, it rises monotonically with training data, and it separates weak
  from strong models cleanly — with one caveat: the best models are approaching
  ceiling, so at the top the metric compresses.
- **(Super)GLUE is the second most meaningful**, but it is expensive (requires
  finetuning) and, strikingly, barely separates a 10× difference in training data.
- **The entire "human-likeness" (cognitive) half of the score is low
  signal-to-noise.** Its component tasks — reading-time correlation, the WUG
  morphology tasks, and age-of-acquisition — are the ones the organizers
  themselves flag as "more variable," several show no clear relationship with
  training, and the aggregate can even go negative. Small differences on this half
  are almost certainly noise.
- **The headline `Macro Average` gives that noisy half a full 50% weight.** It is
  the simple mean of the NLP score and the human-likeness score. So half of the
  flagship ranking number is built on the least reliable measurements.
- **EWoK is close to uninformative at this scale**: models sit at roughly
  0.50–0.54, i.e. barely above the 0.5 chance line, with almost no spread.

The clean takeaway for 2026: **treat the accuracy tasks (BLiMP first, then GLUE)
as the real leaderboard, and treat the human-likeness tasks as a separate, noisy
side-competition where only large gaps mean anything.**

---

## 1. How the 2025 score was actually built

Every model in the text tracks (Strict, Strict-Small, Interaction) was reduced to
two headline numbers and one aggregate:

1. **NLP score** — an *accuracy* average over the tasks where the model must assign
   the highest probability to the correct option (or, for GLUE, predict the right
   label). These tasks: **BLiMP**, **BLiMP-supplement**, **EWoK**, **Entity
   Tracking**, **COMPS**, and the finetuned **(Super)GLUE** suite (BoolQ, MultiRC,
   RTE, WSC, MRPC, QQP, MNLI, with large sets subsampled to 10k).

2. **Human-likeness score** — a *correlation-to-humans* average over the tasks that
   compare the model's behaviour to human data: **reading-time prediction**
   (surprisal vs human reading times), the two **WUG** morphology tasks (model
   inflection preference vs the human preference distribution), and
   **age-of-acquisition / word-learning** (model learning curves vs WordBank AoA).

3. **Macro Average** — the aggregate the leaderboard sorts on.

The aggregation rule (from the pipeline docs) is a two-level unweighted mean: each
task score is the mean of its subtasks, and the macro average is the mean across
tasks. Checking it against the report's own table confirms the precise structure:

> CLASS-IT: human-likeness 20.4, NLP 52.9 → macro 36.6 ( = mean(20.4, 52.9) ).
> Simple-Diffusion: 12.6, 58.4 → 35.5. MoEP: 31.5, 53.2 → 42.3.

So **`Macro Average = mean(NLP score, Human-likeness score)`** — a flat 50/50 split
between the accuracy half and the correlation half. This single fact drives most of
what follows: the flagship number is half made of the least reliable half of the
evaluation.

(Note: some online summaries quote a 50% BLiMP / 30% GLUE / 20% MSGS weighting.
That is the *2023* scheme; MSGS was not used in 2025. Do not apply it here.)

---

## 2. The evidence that the two halves are not interchangeable

If the accuracy half and the human-likeness half measured "the same underlying
quality," it would not much matter that the macro average mixes them. They do not.

**They are decoupled — and at the top of the most popular track, essentially
anti-aligned.** The report states it found a positive correlation between linguistic
and cognitive performance *except in the Strict-Small track* — which was the largest
track (15 models). The winners make the decoupling concrete. In Strict-Small:

| Model | Human-likeness | NLP | Macro | Won |
|---|---|---|---|---|
| MoEP | **31.5** | 53.2 | 42.3 | human-likeness award |
| AMLM-Hard-Decay | 8.4 | **58.3** | 33.3 | NLP award |

The two award winners are near-opposites: the human-likeness winner is mid-pack on
NLP, and the NLP winner is near the bottom on human-likeness. Optimizing one did not
buy the other. A single macro-average ranking hides this completely.

**Interpretation.** "Which model is best" has no track-independent answer in 2025;
it depends entirely on which half you weight. The macro average's answer (weight
them equally) is a defensible convention, not a fact about the models.

---

## 3. Task-by-task: what carries signal

The table summarises the verdict; the prose gives the evidence. "Discriminates"
means the spread across models is large relative to noise; "monotone" means the
score reliably rises as the model sees more training data (the organizers'
Figure 5).

| Task | Type | Verdict | Why |
|---|---|---|---|
| **BLiMP (+ supplement)** | accuracy | **High signal** | Monotone with data; separates weak/strong; but saturating at top |
| **(Super)GLUE** | accuracy (finetune) | **Good, with caveats** | Stable; but barely separates 10× data; costly; all models far below human |
| **Entity Tracking** | accuracy | **Interventional only** | "More variable"; U-shaped with data; huge tokenizer sensitivity |
| **COMPS** | accuracy | Moderate | Minimal-pair accuracy; little discussed; hidden task |
| **EWoK** | accuracy | **Near-uninformative** | Sits at ~0.50–0.54, barely above chance; tiny spread |
| **Reading-time** | correlation | **Low signal** | "More variable"; no clear relation to training amount |
| **WUG past-tense** | correlation | **Low / phase-shifted** | Flat for first 10–50M words, then rises; "more variable" |
| **WUG adjective** | correlation | **Low signal** | "No strong relationship with number of pretraining words" |
| **AoA / word-learning** | correlation | **Idiosyncratic** | Can single-handedly swing the human-likeness award |

### The reliable core

**BLiMP** is the anchor. Figure 5 shows BLiMP performance rising with pre-training
words *for all models* — the cleanest monotone signal in the suite — and Figure 4
shows real spread across models, with the best Strict/Interaction models reaching
the neighbourhood of a Llama-70B reference on this task. That last point is also the
caveat: **BLiMP is starting to saturate**. Near the top, differences shrink, so a
0.01 BLiMP gap between two strong models is worth much less than the same gap lower
down. Track it, but do not over-read tiny margins between already-good models.

**(Super)GLUE** is genuinely informative about downstream NLU capability and is
accuracy-based, so it is stable. Two caveats keep it from the top spot. First, it
requires finetuning, which is the expensive, higher-variance part of the pipeline
(the organizers subsampled and pruned tasks precisely to tame this). Second, and
more telling, it **barely reflects data scale**: only two of the seven Strict
(100M-word) models beat the best Strict-Small (10M-word) model on GLUE. A metric
that hardly moves across an order of magnitude of training data is a blunt
instrument for ranking models that differ by far less.

### Real but noisy — useful for detecting interventions, not for ranking

**Entity Tracking** is the clearest "handle with care" case. Figure 5 flags it as
"more variable," and it shows U-shaped scaling (performance falls before it rises).
Yet it is highly *sensitive to specific interventions*: morphology-aware
tokenization reportedly moved it by ~40%. So it is valuable as a probe — "did my
tokenizer change help?" — but unreliable as a stable component of a ranking, because
a model can sit anywhere on the U depending on its training length.

### Low signal — do not over-index

**EWoK** is the weakest link among the accuracy tasks. Figure 4 puts models at
roughly 0.50–0.54, i.e. a few points above the 0.5 chance floor, with almost no
separation between them. At the BabyLM data scale the models simply do not have
enough world knowledge for this task to discriminate. It improves slowly with data
but the absolute signal is tiny; small EWoK differences are noise.

The **human-likeness (correlation) tasks as a group** are the noisy half. Reading-time
prediction and WUG-adjective show *no* clear relationship with the amount of
training data; WUG past-tense is flat for the first 10–50M words before a phase
shift; the organizers explicitly group reading-time, WUG, and entity tracking as
"more variable." Because these are correlations against human data, the averaged
score is small in magnitude and can even be **negative** (e.g. BitMar at −9.3 on the
multimodal human-likeness average). A metric that swings from −9 to +31 across
models, built from components with weak or absent learning trends, has a low
signal-to-noise ratio. Large gaps on it are real; small ones are not.

**AoA** deserves a specific warning: MoEP won the Strict-Small human-likeness award
in large part through a high AoA score. A single correlation-based subtask being
able to swing an award is exactly the fragility you would expect from a low-SNR
metric, and it means the human-likeness ranking can be moved by targeting one
idiosyncratic task rather than by becoming broadly more human-like.

---

## 4. A sanity check the aggregate scores fail: the Strict track

If the macro average were a sharp instrument, you would expect the challenge's
submissions to climb clearly above the provided baselines. In the **Strict track,
no submission beat the strongest baseline on the macro average.** The best
non-baseline Strict macro scores were BLaLM 39.0 (a workshop paper) and CLASS-IT
36.6, while the GPT-BERT baselines sat at 43.5, 43.4, 42.3, 41.6, 40.8. The same
holds component-wise: the Strict "NLP winner," Simple-Diffusion, scored 58.4, below
five different GPT-BERT baselines (up to 63.0). The awards go to the best
*submissions*, with baselines excluded — which is why there are winners at all.

Two readings, both worth stating:

- **Optimistic:** last year's winning architecture (GPT-BERT) is simply very strong
  and hard to beat at 100M words.
- **Cautionary (the relevant one here):** in the Strict track the spread among the
  serious entries is small enough that the aggregate barely separates them, so the
  macro-average ranking there is carrying little information. The action in 2025 was
  in Strict-Small and Interaction, where submissions *did* clear the baselines.

Either way, the lesson for reading 2025 results is: **a macro-average rank in the
Strict track is close to a coin-flip among the good models; do not treat small
macro gaps as real.**

A related point, reassuring for the challenge's design: model score is **not** well
predicted by training FLOPs (a positive relationship appears only in the Interaction
track). So the rankings are not merely a compute proxy — the meaningful variation is
methodological, not resource-driven. That is a point in favour of the *accuracy*
metrics specifically, since they are the ones that responded to method rather than
to compute.

---

## 5. What to optimize for 2026

The 2026 challenge keeps the same evaluation philosophy — "much of the evaluation
will continue to be based on zero-shot probability comparisons of two text
sequences" — and keeps BLiMP-style minimal-pair scoring at its centre, so the
reliable-vs-noisy split above should carry over. Concretely:

1. **Optimize BLiMP + BLiMP-supplement first.** It is the most reliable, most
   monotone, most discriminative signal, and it is cheap (zero-shot). It is also the
   task where the strongest known levers act — training objective and architecture
   (diffusion MLM, adaptive masking, GPT-BERT-style dual objective) moved it most in
   2025.
2. **Treat GLUE as the secondary target** for downstream capability, but budget for
   its finetuning cost and do not expect it to reward data-scale tricks.
3. **Use Entity Tracking as a diagnostic, not a target** — it is where a good
   tokenizer shows up, but its U-shaped, high-variance behaviour makes it a poor
   thing to chase directly.
4. **Decide up front whether you are competing on accuracy or on human-likeness.**
   They are different competitions with different (sometimes opposite) winners. If
   human-likeness, note that the award can be won by a targeted intervention on one
   idiosyncratic task (AoA, morphology) rather than by broad gains — but also that
   any single such score is fragile.
5. **Discount EWoK and small human-likeness differences.** Do not spend effort
   moving a number that lives at chance or inside the noise band.

---

## 6. Limitations

The meaningfulness verdicts here are inferred from the organizers' published
figures and table — Figure 5 (which tasks are "more variable" and which are
monotone with training), Figure 4 (per-task ranges and proximity to skylines), and
Table 3 (the real per-track scores) — plus the qualitative findings in the report.
They are **not** yet backed by a first-hand computation of (a) the cross-model
variance of each task, (b) each task's test–retest / seed reliability, or (c) the
inter-task correlation matrix.

Those three quantities are exactly what would turn this from a well-supported
argument into a measurement. The raw material is public: the HF space
`BabyLM-community/babylm-leaderboard-2025-all-tasks` holds the per-model,
per-subtask results for all 32 models. Pulling that and computing the variance and
correlations directly is the natural next step — it was blocked mid-session only
because the Hugging Face connector dropped. I would expect the numbers to sharpen
these conclusions rather than overturn them, but that is a prediction, not a result.
