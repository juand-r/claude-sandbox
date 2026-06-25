# Claudespeak — consolidated findings (pilot, Phases 1–2)

**Date:** 2026-06-24 · **Scope:** Claude Opus 4.8 (effort=high, adaptive thinking),
characterized comparatively against human writing and other LLMs on two
topic-matched parallel corpora. This consolidates Steps 1–5 of `PLAN_phase2.md`.
Per-step detail lives in the sibling reports; this is the argument and the bottom
line, with boundaries stated.

## The claim in one paragraph

Claude has a real, measurable writing style that is **identifiable from prose
alone** — not merely from its markdown formatting, and **not** from the
stereotyped "delve" vocabulary (which is a GPT trait Claude actually avoids).
Claude's fingerprint is **structural, rhythmic, and interactional**: heavy
markdown scaffolding; markedly higher sentence-length variability; denser
content-word usage; a strong em-dash habit; and — most diagnostically — a
verbatim *offer-to-continue closing move* ("would you like me to go deeper
into…") that no other source in our data ever produces. A simple classifier
separates Claude from six modern models at AUC 0.87 on prose alone.

## Evidence base

Two parallel corpora, every cell saved with full provenance (`data/corpus/`):

| Track | Prompts | Sources (same prompt each) |
|---|---|---|
| HC3 (human-anchored) | 200, 5 domains | human, old-ChatGPT (GPT-3.5), GPT-4o, **Claude Opus 4.8** |
| AlpacaEval (modern models) | 200 instructions | gpt-4-turbo, gpt-4o, gemini-pro, deepseek-67b, Qwen2-72B, Llama-3-70B, **Claude Opus 4.8** |

Claude (and GPT-4o on HC3) self-generated; all other cells reused from the source
datasets. Topic is held constant across sources within each track.

## What Claudespeak *is* (the characterization)

**1. Structural — heavy markdown** (Step 1). Bold 4.45/100w, bullets 3.86, headers
1.75, where human and old-ChatGPT use essentially none (Cohen's d ≈ 2–3). Real,
but a formatting habit — so we tested whether anything survives stripping it.

**2. Rhythmic — survives markdown stripping** (Steps 1–2, the load-bearing result).
On raw prose, Claude still separates by:
- **Sentence-length burstiness** — it interleaves short and long sentences far
  more than anyone else (length-controlled OLS t = 20.6).
- **Content-word density** — lower function-word rate (t = −14.4).
- **Em-dash habit** (t = 12.6).
These survive controlling for answer length, and **replicate against six modern
models** on AlpacaEval (burstiness d = 1.01, em-dash d = 0.63).

**3. Interactional — the offer-to-continue closer** (Steps 1 & 5, the most
diagnostic Claudeism). Data-driven n-gram mining and arbitrary-length
suffix-automaton mining both surface the same template. Spans up to **8 words**
that Claude emits dozens of times and that occur **zero times across humans + all
six other models combined**: "would you like me to explain any", "would you like
me to go deeper into", "would you like me to expand on any". Its anti-signature is
the formal frame **"it is important to"** — a GPT-ism Claude underuses.

**4. Lexical — conversational, not "delve"** (lexicon review + Step 3). Claude
leans on subjective/casual markers ("actually" ~6× GPT-4o, "feel", "it's worth").
This is a *secondary* signal beneath the structural one.

## What Claudespeak is *not*

**The "delve" vocabulary is a GPT/other-model trait, and Claude is the cleanest
frontier model on it** (lexicon review + Step 3). In the essay genre that elicits
these words, Claude is the **only** model with zero "delve"/"delves" and the
**lowest** "crucial" usage of all seven (0.039 vs GPT-4-turbo 0.42). The popular
"AI overuses delve" belief is true — for GPT — and is the opposite of a Claude
signature. (This corrected an early overclaim; see `LITREVIEW_lexical_tics.md`.)

## How separable is it (Step 4)

Logistic regression on interpretable features, 5-fold CV:

| Track | with formatting | prose only |
|---|---|---|
| HC3 (vs human / GPT-4o / old-ChatGPT) | AUC 0.982 | 0.946 |
| AlpacaEval (vs 6 modern models) | AUC 0.901 | 0.867 |

Stripping markdown barely dents it, and the driving coefficients are exactly the
features above — an independent-method confirmation of the characterization.
Step 5 adds that Claude also has the **highest n-gram novelty** of all sources
(its phrasing overlaps least with the pool).

## Boundaries (do not over-read)

- **One Claude configuration** (Opus 4.8, effort=high). Effort/thinking sweeps and
  other versions are untested — an obvious next axis.
- **Two genres** (Q&A, instructions), English only.
- **Reused contrast models are their published vintages** (gemini-pro 1.0,
  deepseek-67b, Qwen2-72B, GPT-4-turbo/4o 2024) — modern-ish, not absolute latest.
- **n-gram novelty is relative to our pool**, not an absolute-creativity claim.
- **Human anchor is informal web text** (HC3); part of the human–Claude gap is
  register, not authorship.

## Bottom line

Across two corpora, four methods (effect sizes, log-odds n-grams, a classifier,
suffix-automaton mining), and against humans plus seven other models, the same
fingerprint recurs and survives every control: **Claudespeak = markdown-scaffolded,
rhythmically varied, content-dense, engagement-and-offer-oriented prose — and
specifically not the "delve" register.** The most quotable single artifact is the
closer no one else writes: *"Would you like me to go deeper into any of these?"*

## Reproduce
See `README.md`. Pipeline: `acquire_hc3.py` / `acquire_alpacaeval.py` →
`generate_pilot.py` / `generate_alpaca.py` → `analyze_pilot.py`,
`analyze_ablation.py`, `analyze_lexicon.py`, `ngram_signature.py`,
`analyze_length_control.py`, `analyze_alpaca.py`, `classify.py`,
`rusty_dawg_mine.py`. Reports in `reports/`.
