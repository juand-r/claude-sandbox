"""Shared LLM-call helper for the time experiments.

One unified `call()` across Anthropic and OpenAI that returns the text plus the
data every experiment needs: wall-clock latency and token usage. Handles the
`max_tokens` vs `max_completion_tokens` split and retries transient errors.

Import this from each experiment's run.py. Do not duplicate provider logic.
"""

import os
import time
from dataclasses import dataclass, asdict

from anthropic import Anthropic
from openai import OpenAI

# --- Model roster -----------------------------------------------------------
# provider, api_id. "tier" is informational. Reasoning models burn hidden tokens,
# so latency decouples from visible output length — relevant to E1/E2.
MODELS = {
    # Anthropic
    "haiku":   ("anthropic", "claude-haiku-4-5-20251001"),
    "sonnet":  ("anthropic", "claude-sonnet-4-6"),
    "opus":    ("anthropic", "claude-opus-4-8"),
    # OpenAI
    "gpt4o-mini": ("openai", "gpt-4o-mini"),
    "gpt4o":      ("openai", "gpt-4o"),
    "gpt5":       ("openai", "gpt-5"),       # reasoning model
    "gpt5.2":     ("openai", "gpt-5.2"),     # reasoning model
    "o4-mini":    ("openai", "o4-mini"),     # reasoning model
}

REASONING_MODELS = {"gpt5", "gpt5.2", "o4-mini"}

_anthropic = None
_openai = None


def _clients():
    global _anthropic, _openai
    if _anthropic is None:
        _anthropic = Anthropic()
    if _openai is None:
        _openai = OpenAI()
    return _anthropic, _openai


@dataclass
class Result:
    model: str
    text: str
    latency_s: float       # wall-clock for the API call
    input_tokens: int
    output_tokens: int     # includes reasoning tokens for reasoning models
    reasoning_tokens: int = 0   # OpenAI reasoning models only; 0 otherwise
    ok: bool = True
    error: str = ""

    def to_dict(self):
        return asdict(self)


def call(model: str, prompt: str, *, system: str | None = None,
         max_tokens: int = 1024, temperature: float | None = None,
         retries: int = 4) -> Result:
    """Call a model by roster key (e.g. 'sonnet', 'gpt5'). Returns Result.

    latency_s is measured around the network call. For reasoning models the
    token budget is bumped up because hidden reasoning consumes output tokens.
    """
    if model not in MODELS:
        raise ValueError(f"unknown model {model!r}; pick from {list(MODELS)}")
    provider, api_id = MODELS[model]
    anthropic_c, openai_c = _clients()

    if model in REASONING_MODELS:
        max_tokens = max(max_tokens, 4096)

    last_err = ""
    for attempt in range(retries):
        try:
            t0 = time.perf_counter()
            if provider == "anthropic":
                kwargs = dict(model=api_id, max_tokens=max_tokens,
                              messages=[{"role": "user", "content": prompt}])
                if system:
                    kwargs["system"] = system
                if temperature is not None:
                    kwargs["temperature"] = temperature
                m = anthropic_c.messages.create(**kwargs)
                dt = time.perf_counter() - t0
                text = "".join(b.text for b in m.content if b.type == "text")
                return Result(model, text, dt, m.usage.input_tokens,
                              m.usage.output_tokens)
            else:  # openai
                msgs = ([{"role": "system", "content": system}] if system else []) \
                       + [{"role": "user", "content": prompt}]
                kwargs = dict(model=api_id, messages=msgs)
                # reasoning + gpt-5 family use max_completion_tokens and reject temperature
                if model in REASONING_MODELS:
                    kwargs["max_completion_tokens"] = max_tokens
                else:
                    kwargs["max_tokens"] = max_tokens
                    if temperature is not None:
                        kwargs["temperature"] = temperature
                r = openai_c.chat.completions.create(**kwargs)
                dt = time.perf_counter() - t0
                text = r.choices[0].message.content or ""
                u = r.usage
                det = getattr(u, "completion_tokens_details", None)
                rtok = getattr(det, "reasoning_tokens", 0) or 0
                return Result(model, text, dt, u.prompt_tokens, u.completion_tokens,
                              reasoning_tokens=rtok)
        except Exception as e:  # noqa: BLE001 - surface error after retries
            last_err = repr(e)[:300]
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    return Result(model, "", 0.0, 0, 0, ok=False, error=last_err)


if __name__ == "__main__":
    # quick self-test
    for key in ["haiku", "gpt4o-mini"]:
        r = call(key, "Reply with exactly: OK", max_tokens=10)
        print(key, "->", repr(r.text.strip()), f"{r.latency_s:.2f}s",
              "out_tok", r.output_tokens, "ok" if r.ok else r.error)
