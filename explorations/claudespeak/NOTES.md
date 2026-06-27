# Claudespeak — working notes / progress log

Newest entries on top. See PLAN.md for the approved plan; this file logs what was
actually done, decisions made during execution, and caveats.

## 2026-06-24 — Phase 0 begins (infra + pilot corpus)

**Generation access in this environment:** ANTHROPIC_API_KEY ✓, OPENAI_API_KEY ✓,
HF_TOKEN ✓. No Gemini/DeepSeek/Qwen keys → those contrast cells must be *reused*
from existing parallel datasets (as planned), not generated here.

**Reproducibility infra built:**
- `schema/record_schema.md` + `src/schema.py` — canonical record (one generation
  per line, JSONL). Validation fails loudly if a self-generated model record
  lacks `gen_params` or git commit. Every self-generated call also saves the
  verbatim API response under `data/raw_responses/`.
- `src/generate.py` — Claude (Opus 4.8, adaptive thinking + effort knob; logs
  temperature=null since Opus 4.8 rejects it) and OpenAI GPT wrappers.
- `src/generate_pilot.py` — resumable, append-after-each-call driver. Safe
  against environment reclamation (skips completed `(prompt_id, generator)`).

**Pilot corpus design (first cut = human-anchored track):**
- Source: **HC3** (`Hello-SimpleAI/HC3`, all.jsonl). Gives per-question human +
  GPT-3.5-era ChatGPT answers across 5 domains.
- Sample: **200 prompts**, 40/domain, seed=42 (`src/acquire_hc3.py`). Domain
  labels collapse reddit_eli5+open_qa → "general" (80), + finance/medicine/cs_ai
  (40 each).
- Cells per prompt: `human` (reused), `chatgpt-hc3` (reused, old GPT-3.5),
  `claude-opus-4-8` (generated, effort=high), `gpt-4o` (generated). → 4-way
  parallel, topic-matched, with a real human anchor.

**Why HC3 first, AlpacaEval next:** HC3 is the cleanest *human-anchored* parallel
set and needs no keys we lack. The user-named modern contrast models (2×GPT,
Gemini, DeepSeek, Qwen) are not in HC3; we add them next via **AlpacaEval** (many
models on identical instructions, reused for free) — that track has no human, so
the two tracks are complementary. Both feed the same feature pipeline.

**Caveats logged in records:**
- HC3 human answers are pre-2023 web text (reddit/wiki/etc.) — genuine human, but
  not professionally edited; some are short/informal.
- `chatgpt-hc3` is GPT-3.5 era, an *old-model* baseline, not a current frontier
  contrast.
- HC3 ELI5 questions store the title duplicated into the body; we feed all models
  the identical verbatim question to preserve parallelism.

**License:** HC3 is public research data (BY-SA / research use). We commit a
200-row research subset + derived generations.

### Phase 1 first cut — DONE (see reports/FINDINGS_pilot.md)
- [x] Generated Claude Opus 4.8 + GPT-4o over 200 prompts (400/400 ok). Full
      4-way parallel corpus: human / chatgpt-hc3 / gpt-4o / claude-opus-4-8.
- [x] Descriptive stylometry + Claude-vs-rest effect sizes → reports/pilot_stylometry.md
- [x] Markdown-stripped ablation → reports/pilot_ablation_markdown.md

**Headline result:** Claude signal is large AND survives markdown stripping.
Raw-prose separators: sentence burstiness (d≈1.69), function-word density
(d≈1.47), em-dash habit (d≈0.87). Lexical tics ("delve" etc.) DON'T separate
(d≈0.15) — contra popular belief. Claude is LESS lexically diverse than humans.

### Lexical-tic reconciliation — DONE (reports/LITREVIEW_lexical_tics.md)
JdR asked to reconcile "tics don't separate Claude" with the delve discourse.
Result: **delve/crucial/intricate are GPT/ChatGPT signatures, not Claude.**
- Literature: Kobak 2024 (excess vocab → ChatGPT); delve origin = OpenAI RLHF;
  arXiv 2502.08972 (Claude=casual, GPT=formal "crucial to").
