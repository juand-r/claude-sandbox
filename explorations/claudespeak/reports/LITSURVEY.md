# Literature Survey: Related Work and Data Sources for Claudespeak

This survey supports the paper *Claudespeak: Characterizing the Stylistic Fingerprint
of a Frontier Language Model*. It was produced by four focused research passes
(LLM style fingerprinting; machine-text detection & model attribution; lexical
markers & LLM language influence; persona/RLHF behavioral signatures), followed by
a verification pass against arXiv and the Hugging Face Hub.

The goal is threefold, matching the request: (1) papers we should be **aware of**,
(2) papers we should **cite**, and (3) **data sources** we could incorporate.

## How to read this

Each entry carries a **confidence/verification** tag:

- **[VERIFIED]** — title and author list checked directly against arXiv/HF in this pass.
- **[KNOWN]** — a well-established paper I am confident exists from prior knowledge;
  metadata not re-fetched here but standard. Verify the exact key/venue before camera-ready.
- **[UNVERIFIED]** — surfaced by a research pass but the arXiv ID did **not** resolve
  cleanly on check, or could only be "confirmed" by an echo of the query. **Do not cite
  until independently confirmed.** Listed only so we know the claimed result exists in the wild.

A recurring caution: several of the most thematically on-point items are recent
(2025–2026) preprints. Where the checker rejected the ID or merely echoed the
guessed title, the entry is marked UNVERIFIED. Two are non-archival (company blogs);
those are flagged for `howpublished` so reviewers don't mistake them for peer-reviewed work.

We currently cite 19 references (see `paper/custom.bib`). This survey deliberately
avoids re-listing them except to note close neighbors.

---

## Part 1 — Papers we should CITE (organized by Related Work paragraph)

### 1a. Stylometry / "does LLM text differ in style" (our closest methodological neighbors)

This is the thinnest part of our current bibliography and the most important to fix:
our method (topic-matched parallel corpora + interpretable stylometry + an attribution
classifier) has very close precedents we do not yet cite.

- **[VERIFIED] Reinhart et al. 2025 — "Do LLMs write like humans? Variation in
  grammatical and rhetorical styles."** PNAS 122(8); arXiv:2410.16107. *The single
  closest precedent.* Parallel human/LLM corpora from shared prompts (Llama 3, GPT-4o)
  + Biber's lexical/grammatical/rhetorical feature set; finds systematic, scale-growing,
  instruction-tuning-amplified style differences. **Must cite, and position against
  directly** — our novelty over it is the single-model depth (Claude specifically),
  the interactional offer-closer, the suffix-automaton novelty, and the 4-track
  replication. There is also a companion notebook (refsmmat.com) with function-word-only
  ablations, useful as a "see also."

- **[VERIFIED] Sun et al. 2025 — "Idiosyncrasies in Large Language Models."** ICML 2025;
  arXiv:2502.12150. 97.1% five-way accuracy distinguishing ChatGPT/Claude/Grok/Gemini/
  DeepSeek; idiosyncrasies rooted in word-level distributions, surviving rewriting/
  translation/summarization. **Strong motivation citation** that per-model fingerprints
  (Claude included) are real and stable.

- **[VERIFIED] McGovern et al. 2024 — "Your Large Language Models Are Leaving
  Fingerprints."** arXiv:2405.14057. LLMs leave fingerprints as small frequency
  differences in lexical/morphosyntactic features; simple n-gram + POS classifiers are
  robust in- and out-of-domain. **Directly supports our interpretable-classifier and
  log-odds n-gram sections.**

- **[KNOWN] Kumarage & Liu 2023 — "Neural Authorship Attribution: Stylometric Analysis
  on Large Language Models."** arXiv:2308.07305. Interpretable lexical/syntactic/
  structural stylometry for *model* attribution. Our closest analog on the attribution side.

- **[KNOWN] O'Sullivan 2025 — "Stylometric comparisons of human versus AI-generated
  creative writing."** Humanities & Social Sciences Communications (Nature). Burrows's
  Delta on matched short stories; connects the classical stylometry we already cite
  (burrows2002delta) to the LLM question.

