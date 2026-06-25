# Critical review of `paper/main.tex` (Claudespeak draft)

Reviewer stance: adversarial but constructive, as if refereeing for an *ACL
short/long paper. Severity tags: **[BLOCKER]** (wrong/inconsistent, must fix),
**[MAJOR]** (weakens the paper, should fix), **[MINOR]** (polish). Line/section
pointers are to the current `main.tex`.

## Summary judgment
The core story is clear, well-motivated, and unusually well-controlled for this
genre (parallel corpora, length control, four/five converging methods, an honest
coverage audit). The delve reconciliation and the offer-closer are genuinely
novel, quotable findings. But the draft has **internal numerical inconsistencies
(two different coverage runs and two different "mood" measures mixed together)**,
a **methodological circularity in the coverage audit that is currently
unstated**, and several **over-strong absolute claims** that need scoping. None
are fatal; all are fixable. It is not submittable as-is, but it is close.

---

## BLOCKERS (internal inconsistency / correctness)

### B1. Stale numbers: intent table + flags are from an old run
`Table~\ref{tab:coverage}` (intent distribution, lines ~201–213) and its flag
rows do **not** match the regenerated `coverage_labels.csv`:

| cell | paper | current CSV |
|---|---|---|
| explanation HC3 / Alpaca | 95 / 34 | **94 / 33** |
| factual QA HC3 / Alpaca | 55 / 28 | **53 / 29** |
| advice HC3 / Alpaca | 46 / 31 | **49 / 31** |
| instruction HC3 / Alpaca | 2 / 29 | **3 / 26** |
| creative Alpaca | 23 | **24** |
| math Alpaca | 15 | **14** |
| code Alpaca | 10 | **11** |
| multi-turn flag HC3 / Alpaca | 5 / 3 | **8 / 4** |
| subjective flag HC3 / Alpaca | 13 / 35 | **14 / 39** |

The intent table came from the first coverage run; the appendix variety table
(`Table~\ref{tab:variety}`) came from the **second** run. **All audit numbers in
the paper must come from one run.** Regenerate the table from the current CSV (or
re-run the audit once and freeze it). This is the kind of thing a reviewer checks
against released data and it currently fails.

### B2. Two conflicting "mood" measures presented as if one
- §\ref{sec:coverage} bullet 1 reports a **syntactic** prompt mood
  (`stats_prompt_mood.csv`): HC3 74% interrogative / 2% imperative / 24%
  declarative; Alpaca 58% / 20% / 21%.
- `Table~\ref{tab:variety}` reports an **LLM "speech act"**: HC3 question 150,
  directive 46 (=75% / 23%); Alpaca question 106, directive 93 (=53% / 46%).

For AlpacaEval these disagree sharply: **imperative 20% (syntactic) vs directive
46% (LLM)**. Both are defensible (syntax vs pragmatics: "Can you write…?" is
syntactically interrogative but pragmatically a directive), but the paper never
says they are two different constructs, so they read as a contradiction. Fix:
name them distinctly ("syntactic mood" vs "pragmatic speech act"), and either
reconcile or drop one. Right now a careful reader loses trust here.

