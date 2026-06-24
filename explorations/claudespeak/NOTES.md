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

### TODO (next)
- [ ] Length-stratified re-run of the prose ablation (robustness).
- [ ] AlpacaEval track: modern Gemini/DeepSeek/Qwen/Llama/Phi (reused) + Claude.
- [ ] Claude thinking-effort sweep (low/med/high).
- [ ] n-gram mining (rusty-dawg / infini-gram) for over-represented phrases.
- [ ] Interpretable classifier on prose-only features (separability number).
