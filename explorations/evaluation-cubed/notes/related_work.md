# Literature review (done 2026-07-25)

Purpose: find the gap, avoid re-deriving known results, and fix the design *before*
freezing it. Several findings below changed the plan; those are marked **[ACTION]**.

## 1. Meta-evaluation of judges: the state of the art

**Norman et al., "Reliability without Validity: A Systematic, Large-Scale Evaluation of
LLM-as-a-Judge Models Across Agreement, Consistency, and Bias" (arXiv 2606.19544).**
The largest study of its kind: 21 judges, 9 providers, MT-Bench / JudgeBench /
RewardBench, 118 runs, ~541k judgements. Findings: exact-match agreement overstates
discrimination (κ deflation of 33–41 pp on MT-Bench); **judge rankings shift by up to 14
positions across benchmarks**; high test–retest reliability (>0.95) coexists with severe
position bias (consistency–bias paradox); verbosity bias small (<0.011) under a single
pairwise rubric. No theorems. No new metric — they distil a "Minimum Viable Validation
Protocol". Nothing label-free.

This is the closest empirical neighbour and it must be cited prominently. What it
establishes: judge *rankings* are unstable across meta-benchmarks. What it does not do:
(i) explain *why* pooled agreement cannot settle the question, (ii) connect meta-evaluation
scores to **downstream system-ranking fidelity**, (iii) treat judge choice as a decision
with measurable regret, (iv) offer any label-free remedy. Those are our four contributions.

Note also the tension we can engage: they find verbosity bias small *under a pairwise
rubric*. Our pilot shows large style effects under *pointwise* scoring. That suggests
style bias is protocol-dependent, which we can test directly since our grid crosses
pointwise and pairwise protocols. **[ACTION]** keep the pairwise arm; report the contrast.

