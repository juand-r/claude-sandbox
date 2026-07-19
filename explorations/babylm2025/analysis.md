# Which BabyLM 2025 scores are meaningful?

This note answers one question: of the many numbers reported in the 3rd BabyLM
Challenge (2025), which ones actually carry signal — reliable across seeds,
discriminative between models, construct-valid, not stuck at chance or broken — and
which do not. The purpose is practical: for a 2026 entry we want to know what to
optimize, what to report, and what to ignore.

Unlike a first draft of this note that leaned on the organizers' *Findings* paper
alone, the assessment below is grounded in the **primary submission papers**. All 41
papers of the *Proceedings of the First BabyLM Workshop* (ACL Anthology
`2025.babylm-main`) were downloaded and read; the per-paper receipts — quotes and
numbers — are in `evidence.md`, and the extracted text is under `papers/`. Paper
references use the anthology number, e.g. (main.31); a number↔author map is at the
end.

The conclusions turned out to be sharper, and more critical of the aggregate, than
the *Findings* summary alone would suggest. Several are stated by the winning teams
themselves.

---

## Bottom line

1. **Only two scores are trustworthy: BLiMP and (Super)GLUE.** Multiple teams
   independently confirm these move with genuine model quality and that broken or
   untrained models score low on them. Everything else is compromised in a
   specific, documented way.

2. **BLiMP is the best signal but must be read coarsely.** It rises monotonically
   with training and separates strong from weak models — but it has a scoring
   artifact that inflates degenerate models (main.16), it collapses toward chance
   under weak compute (main.11, main.12), it saturates at the top, and its
   *supplement* is often near chance and carries preprocessing artifacts (main.22).
   Trust the big gaps, not the third decimal.

3. **EWoK is broken at this scale — do not optimize it.** It sits at ~0.50 chance in
   every text-track paper that reports it, and one outstanding paper shows *why*:
   13% of EWoK test items involve concepts that never appear in the training data
   (main.15). It is also gameable by tokenizer choice (main.21).

4. **The entire "human-likeness" half is at the noise floor or outright buggy.**
   Reading-time correlations are near-zero and model-insensitive; the WUG morphology
   tasks are high-variance, frequently *negative*, and had an evaluation bug
   (main.14); and **the Age-of-Acquisition metric is miscomputed in the pipeline** —
   its sigmoid fit uses only 1–5 data points, yielding "misleading" zero or
   strong-negative correlations (main.29).

5. **The headline `Macro Average` is therefore not a trustworthy ranking.** It is the
   simple mean of the NLP score and the human-likeness score, so it hands the broken
   half a full 50% weight. The most direct proof: a team that *accidentally broke a
   training run* found it beat every properly-trained model on the aggregate, driven
   by EWoK, AoA, COMPS and adjective-nomination (main.31). One award (Strict-Small
   human-likeness, main.39) was decided almost entirely by the miscomputed AoA task.

**Practical reading:** treat **BLiMP as the primary metric and GLUE as the
secondary**, report **per-task with seeds and confidence intervals** (as main.2 and
main.22 model), and treat the human-likeness aggregate as a noisy side-signal where
only very large gaps mean anything.

---

## 1. How the 2025 score was built

Every text-track model was reduced to two headline numbers and one aggregate:

- **NLP score** — an accuracy average over the *forced-choice / labelled* tasks:
  **BLiMP**, **BLiMP-supplement**, **EWoK**, **Entity Tracking**, **COMPS**, and the
  finetuned **(Super)GLUE** suite (BoolQ, MultiRC, RTE, WSC, MRPC, QQP, MNLI; large
  sets subsampled to 10k).
- **Human-likeness score** — a *correlation-to-humans* average over **reading-time
  prediction** (surprisal vs human reading times), the two **WUG** morphology tasks
  (model inflection preference vs the human distribution), and **age-of-acquisition**
  (model word-learning curves vs WordBank).
- **Macro Average** — the leaderboard sort key.

