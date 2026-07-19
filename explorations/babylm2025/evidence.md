# Evidence: per-paper receipts on BabyLM 2025 score reliability

This file backs the claims in `analysis.md`. It records, per paper, the reported
scores and any statement bearing on whether a metric is reliable, at chance,
saturated, buggy, or non-discriminative. Papers are the ACL Anthology
`2025.babylm-main.N` proceedings; extracted text is under `papers/pN.txt`. Compiled
from a full read of all 41 papers (five parallel readers, cross-checked).

Legend for the recurring findings:
- **EWoK@chance** — EWoK ≈ 0.50 regardless of model.
- **ET-var** — Entity Tracking high variance / instability.
- **WUG-bad** — WUG negative / sign-flipping / buggy / gameable.
- **AoA-bad** — AoA near-zero / negative / miscomputed.
- **RT-floor** — reading-time correlations ≈ 0 and model-insensitive.
- **non-transfer** — improving one metric-family did not improve another.

---

## Tier 1 — direct critiques of the evaluation (most load-bearing)

### main.16 — Păpușoi & Nisioi, "A Comparison of Elementary Baselines"
- **BLiMP tie-counting artifact:** "In 22 of the 67 BLiMP subtasks, the two sentences
  in each minimal pair are permutations of the same multiset of words. Any scorer
  that is invariant to word order assigns identical sentence scores … ties are
  counted as correct, which inflates accuracy." Persists in 2025 pipeline; a dummy
  model with equal log-likelihoods "yields a reported score of 100.0."
- Removing the 22 subtasks: Zipf word-frequency baseline drops 0.663 → 0.498 on
  Strict-Small (to chance).
- Discriminability worry: arbitrary dataset changes shift scores ≥0.05 → "when to
  decide if a system is actually stronger than another."

### main.31 — Edman & Fraser, "Mask and You Shall Receive" / AMLM (Strict-Small NLP winner)
- Appendix C "Should we trust BabyLM Metrics?" — the single richest source.
- Untrained model scores Adj-Nom 77.4; a *failed* run (spiked loss) scores 78.1 and
  its aggregate (45.4) **beats every properly-trained model**, via EWoK, adj-nom,
  COMPS, AoA.
- Verdict: "For BLiMP and (Super)GLUE the answer appears to be yes [trust]. … For
  self-paced reading and eye-tracking, the numbers appear to stay relatively similar,
  regardless of the model. And for the rest, their scores should probably be taken
  with a baby fist of salt."
- "the final scoring metric seems to be unfairly skewed"; "the variance in these
  metrics [adj-nom, past-tense] is high."

### main.29 — Padovani et al., "Dialogue Is Not Enough" (llamalogue)
- **AoA miscomputed:** "only very few data points (1–5 words) are considered … due to
  an unpassed condition on the parameters of the fitted sigmoid function within AoA
  computation in the evaluation pipeline. Limited data points lead to either a score
  of zero or a strong negative correlation; hence, these results can be misleading."
  (Their AoA = −79.6.)
- non-transfer: "none of these fine-tuning techniques improves performance on more
  formal benchmarks"; interaction-tuning only helps "benchmarks that also test for
  this goal." BLiMP for dialogue-only models "clustering around chance level."

### main.15 — Ganescu et al., "Looking to Learn" (outstanding paper)
- **EWoK broken, with mechanism:** "EWoK demonstrates no sensitivity to changes in
  architecture or training strategy, with performance remaining around 50% regardless
  of the experiment conditions." "37.69% of the EWoK examples [have] at least one …
  concept appear fewer than 100 times in training, with 13% … having both concepts
  appearing 0 times … the training dataset does not properly support EWoK."
- VQA depends on VQA-format training data; global-embedding bottleneck; non-transfer
  (gating helps Winoground, hurts VQA).

---

## Tier 2 — quantitative reliability evidence

### main.14 — Haller et al., "BLaLM" (linear attention)
- **WUG eval bug:** "a bug was discovered in the evaluation for the WuG task … we
  therefore exclude this task from our reported [intermediate] results."
