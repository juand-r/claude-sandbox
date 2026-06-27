# Annotated Bibliography for Claudespeak

This is the annotated companion to the literature survey. Each entry gives a short
summary, why it matters to us, and how it relates to our paper. Entries in Parts
1–6 have been **merged into `paper/custom.bib`** and their metadata verified against
arXiv (June 2026) unless marked otherwise. Part 7 lists items we found but did
**not** add to the bib (unverified IDs or grey literature) — documented for
completeness; verify before citing.

Existing citations already in the paper (DetectGPT, Binoculars, RAID, the RoBERTa
detector, watermarking, the authorship-attribution survey, Fightin' Words, kobak
delve, the Willison blog, Burrows's Delta, rusty-dawg, infini-gram, the two
sycophancy papers, the Claude 4 system card, HC3, AlpacaEval, WildChat, No Robots)
are not re-annotated here.

---

## Part 1 — LLM stylistic fingerprinting and style comparison

These are our closest methodological neighbors; before this survey we cited none of them.

### reinhart2025llmwrite — *Do LLMs write like humans? Variation in grammatical and rhetorical styles* (PNAS 2025; arXiv:2410.16107)
Builds parallel human/LLM corpora from shared prompts and applies Douglas Biber's
lexical/grammatical/rhetorical feature inventory to GPT-4o and Llama 3, finding
systematic stylistic differences (more present-participial clauses, nominalizations,
that-clauses) that grow with model scale and are larger for instruction-tuned than
base models.
**Why we care / relation:** This is the single closest precedent to Claudespeak —
topic-matched parallel corpora plus interpretable stylometry. We position against it
directly: our contribution is the single-model *depth* on Claude specifically, the
*interactional* offer-to-continue closer (which Biber-style features do not capture),
the suffix-automaton novelty evidence, and the four-track replication. It belongs in
the stylometry paragraph and is worth a sentence in the introduction.

### sun2025idiosyncrasies — *Idiosyncrasies in Large Language Models* (ICML 2025; arXiv:2502.12150)
Frames model identification as classification and reaches 97.1% five-way accuracy
distinguishing ChatGPT/Claude/Grok/Gemini/DeepSeek; the idiosyncrasies are rooted in
word-level distributions and survive paraphrase, translation, and summarization.
**Why we care / relation:** Strong, recent evidence that per-model fingerprints
(Claude included) are real and stable — the premise our whole paper builds on. We
cite it as motivation in the stylometry/attribution discussion; our work then *opens
the black box* and says what Claude's idiosyncrasy actually is.

### mcgovern2024fingerprints — *Your Large Language Models Are Leaving Fingerprints* (arXiv:2405.14057)
Shows that LLMs leave detectable "fingerprints" as small differences in the frequency
of lexical and morphosyntactic features, and that simple n-gram + POS classifiers are
robust in- and out-of-domain.
**Why we care / relation:** Directly supports our interpretable-classifier and
log-odds n-gram analyses: the signal lives in interpretable feature frequencies, not
only in deep representations. Cite in the stylometry/attribution paragraph alongside our classifier.

### kumarage2023neural — *Neural Authorship Attribution: Stylometric Analysis on Large Language Models* (arXiv:2308.07305)
Attributes text to the originating LLM using interpretable lexical/syntactic/
structural stylometric features, comparing proprietary and open-source families.
**Why we care / relation:** Our closest analog on the *attribution* side — interpretable
stylometry rather than a black-box detector. We cite it to show our feature-based
approach has precedent for telling models apart, while noting our goal is
characterization, not a label.

### osullivan2025stylometry — *Stylometric comparisons of human versus AI-generated creative writing* (Humanities and Social Sciences Communications, 2025)
Applies Burrows's Delta (most-frequent-word distributions) to matched human and LLM
short stories; GPT-4 is more internally consistent than GPT-3.5, and both remain
distinguishable from humans.
**Why we care / relation:** Bridges the classical stylometry we already cite
(Burrows) to the LLM-style question, and is a creative-writing data point relevant to
our WildChat track (heavy on creative writing). Cite in the stylometry paragraph.