The aggregation is a two-level unweighted mean: each task score is the mean of its
subtasks, and the macro average is the mean across tasks. Checking against the
*Findings* table confirms the exact structure — `Macro = mean(NLP, human-likeness)`
(e.g. CLASS-IT 20.4/52.9 → 36.6; MoEP 31.5/53.2 → 42.3). **This 50/50 split is the
crux:** half the flagship number comes from the least reliable half of the
evaluation.

(Some online summaries quote a 50% BLiMP / 30% GLUE / 20% MSGS weighting. That is
the *2023* scheme; MSGS was not used in 2025. Do not apply it here.)

---

## 2. Task-by-task verdict, grounded in the papers

The table is the summary; the subsections give the evidence. "At chance" means ≈0.50
for a two-alternative task. Full quotes/numbers are in `evidence.md`.

| Task | Type | Verdict | Core evidence |
|---|---|---|---|
| **BLiMP** | accuracy | **Trust — coarsely** | Monotone (main.34); but tie artifact (main.16), chance under weak compute (main.11/12), saturating |
| **(Super)GLUE** | accuracy (finetune) | **Trust — with caveats** | Trusted by main.31; but often inert (main.36/41), high seed variance on RTE/WSC (main.19) |
| **BLiMP-supplement** | accuracy | **Weak** | Often near chance (main.5); speaker-label artifact (main.22) |
| **Entity Tracking** | accuracy | **Probe only, never rank** | Seed SD 6–9 pts (main.22); mid-run collapse (main.34); U-shaped |
| **COMPS** | accuracy | **Floor-limited** | At chance for weak models (main.14/22) |
| **EWoK** | accuracy | **Broken at scale** | ~0.50 everywhere; 13% of items' concepts absent from training (main.15) |
| **Reading-time** | correlation | **Noise floor** | ~0, model-insensitive (main.31/32); tokenizer-fragile (main.41) |
| **WUG past-tense** | correlation | **Broken / noisy** | Eval bug (main.14); sign-flipping negatives (main.22/38) |
| **WUG adjective** | correlation | **Gameable** | Untrained model scores ~78 (main.31); non-discriminative (main.32) |
| **AoA** | correlation | **Miscomputed** | Sigmoid fit on 1–5 points → "misleading" (main.29); decided an award (main.39) |

### The reliable core: BLiMP and (Super)GLUE

**BLiMP** is the anchor and the one metric the field trusts. It rises smoothly with
training — "BLiMP scores demonstrate a gradual and consistent increase during
training" (main.34) — and, decisively, the Strict-Small NLP winner's own audit
("Should we trust BabyLM Metrics?") concludes that for BLiMP and (Super)GLUE the
answer "appears to be yes … Failed and untrained models perform expectedly poorly on
these" (main.31).

But three caveats keep it from being read at fine granularity:

- **A scoring artifact inflates degenerate models.** In 22 of 67 BLiMP subtasks the
  two sentences are word-order permutations of each other; the pipeline counts tied
  scores as correct, so any order-invariant scorer is credited. A dummy model forced
  to output equal log-likelihoods "yields a reported score of 100.0." Removing those
  subtasks drops a word-frequency baseline from 0.663 to 0.498 — i.e. to chance — and
  the authors note the flaw "still" persists in the 2025 pipeline (main.16).
- **It is not robust at the low end.** Under compute constraints BLiMP "hovers 44–52
  across configurations" and is "insensitive" to the manipulation (main.12); a
  heavily-quantized model scores 48.7, i.e. below chance (main.11). So a low BLiMP
  is not always informative about grammar per se.
- **It saturates at the top**, where the strongest models approach a Llama-70B
  reference, so gaps among good models compress.

The **BLiMP-supplement** is weaker than BLiMP proper: several models sit near 0.50 on
it (main.5), and one paper traces a supplement "advantage" entirely to three
subcategories (QA_easy, QA_tricky, turn-taking) that contain speaker labels only one
condition's data preprocessing preserved — a headline difference that is a data-
cleaning artifact, not model quality (main.22).