- EWoK@chance (50.6 final SS); COMPS@chance (50.5); WUG-past −20.7 (SS) vs 37.5 (S).
- ET-var: curated-100M Entity 14.65 vs curated-10M 39.46; 3 identical runs Entity
  {22.27, 15.39, 15.98}. Macro run-to-run SD ~1–2 pts (35.75 ± 1.74; 36.24 ± 1.16).
- Perplexity ≠ downstream (lowest PPL ≠ best score).

### main.22 — "Do Syntactic Categories Help…" (4 seeds — best variance source)
- ET-var: Entity 20.70 ± 6.09; 31.68 ± 8.75 — seed SD 6–9 pts.
- WUG-bad: WUG_past −24.32 ± 3.86 to +2.28 ± 7.98 (sign-flipping, SD up to ±10).
- EWoK@chance 49.94–50.53; COMPS 51.19–52.94; both "margins are small."
- **Supplement artifact:** B1's higher BLiMP-Supplement is "concentrated in … QA_easy,
  QA_tricky, and turn-taking; each containing speaker labels" — only B1's preprocessing
  kept speaker labels. Headline gap = data-cleaning artifact.
- RT tiny (SPR 0.04–0.17, ET 0.35–0.65). non-transfer across families.

### main.2 — Ulm et al., "Contrastive Decoding" (10 seeds, bootstrap CIs — best rigor)
- EWoK compressed near chance (53.0–53.8 all methods).
- ET is the strongest reliable signal for their method (+7.3%, ***), but swings
  25.5–30.4; Vhead control −8.45%.
- WUG high SE (±2.47), swings 64.67–70.55. RT ~1.8, "no reliable difference."
- non-transfer (thesis): reasoning tasks benefit from CD data; linguistic-competence
  tasks from standard sampling. Warns single fixed checkpoint misleads.

### main.26 — Schoenegger et al., "Influence-driven Curriculum" (84 models)
- EWoK inert 0.494–0.519 across 14 curricula. ET-var 0.164–0.306 (≈2×), most volatile.
  WUG_adj 0.42–0.60.
- Training loss ≠ downstream; ascending ≈ descending ordering (mechanism = batch
  grouping, not developmental plausibility).

### main.34 — Fysikoudi et al., "Active Curriculum LM"
- ET-var (direct): "entity tracking exhibits pronounced instability: … rises to 41.8
  at 20M tokens before collapsing to 13.4 by the end of training."
- BLiMP monotone: "gradual and consistent increase … from 49.3 to 56.5."
- EWoK & COMPS pinned ~50 across all configs. AoA mostly −0.07–0, one outlier 10.04.

### main.36 — "Batch-wise Convergent Pre-training"
- **GLUE frozen at exactly 57.7** for every proposed/controlled config (zero
  discrimination). EWoK@chance; COMPS near chance for proposed models.
- WUG-past unstable/negative (|Δ| up to 17.4 from an optimizer toggle). RT ≈ 0.
- non-transfer: BLiMP down while WUG-Adj/Entity up (a barely-trained model beats
  GPT-BERT on WUG-Adj 57.5 vs 41.2 and Entity 41.8 vs 39.9).

### main.41 — Aynetdinov & Akbik, "Multi-Token Prediction"
- **EWoK stated broken:** "none of the models perform better than a random guess …
  all models perform around chance level throughout all epochs" (blamed on data's
  scarce factual content).
- ET improves with MTP (13.74→18.60) but "drops sharply after the first epoch"; BLiMP
  down as ET up (explicit trade-off). RT sign-flips with vocab size. SuperGLUE ~63.5
  flat (insensitive to objective).

### main.12 — Loáiciga et al., "Smaller batch sizes for ELC-BERT"
- BLiMP collapses to 44–52 (vs 80 original) and is "insensitive" to batch/accumulation;
  hovers near chance across 12 configs.
- MSGS moves opposite to BLiMP; architecture advantage "mostly disappears" once
  training-time is controlled → rankings track compute.
