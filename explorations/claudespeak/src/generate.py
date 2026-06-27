"""Generation wrappers that emit fully-provenanced corpus Records.

Currently supports:
  - Claude (Anthropic) — Opus 4.8 family, adaptive thinking + effort knob.
  - OpenAI GPT — a current GPT for the self-generated contrast cell.

Gemini / DeepSeek / Qwen are NOT generated here (no API keys); those cells are
reused from existing parallel datasets via acquire.py.

Every call saves the verbatim API response and records the exact decoding config.
"""
from __future__ import annotations

import os
from typing import Optional

from schema import Record, save_raw_response

# ----------------------------------------------------------------------------
# Claude
# ----------------------------------------------------------------------------
import anthropic

_anthropic_client = None


def _anthropic():
    global _anthropic_client
    if _anthropic_client is None:
        _anthropic_client = anthropic.Anthropic()
    return _anthropic_client


def generate_claude(
    prompt: str,
    prompt_id: str,
    *,
    model: str = "claude-opus-4-8",
    effort: Optional[str] = "high",   # None => thinking disabled
    system_prompt: Optional[str] = None,
    max_tokens: int = 4096,
    prompt_source: Optional[dict] = None,
    domain: Optional[str] = None,
    task_type: Optional[str] = None,
) -> Record:
    """Generate one Claude completion. effort=None disables thinking.

    Opus 4.8 rejects temperature/top_p/top_k, so they are recorded as null.
    Decoding levers that matter for Claude: `effort` and `system_prompt`.
    """
    if effort is None:
        thinking = {"type": "disabled"}
        output_config = None
    else:
        thinking = {"type": "adaptive"}
        output_config = {"effort": effort}

    kwargs = dict(model=model, max_tokens=max_tokens, thinking=thinking,
                  messages=[{"role": "user", "content": prompt}])
    if output_config is not None:
        kwargs["output_config"] = output_config
    if system_prompt is not None:
        kwargs["system"] = system_prompt

    resp = _anthropic().messages.create(**kwargs)

    text = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
    thinking_text = "".join(
        getattr(b, "thinking", "") for b in resp.content
        if getattr(b, "type", None) == "thinking"
    )

    rec = Record(
        prompt=prompt, prompt_id=prompt_id,
        generator=model, generator_family="claude", generator_version=model,
        source_type="model", completion=text, provenance="self_generated",
        prompt_source=prompt_source or {}, domain=domain, task_type=task_type,
        gen_params={
            "temperature": None, "top_p": None, "top_k": None,
            "max_tokens": max_tokens,
            "thinking": {"type": thinking["type"], "effort": effort},
            "system_prompt": system_prompt,
            "stop_reason": resp.stop_reason,
            "api": {"provider": "anthropic", "endpoint": "messages",
                    "sdk_version": anthropic.__version__},
        },
        usage={
            "input_tokens": resp.usage.input_tokens,
            "output_tokens": resp.usage.output_tokens,
            "thinking_chars": len(thinking_text),
        },
    )
    rec.raw_response_path = save_raw_response(model, rec.record_id,
                                              resp.model_dump())
    return rec