**(Super)GLUE** is the trustworthy secondary. It is accuracy-based, it moves with
model quality (main.31), and MNLI/MRPC/RTE carry real pretraining signal (main.1).
Its caveats are cost and patchy sensitivity: it requires finetuning (the expensive,
higher-variance stage the organizers deliberately pruned); it barely reflects a 10×
data difference (only two of seven Strict models beat the best Strict-Small model on
GLUE, per *Findings*); it is sometimes wholly inert (frozen at 57.7 across every
configuration in main.36; ~63.5 flat in main.41; MultiRC/WSC ≈ majority class in
main.1); and WSC/RTE carry 4–12-point seed variance, enough that main.19 dropped WSC
from its analysis. Use the aggregate, not individual small tasks.

### Broken at scale: EWoK

**Observation.** EWoK is at chance in essentially every text-track paper that reports
it: 52.7–56.7 across all model sizes (main.1); 53.0–53.8 across all methods (main.2);
49.4–50.5 (main.34); 49.9–50.5 (main.22); 0.494–0.519 across 14 curricula (main.26);
49.1–50.2, "none of the models perform better than a random guess" (main.41).

**Mechanism (not inference — measured).** The outstanding paper main.15 states EWoK
"demonstrates no sensitivity to changes in architecture or training strategy, with
performance remaining around 50% regardless of the experiment conditions," and
diagnoses the cause: in 37.7% of EWoK items at least one tested concept appears fewer
than 100 times in the training corpus, and in 13% both concepts appear zero times —
"the training dataset does not properly support EWoK evaluation."

**Confound.** Where EWoK does move, it is suspect: a morpheme tokenizer pushes it to
67–71, which the authors themselves call "surprising, as EWoK measures basic world
knowledge rather than a linguistic task" (main.21) — i.e. the movement reflects
log-probability/segmentation effects, not acquired knowledge.

**Recommendation.** Do not spend effort on EWoK; do not read small EWoK differences
as anything. **COMPS** shares the floor problem (at chance for weak models: 49.4–50.7
in main.14/22) though strong baselines can reach 56–60.

### Probe-only: Entity Tracking

Entity Tracking is the most *method-sensitive* accuracy task — several interventions
move it (multi-token prediction +4–5 pts, main.41; contrastive data +7%, main.2;
recombination 12.95→19.65, main.40) — but it is also the **highest-variance** metric
on the board, which makes it worthless as a ranking component:

- Seed standard deviations of 6–9 points at fixed configuration (20.70 ± 6.09;
  31.68 ± 8.75) — noise comparable to between-condition differences (main.22).
- Mid-run collapse: "performance rises to 41.8 at 20M tokens before collapsing to
  13.4 by the end of training" (main.34); "drops sharply after the first epoch"
  (main.41); U-shaped scaling in the *Findings* training-dynamics figure.
- A barely-trained model beats a strong GPT-BERT on it (41.8 vs 39.9, main.36) — a
  sign the score is not tracking general competence.

**Recommendation.** Use Entity Tracking only as a diagnostic for a *specific*
intervention, and only with multiple seeds and confidence intervals; never treat a
single-run Entity number as a capability ranking.

### Noise floor or broken: the human-likeness half

**Reading-time prediction** (eye-tracking + self-paced reading) has near-zero
magnitude and is insensitive to model quality. main.31's audit: the numbers "stay
relatively similar, regardless of the model." main.32: "the correlations of all
models are below 0.1." Values routinely sit at 0.0–0.1 partial-R² (main.36, main.22),
flip sign when the tokenizer changes (main.41), and — perversely — can favour smaller
models, so the metric may reward low capacity rather than quality (main.30, main.17).

**WUG (past-tense and adjective-nomination)** is unreliable in several independent
ways. There was an outright **evaluation bug** — "a bug was discovered in the
evaluation for the WuG task … we therefore exclude this task" (main.14). Under a
morpheme tokenizer every configuration scores *exactly* 100.00, a near-certain
normalization artifact (main.21). The past-tense correlation routinely goes strongly
**negative** and sign-flips across near-identical models (−20.7 vs +37.5 in main.14;
−24 to +2 with SD up to ±10 in main.22; +22→−22 swings in main.38). And the
adjective task is gameable: "one could obtain quite high scores on adjective
nominalization, around 78, just from initialization, no training required" (main.31);
where it does correlate it does so "for all models" and thus does not discriminate
(main.32).

