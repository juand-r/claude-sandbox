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

### Decision: reuse datasets that *already* have many models' completions per prompt; generate only the missing cells
The cost- and confound-minimizing move (per JdR): find datasets shaped as
`{prompt_i, {model_A: completion, model_B: completion, ..., human: completion}}`
where the **completions already exist for the same prompt**, then generate only
the cells we lack (chiefly Claude Opus 4.8, and any target model the dataset
misses). This holds topic constant for free and minimizes generation cost.

Datasets with this "many models, same prompt" shape (to verify in Phase 0):
- **AlpacaEval** — ~805 fixed instructions answered by *dozens* of models;
  per-model `model_outputs` are published. Strong free source for GPT/Gemini/
  DeepSeek/Qwen/Phi/Llama completions on identical prompts.
- **MT-Bench** — 80 questions, **2-turn**, many models' answers published
  (also our cheapest existing handle on the multi-turn question — see §9).
- **Arena-Hard-Auto / Chatbot Arena** — many model answers per hard prompt.
- **RAID / M4** — same prompts across many generators (older Claude, useful as
  baselines and for method validation).

We then generate the **Claude Opus 4.8** completions on those same prompts, plus
any of the five target contrast models a given dataset is missing.

### Resolved design parameters (from iteration with JdR)
- **Contrast models:** 2× GPT, 1× Gemini, 1× DeepSeek, 1× Qwen — plus *reuse*
  any other models present in the source datasets (Phi, Llama, etc.) as bonus
  references. Reuse from datasets where possible; generate only what's missing.
- **Claude:** Opus 4.8. Optionally sweep **thinking effort** (low/med/high) as a
  within-Claude variable — deferred toggle, not required for the first cut.
- **"Genre" → two cleaner axes.** "Open Q&A" is a *task type*, not a genre. We
  separate **domain** (topic: science, history, coding, finance, …) from
  **task/format type** (Q&A, explanation, email/message, summary, creative).
  Pilot: whatever the chosen source datasets already cover (likely
  instruction-following Q&A + explanation); add email and others later.
- **Pilot scale:** 200 prompts.
- **Human anchor:** use all available license-clean sources (ELI5 /
  StackExchange / HC3-human / arena), pooled.

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

- **Phase 0 — Infra & pilot corpus.** 200 prompts. Identify source datasets with
  many-models-per-prompt completions; reuse contrast cells (2× GPT, Gemini,
  DeepSeek, Qwen, + bonus Phi/Llama) and the human anchor; generate only the
  missing cells (chiefly Claude Opus 4.8). Repo skeleton, generation script with
  controls (version, effort, prompt, domain, task-type), storage format.
  **Cost-check before generating (see §9).**
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

## 8. Decisions — RESOLVED (iteration 2)
1. Contrast models: 2× GPT, 1× Gemini, 1× DeepSeek, 1× Qwen; reuse Phi/Llama/etc. if present in source datasets. ✔
2. Claude: Opus 4.8; thinking-effort sweep optional/deferred. ✔
3. Genre reframed as **domain × task-type**; pilot uses what source datasets cover. ✔
4. Pilot scale: 200 prompts. ✔
5. Human anchor: all available license-clean sources, pooled. ✔

Remaining for me to settle in Phase 0 (no blocking input needed): exact source
datasets, which contrast cells must be self-generated vs reused, generation SDKs
for non-Claude models.

---

## 9. Cost estimate (BEFORE any generation — per JdR's requirement)

**Pricing (verified via claude-api skill, 2026-06-24):** Opus 4.8 = **$5.00 / 1M
input tokens, $25.00 / 1M output tokens**. **Batch API = flat 50% off** both.

**What we pay for:** only the cells we generate ourselves. Contrast-model
completions reused from AlpacaEval/MT-Bench/etc. cost **$0**. The dominant cost
is generating Claude Opus 4.8 on the 200 pilot prompts.

**Assumptions per prompt:** ~200 input tokens (prompt + small system), and
output that depends on whether thinking is on:

| Scenario | Output tok/prompt | Cost/prompt | × 200 prompts | With Batch −50% |
|---|---|---|---|---|
| No thinking (plain Q&A) | ~600 | $0.016 | **$3.20** | **$1.60** |
| High thinking effort | ~2,000 | $0.051 | **$10.20** | **$5.10** |
| 3-effort sweep (low/med/high) | ~600+1200+2000 | — | **~$19** | **~$9.50** |

**Pilot total: single-digit dollars** (~$2 without a thinking sweep, ~$10–20 with
one). If we must also self-generate some contrast models (e.g. a model absent
from the datasets) via their own APIs, add roughly a few dollars each — GPT/Gemini
comparable per-token, DeepSeek/Qwen much cheaper. **Order of magnitude for the
whole pilot: well under $50.**

**Scaling note:** even a 10× larger study (2,000 prompts) with a multi-version
Claude sweep stays in the low hundreds of dollars. Generation cost is not the
binding constraint here; careful corpus design is. I will report actual spend
after Phase 0 and will not exceed the pilot scope without checking first.

---

## 10. Does some Claudespeak only emerge in multi-turn? (JdR follow-up)

**Hypothesis: yes, plausibly.** Several candidate Claudeisms are turn-dependent —
escalating sycophancy/agreement, persona drift, the recap-and-offer-next-step
closing move, growing verbosity, and "Great question!" re-openers. The Sense B
attractor (§Appendix) is *inherently* multi-turn and only appears over many turns.

**Data we have for it, cheapest first:**
- **MT-Bench** — 2-turn, many models, **parallel** (same prompts). Lets us test
  single- vs second-turn style shifts *comparatively* at near-zero cost. Best
  existing handle.
- **LMSYS-Chat-1M / WildChat** — genuinely long multi-turn, but **one model per
  conversation** (not parallel) and mostly non-Claude / old-Claude. Usable for
  characterizing *within-model* turn dynamics, not clean cross-model contrast.
- **Self-generated** — to get long, parallel, recent-Claude multi-turn we would
  script fixed multi-turn scenarios and run each model through them. This is the
  bridge to Sense B/C and a natural Phase 5 item.

**Plan:** treat turn-position as a variable from Phase 1 (single-turn now), add
MT-Bench's 2-turn contrast as a low-cost probe, and reserve long-horizon
multi-turn elicitation for Phase 5.

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