---

## Part 2 — "AI-ese" / slop

### shaib2025slop — *Measuring AI "Slop" in Text* (arXiv:2509.19163)
Develops a taxonomy and interpretable dimensions for low-quality "AI slop" via expert
interviews and span-level annotation, and shows binary slop judgments correlate with
coherence/relevance.
**Why we care / relation:** The reference for treating "AI-ese" as a *measurable*
construct, which is exactly the spirit of our interpretable features. Useful to frame
the broader phenomenon our markers (markdown scaffolding, em-dash, hedges) sit within.

---

## Part 3 — Excess vocabulary and LLM influence on writing

Extends our "delve is a GPT trait Claude avoids" reconciliation.

### juzek2024delve — *Why Does ChatGPT "Delve" So Much? Exploring the Sources of Lexical Overrepresentation in LLMs* (COLING 2025; arXiv:2412.11385)
Identifies ~21 "focal words" overrepresented by ChatGPT and tests RLHF/annotator-
preference explanations for the overrepresentation.
**Why we care / relation:** The peer-reviewed anchor for the "RLHF causes lexical
habits" claim — replaces leaning solely on the Willison blog we currently cite. Cite
in the excess-vocabulary paragraph next to kobak and willison.

### geng2024transforming — *Is ChatGPT Transforming Academics' Writing Style?* (arXiv:2404.08627)
Models word-frequency distributions across ~1M arXiv abstracts (2018–2024) as a
human/LLM mixture and estimates ~35% of CS abstracts are ChatGPT-influenced.
**Why we care / relation:** A second, independent corpus/method for the excess-vocab
phenomenon (the Geng & Trotta lineage). Cite as corroborating evidence that the
lexical signal is real and measurable.

### geng2025coevolution — *Human-LLM Coevolution: Evidence from Academic Writing* (arXiv:2502.09606)
Documents that "delve" *declined* in frequency soon after it was publicly flagged in
2024 while other markers kept rising — evidence that authors curate LLM output.
**Why we care / relation:** Directly strengthens our framing that marker-word lists
are unstable and provenance-specific. We use it to argue that borrowing a fixed
"AI word list" is the wrong instrument — exactly our methodological lesson.

### liang2024mapping — *Mapping the Increasing Use of LLMs in Scientific Papers* (arXiv:2404.01268; later Nature Human Behaviour 2025)
A population-level maximum-likelihood estimator over ~950k papers finds up to ~17.5%
LLM-modified text in CS and flags "realm/intricate/showcasing/pivotal."
**Why we care / relation:** The methodological backbone for corpus-level frequency-
shift estimation; cite as the scaled-up companion to kobak and to motivate why
characterizing model lexicon matters.

### liang2024monitoring — *Monitoring AI-Modified Content at Scale: ... AI Conference Peer Reviews* (ICML 2024; arXiv:2403.07183)
Extends the same estimator to peer reviews, estimating 6.5–16.9% substantially
LLM-modified.
**Why we care / relation:** Shows the lexical-shift signal generalizes beyond
abstracts. Optional supporting cite in the excess-vocab paragraph.

### yakura2024spoken — *Empirical Evidence of LLM's Influence on Human Spoken Communication* (arXiv:2409.01754)
Analyzes ~280k academic talks and finds ChatGPT-associated words rising in *spoken*
language after release — a human→machine→human feedback loop.
**Why we care / relation:** Good introduction-level motivation for *why* model style
matters culturally (style contamination), complementing kobak.

---

## Part 4 — n-gram novelty, memorization, corpus search

Extends our suffix-automaton section (we cite the rusty-dawg tool and infini-gram).

### merrill2024ngramnovelty — *Evaluating n-Gram Novelty of Language Models Using Rusty-DAWG* (EMNLP 2024; arXiv:2406.13069)
Defines n-gram novelty and non-novel-suffix-length metrics and measures LLM verbatim
reuse against pretraining data via a suffix automaton.
**Why we care / relation:** The *methods/results* paper paired with the rusty-dawg
tool we already cite — we should cite both, since our novelty analysis uses exactly
this machinery. Central to the suffix-automaton paragraph.

