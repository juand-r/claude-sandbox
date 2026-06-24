# Claudespeak

Characterizing the stylistic fingerprint of Anthropic's Claude, comparatively
against human text and other LLMs. See `PLAN.md` for the approved plan and
`NOTES.md` for the running log.

## Layout
- `PLAN.md` — approved plan (scope, methods, cost, phasing).
- `NOTES.md` — progress log + decisions/caveats.
- `schema/record_schema.md` — corpus record format (one generation per JSONL line).
- `src/` — pipeline:
  - `schema.py` — record dataclass + JSONL I/O + raw-response saving.
  - `generate.py` — Claude / OpenAI generation wrappers (full provenance).
  - `acquire_hc3.py` — build pilot manifest + reused human/ChatGPT cells from HC3.
  - `generate_pilot.py` — resumable driver for self-generated cells.
- `data/`
  - `sources/` — prompt manifests + cached source data.
  - `corpus/` — normalized JSONL records (the reusable dataset).
  - `raw_responses/` — verbatim API responses (belt-and-suspenders).

## Reproduce the pilot
```bash
pip install anthropic openai 'datasets>=2.0' pandas numpy
export ANTHROPIC_API_KEY=... OPENAI_API_KEY=... HF_TOKEN=...
cd explorations/claudespeak
python3 src/acquire_hc3.py        # manifest + reused human/chatgpt cells
python3 src/generate_pilot.py     # generate Claude + GPT-4o (resumable)
```

Every generation is saved with full metadata (model, version, effort/temperature,
system prompt, token usage, timestamp, git commit), so the corpus is reusable for
any downstream analysis without regenerating.