- **[KNOWN/verify IDs] Other interpretable-stylometry neighbors** (cite 1–2, not all):
  Przystalski et al. 2025 (arXiv:2507.00838, StyloMetrix on short samples; "grammatical
  standardisation of LLMs" — supports our burstiness/standardization angle); Milička et
  al. 2025 (arXiv:2509.10179, Biber multidimensional analysis over 16 models, cross-lingual);
  Smith et al. 2025 (arXiv:2505.09056, ~3M texts/12 LLMs, cross-model vocabulary
  non-overlap — supports our log-odds divergence). Verify IDs before use.

### 1b. "AI-ese" / slop / formatting markers (a theme we currently lack)

Our markers include markdown scaffolding and the em-dash habit; there is now a small
literature operationalizing exactly this.

- **[VERIFIED] Shaib et al. 2025 — "Measuring AI 'Slop' in Text."** arXiv:2509.19163.
  Taxonomy + interpretable dimensions for low-quality AI text via expert annotation.
  The reference for framing "AI-ese" as measurable dimensions.

- **[UNVERIFIED] "The Last Fingerprint: How Markdown Training Shapes LLM Prose"**
  (claimed arXiv:2603.27006, single author). Thematically perfect (argues the em-dash
  is "markdown leaking into prose"), but the ID did not verify cleanly and the author
  is uncorroborated. **Do not cite without confirming it exists.** If real, it would be
  a strong mechanistic companion to our em-dash/markdown finding.

### 1c. Excess vocabulary / "delve" / LLM influence on writing (extends our delve reconciliation)

We cite kobak2024delving and the willison2024delve blog; the peer-reviewed and
corpus-scale neighbors are missing.

- **[VERIFIED] Juzek & Ward 2024 — "Why Does ChatGPT 'Delve' So Much? Exploring the
  Sources of Lexical Overrepresentation in LLMs."** COLING 2025; arXiv:2412.11385.
  *The peer-reviewed anchor for the RLHF-causes-lexical-habits claim* — replaces leaning
  on the Willison blog. High priority.

- **[KNOWN] Liang et al. 2024 — "Mapping the Increasing Use of LLMs in Scientific
  Papers."** arXiv:2404.01268 (→ Nature Human Behaviour 2025). Population-level estimator
  over ~950k papers; flags "realm/intricate/showcasing/pivotal." Methodological backbone
  for corpus-level frequency shifts.

- **[KNOWN] Liang et al. 2024 — "Monitoring AI-Modified Content at Scale (peer reviews)."**
  ICML 2024; arXiv:2403.07183. Same estimator on conference reviews; shows the lexical
  signal generalizes.

- **[KNOWN] Geng & Trotta 2024 — "Is ChatGPT Transforming Academics' Writing Style?"**
  arXiv:2404.08627. Mixture-model word-frequency estimate on ~1M arXiv abstracts. The
  Geng & Trotta neighbor of kobak.

- **[KNOWN] Geng & Trotta 2025 — "Human-LLM Coevolution: Evidence from Academic
  Writing."** arXiv:2502.09606. "delve" *declined* after being publicly outed while other
  markers kept rising. **Directly strengthens our framing**: the folklore became
  self-undermining; word-lists are unstable and GPT-specific.

- **[KNOWN] Yakura et al. 2024 — "Empirical Evidence of LLM's Influence on Human Spoken
  Communication."** arXiv:2409.01754. ChatGPT-associated words rising in spoken language
  (~280k talks). Good Intro motivation for *why characterizing model style matters*
  (style contamination).

### 1d. n-gram novelty / memorization / corpus-search tooling (extends our suffix-automaton section)

We cite merrill2024rustydawg (the tool) and liu2024infinigram. Missing the paired
results paper and the memorization/novelty anchors.

- **[VERIFIED] Merrill, Smith & Elazar 2024 — "Evaluating n-Gram Novelty of Language
  Models Using Rusty-DAWG."** EMNLP 2024; arXiv:2406.13069. *The methods/results paper
  paired with the rusty-dawg tool we already cite* — cite both. High priority.

- **[KNOWN] Carlini et al. 2023 — "Quantifying Memorization Across Neural Language
  Models."** ICLR 2023; arXiv:2202.07646. Canonical memorization reference for the
  memorization-vs-novelty discussion.

- **[KNOWN] Elazar et al. 2024 — "What's In My Big Data? (WiMBD)."** ICLR 2024;
  arXiv:2310.20707. Scalable corpus count+search; standard neighbor to infini-gram/rusty-dawg.

- **[KNOWN] Lu et al. 2024 — "AI as Humanity's Salieri: Quantifying Linguistic Creativity
  ... (Creativity Index)."** arXiv:2410.04265. Verbatim/near-verbatim web coverage; humans
  more "creative" than LLMs and *alignment reduces creativity ~30%*. Links n-gram reuse,
  novelty, and alignment-homogenization — a hub citation for our novelty paragraph.

- **[KNOWN, as caveat] Lu et al. 2025 — "Death of the Novel(ty): Beyond n-Gram Novelty as
  a Metric for Textual Creativity."** arXiv:2509.22641. ~91% of top-novelty expressions are
  not judged creative. **Cite as the honest caveat** that our n-gram novelty ≠ creativity
  (we already hedge this; this is the citation for the hedge).

### 1e. Detection & model attribution (extends our two existing paragraphs)

We cite DetectGPT, Binoculars, RAID, the RoBERTa detector, watermarking, and an
authorship-attribution survey, but no concrete attribution methods, no robustness anchor,
and none of the post-DetectGPT statistical wave.

- **[KNOWN] Kumarage et al. 2024 — "A Survey of AI-generated Text Forensic Systems:
  Detection, Attribution, and Characterization."** arXiv:2403.01152. *Best single citation
  to position our paper* — its taxonomy is exactly detection / attribution / **characterization**.
  High priority.

- **[VERIFIED-elsewhere/KNOWN] Rivera Soto et al. 2025 — "Language Models Optimized to
  Fool Detectors Still Have a Distinct Style."** arXiv:2505.14608. Even detector-evading
  text retains a stylometric signature. **Strong motivation** that style persists beyond
  surface detectability. (Companion: Rivera Soto et al. 2024, "Few-Shot Detection using
  Style Representations," arXiv:2401.06712.)

- **[KNOWN] Attribution methods** (cite 2–3): Li et al. 2023 "Origin Tracing / Sniffer"
  (arXiv:2304.14072); Venkatraman et al. 2024 "GPT-who" (UID features, arXiv:2310.06202);
  Uchendu et al. 2021 "TURINGBENCH" (arXiv:2109.13296). Optionally Shi et al. 2025
  "PhantomHunter" (family-level attribution, arXiv:2506.15683) for the family-vs-instance point.

- **[KNOWN] Robustness/brittleness trio** (we have none): Krishna et al. 2023 "DIPPER —
  paraphrasing evades detectors" (NeurIPS; arXiv:2303.13408); Sadasivan et al. 2023 "Can
  AI-Generated Text be Reliably Detected?" (arXiv:2303.11156); Hu et al. 2023 "RADAR"
  (adversarial defense; arXiv:2307.03838).

- **[KNOWN] Post-DetectGPT statistical wave + in-the-wild benchmarks** (cite selectively):
  Bao et al. 2024 "Fast-DetectGPT" (ICLR; arXiv:2310.05130); Verma et al. 2024
  "Ghostbuster" (NAACL; arXiv:2305.15047); Li et al. 2024 "MAGE: detection in the wild"
  (ACL; arXiv:2305.13242); Wang et al. 2024 "M4" (EACL; arXiv:2305.14902). Optionally
  DNA-GPT (n-gram divergence; arXiv:2305.17359) given our n-gram angle.

- **[KNOWN, supports our register caveat] Doughman et al. 2024 — "Exploring the
  Limitations of Detecting Machine-Generated Text."** arXiv:2406.11073. Detectors degrade
  on easier-to-read text — supports our point that register, not just authorship, drives
  separability.

### 1f. Persona / RLHF shapes style (a theme we gesture at but don't anchor)

Our Discussion attributes the style to post-training; these make that defensible.

- **[KNOWN] Ouyang et al. 2022 — "Training LMs to Follow Instructions with Human
  Feedback" (InstructGPT).** NeurIPS 2022; arXiv:2203.02155. The canonical "assistant is a
  product of RLHF" anchor.

- **[KNOWN] Bai et al. 2022 — "Constitutional AI."** arXiv:2212.08073. Anthropic's RLAIF;
  directly relevant to Claude's specific voice (non-evasive refusals).

- **[KNOWN] Shanahan et al. 2023 — "Role Play with Large Language Models."** Nature 623;
  arXiv:2305.16367. Theoretical grounding for "the assistant" as a trained persona.

- **[VERIFIED] Chen et al. 2025 — "Persona Vectors: Monitoring and Controlling Character
  Traits in Language Models."** arXiv:2507.21509 (Runjin Chen, Andy Arditi, Henry Sleight,
  Owain Evans, Jack Lindsey). Activation-space directions for traits, shifting during
  training — mechanistic support for "post-training induces stable persona/style."

- **[NON-ARCHIVAL] Anthropic 2024 — "Claude's Character."**
  anthropic.com/research/claude-character. The most direct evidence Claude's voice is
  *deliberately trained*. Cite with `howpublished` (company blog), not as peer-reviewed.

- **[VERIFIED] Zhang et al. 2024 — "From Lists to Emojis: How Format Bias Affects Model
  Alignment."** arXiv:2409.11704. Reward models/judges prefer bold/lists/emojis; bias
  worsens after fine-tuning. **Direct support that RLHF induces formatting habits** — one
  of our markers.

- **[KNOWN] Singhal et al. 2023 — "A Long Way to Go: Length Correlations in RLHF."**
  arXiv:2310.03716. Reward correlates with length; RLHF inflates verbosity. Supports the
  verbosity/closer aspect of our signature.

- **[VERIFIED-HF/KNOWN] Kirk et al. 2024 — "Understanding the Effects of RLHF on LLM
  Generalisation and Diversity."** ICLR 2024; arXiv:2310.06452. RLHF reduces output
  diversity. Supports "RLHF narrows word choice." (Companion mechanism: Padmakumar & He
  2024, "Does Writing with Language Models Reduce Content Diversity?", ICLR; arXiv:2309.05196.)

- **[KNOWN] Zheng et al. 2023 — "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena."**
  NeurIPS 2023; arXiv:2306.05685. Documents verbosity bias in judges; also the MT-Bench /
  Arena data source (see Part 3). Doubly useful.

- **[KNOWN] Sycophancy/refusal/multi-turn neighbors** (for our future-work framing):
  Xu et al. 2023 "Ask Again, Then Fail" (multi-turn judgment flips; arXiv:2310.02174) —
  cleanest citation for our planned corrective-dynamics track; Röttger et al. 2024 "XSTest"
  (over-refusal; arXiv:2308.01263); Li et al. 2024 "Persona Drift" (arXiv:2402.10962) and
  Kim et al. 2024 "Identity Drift" (arXiv:2412.00804) for the Claude-to-Claude self-
  interaction future work.

- **[UNVERIFIED] "The Assistant Axis: Situating and Stabilizing the Default Persona of
  Language Models"** (claimed arXiv:2601.10387). On-point (an activation direction for the
  default assistant persona) but a 2026 preprint the checker only echoed. Verify before citing.

