# Claudespeak corpus — record schema

The corpus is stored as **JSONL** (one JSON object per line) under `data/corpus/`.
Each line is **one generation**: a single completion of one prompt by one source
(a model or a human). Parallel cells (same prompt, different sources) share a
`prompt_id`. Multi-turn cells share a `conversation_id`.

Design goal (per project owner): **everything needed to reproduce or reuse a
generation lives in the record.** If we have all records, we never regenerate,
and any downstream analysis runs off the saved corpus alone.

## Fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `record_id` | str | yes | Globally unique id for this generation (uuid4). |
| `prompt_id` | str | yes | Stable id shared by all sources answering the *same* prompt. |
| `conversation_id` | str | yes | Groups turns of one multi-turn conversation. Equals `prompt_id` for single-turn. |
| `turn_index` | int | yes | 0 for the first/only assistant turn; increments per turn. |
| `prompt` | str | yes | The full user prompt/instruction this completion answers. |
| `prompt_source` | obj | yes | `{dataset, dataset_version, original_id, split}` — provenance of the prompt. |
| `domain` | str\|null | no | Topic area if known (science, history, coding, finance, …). |
| `task_type` | str\|null | no | Format/task (qa, explanation, email, summary, creative, …). |
| `source_type` | str | yes | `"model"` or `"human"`. |
| `generator` | str | yes | Display name of the producer (e.g. `claude-opus-4-8`, `gpt-4o`, `human`). |
| `generator_family` | str | yes | `claude` \| `openai` \| `google` \| `deepseek` \| `qwen` \| `meta` \| `microsoft` \| `human` \| `other`. |
| `generator_version` | str\|null | yes | Exact model id / snapshot string (null for human). |
| `provenance` | str | yes | `"self_generated"` or `"reused"`. |
| `reuse_source` | obj\|null | if reused | `{dataset, dataset_version, original_id, url}` for reused completions. |
| `completion` | str | yes | The generated/written text. |
| `gen_params` | obj | yes | Decoding/config — see below. Empty `{}` for reused/human where unknown. |
| `usage` | obj\|null | no | `{input_tokens, output_tokens, thinking_tokens}` when reported by the API. |
| `timestamp_utc` | str | yes | ISO-8601 UTC of when the record was created. |
| `harness_git_commit` | str\|null | yes | Git commit of this repo when generated (reproducibility). |
| `raw_response_path` | str\|null | no | Relative path to the verbatim API response under `data/raw_responses/`. |
| `notes` | str\|null | no | Free-text caveats (e.g. "human anchor matched on domain, not prompt"). |

### `gen_params` (the reproducibility core)

For **self-generated** model records, capture exactly what controls the output:

| Key | Meaning |
|---|---|
| `temperature` | Sampling temperature (null if the model/endpoint forbids it — e.g. Opus 4.8 rejects `temperature`). |
| `top_p`, `top_k` | If used (null otherwise). |
| `max_tokens` | Output cap requested. |
| `thinking` | `{type: "adaptive"\|"disabled"\|null, effort: "low"\|"medium"\|"high"\|"xhigh"\|"max"\|null}`. |
| `system_prompt` | The exact system prompt string (or null). |
| `seed` | If the endpoint supports one. |
| `stop_reason` | Reported stop reason. |
| `api` | `{provider, endpoint, sdk_version}`. |

> Note: Opus 4.8 does **not** accept `temperature`/`top_p`/`top_k` (400 error) and
> uses adaptive thinking with an `effort` knob. So for Claude, the meaningful
> decoding levers are `effort` and `system_prompt`, recorded above. We log
> `temperature: null` for Claude rather than omitting the field, so the schema is
> uniform across providers.

## Raw responses

Every self-generated call also writes the **verbatim API response JSON** to
`data/raw_responses/<generator>/<record_id>.json`. The normalized record points
to it via `raw_response_path`. This is belt-and-suspenders: even if our
normalization has a bug, the original response is preserved.

## Invariants

- One JSONL line = one generation. Never overwrite; append-only.
- `(prompt_id, generator, turn_index)` is unique within a corpus file.
- Reused records must carry `reuse_source`; self-generated must carry
  `harness_git_commit` and (for models) non-empty `gen_params`.