### carlini2023memorization — *Quantifying Memorization Across Neural Language Models* (ICLR 2023; arXiv:2202.07646)
Shows verbatim memorization grows with model scale, data duplication, and context length.
**Why we care / relation:** The canonical memorization reference for our memorization-
vs-novelty discussion; grounds the claim that high novelty is not guaranteed.

### elazar2024wimbd — *What's In My Big Data? (WiMBD)* (ICLR 2024; arXiv:2310.20707)
A scalable count-and-search system over training corpora that quantifies duplication
and benchmark contamination.
**Why we care / relation:** The standard corpus-search neighbor to infini-gram and
rusty-dawg; cite in the tooling sentence of the novelty paragraph.

### lu2024creativityindex — *AI as Humanity's Salieri: Quantifying Linguistic Creativity ... (Creativity Index)* (arXiv:2410.04265)
Introduces a Creativity Index based on verbatim/near-verbatim web coverage; finds
humans ~66% more "creative" than LLMs and that alignment reduces creativity ~30%.
**Why we care / relation:** Links n-gram reuse, novelty, and the alignment-
homogenization thread — a hub citation for our novelty paragraph and for the
"RLHF narrows style" argument.

### saakyan2026deathofnovelty — *Death of the Novel(ty): Beyond n-Gram Novelty as a Metric for Textual Creativity* (ICLR 2026; arXiv:2509.22641)
Argues n-gram novelty is a poor creativity proxy — ~91% of top-novelty expressions
are not judged creative by experts.
**Why we care / relation:** The honest caveat for our novelty result. We already hedge
that novelty means "relative distinctiveness, not creativity"; this is the citation
for that hedge. (Note: authors are Saakyan, Kim, Muresan, Chakrabarty — an early
draft of our survey misattributed it; corrected here.)

---

## Part 5 — Detection and model attribution

Extends our two existing Related Work paragraphs, which lacked concrete attribution
methods, a robustness anchor, and the post-DetectGPT statistical wave.

### kumarage2024forensicsurvey — *A Survey of AI-generated Text Forensic Systems: Detection, Attribution, and Characterization* (arXiv:2403.01152)
A taxonomy of the field organized around three pillars: detection, attribution, and
**characterization**.
**Why we care / relation:** The best single citation to *position* our paper — it
names "characterization" as a recognized but under-populated category, which is
precisely our contribution. Anchor the attribution paragraph with it.

### riverasoto2025fingerprints — *Attacks on Machine-Text Detectors Retain Stylistic Fingerprints* (arXiv:2505.14608)
Shows that even text optimized to evade detectors retains a measurable stylistic
signature recoverable by stylometry.
**Why we care / relation:** Strong motivation that style persists beyond surface
detectability — i.e., a model's voice is robust, which is the premise of
characterizing it. Cite in the attribution/stylometry bridge.

### riverasoto2024fewshot — *Few-Shot Detection of Machine-Generated Text using Style Representations* (ICLR 2024; arXiv:2401.06712)
Uses learned authorship/style representations to detect and attribute machine text
with few examples.
**Why we care / relation:** Establishes style-representation features as an attribution
signal; a learned-representation counterpart to our interpretable features.

### li2023origintracing — *Origin Tracing and Detecting of LLMs* (arXiv:2304.14072)
Introduces "Sniffer," tracing text to its source LLM using contrastive perplexity
features across reference models.
**Why we care / relation:** A concrete origin-tracing method for the attribution
paragraph; contrast with our interpretable, generation-side approach.

### venkatraman2024gptwho — *GPT-who: An Information Density-based Machine-Generated Text Detector* (Findings of NAACL 2024; arXiv:2310.06202)
A psycholinguistically-motivated multi-class detector using Uniform Information
Density features that map back to tokens; UID signatures cluster by model family.
**Why we care / relation:** Interpretable-feature attribution, close in spirit to our
method; cite in the attribution paragraph.

