# Investigation note: corpus coverage — what slice of Claude are we measuring?

**Date:** 2026-06-25 · **Trigger:** JdR observed that characteristic Claude moves
(e.g. *"you're right to push back on that"*) may never be elicited by our prompts,
and asked how good our coverage is — in both quality and prompt type — and how
much we actually need. This note records the investigation in full, because the
finding reshapes the project: **extending characterization beyond the narrow
slice we started with is itself a contribution**, not merely a limitation.

## 1. Why coverage is a first-order concern, not a detail

A stylometric characterization is only as general as the behavior it elicits. If
the prompts only ask for factual explanations, then "Claudespeak" as measured is
really "Claude's factual-explanation voice." Style is context-dependent: the
register Claude uses to refuse, to concede a point, to comfort someone, to write
code, or to push back on a wrong claim is plausibly different from its
encyclopedia voice. A claim about "Claude's style" that rests on one quadrant of
the behavior space silently overgeneralizes. This is the validity threat we
audited before investing in the secondary experiments (effort, versions,
multi-turn).

## 2. What we did (reproducible)

Two instruments, both re-runnable on any future corpus:

- **Intent audit** (`src/analyze_coverage.py`): an LLM labels every prompt with a
  primary intent from a fixed 13-category taxonomy and three interaction flags
  (subjective, sensitive, multiturn_implied). Output:
  `data/corpus/coverage_labels.csv`.
- **Dataset statistics** (`src/dataset_stats.py`): volume by source and domain;
  prompt- and response-length distributions; a sentence-mood split
  (interrogative / imperative / exclamatory / declarative); register signals
  (first/second-person pronoun rates, Flesch readability); and the intent
  distribution. Output: `reports/dataset_stats.md` + `data/corpus/stats_*.csv`.

These are deliberately separated from the analysis so the audit is an instrument
of record, not a one-off.

## 3. What we found

### 3.1 Intent is skewed to information delivery
- **HC3** (200 prompts): 48% explanation, 28% factual-QA, 23% advice; ~0% code,
  creative, opinion, or emotional. It is an informational-QA corpus by
  construction.
- **AlpacaEval** (200): broader — creative 12%, math 8%, opinion 6%, code 5%,
  classification 4%, summarize/edit 3% — but still dominated by
  explanation/advice/instruction, and still all single-turn.

### 3.2 Interaction is single-turn and cooperative
Across both tracks, `multiturn_implied` is ~**2%** (8/400). There is essentially
**no adversarial or corrective context**: the user never challenges Claude,
corrects it, or states something contestable for it to engage. `personal_emotional`
≈ 1, `roleplay` ≈ 2. The corpus cannot, even in principle, elicit concession or
push-back behavior.

### 3.3 Stance is rarely contested
Only 48/400 prompts are subjective; the corpus almost never asks Claude to hold,
defend, or revise a position. Sensitive prompts exist mostly in HC3 (66, largely
medicine), but as information requests, not as refusal-provoking asks.

### 3.3b Prompt variety is narrow on every axis (speech act, register, tone, topic)
Profiling the prompts themselves (not the responses) along several axes confirms
the uniformity:
- **Speech act:** questions (HC3 75%, AlpacaEval 53%) or directives (23% / 46%);
  **assertions $\le$1 per track.** The corpus essentially never states a claim for
  Claude to agree with, qualify, or contest.
- **Register:** neutral 65% / casual ~33% / **formal ~2%**.
- **Tone:** **neutral 82–87%**; emotional 10%/2%, playful/urgent marginal; no
  hostile prompts.
- **Topic:** concentrated (HC3: health 28%, science 24%, finance 20% = ~72% in
  three topics); `personal_life` ~0 in HC3.
This matters because the missing behaviors are *gated on the missing cells*: the
concession/push-back register needs declarative challenges (assertions), which are
absent; an emotional-support register needs emotional tone, which is marginal.

### 3.4 A coverage win that doubles as a result
The audit's statistics also produced a genuine finding. In the sentence-mood
split, Claude's responses are **17% interrogative on HC3 and 10% on AlpacaEval,
versus ≤4% for every other source** — the quantitative signature of the
offer-to-continue closer at the sentence level — and Claude's readability is
lowest (Flesch ~40 vs 46–52), consistent with its higher content-word density.
So the coverage instrument is not just bookkeeping; it independently corroborates
the fingerprint.

## 4. Interpretation

We have characterized **one quadrant**: single-turn × cooperative ×
informational/instructional. The fingerprint we report (markdown scaffolding,
sentence-length burstiness, content-word density, em-dashes, the offer-closer) is
robust *within that quadrant*, replicated across two corpora and eight comparison
sources. But behaviors gated on the other quadrants — corrective concession,
sycophancy under pressure, refusal register, emotional-support voice, code and
creative registers — are outside what we have observed. The *"you're right to
push back"* move is the clean example: it is structurally impossible to observe
without a multi-turn challenge, of which we have almost none.

## 5. How much do we need

The binding constraint is **breadth of cells, not samples per cell.** Our effect
sizes are large and stable at n=200, and even phrase-level templates (the
offer-closer) were detectable at that n; so depth is already sufficient where a
cell is populated. What is missing is whole cells. The plan therefore prioritizes
*populating empty cells* over adding more informational-QA prompts, targeting
~100–150 prompts per major intent cell and ~80–120 constructed multi-turn
corrective scenarios. Relative proportions should be anchored to real-usage
distributions (WildChat, LMSYS-Chat-1M) so the expanded corpus is representative
rather than arbitrary. Full design in `PLAN_coverage.md`.

## 6. Why this is a contribution, not just a caveat

Most LLM-stylometry work characterizes models on convenient single-turn,
cooperative prompts (detection benchmarks, instruction sets). Treating the
**behavior space itself as the object of study** — defining a coverage taxonomy
(intent × interaction structure × stance), measuring where existing corpora sit,
and deliberately extending characterization into the under-observed cells
(multi-turn corrective, contested-stance, sensitive, emotional, code/creative) —
is a methodological contribution of this work. The headline empirical example we
will pursue first is the concession/push-back register, which the current
literature and corpora do not isolate.

## 7. Status / next
- Audit instruments + current-corpus stats: **done** (this note,
  `reports/dataset_stats.md`).
- Paper: add a Corpus-statistics section and a coverage contribution + scope
  statement: **in progress**.
- Expansion (PLAN_coverage.md §3): broaden single-turn intent → construct
  multi-turn corrective scenarios → small sensitive/refusal set → then revisit
  Exp A/B/C on the broadened corpus.
- Open scope questions for JdR: representative vs. balanced proportions; include
  sensitive/refusal now or defer; generation-budget ceiling for expansion.
