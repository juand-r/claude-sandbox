"""
Backend handlers for ML effects.

Each handler is a function that takes an effect and does something
concrete with it. Handlers are pluggable -- swap CSV for W&B,
local for SLURM, etc.

Handlers are intentionally simple. A handler is just a function:
    def my_handler(effect: SomeEffect) -> Any

No classes, no frameworks, no registration ceremony.
"""

from __future__ import annotations

import json
import os
import pickle
import sys
import time
from pathlib import Path
from typing import Any

from effects import Effect
from ml_effects import (
    Log, LogParams, Save, Load,
    AllocCompute, ReleaseCompute, Progress,
)
from verbs import VerbStarted, VerbCompleted, VerbFailed


# ---------------------------------------------------------------------------
# Console handlers (simplest possible -- print to stdout)
# ---------------------------------------------------------------------------

def console_logger(effect: Log):
    """Log metrics to stdout."""
    step_str = f"[step {effect.step}] " if effect.step is not None else ""
    print(f"  {step_str}{effect.key}: {effect.value:.4f}")


def console_params(effect: LogParams):
    """Log hyperparameters to stdout."""
    print(f"  params: {effect.params}")


def console_progress(effect: Progress):
    """Show progress bar on stdout."""
    pct = effect.current / effect.total * 100
    bar_len = 30
    filled = int(bar_len * effect.current / effect.total)
    bar = "=" * filled + "-" * (bar_len - filled)
    msg = f" {effect.message}" if effect.message else ""
    print(f"\r  [{bar}] {pct:5.1f}%{msg}", end="", flush=True)
    if effect.current == effect.total:
        print()  # newline at end


# ---------------------------------------------------------------------------
# CSV handler (simple file-based tracking)
# ---------------------------------------------------------------------------

class CSVLogger:
    """Log metrics to CSV files. One file per metric key."""

    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._files: dict[str, Any] = {}
        self._run_id: str | None = None

    def set_run_id(self, run_id: str):
        self._run_id = run_id

    def __call__(self, effect: Log):
        key = effect.key
        if key not in self._files:
            path = self.output_dir / f"{key}.csv"
            is_new = not path.exists()
            f = open(path, "a")
            if is_new:
                f.write("run_id,step,value\n")
            self._files[key] = f

        f = self._files[key]
        run_id = self._run_id or "unknown"
        step = effect.step if effect.step is not None else ""
        f.write(f"{run_id},{step},{effect.value}\n")
        f.flush()

    def close(self):
        for f in self._files.values():
            f.close()
        self._files.clear()


# ---------------------------------------------------------------------------
# Local filesystem storage handler
# ---------------------------------------------------------------------------

class LocalStorage:
    """Save/load artifacts to local filesystem using pickle."""

    def __init__(self, root: str = "artifacts"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def __call__(self, effect: Save | Load):
        if isinstance(effect, Save):
            return self._save(effect)
        elif isinstance(effect, Load):
            return self._load(effect)

    def _save(self, effect: Save):
        path = self.root / f"{effect.name}.pkl"
        with open(path, "wb") as f:
            pickle.dump(effect.obj, f)

        # Save metadata alongside
        if effect.metadata:
            meta_path = self.root / f"{effect.name}.meta.json"
            with open(meta_path, "w") as f:
                json.dump(effect.metadata, f, indent=2, default=str)

        return str(path)

    def _load(self, effect: Load):
        path = self.root / f"{effect.name}.pkl"
        if not path.exists():
            raise FileNotFoundError(f"Artifact not found: {path}")
        with open(path, "rb") as f:
            return pickle.load(f)


# ---------------------------------------------------------------------------
# Local compute handler (just runs on current machine)
# ---------------------------------------------------------------------------

def local_compute(effect: AllocCompute | ReleaseCompute):
    """Local compute -- no resource allocation needed."""
    if isinstance(effect, AllocCompute):
        # In a real system, this would check GPU availability, etc.
        return {"device": "cpu"}
    elif isinstance(effect, ReleaseCompute):
        pass  # nothing to release locally


# ---------------------------------------------------------------------------
# Verb lifecycle handler (prints verb start/end/fail)
# ---------------------------------------------------------------------------

def lifecycle_printer(effect: VerbStarted | VerbCompleted | VerbFailed):
    """Print verb lifecycle events."""
    if isinstance(effect, VerbStarted):
        print(f"\n--- {effect.verb_name} started ---")
    elif isinstance(effect, VerbCompleted):
        print(f"--- {effect.verb_name} completed ({effect.elapsed:.2f}s) ---")
    elif isinstance(effect, VerbFailed):
        print(f"--- {effect.verb_name} FAILED ({effect.elapsed:.2f}s): {effect.error} ---")


# ---------------------------------------------------------------------------
# Convenience: bundle all handlers for a "local development" setup
# ---------------------------------------------------------------------------

def local_dev_handlers() -> dict[type, Any]:
    """Return a handler set for local development.

    This is equivalent to the backend config in the language:
        tracking: Console
        storage: LocalFS { root: "artifacts/" }
        compute: Local
    """
    return {
        Log: console_logger,
        LogParams: console_params,
        Save: LocalStorage("artifacts"),
        Load: LocalStorage("artifacts"),
        AllocCompute: local_compute,
        ReleaseCompute: local_compute,
        Progress: console_progress,
        VerbStarted: lifecycle_printer,
        VerbCompleted: lifecycle_printer,
        VerbFailed: lifecycle_printer,
    }