### uchendu2021turingbench — *TURINGBENCH: A Benchmark Environment for Turing Test in the Age of Neural Text Generation* (Findings of EMNLP 2021; arXiv:2109.13296)
The first benchmark with both a human-vs-machine task and a multi-class authorship-
attribution task across ~19 generators.
**Why we care / relation:** Foundational framing of attribution as multi-class;
worth citing even though pre-2023 to credit the problem formulation.

### bao2024fastdetectgpt — *Fast-DetectGPT: ... Conditional Probability Curvature* (ICLR 2024; arXiv:2310.05130)
Replaces DetectGPT's perturbation step with conditional sampling; roughly two orders
of magnitude faster and more accurate.
**Why we care / relation:** The natural successor to the DetectGPT we already cite;
include to keep the detection paragraph current.

### verma2024ghostbuster — *Ghostbuster: Detecting Text Ghostwritten by Large Language Models* (NAACL 2024; arXiv:2305.15047)
A black-box detector using structured search over features from weaker LMs, with
released cross-domain datasets.
**Why we care / relation:** A standard modern black-box detector we currently omit;
cite in the detection paragraph.

### li2024mage — *MAGE: Machine-generated Text Detection in the Wild* (ACL 2024; arXiv:2305.13242)
A large multi-generator, multi-domain testbed quantifying the out-of-distribution
generalization gap of detectors.
**Why we care / relation:** The "in the wild" benchmark complementing RAID; also a
candidate external corpus for out-of-distribution checks of our fingerprint.

### wang2024m4 — *M4: Multi-generator, Multi-domain, Multi-lingual Black-Box MGT Detection* (EACL 2024; arXiv:2305.14902)
A multilingual, multi-generator detection benchmark (basis for the SemEval-2024
Task 8 line).
**Why we care / relation:** Cite for cross-lingual/cross-generator robustness; relevant
to our English-only limitation and to future multilingual extension.

### krishna2023dipper — *Paraphrasing Evades Detectors of AI-generated Text, but Retrieval is an Effective Defense* (NeurIPS 2023; arXiv:2303.13408)
The DIPPER paraphraser collapses detector accuracy; retrieval is proposed as a defense.
**Why we care / relation:** Canonical brittleness result; we cite it to note that
surface detectability is fragile, which is *why* a robust stylistic characterization
is valuable.

### sadasivan2023reliable — *Can AI-Generated Text be Reliably Detected?* (arXiv:2303.11156)
An impossibility-style argument plus a recursive-paraphrasing attack defeating a range
of detectors.
**Why we care / relation:** The "fundamental limits" citation for the detection
paragraph; motivates characterization over detection.

### hu2023radar — *RADAR: Robust AI-Text Detection via Adversarial Learning* (NeurIPS 2023; arXiv:2307.03838)
Jointly trains a paraphraser and detector adversarially for paraphrase robustness.
**Why we care / relation:** The "defense" counterpoint to the two brittleness papers;
completes a balanced robustness sub-point.

---

## Part 6 — Persona and how post-training (RLHF) shapes style

Makes our Discussion claim ("the profile is consistent with RLHF") defensible.

### ouyang2022instructgpt — *Training Language Models to Follow Instructions with Human Feedback* (NeurIPS 2022; arXiv:2203.02155)
The InstructGPT/RLHF paper establishing that helpful "assistant" behavior is a product
of preference fine-tuning.
**Why we care / relation:** The canonical anchor for "style is shaped by post-training."

### bai2022constitutional — *Constitutional AI: Harmlessness from AI Feedback* (arXiv:2212.08073)
Anthropic's RLAIF method.
**Why we care / relation:** Directly relevant to Claude's specific voice (non-evasive,
explains objections); ties the pipeline to the tone we observe.

### shanahan2023roleplay — *Role Play with Large Language Models* (Nature 2023; arXiv:2305.16367)
Frames the dialogue agent as role-playing a character / superposition of personas.
**Why we care / relation:** Theoretical grounding for treating "the assistant" — and
its stylistic habits, like our offer-closer — as a trained persona.

