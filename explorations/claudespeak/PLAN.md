# Claudespeak — Characterization Project

**Status:** DRAFT v0 — for iteration. Nothing here is final until approved.
**Date started:** 2026-06-24
**Branch:** main (per instruction)

---

## 1. What we are studying

"Claudespeak" = the recognizable stylistic fingerprint of Anthropic's Claude
models. We treat it as **one voice appearing across three communicative
contexts**:

- **A — user-facing prose** (Claude → human): the polished register. *This is the spine.*
- **B — Claude → Claude** (drift / attractor when Claude talks to copies of itself).
- **C — Claude's own thinking** (self-talk / reasoning register).

A is where we start. The feature pipeline and reference infrastructure we build
for A must carry over to B and C without redesign.

### The central question (Sense A)
Comparatively: **can we separate Claude prose from human prose and from
other-LLM prose, and — more importantly — *what features carry the signal*?**
The goal is characterization, not just a detector. A black-box classifier that
hits 99% but tells us nothing about *what* is Claude-like is a failure for this
project.

### The one confound that can sink the project
**Topic / genre / length / formatting.** If Claude answers essay prompts and the
"human" set is tweets, any model learns topic, not voice. **Mitigation: a
parallel corpus** — same prompts, multiple sources — so style is the main thing
that varies. Length and markdown formatting are secondary confounds we control
explicitly (see §5).

---

## 2. Data strategy

### Finding from the data scan (see Appendix A)
No public parallel corpus pairs the **same prompts** with answers from **recent
Claude (3.5/3.7/4.x)** + humans + current other LLMs. Old Claude-v1 exists in
LMSYS arena data, but that is not the voice we care about.

### Decision: build a parallel corpus by reusing human anchors + generating model answers
1. Take prompts **and** human answers from an existing, license-clean source
   (candidates: ELI5 / r/AskHistorians-style QA, StackExchange, HC3's human
   side, arena prompts). This gives a genuine human anchor at zero generation cost.
2. Generate answers to **the same prompts** from Claude (our target versions)
   and from 2–3 other LLMs.
3. Result: matched (prompt) × (source) cells → topic is held constant across sources.

This is incremental-friendly: start with ONE genre and a small prompt set,
validate the pipeline and the signal, then scale.

### Open decisions (need your input — see §8)
- Which **other LLMs** as contrast (default: a GPT-class, Gemini, one open model).
- Which **Claude versions** (default: Opus 4.8 only for the pilot; add Sonnet/Haiku + an older 3.x later to study intra-Claude drift).
- Which **genres** (default pilot: open Q&A; later add short essay/explanation + email/message).
- **Scale/budget** for generation (default pilot: ~100–200 prompts × ~4 sources).

---

## 3. Methods (layered; all three reinforce each other)

