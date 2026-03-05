# Minimal-Lang Prototype: Verb/Effect Engine

Working prototype of the core runtime mechanism for minimal-lang.
Not a parser -- the engine that would power the language.

## What this demonstrates

The thesis: **verbs are contracts, not just functions.** A verb declares
what effects it needs (logging, storage, compute). The system checks
these requirements at composition time and provides pluggable backends.

The researcher writes ONLY the domain-specific logic. The system handles
logging, checkpointing, resource allocation, progress tracking, etc.

## Architecture

```
effects.py      -- Core algebraic effect system (perform/handle)
verbs.py        -- Verb schema, registry, @verb decorator
ml_effects.py   -- ML domain effects (Log, Save, AllocCompute, etc.)
ml_verbs.py     -- ML domain verbs (train, evaluate, sweep)
handlers.py     -- Backend handlers (console, CSV, local filesystem)
demo.py         -- Working demo: single run, sweep, analysis, backend swap
test_effects.py -- Tests (24 tests)
```

## Run

```bash
python demo.py              # Run the full demo
python -m pytest test_effects.py -v  # Run tests
```

## Key concepts

1. **Effects** describe WHAT code wants (`Log("loss", 0.5)`) -- not HOW
2. **Handlers** decide HOW (`console_logger`, `CSVLogger`, `wandb_logger`)
3. **Verbs** declare which effects they need (`@verb(needs=[Log, Save])`)
4. **The system checks** that all effects are handled before running
5. **Backends are swappable** -- change one line to go from console to W&B