---

## Part 2 — The single most useful framing takeaway

Across all four passes, **no paper isolates an *interactional* closing move** (our
"offer-to-continue," e.g. "would you like me to go deeper into…") **as a named stylistic
signature.** The literature covers per-model fingerprints (Sun, McGovern), human-vs-LLM
style (Reinhart), excess vocabulary (kobak, Juzek, Geng/Liang), RLHF-induced verbosity and
formatting (Singhal, Zhang), and persona/drift — but the recurring conversational *move* as
a fingerprint appears genuinely novel to us. This is the cleanest thing to claim as our own,
and it sits in a gap between the "static style" literature and the "multi-turn drift"
literature.

The second framing point: position explicitly against **Reinhart 2025** (closest method),
**Sun 2025** (closest "models are distinguishable" result), and the **Kumarage 2024
forensic survey** (which names "characterization" as a pillar — i.e. our category exists and
is under-populated). The **Geng & Trotta 2025 coevolution** result also directly reinforces
our delve-reconciliation (marker words are unstable and GPT-specific).

---

## Part 3 — Data sources we could incorporate

Verified on the Hugging Face Hub unless noted. Our design needs: (a) shared-prompt parallel
cells across models, (b) more prompt diversity, (c) eventually multi-turn. Caveat that
applies to all reused chat logs: they contain **older Claude versions** (claude-1/2/instant),
not Opus 4.8 — so they serve as additional *contrast* cells, real prompts, and as material
for the intra-Claude-**version** analysis (our deferred Exp B), while our Opus 4.8 cells are
still self-generated.

