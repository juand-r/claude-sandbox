"""
Algebraic effect system for minimal-lang.

The core idea: code performs effects (says WHAT it wants), handlers
decide HOW to fulfill them. Functions in the middle don't need to know
about the handlers -- effects propagate up the call stack automatically.

This is a simplified version of algebraic effects using Python's
contextvars and a handler stack. Not as elegant as Koka or Eff, but
it works and demonstrates the mechanism.

Usage:
    # Define an effect type
    class Log(Effect):
        def __init__(self, key, value):
            self.key = key
            self.value = value

    # Perform an effect (in verb body)
    perform(Log("loss", 0.5))

    # Handle an effect (at composition site)
    with handle(Log, my_logger):
        train(model, data, config)
"""

from __future__ import annotations

import contextvars
import warnings
from dataclasses import dataclass
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Handler stack: thread-local stack of effect handlers
# ---------------------------------------------------------------------------

_handler_stack: contextvars.ContextVar[list[tuple[type, Callable]]] = (
    contextvars.ContextVar("_handler_stack", default=[])
)

# ---------------------------------------------------------------------------
# Effect tracking: records which effect types were actually performed
# during a verb execution, so we can detect undeclared effects.
# ---------------------------------------------------------------------------

_effect_tracker: contextvars.ContextVar[list[set[type]] | None] = (
    contextvars.ContextVar("_effect_tracker", default=None)
)


def _get_stack() -> list[tuple[type, Callable]]:
    """Get the current handler stack, creating if needed."""
    try:
        return _handler_stack.get()
    except LookupError:
        stack: list[tuple[type, Callable]] = []
        _handler_stack.set(stack)
        return stack


# ---------------------------------------------------------------------------
# Effect base class
# ---------------------------------------------------------------------------

class Effect:
    """Base class for all effects.

    Subclass this to define new effect types. Effects are plain data
    objects that describe WHAT the code wants, not HOW to do it.
    """
    pass


# ---------------------------------------------------------------------------
# Core operations: perform and handle
# ---------------------------------------------------------------------------

def perform(effect: Effect) -> Any:
    """Perform an effect, dispatching to the nearest handler.

    Walks the handler stack from top (most recently installed) to bottom,
    looking for a handler that matches the effect type. If found, calls
    the handler. If not found, raises UnhandledEffectError.

    This is the ONLY way verb bodies should interact with the outside
    world. No direct I/O, no direct library calls -- just perform effects.
    """
    # Record that this effect type was performed (for undeclared effect detection)
    tracker_stack = _get_tracker_stack()
    if tracker_stack:
        tracker_stack[-1].add(type(effect))

    stack = _get_stack()

    # Walk from top of stack (most recent handler) downward
    for effect_type, handler_fn in reversed(stack):
        if isinstance(effect, effect_type):
            return handler_fn(effect)

    raise UnhandledEffectError(
        f"No handler for effect {type(effect).__name__}. "
        f"Active handlers: {[t.__name__ for t, _ in stack]}"
    )


def _get_tracker_stack() -> list[set[type]]:
    """Get the effect tracker stack, creating if needed."""
    try:
        stack = _effect_tracker.get()
    except LookupError:
        stack = None
    if stack is None:
        stack = []
        _effect_tracker.set(stack)
    return stack


class track_effects:
    """Context manager that tracks which effect types are performed.

    Used by the verb wrapper to detect undeclared effects.

    Usage:
        with track_effects() as tracker:
            some_function()
        performed = tracker.performed  # set of effect types
    """

    def __init__(self):
        self.performed: set[type] = set()

    def __enter__(self):
        _get_tracker_stack().append(self.performed)
        return self

    def __exit__(self, *exc):
        stack = _get_tracker_stack()
        if stack:
            stack.pop()
        return False


class handle:
    """Context manager that installs an effect handler.

    Usage:
        with handle(Log, my_logger):
            # any perform(Log(...)) in here will call my_logger
            train(model, data, config)

    Handlers compose by nesting:
        with handle(Log, wandb_logger):
            with handle(Compute, local_gpu):
                train(model, data, config)

    Or using handle_many:
        with handle_many({Log: wandb_logger, Compute: local_gpu}):
            train(model, data, config)
    """

    def __init__(self, effect_type: type, handler_fn: Callable):
        self.effect_type = effect_type
        self.handler_fn = handler_fn
        self._stack: list[tuple[type, Callable]] | None = None

    def __enter__(self):
        self._stack = _get_stack()
        self._stack.append((self.effect_type, self.handler_fn))
        return self

    def __exit__(self, *exc):
        if self._stack is not None:
            self._stack.pop()
        return False


class handle_many:
    """Install multiple effect handlers at once.

    Usage:
        with handle_many({Log: wandb_logger, Compute: local_gpu}):
            train(model, data, config)
    """

    def __init__(self, handlers: dict[type, Callable]):
        self.handlers = handlers
        self._stack: list[tuple[type, Callable]] | None = None
        self._count = 0

    def __enter__(self):
        self._stack = _get_stack()
        for effect_type, handler_fn in self.handlers.items():
            self._stack.append((effect_type, handler_fn))
            self._count += 1
        return self

    def __exit__(self, *exc):
        if self._stack is not None:
            for _ in range(self._count):
                self._stack.pop()
        return False


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class UnhandledEffectError(RuntimeError):
    """Raised when an effect is performed with no matching handler."""
    pass
