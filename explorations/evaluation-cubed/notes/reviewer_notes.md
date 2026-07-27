# Reviewer notes — read as a non-expert

Persona: NeurIPS reviewer, competent ML researcher, works on training methods. Has used an
LLM judge once. Does not know RewardBench from JudgeBench, has never thought about
meta-evaluation as a topic. Reading the PDF once, carefully, at normal reviewing speed.

Recording every place I stumbled, in the order I hit them, then ranking.

---

## Blocking problems

### B1. "Resolution limit" names two different things
This is the worst one and it broke my reading of the whole results section.

- Definition 6 (p4): `δ_style(J) = R_J / β_J`. Called "the resolution limit".
- Section 4, Observation 3 (p6): "We define a judge's **measured resolution limit** as the
  smallest gap beyond which adversarial accuracy stays above 0.95."

Those are not the same quantity. One is a theoretical ratio, one is an empirical threshold
read off a curve. But both are called "the resolution limit", and Figure 3 plots one against
the other with axes "label-free predictor δ_style" and "observed resolution limit". So by
Figure 3 I finally worked out they must be different — 25 pages of reading effort later than I
should have.

Worse: Table 2 is titled "Predicting a judge's resolution limit" and lists `δ_style` as a
*predictor* of it. If `δ_style` **is** the resolution limit (Definition 6), the table is
predicting a thing with itself. I genuinely could not tell whether the central result was
circular. That is a fatal reading experience for a headline claim.

**Fix:** two distinct names, introduced together, with one sentence saying explicitly that one
is a label-free *estimate* of the other, and that the paper's claim is that the estimate is
accurate.

### B2. Symbol collision: `δ(s)` vs `δ_style`
`δ(s)` is a system's differential bias, in judge-score units. `δ_style` is a resolution limit,
in quality units. Different objects, different units, same Greek letter. Combined with B1 this
made Section 2.5 very hard.

**Fix:** rename one. `δ_style` should not be a δ at all.

### B3. Theorem 3 appears to be contradicted by Section 5
Theorem 3 (p4): no pooled metric can determine ranking validity — there exist judges with equal
pooled score and opposite ranking accuracy.

Section 5 (p7): pooled accuracy predicts the resolution limit at ρ = −0.89, robustly, across
five compositions.

On first read these flatly contradict. I wrote "??" in the margin. The reconciliation —
Theorem 3 is a worst-case non-identifiability result, Section 5 is a typical-case empirical
correlation over one particular judge pool — is *never stated*. The paper needs one paragraph
saying "these are consistent, and here is why", or a reviewer will call it an internal
inconsistency. Right now Contribution 2 and Section 5 read as if written by different people.

### B4. How can a resolution limit be 0.83% when there are only 6 claims per answer?
One claim out of six is 16.7%. The finest possible difference on a *single answer* is 16.7%.
So what does "resolves 0.83% of an answer's factual content" mean? I stared at this for a
while. I *think* the answer is that quality is a system-level average over 85 items, and the
mixture construction moves a fraction of items between corruption levels, so system-level gaps
are continuous and can be far below 1/6. But the paper never says this, and "% of an answer's
factual content" actively points the reader at a single answer.

**Fix:** say it explicitly, and consider changing the phrasing to "% of factual content,
averaged over the evaluation set".

### B5. SRA is used but never defined
Theorem 3 states `SRA(J₁) = 1` and `SRA(J₂) = 0`. SRA is never defined anywhere in the main
text. Section 4 uses the phrase "system ranking accuracy" but never connects it to the acronym
or gives a formula. I had to guess.

---

## Serious but not blocking

### S1. There is no example of an actual item, answer, or corruption
This is a *benchmark* paper. I finished it without ever seeing one question, one atomic claim,
one corrupted claim, or one rendered answer in any of the three styles. I am asked to believe
the corruptions are "minimal and plausible" and that restyling "changes no factual content", on
assertion. One concrete example would do more for my confidence than a page of validation
statistics.

### S2. The three styles are never described
"plain, polished, padded" appear in Section 3 as bare names. The only hint about what they mean
is "verbose, hedged" in the worked example. What is "polished"? Bullets? Headings? I cannot
judge whether the transformation family is reasonable without knowing what is in it — and the
entire certificate is explicitly *relative to* that family, so this is load-bearing.