### High value — naturally parallel (same prompt, multiple models)

- **lmsys/chatbot_arena_conversations** [VERIFIED]. 33K conversations with *pairwise*
  responses from two models to the same prompt + human preference; arXiv:2306.05685
  (Zheng et al.). Gated. **Best fit for our parallel design** — two-model same-prompt cells
  out of the box, and it contains Claude (older) responses we can harvest as contrast.
- **lmsys/lmsys-chat-1m** [VERIFIED]. 1M real conversations with 25 models; arXiv:2309.11998.
  Gated. Huge prompt diversity and many models (incl. older Claude); not strictly parallel,
  but the prompt pool is excellent for sampling under-covered intents (like we did with WildChat).

### High value — multi-turn (for the deferred multi-turn track)

- **lmsys/mt_bench_human_judgments** [VERIFIED]. 3.3K expert pairwise judgments over 80
  MT-Bench multi-turn questions, 6 models (GPT-4/3.5, Claude-v1, Vicuna, Alpaca, Llama-13b);
  arXiv:2306.05685. The natural seed for our planned two-turn comparative probes.

### Useful — human-vs-AI and detection corpora (broaden contrast / external validation)

- **Existing & in use:** HC3, AlpacaEval, WildChat (allenai/WildChat-1M), No Robots
  (HuggingFaceH4/no_robots).