- "risk that the whole task 'overfits' on the most successful-seeming approaches …
  what even is an appropriate measure of human acquisition realism?"

---

## Tier 3 — corroborating scores (at-chance / non-transfer)

### main.1 — Velasco & Roque, "Text Complexity"
EWoK 52.7–56.7 all sizes (barely above chance); ET erratic (16→30→collapse to 20.8 at
500M, chance 20%); ARC-Challenge at chance; MultiRC/WSC ≈ majority; non-transfer
(fine-tuning inert to zero-shot knowledge/entity differences); 500M < 256M (data
bottleneck).

### main.5 — Takmaz et al., "Model Merging" (multimodal)
EWoK plotted 49–53 (chance); BLiMP-supplement 50–58 (near floor, "do not perform
well"); WUG-past correlation −0.20 to +0.05 (≈0); Winoground 0.46–0.54 (chance line
drawn). non-transfer: vision hurts grammar (BLiMP) but helps EWoK/Entity.

### main.11 — Aman et al., "BitMar" (low-bit multimodal)
BLiMP 48.7 (**below chance**); WUG −0.16/−0.22 (negative); reading degraded by memory
(1.11→0.44); GLUE-family "no significant changes" under an intervention that moved
zero-shot. non-transfer in ablation (entity/COMPS up, WUG/reading down).

### main.35 — Fusco et al., "Linguistic Units as Tokens"
EWoK 49.4–50.6 (chance, all tokenizers); SPR 0.1–4.3 (≈0); ET 13.9–64.4 (huge spread);
WUG_ADJ 66.1/37.6/33.1/−43.1 and WUG_PAST −5.0/12.1/−29.4/−2.6 and AoA 11.7/−25.6/
−31.7/16.3 (all swing 40–100 pts, include large negatives). GLUE/BLiMP comparatively
tight.

### main.10 — Salhan et al., "Best Sequence Length"
EWoK 49.7–52.5 (flat/"less sensitive"); ET 12.5–40.4 (wild, NaN at extremes); WUG up
to 90 then collapses; "no single sequence length is optimal across tasks."

