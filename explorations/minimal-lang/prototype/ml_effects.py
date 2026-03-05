"""
ML domain effects.

These are the effect types that ML verbs can perform.
They describe WHAT the verb wants, not HOW to do it.

Each effect is a plain data object. The handler decides
the implementation (W&B vs CSV vs stdout, GPU vs CPU, etc).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from effects import Effect


# ---------------------------------------------------------------------------
# Logging / tracking
# ---------------------------------------------------------------------------

class Log(Effect):
    """Log a metric value at a given step."""
    def __init__(self, key: str, value: float, step: int | None = None):
        self.key = key
        self.value = value
        self.step = step


class LogParams(Effect):
    """Log hyperparameters for the current run."""
    def __init__(self, params: dict[str, Any]):
        self.params = params


# ---------------------------------------------------------------------------
# Saving / loading artifacts
# ---------------------------------------------------------------------------

class Save(Effect):
    """Save an artifact (model, data, etc) to storage."""
    def __init__(self, name: str, obj: Any, metadata: dict[str, Any] | None = None):
        self.name = name
        self.obj = obj
        self.metadata = metadata or {}


class Load(Effect):
    """Load a previously saved artifact."""
    def __init__(self, name: str):
        self.name = name


# ---------------------------------------------------------------------------
# Compute / resource allocation
# ---------------------------------------------------------------------------

class AllocCompute(Effect):
    """Request compute resources for a run."""
    def __init__(self, requirements: dict[str, Any] | None = None):
        self.requirements = requirements or {}


class ReleaseCompute(Effect):
    """Release compute resources after a run."""
    def __init__(self, handle: Any = None):
        self.handle = handle


# ---------------------------------------------------------------------------
# Progress tracking
# ---------------------------------------------------------------------------

class Progress(Effect):
    """Report progress of a long-running operation."""
    def __init__(self, current: int, total: int, message: str = ""):
        self.current = current
        self.total = total
        self.message = message