### chen2025personavectors — *Persona Vectors: Monitoring and Controlling Character Traits in Language Models* (arXiv:2507.21509)
Finds activation-space directions for character traits that can be steered and that
shift during training.
**Why we care / relation:** Mechanistic support that post-training induces and can move
a stable persona/style — relevant to why Claude's voice is so consistent.

### anthropic2024claudecharacter — *Claude's Character* (Anthropic blog, 2024)
Describes Anthropic's deliberate "character training" using synthetic self-generated data.
**Why we care / relation:** The most direct evidence that Claude's distinctive voice is
*intentionally trained* — load-bearing for our thesis. Cite as grey literature
(`howpublished`), not peer-reviewed.

### zhang2024formatbias — *From Lists to Emojis: How Format Bias Affects Model Alignment* (arXiv:2409.11704)
Shows reward models and LLM judges prefer bold, lists, and emojis, and that this bias
worsens after fine-tuning.
**Why we care / relation:** Direct mechanistic support that RLHF induces *formatting*
habits — one of our headline markers (markdown scaffolding). Strong cite in both the
markdown-results discussion and the persona/RLHF paragraph.

### singhal2023length — *A Long Way to Go: Investigating Length Correlations in RLHF* (arXiv:2310.03716)
Shows reward strongly correlates with response length; a length-only reward reproduces
most RLHF gains.
**Why we care / relation:** Explains the verbosity component of our signature; relevant
to our length-control section (we show the fingerprint is *not* just length, but length
itself is an RLHF artifact).

### kirk2024rlhfdiversity — *Understanding the Effects of RLHF on LLM Generalisation and Diversity* (ICLR 2024; arXiv:2310.06452)
RLHF improves OOD generalization but reduces output diversity relative to SFT.
**Why we care / relation:** Supports "RLHF narrows word choice/style," connecting to
our content-density and novelty findings.

### padmakumar2024diversity — *Does Writing with Language Models Reduce Content Diversity?* (ICLR 2024; arXiv:2309.05196)
Feedback-tuned (but not base) models reduce inter-author lexical/content diversity in
a controlled writing study.
**Why we care / relation:** Connects RLHF-style tuning to homogenization of human
writing; pairs with kirk and lu (Creativity Index).

### zheng2023mtbench — *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (NeurIPS 2023; arXiv:2306.05685)
Introduces MT-Bench (multi-turn) and documents verbosity and self-enhancement biases
in LLM judges.
**Why we care / relation:** Doubly useful — evidence that the preference signal driving
training rewards verbose/structured style, AND a multi-turn data source for our
deferred multi-turn track.

### xu2023askagain — *Ask Again, Then Fail: Large Language Models' Vacillations in Judgment* (ACL 2024; arXiv:2310.02174)
Models flip correct answers after "Are you sure?"-style follow-ups (the Follow-up
Questioning Mechanism).
**Why we care / relation:** The cleanest citation for our planned multi-turn corrective
dynamics — agreement under conversational pressure.

### rottger2024xstest — *XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in LLMs* (NAACL 2024; arXiv:2308.01263)
Shows over-refusal stems from lexical overfitting, with a contrast set of safe/unsafe prompts.
**Why we care / relation:** Supports the idea that refusal *style* is a post-training
artifact — relevant to the sensitive/refusal cell our coverage audit flags as thin.

### li2024instability — *Measuring and Controlling Instruction (In)Stability in Language Model Dialogs* (arXiv:2402.10962)
Finds significant persona/instruction drift within ~8 turns, attributed to attention decay.
**Why we care / relation:** Relevant to persona stability and our future multi-turn /
Claude-to-Claude work. (Note: the survey draft mislabeled this as "Persona Drift";
true title corrected here.)

### choi2024identitydrift — *Examining Identity Drift in Conversations of LLM Agents* (arXiv:2412.00804)
Larger models drift *more* in identity, and agents adopt their partner's persona.
**Why we care / relation:** A neighbor to the Claude-to-Claude "spiritual bliss"
attractor we already mention; supports our self-interaction future work.

---

