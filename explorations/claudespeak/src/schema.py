"""Canonical corpus record schema + JSONL I/O for the Claudespeak project.

One record = one generation (a single completion of one prompt by one source,
model or human). See ../schema/record_schema.md for the field documentation.

The point of this module: make it trivial to write fully-provenanced records and
impossible to forget the reproducibility metadata. If a self-generated model
record is missing gen_params, validation fails loudly.
"""
from __future__ import annotations

import dataclasses
import datetime as _dt
import json
import os
import subprocess
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RAW_DIR = os.path.join(REPO, "data", "raw_responses")
CORPUS_DIR = os.path.join(REPO, "data", "corpus")


def utcnow_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def git_commit() -> Optional[str]:
    """Current repo commit, for reproducibility. None if unavailable."""
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO, stderr=subprocess.DEVNULL
        )
        return out.decode().strip()
    except Exception:
        return None


@dataclass
class Record:
    # identity / linkage
    prompt: str
    prompt_id: str
    generator: str
    generator_family: str
    source_type: str  # "model" | "human"
    completion: str
    generator_version: Optional[str] = None
    provenance: str = "self_generated"  # "self_generated" | "reused"
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: Optional[str] = None  # defaults to prompt_id if None
    turn_index: int = 0

    # provenance of the prompt and (if reused) the completion
    prompt_source: dict = field(default_factory=dict)
    reuse_source: Optional[dict] = None

    # descriptive
    domain: Optional[str] = None
    task_type: Optional[str] = None

    # reproducibility core
    gen_params: dict = field(default_factory=dict)
    usage: Optional[dict] = None
    thinking_text: Optional[str] = None  # captured reasoning trace (Sense C); may be None
    timestamp_utc: str = field(default_factory=utcnow_iso)
    harness_git_commit: Optional[str] = field(default_factory=git_commit)
    raw_response_path: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self):
        if self.conversation_id is None:
            self.conversation_id = self.prompt_id

    def validate(self) -> None:
        """Fail loudly if reproducibility metadata is missing."""
        assert self.source_type in ("model", "human"), self.source_type
        assert self.generator_family in (
            "claude", "openai", "google", "deepseek", "qwen",
            "meta", "microsoft", "mistral", "human", "other",
        ), self.generator_family
        assert self.provenance in ("self_generated", "reused"), self.provenance
        assert self.completion is not None, "completion missing"
        assert self.prompt_id and self.generator, "prompt_id/generator required"
        if self.provenance == "reused":
            assert self.reuse_source, "reused record needs reuse_source"
        if self.provenance == "self_generated" and self.source_type == "model":
            assert self.harness_git_commit is not None, "need git commit for self-gen"
            assert self.gen_params, "self-generated model record needs gen_params"

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


def append_records(path: str, records: list[Record]) -> None:
    """Append validated records to a JSONL corpus file (append-only)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for r in records:
        r.validate()
    with open(path, "a", encoding="utf-8") as f:
        for r in records:
            f.write(r.to_json() + "\n")


def read_records(path: str) -> list[dict]:
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def save_raw_response(generator: str, record_id: str, raw: Any) -> str:
    """Write the verbatim API response; return path relative to repo root."""
    d = os.path.join(RAW_DIR, generator.replace("/", "_"))
    os.makedirs(d, exist_ok=True)
    rel = os.path.join("data", "raw_responses", generator.replace("/", "_"),
                       f"{record_id}.json")
    with open(os.path.join(REPO, rel), "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2, default=str)
    return rel


if __name__ == "__main__":
    # smoke test
    r = Record(
        prompt="What is the capital of France?",
        prompt_id="demo-1",
        generator="claude-opus-4-8",
        generator_family="claude",
        generator_version="claude-opus-4-8",
        source_type="model",
        completion="Paris.",
        gen_params={"thinking": {"type": "adaptive", "effort": "high"},
                    "temperature": None, "max_tokens": 1024,
                    "system_prompt": None},
        usage={"input_tokens": 12, "output_tokens": 3},
    )
    r.validate()
    print(r.to_json())
    print("schema smoke test OK")
