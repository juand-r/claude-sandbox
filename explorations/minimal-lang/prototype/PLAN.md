# Prototype Plan

## Goal

Build a working Python prototype of the verb/effect system.
Not a parser -- the runtime engine that would power the language.

## Architecture

```
effects.py      -- Core algebraic effect system (perform/handle)
verbs.py        -- Verb schema, registry, decorator
handlers.py     -- Backend handlers (logging, checkpointing, compute)
ml_domain.py    -- ML domain pack: train, evaluate, sweep verbs
demo.py         -- Working demo: define model, run sweep, get results
```

## Key Design Decisions

1. Effects are simple: `perform(Log("train_loss", 0.5))` -- the verb body
   says WHAT it wants, not HOW to do it. The handler decides HOW.

2. Verbs are decorated functions that declare their effect requirements.
   The system checks at composition time that all effects are handled.

3. Handlers are context managers that intercept effects. They compose:
   `with handle(Log, wandb_logger), handle(Compute, local_gpu):`.

4. Sweep is a higher-order verb that takes another verb and runs it
   across a config grid, handling parallelism and failure.

## Status

- [x] effects.py -- core effect system
- [x] verbs.py -- verb schema and registry
- [x] handlers.py -- backend handlers
- [x] ml_effects.py + ml_verbs.py -- ML domain effects and verbs
- [x] demo.py -- working demo
- [x] test_effects.py -- 24 tests, all passing