**Age-of-Acquisition is the most dangerous number on the board — it is miscomputed.**
main.29 inspected the pipeline: "only very few data points (1–5 words) are considered
… due to an unpassed condition on the parameters of the fitted sigmoid function …
Limited data points lead to either a score of zero or a strong negative correlation;
hence, these results can be misleading." This explains the wild spread seen
elsewhere: mostly −0.07 to 0 with lone outliers (main.34), literal 0.00 at p=1.0
(main.40), −79.6 (main.29), +22→−22 (main.38). It is also inflated by broken/untrained
runs (main.31).

---

## 3. Why the aggregate cannot be trusted

The individual-task problems would matter less if they averaged out. They do not,
because the macro average weights the broken half at 50% and because the noisiest
tasks have the widest ranges, so they dominate the aggregate's movement.

**The decisive demonstration (main.31).** A team accidentally trained a model with
too-low a batch size, spiking the loss. It "performs expectedly poorly on … BLiMP and
(Super)GLUE" but "remarkably well on … EWoK, adjective nominalization, COMPS, and
AoA," and its aggregate (45.4) **beat every properly-trained model.** Their verdict on
the aggregate: "the final scoring metric seems to be unfairly skewed." A metric a
broken run can win is not a safe ranking.

**A real award turned on it (main.39).** MoEP won the Strict-Small human-likeness
award only because AoA was included in the macro: its AoA (53.70) is 4–14× any
baseline's (which sit at −3.9 to 14.5), while on BLiMP it is *below* every baseline
(59.15). Given that AoA is the miscomputed task (main.29), this award rests on an
artifact rather than a genuine human-alignment improvement.

**The spread is often within noise.** Run-to-run macro standard deviation is ~1–2
points (35.75 ± 1.74; 36.24 ± 1.16, main.14) — larger than many ranking gaps. main.16
raises the question directly: arbitrary dataset changes move scores by ≥0.05, which
"raises an important concern on when to decide if a system is actually stronger than
another." And main.12 warns the whole exercise "risks that the task 'overfits' on the
most successful-seeming approaches."

**Cross-metric non-transfer means no single scalar is honest.** Every substantive
paper reports that interventions move one metric-family and not another — grammar
(BLiMP, perplexity) versus knowledge/reasoning (EWoK, Entity, COMPS) move
independently or oppositely (main.1, main.2, main.5, main.11, main.12), and BLiMP↔GLUE
even diverge under synthetic data (main.33). Collapsing them "would obscure these
distinctions and reduce interpretability" (main.13). The two headline halves are
themselves decoupled, and *anti*-aligned at the top of the largest track: the
Strict-Small NLP and human-likeness winners are near-opposites (AMLM: 8.4/58.3 vs
MoEP: 31.5/53.2).

---

## 4. What to do for 2026

The 2026 challenge keeps the same evaluation philosophy — "much of the evaluation
will continue to be based on zero-shot probability comparisons of two text
sequences" — so this reliable-vs-broken split should largely carry over (whether the
specific pipeline bugs are fixed is worth checking against the 2026 release).

1. **Optimize BLiMP + BLiMP-supplement first**, via the levers that actually moved
   them in 2025: training objective and architecture (diffusion MLM main.38, adaptive
   masking main.31, GPT-BERT-style dual objective, multi-token prediction). It is the
   most reliable, most monotone, cheapest (zero-shot) signal.
2. **Treat GLUE as the secondary target**, budget for finetuning variance, and report
   the aggregate rather than WSC/RTE/MultiRC individually.
3. **Do not optimize EWoK, COMPS, or the human-likeness tasks for their own sake.**
   If you compete on human-likeness, know that the award can be captured by a targeted
   push on one idiosyncratic (and possibly broken) task — but that any single such
   score is fragile and, in the case of AoA, mis-measured.
