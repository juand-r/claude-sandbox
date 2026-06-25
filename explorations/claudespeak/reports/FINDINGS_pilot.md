# Pilot findings — Claudespeak, human-anchored (HC3) track

**Date:** 2026-06-24 · **Phase:** 1 (descriptive stylometry) · **Status:** first cut

This reports the first verifiable result of the Claudespeak project: a comparative
stylometric characterization of Claude Opus 4.8 against a human anchor and two
other models, on a topic-matched parallel corpus. It is deliberately scoped to
one corpus track and one Claude configuration; the boundary conditions are stated
throughout so the claims are not over-read.

## 1. Corpus

Source: **HC3** (`Hello-SimpleAI/HC3`). We sampled **200 questions**, 40 from each
of five domains (reddit-ELI5, open-QA, finance, medicine, CS/AI; seed 42),
collapsed for reporting into general (80), finance (40), medicine (40),
CS/AI (40). For every question we hold four parallel cells — the *same prompt*
answered by four sources:

| Source | Role | Provenance |
|---|---|---|
| `human` | human anchor | reused from HC3 (pre-2023 web text) |
| `chatgpt-hc3` | old-model baseline | reused from HC3 (GPT-3.5 era, early 2023) |
| `gpt-4o` | modern non-Claude contrast | self-generated (temp 1.0) |
| `claude-opus-4-8` | target | self-generated (adaptive thinking, effort=high) |

Because the prompt is held constant across sources, topic is controlled: a feature
that separates Claude is a property of *how it writes*, not *what it was asked*.

Every generation is stored with full provenance (model/version, decoding config,
token usage, timestamp, git commit) under `data/corpus/`, plus verbatim API
responses under `data/raw_responses/`. Nothing needs regenerating to rerun any
downstream analysis.

## 2. Method

Per response we compute interpretable features (rates per 100 or 1000 words so
length does not dominate): lexical (type-token ratio, hapax rate, function-word
rate), punctuation/orthography (em-dash, colon, question, exclamation, emoji),
syntax (mean sentence length, sentence-length **burstiness** = std/mean of
words-per-sentence), markdown/structure, and rhetoric/known-LLM tics. We rank
features by **Cohen's d** of Claude vs each other source, and average |d| across
the three comparisons. Code: `src/features.py`, `src/analyze_pilot.py`.

## 3. Result A — there is a large, visible Claude signal

The Phase-1 checkpoint ("is there a real signal?") is answered decisively: yes.
The strongest separators (mean |d| across the three contrasts):

| Feature | mean \|d\| | Claude | human | gpt-4o | chatgpt-hc3 |
|---|---|---|---|---|---|
| markdown headers /100w | 2.90 | 1.75 | 0 | 0.02 | 0 |
| markdown bold /100w | 2.31 | 4.45 | 0 | 1.40 | 0 |
| markdown bullets /100w | 1.81 | 3.86 | 0 | 1.62 | 0.01 |
| sentence burstiness | 1.49 | 0.86 | 0.37 | 0.55 | 0.36 |
| function-word rate | 1.47 | 0.33 | 0.41 | 0.37 | 0.44 |
| em-dash /100w | 0.78 | 0.88 | 0.15 | 0.40 | 0.01 |

**Observation.** The single most Claude-distinguishing trait is heavy markdown
scaffolding — headers, bold, and bullets that the human and old-ChatGPT cells use
essentially never, and that GPT-4o uses far less. Effect sizes of d≈2–3 are very
large.

**Interpretation, with the obvious caveat.** Most of the top raw signal is
*formatting*, not prose. This is exactly the confound flagged in the plan: a
classifier handed these texts would learn "has markdown headers → Claude" and
tell us little about voice. So the formatting result, while real, is not yet a
claim about Claudespeak as a *writing style*.

## 4. Result B — the voice survives markdown stripping (the load-bearing finding)

We strip all markdown markup (headers, bullet markers, bold/italic, code fences,
links → text), keep the underlying words, and recompute on prose only
(`src/analyze_ablation.py`). Claude still separates strongly:

| Prose feature (markdown stripped) | mean \|d\| | Claude | human | gpt-4o | chatgpt-hc3 |
|---|---|---|---|---|---|
| sentence burstiness | 1.69 | 0.86 | 0.37 | 0.55 | 0.36 |
| function-word rate | 1.47 | 0.33 | 0.41 | 0.37 | 0.44 |
| em-dash /100w | 0.87 | 0.88 | 0.15 | 0.40 | 0.01 |
| colon /100w | 0.84 | 1.41 | 0.24 | 1.69 | 0.40 |
| question /100w | 0.82 | 0.61 | 0.28 | 0.01 | 0.07 |