## Part 7 — Data sources (and items NOT added to the bib)

### Data sources worth incorporating
- **zheng2024lmsyschat1m** — *LMSYS-Chat-1M* (arXiv:2309.11998; dataset `lmsys/lmsys-chat-1m`).
  1M real conversations, 25 models. Added to the bib. Excellent prompt-diversity pool;
  includes older Claude versions (useful for the deferred version analysis and as
  contrast, not as Opus 4.8).
- **lmsys/chatbot_arena_conversations** (covered by zheng2023mtbench, arXiv:2306.05685).
  33K *pairwise* two-model responses to the same prompt + human preference. The best fit
  for our parallel design; gated on HF. Recommended as the next diversity add after
  WildChat is topped up.
- **lmsys/mt_bench_human_judgments** (zheng2023mtbench). Multi-turn; the seed for our
  planned two-turn comparative probes.

### Found but NOT added to the bib — verify before citing
- **"The Last Fingerprint: How Markdown Training Shapes LLM Prose"** (claimed
  arXiv:2603.27006). Thematically ideal (em-dash as markdown leakage) but the ID did not
  verify and the single author is uncorroborated. **Do not cite until confirmed.**
- **"StoryScope: Investigating idiosyncrasies in AI fiction"** (claimed arXiv:2604.03136).
  The checker reported this ID does not resolve to a real paper. Verify; if real, it is a
  close neighbor (per-model fiction idiosyncrasies, small interpretable feature set).
- **"The Assistant Axis"** (claimed arXiv:2601.10387). On-point (an activation direction
  for the default assistant persona) but only echo-confirmed. Verify.
- **Reinhart companion notebook** (refsmmat.com) — a blog/notebook with function-word-only
  ablations; cite the PNAS paper instead, mention the notebook only as "see also."
- **Other detection/attribution methods surfaced** but not added to keep the bib focused
  (add if a reviewer asks for more coverage): Fast-DetectGPT neighbors DetectLLM
  (arXiv:2306.05540), DNA-GPT (arXiv:2305.17359), SeqXGPT (arXiv:2310.08903), LLMDet
  (arXiv:2305.15004), PhantomHunter (arXiv:2506.15683), the intrinsic-dimension detector
  (arXiv:2306.04723), and OR-Bench over-refusal (arXiv:2405.20947). Also the obscure
  stylometry items Przystalski et al. (2507.00838), Milička et al. (2509.10179), and
  Smith et al. (2505.09056) — author metadata not independently verified.

---

## How these map onto the paper's Related Work

- **Detecting machine-generated text** (existing): + bao2024fastdetectgpt,
  verma2024ghostbuster, li2024mage, wang2024m4; robustness sub-point
  + krishna2023dipper, sadasivan2023reliable, hu2023radar.
- **Attributing text to a model** (existing): + kumarage2024forensicsurvey,
  li2023origintracing, venkatraman2024gptwho, uchendu2021turingbench,
  riverasoto2024fewshot, riverasoto2025fingerprints, kumarage2023neural.
- **Excess vocabulary / AI-ese** (existing): + juzek2024delve, geng2024transforming,
  geng2025coevolution, liang2024mapping, liang2024monitoring, yakura2024spoken,
  shaib2025slop.
- **Stylometry and n-gram novelty** (existing): + reinhart2025llmwrite,
  sun2025idiosyncrasies, mcgovern2024fingerprints, osullivan2025stylometry,
  merrill2024ngramnovelty, carlini2023memorization, elazar2024wimbd,
  lu2024creativityindex, saakyan2026deathofnovelty.
- **Sycophancy and persona** (existing): + ouyang2022instructgpt, bai2022constitutional,
  shanahan2023roleplay, chen2025personavectors, anthropic2024claudecharacter,
  singhal2023length, zhang2024formatbias, kirk2024rlhfdiversity, padmakumar2024diversity,
  zheng2023mtbench, xu2023askagain, rottger2024xstest, li2024instability,
  choi2024identitydrift.
- **Data** (existing): + zheng2024lmsyschat1m.
</content>