### B3. Method count contradicts itself
Abstract + Intro say **five** methods (stylometry, log-odds n-gram,
length-controlled regression, classifier, suffix-automaton). Discussion (line
~373) says "**four** methods." Pick one (it's five) and make all three places
agree.

---

## MAJOR (validity / completeness)

### M1. Coverage labels are unvalidated LLM annotations from the model under study
The audit labels every prompt with Claude Opus 4.8 — the very model being
characterized — and no human validation or inter-annotator agreement is reported.
This is a real methodological weakness (circularity risk + unaudited error rate)
and is currently **unstated**. Minimum fix: (a) say which model produced the
labels and acknowledge the circularity in Limitations; (b) validate a sample
(e.g., hand-check 50 prompts, report agreement) — cheap and would defuse the
objection. Ideally use a *different* model or two as a cross-check.

### M2. The classifier AUC is not length- or config-controlled
§\ref{sec:length} controls length for the *feature effect sizes*, but the
headline classifier AUCs (Table~\ref{tab:clf}) are not length-controlled, and
Claude's cell is specifically the high-effort-with-thinking configuration, which
is longer/more structured. So the AUC could partly reflect verbosity, not voice.
The prose-only condition helps but does not control length. Fix: add a
length-matched or length-residualized classifier condition, or explicitly caveat
that AUC includes a length component (the feature analysis is the
length-controlled evidence).

### M3. Over-strong absolute claims need scoping to the corpus
- Abstract: "appears dozens of times in Claude and **zero times across humans and
  all other models**." True *in our 400-prompt sample*; phrase as "in our corpus."
- §\ref{sec:dawg}: "zero times across humans plus all six other models combined"
  conflates the two tracks — HC3's reference is human + 2 models, AlpacaEval's is
  6 models with no human. State the per-track reference sets; the current sentence
  is literally inaccurate for either track.
- "absent from all other sources" (contributions, line ~71) — same scoping.

### M4. Related work is thin for the venue
Missing strands a reviewer will expect:
- **Model attribution / "which LLM wrote this"** (authorship of LLM text) — we
  even found such papers; directly relevant to the separability result.
- **AI-text detection methods** beyond RAID (e.g., perplexity/DetectGPT/
  Binoculars) — one sentence.
- **Sycophancy / agreement under pressure** — directly relevant to the
  push-back/concession behavior we foreground as future work; its absence is
  conspicuous given the coverage framing.
- The **"spiritual bliss" attractor** is only in the appendix; one line in
  related work would situate the multi-turn plan.

### M5. No figure
The paper is all tables. At least one figure would help: the **n-gram novelty
curve** (novelty vs n, per source) is the natural candidate and the data already
exist (`reports/ngram_dawg.md`). The interrogative-rate-by-source bar chart is
another. ACL readers expect ≥1 figure.

### M6. The strongest corroboration is buried in stats
Claude's responses being 17%/10% interrogative vs ≤4% (everyone else) is a
striking, independent confirmation of the offer-closer, but it sits in
§\ref{sec:stats}/appendix as a "register signal." Consider promoting it into
§\ref{sec:ngram} (Results) as a headline number — it's stronger than some of what
is in the results tables.

### M7. Bibliography errors (will embarrass at camera-ready)
- `liu2024rustydawg`: authors are wrong ("Liu, William and Merrill, William and
  others"). The Rusty-DAWG paper is **Merrill, Smith, Elazar** (2024). Fix.
- `personalization2025`: author "Anonymous" + title only — needs the real
  citation (arXiv 2502.08972) with correct authors, or drop the specific claim.
- `alpacaeval2023`, `dugan2024raid`, `liu2024infinigram`: verify author lists /
  venues; several were written quickly. Do a citation pass against the real
  entries.

---

## MINOR (clarity / polish)

- **MN1.** Abstract: "AUC 0.95 vs human/GPT-4o" — the HC3 comparison set is *three*
  sources (human, GPT-4o, GPT-3.5-era ChatGPT); say so, and note the AUCs quoted
  are **prose-only** (the with-formatting numbers are higher).
- **MN2.** "lexical-in-the-stereotyped-sense" (abstract) is clunky; rephrase
  (e.g., "rather than a stereotyped word-list").
- **MN3.** Enumerate the **seven models** once (reader currently reconstructs them
  from Table 1). Clarify "seven other models" (total distinct) vs "six modern
  models" (AlpacaEval) so the two counts don't read as a slip.
- **MN4.** §\ref{sec:length}: the OLS and the 253/120/228 lengths are HC3-only —
  label the track.
- **MN5.** §\ref{sec:delve}: text says "0.04 per 1k", table says ".039" — round
  consistently. Also the table omits gemini/deepseek with "same pattern"; either
  show them or give their crucial values (gemini .090, deepseek .054) so the
  "Claude lowest" claim is verifiable in-table.
- **MN6.** No **data availability / licensing** note (HC3, AlpacaEval licenses;
  where the released corpus + code live). Add a short statement (anonymized repo
  for review).
- **MN7.** Methods omits two specifics readers will want: (a) the number of
  interpretable features and the classifier's regularization; (b) that the
  coverage audit is LLM-labeled and by which model. Move those one-liners into
  Methods.
- **MN8.** No CIs/significance on the Cohen's $d$ values (only the OLS gives
  t-stats). One sentence ("all reported $d$ have $p<10^{-3}$ by Welch's t / n per
  cell = …") would suffice.
- **MN9.** Title is generic ("a Frontier Language Model") while everything else
  names Claude; fine, but consider naming Claude in the title for findability.
- **MN10.** Qualitative grounding: a short boxed example of a Claude answer (with
  the markdown + offer-closer) vs a human/GPT answer to the same prompt would make
  the fingerprint vivid; currently the reader never sees a real output.
- **MN11.** "five domains" (Table 1) vs the domain list in appendix collapses
  reddit\_eli5+open\_qa into "general" (4 labels). State the collapse so "5 dom."
  vs 4 rows isn't confusing.

---

## Things possibly forgotten (content)
- **Per-domain robustness:** do the effects hold within each domain, or are they
  driven by one (e.g., medicine)? A small per-domain table would preempt the
  "it's a topic artifact" objection (partly addressed by parallel design, but not
  shown per-domain).
- **Mechanism:** one or two sentences on *why* (RLHF / post-training / Anthropic
  house style) would add interpretive value; currently purely descriptive.
- **Reproducibility pointer:** the paper references `src/...` filenames but no
  repository; for a real submission, an (anonymized) URL.
- **The interrogative-response result (M6)** and the **HC3 novelty number**
  (Claude 0.583 vs human 0.524) are computed but not surfaced.

## What is already good (keep)
- The parallel-corpus design and the explicit length control are stronger than
  most stylometry papers; lead with them.
- The delve reconciliation is crisp and well-evidenced; the per-model table is
  convincing.
- The coverage audit as a *contribution* (not just a limitation) is a genuinely
  good framing and is well-supported by the variety numbers.
- Limitations is honest and specific.

## Suggested priority order to fix
1. B1 (regenerate all audit numbers from one run) — trust.
2. B2 (separate syntactic mood vs speech act) — trust.
3. M1 (validate/caveat LLM coverage labels) — validity.
4. M3 + MN1 (scope absolute claims; abstract precision) — correctness.
5. B3, M7 (method count; bib) — embarrassment-avoidance.
6. M2, M4, M5, M6 (length-controlled classifier; related work; a figure; promote
   the interrogative result) — strengthen.
7. Minor polish.