**Observation.** With formatting removed, three prose features still carry a large
signal: Claude's **sentence-length rhythm is far more variable** (burstiness 0.86
vs 0.36–0.55 — it interleaves short punchy sentences with long ones), its prose is
**denser in content words** (function-word rate 0.33 vs 0.37–0.44), and it retains
its **em-dash habit** (0.88/100w vs ≤0.40 elsewhere).

**Interpretation.** Claudespeak is *more than a formatting habit*. Even reduced to
raw prose, Opus 4.8 is identifiable by rhythm and lexical density. This is the
first defensible piece of the characterization.

## 5. Result C — the "delve" vocabulary is a GPT signature, not a Claude one

> **Refined after literature review** (see `reports/LITREVIEW_lexical_tics.md`).
> The pilot's first pass lumped the stereotyped "LLM tics" into one list and found
> they barely separate Claude (mean |d| ≈ 0.15). That list was effectively a list
> of *ChatGPT/GPT* excess words, so the null for Claude is correct and expected.

- **The stereotyped tic vocabulary (delve, crucial, intricate, comprehensive, …)
  is a GPT/ChatGPT signature.** Kobak et al. (Science Advances 2024) tie the
  post-ChatGPT "excess vocabulary" surge to ChatGPT; the "delve" origin story is
  about OpenAI's RLHF pipeline. In our corpus, **GPT-4o uses every excess word
  more than Claude** — "crucial" 0.73 vs 0.04 /1k (~18×); "delve" itself appears
  zero times (and is not a Claude word regardless). So the popular belief holds —
  *for GPT* — and was never a Claude property.
- **Claude has its own, different lexical lean: conversational/subjective markers**
  — "actually" (1.38/1k, ~6× GPT-4o), "feel", "it's worth", "think". This matches
  a published Claude-vs-GPT-4o contrast (arXiv 2502.08972: Claude favors casual
  "believe"/"feel that"/"kind of"; GPT favors formal "crucial to"). But it is a
  **secondary** signal — smaller than Claude's structural/rhythmic fingerprint.
- **Claude is *less* lexically diverse than humans** (type-token ratio 0.62 vs
  0.73, hapax 0.46 vs 0.59); the sign flips only against GPT-3.5-era text.

Net: Claude's identity here is **structural and rhythmic first** (markdown,
burstiness, function-word density, em-dashes), with a **conversational lexical
lean second** — and it is specifically NOT the delve-class vocabulary that the
popular discourse (correctly) pins on GPT.

## 6. Boundary conditions (do not over-read)

- **One corpus track.** HC3 gives a clean human anchor but only an *old* model
  (GPT-3.5) plus the GPT-4o we generated as modern non-Claude contrast. The
  user-named modern models (Gemini, DeepSeek, Qwen, a second GPT) are not here yet
  — that is the AlpacaEval track (Phase 0b, next).
- **One Claude configuration** (effort=high, adaptive thinking). Effort and
  thinking on/off are uncontrolled here; an effort sweep is planned.
- **Length is normalized but not fully controlled.** Features are per-100/1000
  words, but Claude and old-ChatGPT write longer answers (mean sentence ~27 words)
  than GPT-4o (~16) and human (~23); burstiness and function-word rate could still
  interact with length/genre. A length-stratified re-run is the next robustness
  check.
- **Human anchor is informal web text.** HC3 humans are reddit/wiki writers, not
  professional authors; the human–Claude gap partly reflects register, not just
  authorship.

## 7. What this licenses, and what's next

Licensed claim: *On topic-matched Q&A, Claude Opus 4.8 has a distinctive style
that persists beyond markdown — markedly higher sentence-length variability,
denser content-word usage, and a strong em-dash habit — while NOT being
characterized by the stereotyped "delve"-class vocabulary, and being less
lexically diverse than human writers.*

Next steps (Phase 0b/1 continuation):
1. **Length-stratified re-run** of §4 to confirm burstiness/density survive length control.
2. **AlpacaEval track** — add Gemini/DeepSeek/Qwen/Llama/Phi (reused) + Claude on
   identical instructions, for modern multi-model contrast.
3. **Effort sweep** (low/med/high) as a within-Claude variable.
4. **n-gram mining (rusty-dawg / infini-gram)** for over-represented multi-word
   sequences — the rigorous version of the "Claudeisms" list.
5. **Interpretable classifier** on prose-only features to quantify separability.