def generate_claude_chat(
    messages: list,
    prompt_id: str,
    *,
    model: str = "claude-opus-4-8",
    effort: Optional[str] = "high",
    system_prompt: Optional[str] = None,
    max_tokens: int = 4096,
    conversation_id: Optional[str] = None,
    turn_index: int = 0,
    prompt_source: Optional[dict] = None,
    domain: Optional[str] = None,
    task_type: Optional[str] = None,
    notes: Optional[str] = None,
) -> Record:
    """Multi-turn Claude generation.

    `messages` is a full alternating user/assistant list (last entry must be a
    user turn); this is the primitive behind the multi-turn and self-interaction
    harnesses. Captures the reasoning trace into Record.thinking_text (Sense C).
    The Record's `prompt` field stores the latest user message; the full dialogue
    is reconstructable from conversation_id + turn_index across the corpus file.
    """
    if effort is None:
        thinking = {"type": "disabled"}
        output_config = None
    else:
        thinking = {"type": "adaptive"}
        output_config = {"effort": effort}

    kwargs = dict(model=model, max_tokens=max_tokens, thinking=thinking,
                  messages=messages)
    if output_config is not None:
        kwargs["output_config"] = output_config
    if system_prompt is not None:
        kwargs["system"] = system_prompt

    resp = _anthropic().messages.create(**kwargs)
    text = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
    thinking_text = "".join(
        getattr(b, "thinking", "") for b in resp.content
        if getattr(b, "type", None) == "thinking"
    )
    last_user = next((m["content"] for m in reversed(messages)
                      if m["role"] == "user"), "")

    rec = Record(
        prompt=last_user, prompt_id=prompt_id,
        conversation_id=conversation_id, turn_index=turn_index,
        generator=model, generator_family="claude", generator_version=model,
        source_type="model", completion=text, provenance="self_generated",
        prompt_source=prompt_source or {}, domain=domain, task_type=task_type,
        thinking_text=thinking_text or None, notes=notes,
        gen_params={
            "temperature": None, "top_p": None, "top_k": None,
            "max_tokens": max_tokens,
            "thinking": {"type": thinking["type"], "effort": effort},
            "system_prompt": system_prompt, "n_input_messages": len(messages),
            "stop_reason": resp.stop_reason,
            "api": {"provider": "anthropic", "endpoint": "messages",
                    "sdk_version": anthropic.__version__},
        },
        usage={
            "input_tokens": resp.usage.input_tokens,
            "output_tokens": resp.usage.output_tokens,
            "thinking_chars": len(thinking_text),
        },
    )
    rec.raw_response_path = save_raw_response(model, rec.record_id,
                                              resp.model_dump())
    return rec


# ----------------------------------------------------------------------------
# OpenAI GPT
# ----------------------------------------------------------------------------
import openai

_openai_client = None


def _openai():
    global _openai_client
    if _openai_client is None:
        _openai_client = openai.OpenAI()
    return _openai_client


def generate_openai(
    prompt: str,
    prompt_id: str,
    *,
    model: str = "gpt-4o",
    temperature: float = 1.0,
    system_prompt: Optional[str] = None,
    max_tokens: int = 4096,
    prompt_source: Optional[dict] = None,
    domain: Optional[str] = None,
    task_type: Optional[str] = None,
) -> Record:
    msgs = []
    if system_prompt:
        msgs.append({"role": "system", "content": system_prompt})
    msgs.append({"role": "user", "content": prompt})

    resp = _openai().chat.completions.create(
        model=model, messages=msgs, temperature=temperature,
        max_tokens=max_tokens,
    )
    text = resp.choices[0].message.content or ""

    rec = Record(
        prompt=prompt, prompt_id=prompt_id,
        generator=model, generator_family="openai", generator_version=resp.model,
        source_type="model", completion=text, provenance="self_generated",
        prompt_source=prompt_source or {}, domain=domain, task_type=task_type,
        gen_params={
            "temperature": temperature, "top_p": None, "top_k": None,
            "max_tokens": max_tokens, "thinking": None,
            "system_prompt": system_prompt,
            "stop_reason": resp.choices[0].finish_reason,
            "api": {"provider": "openai", "endpoint": "chat.completions",
                    "sdk_version": openai.__version__},
        },
        usage={
            "input_tokens": resp.usage.prompt_tokens,
            "output_tokens": resp.usage.completion_tokens,
        },
    )
    rec.raw_response_path = save_raw_response(model, rec.record_id,
                                              resp.model_dump())
    return rec


if __name__ == "__main__":
    # live single-prompt test (uses real API)
    r = generate_claude(
        "In one sentence, what makes a good cup of coffee?",
        "smoke-claude-1", effort="low", max_tokens=512,
    )
    print("CLAUDE:", r.completion[:200])
    print("usage:", r.usage, "| effort:", r.gen_params["thinking"])
    print("raw saved:", r.raw_response_path)
