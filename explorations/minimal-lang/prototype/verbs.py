"""
Verb system for minimal-lang.

A verb is a function + a contract. The contract declares:
- What effects the verb needs (so the system can check at composition time)
- What inputs/outputs it expects (for type checking and documentation)
- Metadata for the system to generate infrastructure around it

The @verb decorator wraps a function with this contract and enables
the system to automatically add logging, timing, error handling, etc.

Usage:
    @verb(
        name="train",
        needs=[Log, Save, Compute],
        describes="Train a model on data with given config",
    )
    def train(model, data, config):
        for epoch in range(config.epochs):
            loss = train_one_epoch(model, data)
            perform(Log("train_loss", loss))
        perform(Save("model", model))
        return Run(status="done")
"""

from __future__ import annotations

import functools
import time
import warnings
from dataclasses import dataclass, field
from typing import Any, Callable

from effects import Effect, perform, _get_stack, track_effects


# ---------------------------------------------------------------------------
# Built-in effects that the system uses to wrap verbs
# ---------------------------------------------------------------------------

class VerbStarted(Effect):
    """Emitted when a verb begins execution."""
    def __init__(self, verb_name: str, args: dict[str, Any]):
        self.verb_name = verb_name
        self.args = args


class VerbCompleted(Effect):
    """Emitted when a verb finishes successfully."""
    def __init__(self, verb_name: str, result: Any, elapsed: float):
        self.verb_name = verb_name
        self.result = result
        self.elapsed = elapsed


class VerbFailed(Effect):
    """Emitted when a verb raises an exception."""
    def __init__(self, verb_name: str, error: Exception, elapsed: float):
        self.verb_name = verb_name
        self.error = error
        self.elapsed = elapsed


# ---------------------------------------------------------------------------
# Verb schema
# ---------------------------------------------------------------------------

@dataclass
class VerbSchema:
    """The contract for a verb -- what it needs, what it does."""
    name: str
    needs: list[type]          # Effect types this verb performs
    describes: str = ""        # Human-readable description
    fn: Callable | None = None # The actual implementation


# ---------------------------------------------------------------------------
# Verb registry
# ---------------------------------------------------------------------------

_registry: dict[str, VerbSchema] = {}


def get_verb(name: str) -> VerbSchema:
    """Look up a registered verb by name."""
    if name not in _registry:
        raise KeyError(f"Unknown verb: {name}. Known: {list(_registry.keys())}")
    return _registry[name]


def list_verbs() -> list[VerbSchema]:
    """List all registered verbs."""
    return list(_registry.values())


# ---------------------------------------------------------------------------
# Check that all required effects have handlers
# ---------------------------------------------------------------------------

def check_effects(schema: VerbSchema) -> list[str]:
    """Check which required effects are missing handlers.

    Returns list of missing effect type names. Empty list = all good.
    """
    stack = _get_stack()
    handled_types = {t for t, _ in stack}
    # VerbStarted/Completed/Failed are optional (system effects)
    system_effects = {VerbStarted, VerbCompleted, VerbFailed}
    missing = []
    for needed in schema.needs:
        if needed not in handled_types and needed not in system_effects:
            missing.append(needed.__name__)
    return missing


# ---------------------------------------------------------------------------
# The @verb decorator
# ---------------------------------------------------------------------------

def verb(
    name: str,
    needs: list[type] | None = None,
    describes: str = "",
):
    """Decorator that turns a function into a verb.

    The decorated function:
    1. Gets registered in the verb registry
    2. Checks effect requirements before running
    3. Emits lifecycle effects (VerbStarted, VerbCompleted, VerbFailed)
    4. Tracks timing

    Example:
        @verb(name="train", needs=[Log, Save])
        def train(model, data, config):
            ...
    """
    needs = needs or []

    def decorator(fn: Callable) -> Callable:
        schema = VerbSchema(
            name=name,
            needs=needs,
            describes=describes,
            fn=fn,
        )
        _registry[name] = schema

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            # Check that all required effects have handlers
            missing = check_effects(schema)
            if missing:
                raise RuntimeError(
                    f"Verb '{name}' requires effect handlers for: {missing}. "
                    f"Install them with `handle()` before calling this verb."
                )

            # Emit lifecycle effect (if handler exists)
            arg_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
            arg_dict = dict(zip(arg_names, args))
            arg_dict.update(kwargs)

            _try_perform(VerbStarted(name, arg_dict))

            start = time.time()
            try:
                with track_effects() as tracker:
                    result = fn(*args, **kwargs)
                elapsed = time.time() - start

                # Check for undeclared effects (simulates compile-time checking)
                _check_undeclared(name, schema.needs, tracker.performed)

                _try_perform(VerbCompleted(name, result, elapsed))
                return result
            except Exception as e:
                elapsed = time.time() - start
                _try_perform(VerbFailed(name, e, elapsed))
                raise

        # Attach schema to the function for introspection
        wrapper.schema = schema
        return wrapper

    return decorator


class UndeclaredEffectWarning(UserWarning):
    """Warned when a verb performs effects it didn't declare in `needs`."""
    pass


def _check_undeclared(verb_name: str, declared: list[type], performed: set[type]):
    """Warn if a verb performed effects it didn't declare.

    In a real language with algebraic effects, the type system catches this
    at compile time. Here we catch it at runtime -- better than not at all.

    Lifecycle effects (VerbStarted/Completed/Failed) are excluded since
    they're emitted by the verb wrapper, not by the verb body.
    """
    # These are system-internal effects, not the verb author's responsibility
    system_effects = {VerbStarted, VerbCompleted, VerbFailed}
    declared_set = set(declared) | system_effects

    undeclared = performed - declared_set
    if undeclared:
        names = sorted(t.__name__ for t in undeclared)
        warnings.warn(
            f"Verb '{verb_name}' performed undeclared effects: {names}. "
            f"Add them to the `needs` list in @verb().",
            UndeclaredEffectWarning,
            stacklevel=3,
        )


def _try_perform(effect: Effect):
    """Perform an effect, silently ignoring if no handler exists.

    Used for optional system effects (lifecycle events).
    """
    try:
        perform(effect)
    except RuntimeError:
        pass  # No handler installed -- that's fine for lifecycle effects
