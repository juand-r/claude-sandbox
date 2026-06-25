# Claudespeak — Phase 2 execution plan (ordered, locked)

Approved sequence (JdR, 2026-06-24): do these in order, end with full rusty-dawg.
Each step ends with a committed deliverable + a one-line checkpoint in NOTES.md.
Do not reorder. If a step changes a prior conclusion, correct the prior report.

## Step 1 — Data-driven Claude n-gram signature  ← START HERE
**Goal:** find which unigrams/bigrams/trigrams are genuinely over-represented in
Claude vs the pooled others — *discovered*, not borrowed from AI-word lists.
**Method:** Monroe et al. "Fightin' Words" — log-odds ratio with an informative
Dirichlet prior, z-scored, so rare-token noise doesn't dominate. Claude vs pooled
{human, gpt-4o, chatgpt-hc3}; also pairwise Claude-vs-gpt-4o. n ∈ {1,2,3}.
**Deliverable:** `src/ngram_signature.py`, `reports/claude_ngram_signature.md`
(top Claudean / anti-Claudean terms with z-scores + raw freqs), CSV of scores.
**Checkpoint:** are there clear Claudean words/bigrams beyond punctuation/markdown?

## Step 2 — Length-stratified robustness
**Goal:** confirm the prose findings (sentence burstiness, function-word density,
em-dash) survive controlling for answer length — the main open threat to Result B.
**Method:** bin records by word-count quartile; recompute Claude-vs-others Cohen's
d *within* bins; also report partial correlation / regression of each feature on
source with length as covariate. Reuse `features.py` + markdown-stripped prose.
**Deliverable:** `src/analyze_length_control.py`, `reports/pilot_length_control.md`.
**Checkpoint:** do the headline prose effects hold within length bins?

## Step 3 — AlpacaEval modern-model track
**Goal:** add the modern multi-model contrast JdR asked for (2nd GPT, Gemini,
DeepSeek, Qwen, + bonus Llama/Phi) on identical instructions, reusing published
completions; self-generate only Claude (and a current GPT) on the same prompts.
Genre is instruction-following / essays — where GPT-excess words actually appear,
so we re-test the vocabulary contrast on fairer ground.
**Method:** acquire AlpacaEval `model_outputs` for several models on the 805
instructions (sample ~200, seed-fixed); normalize into corpus records with
provenance=reused; generate Claude Opus 4.8 on the same 200. Re-run Steps 1–2
features/n-grams on this track. (No human cell in this track — by design.)
**Deliverable:** `src/acquire_alpacaeval.py`, `data/corpus/alpaca_*.jsonl`,
`reports/alpaca_track.md`. Update NOTES with which models were reused.
**Checkpoint:** does the structural+rhythmic Claude signature replicate against
*modern* models (not just GPT-4o/human)? Do GPT-excess words show up GPT-side here?

## Step 4 — Interpretable classifier (separability number)
**Goal:** quantify how separable Claude is, and confirm *which* features carry it.
**Method:** logistic regression / linear SVM (Claude vs not-Claude) on the
interpretable feature set; report cross-validated accuracy/AUC and coefficients.
Two conditions: with-formatting and prose-only (markdown stripped). Also a
"no-structural-features" condition to show prose-only separability. Light, no DL.
**Deliverable:** `src/classify.py`, `reports/pilot_classifier.md` (AUC + top
coefficients per condition).
**Checkpoint:** prose-only AUC clearly above chance? coefficients match Steps 1–2?

## Step 5 — Full rusty-dawg / ∞-gram mining (finale)
**Goal:** the rigorous, arbitrary-length n-gram version of Step 1 — over-represented
multi-word spans and n-gram *novelty* of Claude vs references, at scale.
**Method:** build suffix-automaton (CDAWG) indices per source with rusty-dawg
(AI2); query span counts / novelty. Fallbacks if Rust build is hard: infini-gram
API, or a Python suffix-array — flagged loudly, not silent.
**Deliverable:** `src/rusty_dawg_mine.py` (+ build notes), `reports/ngram_dawg.md`,
and a final consolidated `reports/FINDINGS.md` tying Steps 1–5 together.
**Checkpoint:** do long over-represented spans corroborate the Step-1 signature?

## Standing rules
- Persist every generation with full metadata (schema unchanged).
- Commit + push after each step; keep NOTES.md checkpoints current.
- Keep claims inside the tested regime; separate observation/interpretation.