- **[KNOWN] M4 / M4GT-Bench** (multi-generator, multi-domain, multilingual; arXiv:2305.14902,
  2402.11175) and **MAGE** (arXiv:2305.13242) — multi-generator corpora; good for an external
  out-of-distribution check of the fingerprint, less so for parallel design.
- **[KNOWN] Beemo** (arXiv:2411.04032) — expert-*edited* machine text; relevant if we ever
  test robustness of the fingerprint to human editing.
- **[KNOWN] OpenAssistant oasst1/2, Anthropic hh-rlhf, ShareGPT** — large assistant-dialogue
  corpora; mostly single-model or preference data, useful as prompt pools or human/assistant
  contrast, not parallel.
- **[UNVERIFIED] ShareChat** (claimed arXiv:2512.17843, Dec 2025) — newer in-the-wild
  multi-platform chatbot corpus preserving native interface features. Verify before relying on it.

### Recommendation on data

For the **next diversity push** after WildChat is topped up, the highest-leverage add is
**chatbot_arena_conversations**: it is genuinely parallel (two models per prompt), carries a
human preference label, and includes Claude — letting us add real-prompt, multi-model cells
with minimal generation. For the **multi-turn track**, seed from **mt_bench_human_judgments**.
Both are gated (request access on HF).

---

## Part 4 — Recommended "add now" shortlist (verified core)

Highest-priority additions, all VERIFIED in this pass or KNOWN-canonical, grouped by where
they slot into our Related Work. Ready-to-paste BibTeX is in
`reports/litsurvey_additions.bib`. Suggested minimal set (≈12) to add first:

1. reinhart2025llmwrite (stylometry — cornerstone, position against)
2. sun2025idiosyncrasies (per-model fingerprints — motivation)
3. mcgovern2024fingerprints (interpretable n-gram/POS fingerprints)
4. kumarage2024forensicsurvey (positions our "characterization" framing)
5. merrill2024ngramnovelty (pairs with our rusty-dawg tool citation)
6. carlini2023memorization (memorization anchor)
7. juzek2024delve (peer-reviewed RLHF-lexicon anchor; with willison)
8. geng2025coevolution (delve declined after exposure — strengthens our reconciliation)
9. kirk2024rlhfdiversity (RLHF reduces diversity)
10. singhal2023length + zhang2024formatbias (RLHF inflates verbosity & formatting)
11. krishna2023dipper + sadasivan2023reliable (detection brittleness anchor)
12. riverasoto2025distinctstyle (style persists beyond detectability — motivation)

Plus, for the future-work paragraphs: xu2023askagain (corrective dynamics),
mtbench/zheng2023 (multi-turn data), li2024personadrift + kim2024identitydrift
(self-interaction).

## Part 5 — Items flagged DO-NOT-CITE-yet (verify first)

- "The Last Fingerprint: How Markdown Training Shapes LLM Prose" (claimed 2603.27006) —
  ID did not verify; single uncorroborated author. Thematically ideal but treat as unproven.
- "StoryScope: Investigating idiosyncrasies in AI fiction" (claimed 2604.03136) — checker
  reported the ID does not resolve to a real paper.
- "The Assistant Axis" (claimed 2601.10387) — only echo-confirmed; verify.
- "Verbalized Sampling" (claimed 2510.01171), "SycEval" (2502.08177), "Sycophancy under
  Pressure" (2508.13743), Michels "Spiritual Bliss" (PhilArchive, non-archival) — surfaced
  but unverified or grey literature.
</content>
</invoke>
