# Evaluation Cubed (Eval³) — Research Plan

**Question.** LLM evaluation is hard to trust. Meta-evaluation (evaluating the judges)
is the standard response. But meta-evaluation is itself an evaluation procedure, and
nobody checks *it*. This project builds the third level: **evaluating the evaluation of
the evaluators**, and asks whether the standard meta-evaluation protocol actually does
the job it is used for.

---

## 1. The levels

| Level | Object evaluated | Standard practice | Standard metric |
|---|---|---|---|
| L0 | a response | — | — |
| L1 | a system (via a judge) | LLM-as-judge benchmark | win-rate / mean score |
| L2 | a judge | meta-evaluation (MT-Bench agreement, RewardBench, JudgeBench) | **agreement with human gold labels** |
| L3 | a meta-evaluation protocol | **nothing** | **nothing** |

This project supplies L3.

## 2. The central claim to test

Meta-evaluation scores judges by **agreement with gold labels on a pooled item set**.
Judges are *used* to **rank systems**. These are different things.

Write judge error as `e(s,i) = q̂(s,i) − q(s,i)` for system `s`, item `i`.
Mean judge score for a system: `Q̂(s) = Q(s) + ē(s)`, with `ē(s) = μ + δ(s)`.

- `μ` — **global bias**. Shifts every system equally. *Zero effect on ranking.*
- `δ(s)` — **system-differential bias**. *The only term that corrupts ranking.*
- `e(s,i) − ē(s)` — **idiosyncratic noise**. Costs statistical power, unbiased.

Meta-evaluation accuracy is a monotone function of `E|e|`, which **mixes all three**.
Hypothesis: most judge error is `μ` and noise (harmless), so accuracy rankings of judges
are dominated by harmless error and do not predict ranking validity.

**H1 (Accuracy–Validity Gap).** Meta-benchmark accuracy has weak/no predictive power for
downstream system-ranking fidelity.

**H2 (Non-transfer).** A judge validated on one *population of systems* can invert
rankings on another. Judge validity is not distribution-free over systems. Standard
meta-evaluation never tests this because it pools.

**H3 (Regress termination).** Ranking depends only on quality *differences*, not levels.
Quality-preserving and quality-ordering **transformations** give oracle-free access to
differences. Therefore judge validity for ranking is certifiable **without gold labels**,
and the meta-evaluation regress terminates at level 3.

**H4.** Label-free perturbation diagnostics predict held-out ranking fidelity better than
gold-label meta-benchmark accuracy does.

## 3. Ground truth without humans

The blocker for any L2/L3 study is ground truth. We sidestep it by **construction**:

- Build items whose reference answer is a set of `N` atomic, independently checkable claims.
- A "system" is produced by a **known degradation**: corrupt `k` of the `N` claims.
- True quality is then `N − k`, **known by construction**, not by annotation.
- Orthogonally, apply **quality-preserving style transforms** (verbosity, confidence,
  structure). Content set is held fixed ⇒ any judge score change is judge error, by
  construction, with no labels.

Quality grid `k ∈ {0,1,2,3,4}` × style `∈ {plain, polished, padded}` ⇒ up to 15 synthetic
systems with a *known* partial order. Plus a ladder of real models for ecological validity.

This is the methodological core: **construction-based ground truth**, replacing annotation.

## 4. Experimental grid

- **Items**: ~100 open-ended factual questions, each with `N≈6` atomic claims.
- **Systems**: 15 synthetic (5 quality × 3 style) + ~5 real models.
- **Judges**: model ∈ {gpt-4.1-nano, gpt-4.1-mini, gpt-5-nano, gpt-5-mini, gpt-5.4-mini,
  gpt-4o-mini} × protocol ∈ {direct 1-10, rubric, pairwise, pairwise+swap, CoT}.
  Target ~15–20 judge configs.
- **L2 protocols**: (P1) item-level accuracy vs gold, (P2) pairwise preference agreement,
  (P3) system-level correlation on dev systems, (P4) label-free perturbation diagnostics.
- **L3 metric**: **transfer** — rank judges by protocol P on a dev system population,
  measure realized ranking fidelity on a *held-out* system population. A protocol is valid
  iff its judge ranking transfers.

## 5. Deliverables

1. `EVAL3` harness + released data (`data/`, `src/`).
2. Theory: accuracy–validity impossibility result; label-free bound on ranking distortion.
3. Empirical study answering H1–H4.
4. NeurIPS paper (`paper/`), full exposition per repo report guidelines.

## 5b. Literature review — DONE, see `notes/related_work.md`

Should have been step zero. Doing it late nearly cost us: three 2026 papers sit close to
this design. Summary of what it changed:

- **2606.19544 "Reliability without Validity"** already shows judge *rankings* shift across
  meta-benchmarks. So "meta-eval is unstable" is no longer a novel claim. Our novelty must
  be the *reason* (T1), the *downstream bound* (T2), and the *level-3 decision framing*.
- **2605.06161 "Policy Invariance"** proposes a perturbation-based judge score, but states
  explicitly that it does **not** bound downstream ranking error. That is our gap.
- **2603.05485 "Bias-Bounded Evaluation"** enforces bias bounds algorithmically; ours is a
  post-hoc per-pair certificate. Complementary, must be cited.
- **2607.13707 "Test Oracle Problem"** endorses mechanical-perturbation corpora (our design)
  over LLM-generated-negative corpora, but mandates a validation protocol we must adopt:
  manual read of 15–20 items per condition, mean word count per condition, degeneration
  rates. **Adopted as task 6.4b.**
- **2606.19544** finds verbosity bias *small* under a pairwise rubric; our pilot finds large
  style effects under pointwise scoring. Keep the pairwise arm and report the contrast.

Venue decision: **NeurIPS 2026, Track on Evaluations and Datasets** (`eandd`), 9 content
pages. Official `neurips_2026.sty` obtained from an arXiv e-print (the media.neurips.cc
mirror 403s from this sandbox).

## 6. Task list

- [x] 6.0 Literature review (`notes/related_work.md`)
- [x] 6.1 Item + atomic-claim dataset generation — 85 items, 510 verified claim pairs
- [x] 6.4b Oracle-integrity protocol per 2607.13707 — caught the verbatim-concatenation
      fault in `plain`; fixed and re-rendered (`notes/stimulus_integrity_log.md`)
- [x] 6.2–6.7 system grid, judge harness, full run (28 judge configs, 40,120 judgements)
- [x] 6.8–6.11 analysis — **note the mid-project redesign below**
- [x] 6.12 theory (Prop 1, Thm 1 pooling impossibility, Thm 2 certificate)
- [x] 6.13 figures (5) ; 6.14 paper drafted + built ; 6.15 committed and pushed
- [x] audit: all 25 numbers quoted in the paper re-derived from results (`src/audit_numbers.py`)

## 8. Mid-project redesign (recorded, not hidden)

The original grid compared systems at corruption levels k=0..4, i.e. quality gaps up to 4 of
6 claims. **At that separation almost every judge ranks perfectly** (SRA = 1.000 for 18 of 24
pointwise configs; mean 0.977). H1 and H2 as originally written were therefore untestable on
this grid — there was no outcome variance to explain.

Two further hypotheses also failed and are reported in the paper rather than dropped:
- pooled agreement *does* predict ranking validity ordinally (rho = -0.89), contra H1;
- restricting the meta-benchmark to clear-cut, style-matched pairs does *not* destroy that
  signal (rho -0.79 to -0.89), contra the follow-up conjecture.

The redesign: define a system by its *mean* corruption level over items, which yields
arbitrarily fine quality gaps by re-aggregating judge scores already collected — zero extra
API calls. This exposed the quantity that does vary: the **resolution limit**, spanning 60x
across judges. The surviving claim is about **calibration**, not rank order, and the
label-free estimator halves the residual error of the best gold-label predictor.

Lesson for next time: choose the manipulation range by asking what regime the *decision*
lives in, not what makes the manipulation check easy to pass.
- [ ] 6.2 Verify claims are independently checkable (automatic + spot check)
- [ ] 6.3 System construction: corruption + style transforms
- [ ] 6.4 Validate construction (corruptions really are wrong; styles really are neutral)
- [ ] 6.5 Judge harness + caching + concurrency
- [ ] 6.6 Pilot run (small grid), sanity-check signal
- [ ] 6.7 Full run
- [ ] 6.8 Analysis: error decomposition (μ, δ, noise)
- [ ] 6.9 Analysis: H1 accuracy–validity gap
- [ ] 6.10 Analysis: H2 non-transfer across system populations
- [ ] 6.11 Analysis: H4 label-free diagnostics beat gold-label accuracy
- [ ] 6.12 Theory write-up + proofs
- [ ] 6.13 Figures
- [ ] 6.14 Paper draft, revision passes, PDF
- [ ] 6.15 Commit + push

## 7. Notes / risks

- Risk: synthetic corruptions may be too easy for judges ⇒ ceiling effects. Mitigation:
  make corruptions *plausible* (swap a number/date/name to a nearby wrong value), not absurd.
- Risk: style transforms may not be quality-preserving. Mitigation: transforms are applied
  by an LLM under an instruction to preserve every claim verbatim in meaning; verify by
  claim-recovery check.
- Risk: judge grid too small for a regression across judges. Mitigation: ≥15 judge configs.
- No Anthropic API key available programmatically ⇒ OpenAI-only judge pool. Note as a
  limitation; the claims are about the *protocol*, not about specific vendors.