- Our data: GPT-4o > Claude on EVERY excess word that appears (crucial 18×);
  delve = 0 everywhere. Claude leads conversational markers (actually 1.38/1k).
- Corrected FINDINGS_pilot.md §5 (was an overclaim). My tic-list was a GPT-ism
  list mislabeled as generic. Claude's signal is structural/rhythmic first,
  conversational-lexical second.

### Phase 2 (locked plan: PLAN_phase2.md) — Step 1 DONE
**Step 1 (n-gram signature, Fightin' Words):** Claude DOES have a lexical
signature — interactional, not delve-family. Top: the offer-closer
"would you like me to explain in more detail / go deeper into any specific
aspect", "let me", second-person, "actually". Anti-signature: "it is important
to" (GPT frame), formal deferral, function-word connectives. → reports/claude_ngram_signature.md.
Vindicates JdR's point: right words, wrong list before.

### Step 2 (length control) DONE
Headline prose effects survive length control: burstiness OLS t=20.6,
function-word density t=-14.4, em-dash t=12.6, question-rate t=4.6; within-quartile
Cohen's d holds across bins. Caveat: TTR/hapax are length-sensitive (Claude<human
holds only in direct human comparison). → reports/pilot_length_control.md.

### Step 3 (AlpacaEval modern-model track) DONE
1400 records, 7 sources (Claude + 6 reused modern models). Findings:
- Structural/rhythmic signature REPLICATES vs modern: burstiness d=1.01, em-dash
  d=0.63, function-word density d=-0.55, question/offer d=0.50.
- VOCAB RECONCILIATION CONFIRMED: in essay genre, Claude is the LEAST delve/crucial
  model of 7 (only model with delve=delves=0; crucial 0.039 lowest vs GPT 0.34-0.42).
- Offer-closer n-grams replicate ("would you like me to", "let me know if you'd like").
→ reports/alpaca_track.md. Corpus: alpaca_reused.jsonl + alpaca_generated.jsonl.

### Step 4 (interpretable classifier) DONE
Claude highly separable, mostly from prose: HC3 prose-only AUC 0.946 (with-fmt
0.982); AlpacaEval vs 6 modern models prose-only AUC 0.867 (with-fmt 0.901).
Driving coefs match Steps 1-2 (burstiness+, function-word density+, em-dash+,
question/offer+) — independent-method consistency check. → reports/pilot_classifier.md.

### Step 5 (rusty-dawg / suffix-automaton) DONE — finale
Used AI2 rusty_dawg (pip). Gotcha: recompute_lengths() segfaults at scale and is
unnecessary — get_count correct after build() alone (verified).
- Exact long templates UNIQUE to Claude (zero in human+all 6 other models), up to
  8-grams: "would you like me to go deeper into", "...explain any", "...expand on any".
- Claude has HIGHEST n-gram novelty of all 7 sources (phrasing overlaps least).
→ reports/ngram_dawg.md. Consolidated: reports/FINDINGS.md (all 5 steps).

### Phase 2 COMPLETE. Possible next axes: effort/thinking sweep, more Claude
versions, multi-turn (Sense B/C), other genres/languages, larger corpus.

### TODO (next)
- [ ] Length-stratified re-run of the prose ablation (robustness).
- [ ] AlpacaEval track: modern Gemini/DeepSeek/Qwen/Llama/Phi (reused) + Claude.
- [ ] Claude thinking-effort sweep (low/med/high).
- [ ] n-gram mining (rusty-dawg / infini-gram) for over-represented phrases.
- [ ] Interpretable classifier on prose-only features (separability number).

---

## Phase 3.0 — Corpus diversity expansion (WildChat + No Robots)

Motivation (user): "not enough samples and not enough diversity." HC3+AlpacaEval
were 200 prompts each, concentrated in explanation/QA and mostly *questions*.

### Sources added
- **WildChat** (allenai/WildChat-1M): 1500 real single-turn user prompts;
  reused GPT-4-0314 reply as contrast; Claude generated separately.
  src/acquire_wildchat.py, src/generate_wildchat.py.
