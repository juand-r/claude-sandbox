# Phase 3.0 — Coverage assessment & corpus expansion (do BEFORE Exp A/B/C)

Motivation (JdR): our findings so far characterize Claude's voice on a **narrow
slice** — single-turn, cooperative, informational/instructional prompts. Many
characteristic behaviors (e.g. the concession move *"you're right to push back on
that"*) are only elicited by contexts our corpus lacks. Before scaling the
secondary experiments, audit coverage and broaden it. The audit must be
reproducible and feed a Dataset-statistics section in the paper.

## 1. What we measured (reproducible audit)

Instruments (re-runnable on any future corpus):
- `src/analyze_coverage.py` → `data/corpus/coverage_labels.csv` (LLM intent labels
  + flags: subjective / sensitive / multiturn_implied).
- `src/dataset_stats.py` → `reports/dataset_stats.md` + `stats_*.csv` (volume by
  source/domain, prompt & response length distributions, sentence-mood split,
  register signals, intent distribution).

Findings (400 prompts):
- **Intent is skewed to information delivery.** HC3 is 48% explanation / 28%
  factual-QA / 23% advice (≈0% code/creative/opinion/emotional). AlpacaEval is
  broader (creative 12%, math 8%, code 5%, opinion 6%) but still dominated by
  explanation/advice/instruction.
- **Interaction is single-turn and cooperative.** `multiturn_implied` ≈ **2%**
  (8/400); essentially **no adversarial/corrective** context. `personal_emotional`
  ≈ 1, `roleplay` ≈ 2.
- **Stance is rarely contested.** subjective 48/400; the corpus almost never asks
  Claude to take or defend a position, agree/disagree, or be corrected.

Conclusion: we have **one quadrant** (single-turn × cooperative × informational).
Behaviors gated on other quadrants are invisible to the current study.

## 2. Target coverage (what "enough" looks like)

Coverage is not just *n per cell* (we have ample power: huge effect sizes at
n=200); it is **breadth of cells**. We define cells along three axes and aim to
populate the currently-empty ones:

- **Intent / task type:** factual-QA, explanation, instruction, code, creative,
  summarize/edit, advice, opinion/persuasion, math/reasoning,
  personal/emotional, roleplay, classification/extraction.
- **Interaction structure:** single-turn; multi-turn cooperative follow-up;
  **multi-turn corrective** (user pushes back / corrects Claude — rightly or
  wrongly); multi-turn escalating.
- **Stance / stakes:** neutral-informational; subjective/opinion;
  sensitive/safety; interpersonal/emotional.

Anchor the *relative* targets to real usage so the corpus is representative, not
arbitrary: sample/condition on public real-conversation distributions
(WildChat, LMSYS-Chat-1M; cf. usage taxonomies like Anthropic's Clio) rather than
inventing proportions.

## 3. Expansion plan

### 3a. Broaden single-turn intent coverage (found data)
Add prompts per under-covered category from existing sources, then generate
Claude (+ reuse others where parallel):
- **Real-usage prompts:** sample first-turn user messages from **WildChat** and
  **LMSYS-Chat-1M**, stratified to fill the taxonomy and to match real-usage
  proportions. (These also bring code/creative/emotional/opinion naturally.)
- **Targeted sets** where a clean source exists: code (e.g. MBPP/HumanEval-style
  asks), creative (writing-prompts), emotional (EmpatheticDialogues-style),
  opinion/persuasion (debate/CMV-style first turns).
- Target: ~100–150 prompts per major intent cell.

### 3b. Elicit multi-turn corrective behavior (constructed — the key gap)
The *"you're right to push back"* class needs scenarios, not found prompts. Build
a small scenario generator:
- **Push-back scenario:** prompt → Claude answers → user turn that challenges the
  answer ("I don't think that's right because…"); record Claude's turn-2.
- **User-correction scenario:** user asserts a correction (sometimes valid,
  sometimes subtly wrong) → does Claude concede, hold, or over-concede
  (sycophancy)? Vary correctness to probe sycophancy vs. integrity.
- **Contested-claim scenario:** user states something dubious as fact → does
  Claude challenge or defer?
- Seeds drawn from the broadened intent set so topic varies. Target ~80–120
  two/three-turn scenarios. Reuse the schema (`conversation_id`, `turn_index`).
- Metrics: rate of concession markers ("you're right", "good point", "I was
  wrong", "fair", "I'd push back"), agreement vs. disagreement, stance changes.

### 3c. Sensitive / refusal register (small, careful, defensive framing)
A modest set of policy-relevant requests (from an established refusal/safety
benchmark) to characterize Claude's refusal and hedging register vs others.
Keep small and clearly scoped; report aggregate features only.

## 4. How much do we need (power & sizing)
- Per-cell estimation: n≈100–150 gives tight CIs on feature *rates*; effect sizes
  here are large, so this is comfortable. Rare templates (offer-closer) were
  detectable at n=200 — keep ≥100 where a phrase-level claim is intended.
- Breadth over depth: prioritize covering empty cells over adding more
  informational-QA prompts.
- Cost (Opus 4.8, batch −50%): each ~100–150-prompt cell ≈ $2–8 to generate
  Claude; reuse keeps other models free where parallel.

## 5. Reproducibility & paper
- The two audit scripts are the instrument; re-run after each expansion to refresh
  `reports/dataset_stats.md`.
- Paper gets a **Corpus statistics** section (volume by domain; prompt/response
  length distributions; sentence-mood and register splits; intent-coverage table)
  and an explicit coverage-scope statement in Limitations + this expansion as
  future work.

## 6. Sequencing
1. (done) Audit instruments + current-corpus stats.
2. Paper: add Corpus-statistics section + coverage caveat.
3. 3a broaden single-turn intent (WildChat/LMSYS sample).  ← biggest coverage win
4. 3b multi-turn corrective elicitation.  ← unlocks "you're right to push back"
5. 3c sensitive/refusal (small).
6. THEN revisit Exp A/B/C (PLAN_phase3.md) on the broadened corpus.

Open questions for JdR (sizing/scope): how representative vs. how broad (match
real-usage proportions, or balance cells equally?); include sensitive/refusal
(3c) or defer?; total generation budget ceiling for the expansion.
