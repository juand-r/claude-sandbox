# Evaluation Cubed (Eval³)

Evaluating the evaluation of the evaluators. Judges rank systems; meta-evaluation scores
judges by agreement with gold labels; nobody scores the meta-evaluation. This builds the
third level and asks whether meta-evaluation delivers what it is used for.

**Paper:** `paper/eval3.pdf` (NeurIPS 2026 format, Track on Evaluations and Datasets).

## Headline result

Judges are not bad at ranking — at large quality gaps essentially all of them are perfect.
What varies is each judge's **resolution limit**: the smallest true quality gap it can order
reliably once systems differ in surface form.

| | |
|---|---|
| Resolution limits across 28 judge configs | **0.8% → 50%** of an answer's factual content (**60×**) |
| Meta-evaluation accuracy over the same pool | 66.1% → 88.3% (**22 points**) |
| Gold-label accuracy predicting the limit | R² = 0.723, residual **6.3%** of content |
| Label-free predictor `δ_style` | R² = 0.927, residual **3.3%** |
| Certificate, leaderboard regime | raw **0.860** → certified **0.969** at 55.8% coverage |
| Accuracy on pairs the certificate declines | **0.721** |
| Same, threshold estimated on disjoint items | raw 0.838 → certified **0.943** vs 0.683 declined |

The residual of the best gold-label predictor (6.3%) is larger than the entire resolution
limit of the seven best judges — so knowing a judge's meta-benchmark accuracy does not tell
you whether your 5% leaderboard gap is real. The label-free estimator does.

## Real systems

Five real models answering freely span a measured quality range of **0.108** — almost exactly
the median judge's resolution limit (0.108). Real comparisons therefore sit right at the edge
of what these judges can resolve: raw ranking accuracy on fine-grained pairs falls to 0.652,
and the certificate separates 0.754 (certified) from 0.584 (declined).

Read this as showing *which regime* real comparisons occupy, not as a second validation. The
measured quality proxy is coverage-weighted (correlates with answer length, r = 0.31 at item
level) and restyling real answers drifts measured quality by 0.049, so quality-preservation is
approximate here rather than exact by construction. Those are precisely the costs of leaving
construction-based ground truth, which is why the constructed arm carries the main claims.

## Two hypotheses that did not survive

Recorded because they shaped the paper. (1) We expected pooled agreement to fail to predict
ranking validity. It does predict it, ordinally (ρ = −0.89). (2) We expected that building
the meta-benchmark from clear-cut, style-matched pairs would destroy that signal. It does
not (ρ from −0.79 to −0.89). The surviving claim is about *calibration*, not rank order.

## How ground truth is obtained without annotation

Answers are assembled from six atomic factual claims per item. A system corrupts `k` of them
(a wrong date, swapped name, reversed relation), so true quality is a **design parameter**,
not an estimate. The same claim set is rendered in three styles, so restyling is
**quality-preserving by construction** and any judge score difference across styles is judge
error, measurable with no labels. Defining a system by its *mean* corruption level over items
gives arbitrarily fine quality gaps by re-aggregating scores already collected — the whole
continuous quality axis costs zero extra API calls.

## Running it

```bash
pip install openai numpy scipy pandas matplotlib      # needs OPENAI_API_KEY
python3 src/build_items.py 3 32     # 1. item pool          -> data/items.json
python3 src/build_systems.py        # 2. system grid        -> data/answers.json
python3 src/oracle_integrity.py     # 2b. stimulus checks   -> results/oracle_integrity.json
python3 src/judges.py               # 3. 40,120 judgements  -> results/*.jsonl
python3 src/resolution.py           # 4. resolution limits  -> results/resolution.json
python3 src/composition.py          # 5. composition ablation
python3 src/certificate_eval.py     # 6. certificate
python3 src/run_analysis.py         # 7. ANOVA, populations, regret
python3 src/bootstrap.py 300        # 8. bootstrap CIs over items
python3 src/figures.py              # 9. figures
python3 src/real_systems.py         # 10. real-model arm (5 models, measured quality)
python3 src/real_analysis.py        # 11. real-model analysis
python3 src/audit_numbers.py        # 12. verify every number quoted in the paper (41 checks)
cd paper && pdflatex eval3 && bibtex eval3 && pdflatex eval3 && pdflatex eval3
```

Every LLM call is cached in `data/llm_cache.sqlite` (gitignored), so re-runs are free and
exactly reproducible. Failures are loud — a call that fails after retries raises rather than
silently returning a default.

## Layout

```
PLAN.md                        research plan, with the mid-project redesign recorded
notes/related_work.md          literature review; three 2026 papers sit close to this design
notes/theory.md                working notes for the propositions and theorems
notes/stimulus_integrity_log.md the integrity protocol, and the fault it caught
notes/paper_outline.md         argument spine + anticipated reviewer objections
src/                           pipeline (see run order above)
results/                       all measurements as JSON/JSONL
figures/                       five figures, one takeaway each
paper/eval3.tex|.pdf           the paper; official neurips_2026.sty
```

## Notes and caveats

- **One provider.** All judges are OpenAI models; no Anthropic key was available in this
  environment. Claims are about the protocol, not any vendor. Cross-provider replication is
  the obvious next step.
- **Narrow construct.** True quality here is factual-claim correctness — deliberately, since
  that is the dimension along which ground truth is constructible.
- **The real-model arm is the weakest part.** Its quality proxy is not independently
  defensible; see the caveats above and §8 of the paper.
- **The certificate is relative to the declared transformation family.** Its 3.1% shortfall
  from soundness measures confounds outside the three transformations, and is reported rather
  than hidden. `notes/related_work.md` explains how this differs from the closest prior work.
- The `plain` condition was rebuilt after the integrity check found 61–68 of 85 answers were
  verbatim claim-list concatenations. All statistics come from the corrected corpus.
- `neurips_2026.sty` is the official file, recovered from an arXiv e-print because
  `media.neurips.cc` returns 403 from this sandbox.