- **No Robots** (HuggingFaceH4/no_robots): 1500 human prompts AND human answers,
  balanced across 10 task types (Generation/Brainstorm/QA/Rewrite/Summarize/
  Coding/Classify/Extract/Chat). First HUMAN anchor on non-QA tasks.
  src/acquire_no_robots.py, src/generate_norobots.py.

### Generation status
- No Robots Claude: **1500/1500 complete**.
- WildChat Claude: **628/1500** — STOPPED. API hit "credit balance is too low"
  (HTTP 400 invalid_request) around the 600-700 mark while running concurrently
  with No Robots. Remaining ~870 DEFERRED until credits replenished. Job is
  resumable (skips done prompt_ids). 628 is still a usable sample (3x per-track n
  of HC3/AlpacaEval). Cost so far this session ~$0.037/gen.

### Coverage gain (src/analyze_coverage.py, sampled 400/large track)
New tracks fill the gaps HC3/AlpacaEval left empty:
- intent: +creative_writing (WildChat 41%), +code, +roleplay; +classification_
  extraction (NoRobots 25%), +summarize_rewrite (18%), +personal_emotional.
- speech act: flips from HC3's 75% questions to 59-73% DIRECTIVES.
- register: formal appears (WildChat 10%), previously near-absent.
- topic: entertainment/software_code/personal_life/arts now well represented.

### Fingerprint replication (src/analyze_tracks.py)
Claude vs pooled non-Claude, Cohen's d, per track. WildChat aligned to its 628
shared prompts (parallel-corpus control). Headline features replicate 4/4 sign:
burstiness (+), function_word_rate (-), em-dash (+), markdown header/bold/bullet
(+), questions/offer-closer (+ except No Robots, whose classify/extract/rewrite
tasks don't invite continuation). Magnitudes shrink on the diverse tracks
(HC3 had the cleanest contrast) but the fingerprint holds. ttr/colon NOT robust.
→ reports/cross_track_fingerprint.md, reports/dataset_stats.md.

### BLOCKER / decision point
- Finishing WildChat (~870 more Claude gens, ~$32) needs API credits topped up.
- Paper still describes only HC3+AlpacaEval; needs rewrite to fold in the two new
  tracks (corpus tables, coverage section, dataset stats, cross-track result).

---

## Phase 3 harnesses: self-interaction (C2) + multi-turn (C1) — BUILT, awaiting API credits

Built the two generation harnesses the project's most interesting open questions
need. Both are written, structurally tested (role-alternation, resumability,
serialization), and ready to fire the moment the Anthropic credit balance is
topped up. Neither has been run (generation is credit-blocked).

New primitive: `generate.generate_claude_chat(messages, ...)` — multi-turn Claude
generation that captures the reasoning trace into the new `Record.thinking_text`
field (for the Sense C "what does Claude fixate on" analysis).

### C2 — Claude-to-Claude self-interaction (src/generate_selfplay.py)
Two instances of Claude converse from a seed opener for N_TURNS (default 30) across
5 registers (open-ended, philosophical, task, adversarial, everyday) to test where
any attractor (cf. the Claude 4 "spiritual bliss" state) emerges. Seed = A's turn 0;
roles alternate validly from each side. Resumable per conversation. Captures
thinking per turn. Cost ~5x30=150 calls (~a few USD).

### C1 — multi-turn (src/acquire_mtbench.py + src/generate_mtbench.py)
acquire_mtbench.py downloaded the 80 MT-Bench questions (8 categories x 10, two
turns each) -> data/sources/mtbench_manifest.jsonl (DONE, no API). generate_mtbench.py
generates Claude's turn-1 and turn-2 answers per question to test whether the
fingerprint intensifies/shifts across turns. Concurrent, resumable. Cost ~80x2=160 calls.

### To run when credits land
    python3 src/generate_selfplay.py     # -> data/corpus/selfplay_generated.jsonl
    python3 src/generate_mtbench.py      # -> data/corpus/mtbench_generated.jsonl
Then build the analyses (style trajectory over turns; vocab/affirmation/emoji
collapse in self-play; thinking-trace topics for Sense C).