### (a) Descriptive stylometry
Compute interpretable features per text and compare distributions across sources:
- Lexical: function-word rates (Burrows's Delta style), type-token ratio,
  content-word density, hapax rate.
- Punctuation/orthography: em-dash rate (!), comma rate, quotation style,
  emoji, markdown markers (headers, bullets, bold).
- Syntax: sentence-length distribution + **burstiness**, POS n-grams,
  clause depth.
- Rhetoric/structure: tricolons ("X, Y, and Z"), "not just X but Y",
  hedging ("may/can/often"), intro-body-recap shape, signposting.

Deliverable: ranked tables of features most over/under-used by Claude, with
effect sizes — the quantified "Claudeisms".

### (b) n-gram mining with rusty-dawg / infini-gram
Build a suffix-automaton index per source corpus; surface multi-word sequences
**massively over-represented in Claude vs references**, and profile **n-gram
novelty** (how much of Claude's text is high-novelty vs recombined boilerplate).
This is the rigorous version of "eyeballing signature phrases."

### (c) Classifiers — interpretable first, then ML/LLM
- **Interpretable:** logistic regression / linear SVM on the §3a features →
  read the coefficients. The coefficients *are* part of the finding.
- **Embedding-based:** stronger separator to upper-bound detectability; use only
  to measure how separable, not to explain.
- **LLM-as-judge / LLM probe:** ask a model to spot and name stylistic markers;
  cross-check against the quantitative features.

### Guard against the confound, at the method level
- Match or stratify on length; also report results on length-controlled samples.
- Run an ablation **with markdown/formatting stripped** — is Claude still
  identifiable from raw prose alone? This separates "voice" from "formatting habit."

---

## 4. Phasing (start small, verify, move on)

- **Phase 0 — Infra & pilot corpus.** One genre, ~100–200 prompts, human anchor +
  Claude (Opus 4.8) + 2–3 other models. Repo skeleton, generation script with
  controls (version, effort, temperature, prompt, topic), storage format.
- **Phase 1 — Descriptive stylometry.** Run §3a; produce the first "Claudeisms"
  tables + distribution plots. **Checkpoint: is there a visible, real signal?**
- **Phase 2 — n-gram mining (rusty-dawg).** Over-representation + novelty.
- **Phase 3 — Classifiers.** Interpretable → embedding → LLM-judge; length &
  formatting ablations.
- **Phase 4 — Report.** Findings writeup (full exposition per repo guidelines).
- **Phase 5 (stretch) — Sense B/C.** Elicit Claude↔Claude drift and reasoning
  register; reuse the pipeline; test against the bliss-attractor priors.

Each phase ends with a written checkpoint and a commit. We do not proceed past a
phase whose signal is not solid.

---

## 5. Controls we hold fixed (so results are real, not artifacts)
- Same prompts across sources (topic control).
- Length: report raw + length-stratified.
- Formatting: report raw + markdown-stripped.
- Decoding: log temperature / effort / version for every Claude generation.
- Decontamination: keep prompts and answers separate; never let a classifier
  see the prompt as a feature.

---

## 6. Deliverable
Under `explorations/claudespeak/`: a reproducible pipeline (generation +
feature extraction + analysis) and a written report with findings. Notes/logs
kept as we go (NOTES.md), plan checked off here.

---

## 7. Risks / things that could go wrong
- **We measure formatting, not voice.** → markdown-stripping ablation.
- **We measure topic, not voice.** → parallel corpus.
- **Human anchor is itself contaminated** (already AI-edited text on the web). →
  prefer pre-2022 human sources where possible.
- **API access / cost** for multi-model generation. → start tiny.
- **rusty-dawg build friction** (Rust tooling). → fall back to infini-gram API
  or a Python suffix-array if needed (flagged, not silently).

---

## 8. Decisions I need from you before finalizing
1. **Other LLMs** to contrast against? (default: GPT-class + Gemini + one open)
2. **Claude versions**: pilot on Opus 4.8 only, or multi-version from the start?
3. **Genres**: start with open Q&A only, or fix the genre set now?
4. **Scale/budget** comfort for generation (pilot size)?
5. **Human-anchor source** preference (ELI5 / StackExchange / HC3-human / arena)?

---

## Appendix A — Data-availability scan (2026-06-24)

| Resource | Parallel? | Recent Claude? | Use to us |
|---|---|---|---|
| LMSYS Chatbot Arena 33K / Chat-1M | yes (pairwise) | only Claude-v1 (2023) | prompts + old-Claude baseline; not target voice |
| RAID (arXiv 2405.07940) | partial | thin/old | method baselines, detection precedent |
| HC3 (Human-ChatGPT Comparison) | yes | no Claude | human anchor + ChatGPT contrast |
| WildChat / M4 / MAGE | no / multi | little recent Claude | aux references |

**Methods / tools found:** stylometry on short samples (arXiv 2507.00838);
LLM code-authorship attribution (arXiv 2506.17323); rusty-dawg / infini-gram
n-gram novelty (arXiv 2406.13069, infini-gram.io); classic Burrows's Delta /
function-word stylometry.

**Prior work on Claude specifically (Sense B):** spiritual-bliss attractor in
the Claude-4 system card; quantitative priors exist ("consciousness" ~95.7×,
"eternal" ~53.8×, "dance" ~60× per transcript across 200 30-turn
self-conversations). Ready-made target for Phase 5.

**Bottom line:** reuse existing human prompts/answers; generate the Claude and
other-model sides ourselves to get a topic-matched parallel corpus with recent
Claude.