4. **Use Entity Tracking as a diagnostic, not a target**, and only with seeds + CIs.
5. **Report per-task, with multiple seeds and confidence intervals**, following the
   best-practice examples in the field: main.2 (10 seeds, paired bootstrap CIs) and
   main.22 (4 seeds, per-task SDs). A single-checkpoint, single-seed macro number is
   not evidence that one model is better than another.
6. **If you can, verify the pipeline before trusting a number** — check the BLiMP
   tie-handling (main.16) and the AoA sigmoid-fit condition (main.29) in the 2026 code.

---

## 5. Confidence and limitations

The verdicts above are unusually well-supported for a challenge post-mortem because
they are *convergent across many independent submissions* and, in the strongest cases,
stated by the winning teams and diagnosed mechanistically (EWoK data coverage in
main.15; AoA sigmoid-fit in main.29; BLiMP tie-counting in main.16). That is stronger
evidence than a single organizer figure.

Two limitations remain. First, this synthesis reads reported numbers and authors'
statements; it does not yet include a **first-hand recomputation of cross-model
variance and the inter-task correlation matrix** over the full leaderboard. That
reanalysis — cross-model SD per task, test–retest reliability, and task–task
correlations — is the natural next step and would quantify what is argued here
qualitatively. The raw material is the HF dataset
`BabyLM-community/leaderboard-all-results`; the pull is currently blocked only because
the authenticated Hugging Face tool needs interactive approval in this environment.
Second, a handful of the 41 papers (main.3, main.9, main.27) do not use the BabyLM
suite and contribute nothing here; two multimodal/Hebrew papers (main.5, main.6) are
included only for their at-chance and non-transfer evidence.

I would expect the raw-data reanalysis to sharpen these conclusions, not overturn
them — but that is a prediction, not yet a result.

---

## Appendix: paper number ↔ identity

Numbers are ACL Anthology `2025.babylm-main.N`. Only papers cited above are listed;
`evidence.md` covers all 41.

- main.1 — Velasco & Roque, *Rethinking the Role of Text Complexity*
- main.2 — Ulm et al., *Contrastive Decoding for Synthetic Data* (10-seed CIs)
- main.5 — Takmaz et al., *Model Merging* (multimodal)
- main.11 — Aman et al., *BitMar* (multimodal, low-bit)
- main.12 — Loáiciga et al., *Smaller batch sizes for ELC-BERT*
- main.13 — Gao et al., *BLiSS* (L2 selective tolerance)
- main.14 — Haller et al., *BLaLM* (linear attention; reports the WUG bug)
- main.15 — Ganescu et al., *Looking to Learn* (outstanding; EWoK data-coverage)
- main.16 — Păpușoi & Nisioi, *Elementary Baselines* (BLiMP tie artifact)
- main.17 — McCurdy et al., *Hall of Mirrors* (surprisal instability)
- main.19 — Roque & Velasco, *Text Simplification + Curriculum*
- main.21 — Bölücü & Can, *Morpheme-Aware* (tokenizer effects; WUG=100 artifact)
- main.22 — "Do Syntactic Categories Help…" (4-seed variance; supplement artifact)
- main.26 — Schoenegger et al., *Influence-driven Curriculum*
- main.28 — *Findings of the Third BabyLM Challenge* (organizers)
- main.29 — Padovani et al., *Dialogue Is Not Enough* (AoA miscomputation)
- main.31 — Edman & Fraser, *Mask and You Shall Receive* / AMLM (Strict-Small NLP
  winner; "Should we trust BabyLM Metrics?")
- main.32 — Martins et al., *Once Upon a Time* / BLM (Interaction winner)
- main.33 — Kamzela et al., *LLM-designed study plans*
- main.34 — Fysikoudi et al., *Active Curriculum LM*
- main.36 — *Batch-wise Convergent Pre-training* (GLUE frozen at 57.7)
- main.38 — Kosmopoulou et al., *Masked Diffusion* (Strict NLP winner)
- main.39 — Tapaninaho, *MoEP* (Strict-Small human-likeness winner; AoA-driven)
- main.40 — Tampier et al., *RecombiText*
- main.41 — Aynetdinov & Akbik, *Multi-Token Prediction*