### S3. Section 2 depends on Section 3
The worked example (p2) talks about "85 questions", "six atomic reference facts", "plain prose",
"verbose hedged style" and forward-references Section 3.1 for verification. But the benchmark
is not described until p5. I had to hold four undefined constructs in my head for three pages.

### S4. Where does the (0.8%, 16.7%] range in Section 6 come from?
The headline certificate numbers (0.860 → 0.969) are computed over pairs "with true quality gaps
uniform in (0.8%, 16.7%]". Both the range and the uniformity are choices, and they directly set
the headline. Why that range? Why uniform rather than something matched to a real leaderboard?
Without justification the headline reads as tunable.

### S5. The α-cancels remark is confusing
"The common offset µ and the intercept α cancel exactly." α is a constant in Equation 1, so of
course it cancels in a difference; saying so suggests it was ever at risk. It made me re-read
Equation 1 looking for something I had missed.

### S6. "28 judges" vs "28 judge configurations"
Used interchangeably. There are 8 models. Early on I thought there were 28 models and wondered
where they came from.

### S7. Section 7 (real systems) does not tell me what to do with it
It says the certificate "still separates" and simultaneously "not a second validation of the
certificate". So do I count this evidence or not? The honesty is welcome but the reader is left
without a verdict.

---

## Minor

- m1. Theorem 3 uses `n` before it is defined ("within-label score spread scaled by m/n").
- m2. Section 2.2 says q ranges over {0, 1/6, …, 1}, but the actual design only uses k ∈ {0..4},
  so Q ∈ [2/6, 1]. A careful reader notices the mismatch.
- m3. The COT protocol is named but never described. RUBRIC likewise — what is in the rubric?
- m4. "Preprint. ∗indicates equal contribution." on p1 — leftover template artifact, no starred
  authors exist.
- m5. Figure 1's x-axis starts at 10⁰ with no units stated in the caption body (it is "%", in
  the axis label only). Log axis on a percentage confuses at a glance.
- m6. Figure 3(a) title says "resid 3.2%" while Table 2 says 3.3% for the same quantity.
- m7. Abstract says "declining to certify the pairs on which accuracy is 0.721" — grammatically
  suggests it declines *because* accuracy is 0.721. It is the other way round.
- m8. Table 1 rows say "B (wrong)" — took a beat to realise "wrong" labels the judge, not B.

---

## What I would write in the review box

*Summary.* Proposes that LLM judges should be characterised by a "resolution limit" — the
smallest true quality difference they can order reliably when systems differ in surface form —
and gives a label-free way to estimate it, plus a per-comparison certificate. Constructs ground
truth rather than annotating it, which is a genuinely nice methodological move.

*Strengths.* The construction-based ground truth is clever and well validated. The negative
results are reported rather than buried, which is rare and increased my trust. The
certificate's coverage/soundness framing is practically useful. Experiments are large.

*Weaknesses.* Presentation. The central quantity is given two meanings under one name, which
made me suspect the main result was circular. A headline theorem appears to contradict a
headline experiment with no reconciliation offered. No example of the actual data. Several
undefined symbols.

*Score.* Borderline, leaning accept on content, but the presentation issues are severe enough
that I would not fight for it. Almost all of it is fixable without new experiments.

---

## Fix list, prioritised

1. [B1] Split the two "resolution limit" senses; rename and cross-reference.
2. [B2] Rename `δ_style` so it stops colliding with `δ(s)`.
3. [B3] Add an explicit worst-case/typical-case reconciliation of Theorem 3 with Section 5.
4. [B4] Explain that quality gaps are system-level averages; fix "% of an answer's" phrasing.
5. [B5] Define SRA where it is first used.
6. [S1/S2] Add a concrete example item — question, claims, corruption, all three styles.
7. [S3] Give the benchmark a short "what the data looks like" sketch before the worked example.
8. [S4] Justify the sampling range in Section 6, and report sensitivity to it.
9. [S5–S7, m*] Local fixes.