### main.21 — Bölücü & Can, "Morpheme-Aware Tokenization"
**WUG = exactly 100.00** for every morpheme-tokenizer config (artifact); reading
collapses to ~0.06–0.12; EWoK jumps to 67–71 (authors "surprising … EWoK measures
world knowledge") → tokenization/log-prob artifact. Tokenizer highest-leverage
(EWoK +20%, Entity +40%) but confounds sequence-log-prob scoring.

### main.19 — Roque & Velasco, "Text Simplification + Curriculum"
WSC dropped for "high variance (4–12 points) across seeds"; RTE seed SD ±3–6; MultiRC
never beats from-scratch; ET is largest mover (22.4→36.9, ~14 pts) while EWoK/MMLU
barely move; MMLU ≈ chance (23–26).

### main.38 — Kosmopoulou et al., "Masked Diffusion" (Strict NLP winner)
Backend critique: "the MLM evaluation backend is a rather myopic view of likelihood
estimation … it may be suboptimal, further undermining the MDLMs performance." AoA
flips +22.3 (baseline) → −22.0 (submission). WUG-past 27.1→15.4 opposite to WUG-adj.

### main.32 — Martins et al., "Once Upon a Time" (Interaction winner)
"interactive RL primarily enhances narrative coherence and creativity, while leaving
surface-level fluency—measured by the BabyLM tasks—largely unchanged." Only Entity
moved (30.3→33.1). AoA/Eye-T/SPR "all below 0.1" for all models; WUG-A 0.5–0.7 "for
all models" (non-discriminative).

### main.39 — Tapaninaho, "MoEP" (Strict-Small human-likeness winner)
Won macro **only with AoA included**: AoA 53.70 vs baselines −3.9 to 14.5; BLiMP 59.15
below all baselines. Award rests on the miscomputed AoA task.

### main.30 — Capone et al., "CLASS-IT"
non-transfer: "improvements do not consistently transfer to zero-shot tasks";
"performances … may be undermined by the evaluation criteria" (log-likelihood-only
zero-shot favours masked LMs). Reading rewards smaller models (baselines "score almost
zero"). "very inconsistent across tasks and evaluation methods."

### main.25 — Salhan et al., "Teacher Demonstrations / ContingentChat"
Benchmark suite flat across all post-training (Avg ~30.7–31.0); effects only in bespoke
cohesion metrics/human judgement. WUG/RT floor-level for all models. "none of these
benchmarks are well-suited for evaluating causal language model text generation."
Seq-len-4096 variants: BLiMP→55.6 while Entity→40.9 (anti-correlation).

### main.40 — Tampier et al., "RecombiText"
Augmentation helps ET (12.95→19.65; RoBERTa 32.27→38.89) and WUG-past (−0.06→0.24) —
but "no variant achieved statistical significance of p<0.05"; AoA literally 0.00 (p=1.0)
for most variants. EWoK@chance. Different mixes win different metrics (non-transfer).

### main.13 — Gao et al., "BLiSS"
"high performance on BLiMP does not guarantee high performance on BLiSS … clear lack of
a strong positive correlation." Argues against collapsing metrics: "Combining these
metrics into a single score would obscure these distinctions."

### main.33 — Kamzela et al., "LLM-designed study plans"
BLiMP↔GLUE diverge at 10M (human data wins BLiMP, synthetic wins SuperGLUE). SuperGLUE
components barely move (WSC pinned ~0.61–0.69).

### main.4 — Askari et al., "Gricean Maxims" (outstanding paper)
Motivating critique: BLiMP/GLUE "do not directly and comprehensively assess pragmatic
abilities." BabyLMs at/near/below chance on Quantity maxims. Caveat on their own metric:
sequence-score evaluations "prone to bias" from token distribution.

### main.24 — Zain et al., "Co4"
EWoK 49.5–50.1 all models (chance); WUG swings 43→93; ET 13.9→41.4; BLiMP near chance
for Co4 (51–54) — headline "wins" land on the high-variance tasks while it collapses on
BLiMP.

### main.17 — McCurdy et al., "Hall of Mirrors"
Human-scale models (GPT-BERT) "do not consistently prefer either condition"; surprisal
effects non-monotonic and flip across model size → reading-time/surprisal alignment is
fragile and scale-dependent. Cites Oh & Schuler: bigger LMs approximate reading time
*worse*.

### main.6 — Gelboim & Sulem, "TafBERTa" (Hebrew)
7B SOTA DictaLM2.0 scores 31.4 on number agreement (below chance) — large models can be
at/below chance on targeted minimal-pair grammar. Within-benchmark non-transfer
(number vs gender dissociate; gender below 0.50).

### main.23 — Kriš & Šuppa, "SlovakBabyLM"
Curriculum ordering: all comparisons non-significant (p≥0.05). Tokenization is the
central cross-lingual factor (2.13× token inflation for Slovak) and the stated cause of
frequency-CL failure.

### main.18 — Poh et al., "Child-Directed Speech Questions"
5 seeds "to reduce the effect of variance." non-transfer (helps Island/Filler-Gap, hurts
Quantifiers/Irregular). BLiMP subtask wh_vs_that_with_gap_long_distance stuck at 7.62%.

---

## Papers with no BabyLM-suite evaluation (excluded from the argument)
- main.3 (MoE-MLA, TinyStories + GPT-4 judge), main.9 (few-M-param, loss/repro only),
  main.27 (Mamba-Transformer, SlimPajama). main.20 (CurLL) and main.8 (determiner
  trajectories) argue against end-state benchmarks generally but use their own metrics.
- main.7 (FORGETTER) reports only BLiMP and claims it is ~1:1 with next-token loss;
  main.37 (LoRA + artificial languages) reports only BLiMP/EWoK and finds "EWoK does not
  show any consistent correlation with … rank" (EWoK@chance again).
