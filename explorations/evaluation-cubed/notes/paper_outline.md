# Paper outline + anticipated objections

Venue: NeurIPS 2026, Track on Evaluations and Datasets. 9 content pages.

Working title: **Evaluation Cubed: Meta-Evaluation Cannot Certify the Rankings It Is Used
to Justify, and What Can**

## Argument spine (organised by logic, not chronology)

1. **Setup.** Judges rank systems. Meta-evaluation scores judges by agreement with gold
   labels on a pooled item set. Nobody evaluates the meta-evaluation.
2. **Initial finding.** Judge accuracy on a labelled meta-benchmark does not predict
   whether that judge ranks a *different* population of systems correctly.
3. **Mechanism.** Decompose judge error into global bias / differential bias / noise. Only
   differential bias corrupts rankings; pooled accuracy mixes all three. Formalise as an
   invariance-group impossibility (T1): pooled metrics are invariant to a group of
   within-label permutations that ranking fidelity is not invariant to.
4. **Alternative explanation, tested.** Is it just that the metric is bad? No: the *same*
   gold-label metric computed on the *target* population selects well. So the failure is
   population mismatch, not metric design. This kills the "just use better κ" response.
5. **Boundary condition.** Style bias is protocol-dependent: large under pointwise scoring,
   suppressed under pairwise. Engages norman2026reliability's "verbosity bias <0.011".
6. **Intervention.** The perturbation certificate: label-free, per-pair, sound relative to
   a declared transformation family. Coverage/accuracy measured.
7. **Ecological validity.** Repeat on 5 real models with measured (not constructed) quality.
8. **Remaining uncertainty.** Scope limits, honestly.

## Contributions as stated

1. **Eval³**, a benchmark and harness for evaluating meta-evaluation *protocols*, built on
   construction-based ground truth (no annotation).
2. **T1**, an impossibility result: no pooled meta-evaluation metric determines ranking
   validity.
3. **T2**, the perturbation certificate: a label-free sufficient condition for a pairwise
   ranking claim to be correct, with measured coverage.
4. An empirical study quantifying judge-selection **regret** under population shift.
5. The **regress-termination** argument: level-3 grounding is O(1) in systems/judges/items,
   which is why the tower stops here.

## Objections a reviewer will raise, and the answer

**"Verbosity is genuinely bad, so your `padded` transform is not quality-preserving and
your 'pure bias' is partly real signal."**
The sharpest objection. Answer: the certificate is explicitly *relative to a declared
quality construct*. We declare the construct (factual accuracy: fraction of true atomic
claims) and the transformation family must preserve it. Declaring `T` forces you to
declare your construct — this operationalises construct validity rather than dodging it.
**[ACTION]** run the whole analysis again with the restricted family {plain, polished},
which differ only in formatting and are matched in length, to show nothing hinges on
`padded`.

**"The style contrast (99 vs 286 words) is artificially extreme."**
**[ACTION]** report the natural verbosity spread of the 5 real models and compare. If real
models span a comparable range, the imposed factor is in-distribution.

**"Factual-claim coverage is a narrow notion of quality."**
Conceded, and stated as scope. It is the dimension where ground truth is *constructible*,
which is the whole point of the design. Claims are about ranking on factual accuracy.

**"Comparing gold-label@dev against label-free@target is unfair."**
It is exactly the comparison practitioners face: gold-label meta-benchmarks structurally
cannot be computed on your target population without new annotation; perturbation
diagnostics can. We additionally report gold-label@target as a label oracle to isolate the
cause, so the comparison is decomposed rather than rigged.

**"Only OpenAI judges."**
True, and stated. No Anthropic API key was available in the environment. The claims are
about the *protocol*, not about any vendor's models; the judge pool spans a wide capability
range within one provider. Cross-provider replication is the obvious next step.

**"Synthetic corpora are unreliable (cf. balli2026oracle)."**
That paper argues the opposite for *our* design: mechanical-perturbation corpora carry an
automatic oracle, unlike LLM-generated-negative corpora. We run their full validation
protocol and report it (see `notes/stimulus_integrity_log.md`), including a fault it caught
and we fixed.

**"243 populations are not independent."**
Correct; they share systems and items. They are not treated as independent samples — they
are an *enumeration* of the style-assignment design, used to characterise the range of a
judge's fidelity, and all CIs bootstrap over items, which are the independent replicates.

## Figures

- F1 accuracy–validity gap: meta-benchmark accuracy vs realised fidelity, in-dist vs transfer
- F2 error decomposition: stacked SS_quality / SS_style / SS_inter per judge
- F3 fidelity spread across the 243 equal-truth populations, per judge
- F4 judge-selection regret by protocol
- F5 certificate: coverage vs certified accuracy