**"Agreement Metrics for LLM-as-Judge Evaluation: What to Report and Why" (2606.00093).**
On binary verdicts, Pearson/Spearman/Kendall/phi/MCC collapse to one number ("illusion of
corroborating evidence"); recommends accuracy + Cohen's κ + confusion matrix, and an
11-item checklist. Explicitly scoped to single-judge validation: it **does not address
whether agreement predicts system-level ranking**. Good citation for "the field is
refining pooled metrics" — while our T1 says refinement inside that frame cannot succeed.

**"Pooled Leaderboards Hide System-Specific Winners" (2606.29159).** Independent support
for the pooling critique, from reporting-protocol auditing.

**JUDGe 2026 workshop, "Can We Trust the Judge?"** Confirms the question is live.

## 2. Bounding judge bias

**"Towards Provably Unbiased LLM Judges via Bias-Bounded Evaluation" (2603.05485).**
Proposes *average bias-boundedness* (A-BB), an algorithmic framework guaranteeing bounded
harm from any measurable bias; on Arena-Hard-Auto with 4 judges achieves (τ=0.5, δ=0.01)
guarantees while retaining 61–99% of the original ranking correlation.

Closest theoretical neighbour. Difference: A-BB is an **intervention** that modifies the
evaluation to enforce a bound. Ours is a **certificate**: a per-pair, post-hoc soundness
statement about an ordering already produced, requiring no change to the judge. The two
compose; cite as complementary, not competing.

**"Beyond Accuracy: Policy Invariance as a Reliability Test for LLM Safety Judges"
(2605.06161).** Closest neighbour to our label-free diagnostic. Policy Invariance Score
from certified-equivalent rubric rewrites, plus a "Judge Card" reporting template; proves
boundedness/monotonicity of its own score and unbiasedness of a jitter-corrected estimator.
Crucially: rewrites are **certified by three human annotators**, the transforms are
*rubric-side*, and — in their own words — **they do not bound downstream ranking error;
they study judge-level reliability only.**

That is precisely our gap. Ours is output-side, needs no human certification (content is
held fixed by construction rather than judged equivalent after the fact), and the whole
point is the downstream ranking bound.

**"Judge Reliability Harness" (2603.05399)**, **PertEval (2405.19740)**,
**LGMT (2605.23965)**: perturbation/metamorphic stress-testing of LLMs and judges. These
are the intellectual ancestors of the perturbation family; none derives a ranking
certificate.

## 3. The oracle problem in synthetic judge corpora — **this changed the plan**

**"The Test Oracle Problem in Synthetic LLM-as-Judge Corpora: Disappearance, Distortion
and a Validation Protocol" (2607.13707, July 2026).** Reports a pipeline in which the
generation of synthetic negatives silently failed (a shared token budget truncated
generations to ~2 words). Four standard robustness checks missed it; only manual reading
caught it. Two failure modes: **disappearance** (a reported 32-point effect was entirely
fabricated; 0.61 → 1.00 once fixed) and **distortion** (a real Markdown-bullet style bias
had its magnitude and sometimes its *direction* bent by stimulus length: 0.24 → 0.81).
Aggregate statistics cannot tell the two apart.

Their central argument favours our design: **mechanical-perturbation corpora carry an
automatic oracle**, whereas "prompt an LLM for a plausible-but-wrong answer" corpora do
not. Their positive control injected 30% silent no-ops into a perturbation corpus and a
string comparison caught 100% of them at zero cost.

Recommended protocol, before any aggregate statistic:
1. manually read 15–20 raw items per generation condition,
2. report mean word count per condition,
3. report degeneration rates (verbatim copies; fragments under three words).

**[ACTION]** We already do (2) (77/130/286 words) and a claim-level entailment check
(99.6% fidelity). We must add: a **mechanical no-op check** (corrupted claim string must
differ from the true claim), **degeneration rates**, and an actual **manual read of 15–20
items per condition**, all reported in the paper. Our renderer is an LLM, so we do not get
a pure string oracle for the rendering step — but the claim-substitution step is fully
mechanical and therefore string-checkable, and the rendering step is guarded by the
entailment check. Say exactly this in the limitations.

## 4. Benchmark validity more broadly

**"Measuring what Matters: Construct Validity in LLM Benchmarks"** (OpenReview mdA5lVvNcU;
screened 46,114 articles, reviewed 445 benchmark papers): only **16%** used uncertainty
estimates or statistical tests; 27% used convenience sampling; contested construct
definitions are common. Excellent framing citation for the introduction.

**"Benchmarking the Benchmarks: A Validity Audit of Tool-Calling Evaluation" (2607.02577)**
and **BenchBench** (meta-evaluation of benchmarks): level-2-for-benchmarks work. Related
in spirit; different object (benchmarks, not meta-evaluation protocols).

**"A Single Character can Make or Break Your LLM Evals" (2510.05152)**: formatting
sensitivity, supports the style-perturbation family.

Older canon to cite: Zheng et al. 2023 (MT-Bench, position/verbosity/self-enhancement
bias); Lambert et al. 2024 (RewardBench); Dubois et al. 2024 (length-controlled
AlpacaEval); Zeng et al. 2024 (LLMBar); Panickssery et al. 2024 (self-preference);
Chaganty et al. 2018 (control variates for automatic metrics); Boyeau et al. 2024
(prediction-powered AutoEval); Jacobs & Wallach 2021 (measurement/construct validity);
Reiter 2018 (BLEU validity).

## 5. Where the gap actually is, after all this

The field has: better pooled agreement metrics; large audits showing judge rankings are
unstable; perturbation stress-tests that score judges; and one framework that enforces
bias bounds algorithmically.

The field does not have:

1. **A reason.** No formal statement of *why* pooled meta-evaluation cannot certify
   ranking validity. → T1 (invariance-group impossibility).
2. **A downstream bound.** Perturbation diagnostics score judges but stop there; 2605.06161
   says so explicitly. → T2 (perturbation certificate on system-pair orderings).
3. **A level-3 object of study.** Meta-evaluation protocols are never themselves evaluated
   against the decision they inform. → judge-selection regret under population shift.

That is the paper.

## 6. Revisions to the plan forced by this review

- **[ACTION]** add mechanical no-op check + degeneration rates + manual read of 15–20 items
  per condition (2607.13707), and report them.
- **[ACTION]** keep and emphasise the pointwise-vs-pairwise contrast to engage 2606.19544's
  "verbosity bias is small" result.
- **[ACTION]** reposition the certificate against 2605.06161 and 2603.05485 explicitly:
  ours is post-hoc, label-free, output-side, and about *ranking*, not judge reliability.
- **[ACTION]** report uncertainty on every headline number (only 16% of benchmark papers
  do; we should not be in the other 84%).
- Venue: NeurIPS 2026 **Track on Evaluations and Datasets** (`eandd` option in
  neurips_2026.sty). Content limit 9 pages.
