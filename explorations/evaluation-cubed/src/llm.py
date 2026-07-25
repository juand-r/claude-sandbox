"""
Cached, concurrent OpenAI client used by every stage of the Eval-cubed pipeline.

Design notes (for future-me):
  * Every call is keyed by a hash of (model, messages, and all sampling params) and
    stored in a SQLite cache. Re-running a stage therefore costs nothing and is exactly
    reproducible. This matters: the whole project is a study *about* measurement, so the
    measurements themselves must be stable.
  * Failures are loud. A call that fails after retries raises. We do not silently return
    a default, because a silently-defaulted judgement would corrupt every downstream
    statistic in a way that is invisible.
  * Reasoning models (gpt-5.x, o-series) reject `temperature` and use
    `max_completion_tokens`. `chat()` normalises that.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Sequence

from openai import OpenAI

_HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(_HERE, "..", "data", "llm_cache.sqlite")

# Models that use the reasoning-style API surface (no temperature, different token arg).
_REASONING_PREFIXES = ("gpt-5", "o1", "o3", "o4")


def is_reasoning_model(model: str) -> bool:
    return model.startswith(_REASONING_PREFIXES) and "chat-latest" not in model


class _Cache:
    """Tiny SQLite key-value cache. Thread-safe via a lock around a single connection."""

    def __init__(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS cache (k TEXT PRIMARY KEY, v TEXT NOT NULL)"
        )
        self._conn.commit()

    def get(self, key: str) -> str | None:
        with self._lock:
            row = self._conn.execute("SELECT v FROM cache WHERE k = ?", (key,)).fetchone()
        return row[0] if row else None

    def put(self, key: str, value: str) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO cache (k, v) VALUES (?, ?)", (key, value)
            )
            self._conn.commit()

    def count(self) -> int:
        with self._lock:
            return self._conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0]


_cache = _Cache(CACHE_PATH)
_client = OpenAI(timeout=180.0, max_retries=0)

# Crude global usage accounting so we always know what a run cost.
_usage_lock = threading.Lock()
USAGE: dict[str, dict[str, int]] = {}


def _record_usage(model: str, prompt_tokens: int, completion_tokens: int) -> None:
    with _usage_lock:
        u = USAGE.setdefault(model, {"prompt": 0, "completion": 0, "calls": 0})
        u["prompt"] += prompt_tokens
        u["completion"] += completion_tokens
        u["calls"] += 1


def usage_report() -> str:
    with _usage_lock:
        lines = ["model                          calls     prompt  completion"]
        for m, u in sorted(USAGE.items()):
            lines.append(f"{m:<28} {u['calls']:>7} {u['prompt']:>10} {u['completion']:>11}")
        return "\n".join(lines)


def _key(model: str, messages: Sequence[dict], **params) -> str:
    blob = json.dumps(
        {"model": model, "messages": list(messages), "params": params},
        sort_keys=True,
        ensure_ascii=False,
    )
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def chat(
    model: str,
    messages: Sequence[dict],
    *,
    max_tokens: int = 1024,
    temperature: float = 0.0,
    seed: int | None = 0,
    reasoning_effort: str | None = None,
    use_cache: bool = True,
    n_retries: int = 5,
) -> str:
    """Single chat completion, cached. Returns the assistant message text."""
    cache_params = {
        "max_tokens": max_tokens,
        "temperature": temperature,
        "seed": seed,
        "reasoning_effort": reasoning_effort,
    }
    k = _key(model, messages, **cache_params)
    if use_cache:
        hit = _cache.get(k)
        if hit is not None:
            return json.loads(hit)["text"]

    kwargs: dict[str, Any] = {"model": model, "messages": list(messages)}
    if is_reasoning_model(model):
        kwargs["max_completion_tokens"] = max_tokens
        if reasoning_effort:
            kwargs["reasoning_effort"] = reasoning_effort
    else:
        kwargs["max_tokens"] = max_tokens
        kwargs["temperature"] = temperature
        if seed is not None:
            kwargs["seed"] = seed

    last_err: Exception | None = None
    for attempt in range(n_retries):
        try:
            resp = _client.chat.completions.create(**kwargs)
            text = resp.choices[0].message.content or ""
            if not text.strip():
                raise RuntimeError(
                    f"empty completion from {model} "
                    f"(finish_reason={resp.choices[0].finish_reason})"
                )
            if resp.usage:
                _record_usage(model, resp.usage.prompt_tokens, resp.usage.completion_tokens)
            _cache.put(k, json.dumps({"text": text}))
            return text
        except Exception as e:  # noqa: BLE001 - we re-raise below after retries
            last_err = e
            time.sleep(min(2 ** attempt, 30))
    raise RuntimeError(f"chat() failed for {model} after {n_retries} attempts: {last_err}")


@dataclass
class Job:
    """One unit of work for `run_many`. `payload` is carried through untouched."""

    fn: Callable[[], Any]
    payload: Any = None


def run_many(jobs: Sequence[Job], workers: int = 16, desc: str = "") -> list[Any]:
    """Run jobs concurrently, preserving input order. Any exception propagates."""
    results: list[Any] = [None] * len(jobs)
    done = 0
    lock = threading.Lock()
    t0 = time.time()

    def _run(idx: int):
        nonlocal done
        out = jobs[idx].fn()
        with lock:
            done += 1
            if done % 50 == 0 or done == len(jobs):
                el = time.time() - t0
                rate = done / el if el else 0
                print(
                    f"  [{desc}] {done}/{len(jobs)}  {el:6.1f}s  {rate:5.1f}/s",
                    flush=True,
                )
        return idx, out

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for idx, out in ex.map(_run, range(len(jobs))):
            results[idx] = out
    return results


def extract_json(text: str) -> Any:
    """Pull the first JSON object/array out of a model response. Raises if absent."""
    s = text.strip()
    if s.startswith("```"):
        s = s.split("```")[1]
        if s.startswith("json"):
            s = s[4:]
        s = s.strip()
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass
    for opener, closer in (("{", "}"), ("[", "]")):
        i = s.find(opener)
        j = s.rfind(closer)
        if i != -1 and j > i:
            try:
                return json.loads(s[i : j + 1])
            except json.JSONDecodeError:
                continue
    raise ValueError(f"no JSON found in response: {text[:400]!r}")


if __name__ == "__main__":
    print("cache entries:", _cache.count())
    print(chat("gpt-4.1-mini", [{"role": "user", "content": "Reply with exactly: OK"}], max_tokens=8))
    print(usage_report())
