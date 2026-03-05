# Post-Mortem: Minimal-Lang Exploration

## What was the goal?

Design a language that eliminates boilerplate by operating at a higher level
of abstraction -- "the level of thinking." The idea was that most code is
mechanical translation from intent to implementation, and a language could
close that gap.

We narrowed the scope to ML workflows (train, evaluate, sweep) and explored
algebraic effects as the core mechanism: verbs declare WHAT they do, handlers
supply HOW.

## What we built

A Python prototype with:
- An algebraic effect system (perform/handle via context managers)
- A verb system (@verb decorator with declared effect requirements)
- ML-specific verbs (train, evaluate, sweep) and effects (Log, Save, Compute, etc.)
- Runtime detection of undeclared effects (simulating compile-time checking)
- A demo showing swappable backends, sweeps, and error detection

It works mechanically. The code is clean enough. Tests pass.

## Why it doesn't hold up

### 1. It's just Python with extra steps

The effect system is context managers. The verb system is a decorator. There's
no parser, no new syntax, no compilation. Everything we built could be
replaced by dependency injection or callback passing -- patterns Python
already supports natively.

The abstraction layer doesn't earn its keep over existing solutions.

### 2. The boilerplate didn't disappear, it moved

The central claim was: "the verb body stays the same, and all the messy
variation goes into handlers." But someone still writes the handlers. The
W&B integration code, the GPU allocation logic, the S3 checkpoint saving --
all of that still exists, just in a different place.

If it's the same person writing both (which it usually is), the separation
is pure overhead. If it's a team, they already solve this with libraries.

### 3. Real-world variability defeats the abstraction

The bet was that ML workflows have enough common structure to factor out.
But real ML code is messy: custom data pipelines, model surgery, ad-hoc
debugging, one-off hacks. A framework that assumes regularity fights you
when you need irregularity -- which is most of the time.

### 4. The "language of intent" problem is AI-shaped, not language-shaped

The original insight (BRAINSTORM.md) was correct: humans think at layer 3-4
but code at layer 1-2. But the solution isn't a new language -- it's an LLM
that translates between layers in whatever language you already use. Which
is exactly what tools like Claude Code do today.

A new language adds a new thing to learn, a new ecosystem to build, new
tooling to create. The cost-benefit ratio is terrible when LLMs already
bridge the abstraction gap in existing languages.

## What was worth keeping

- **Algebraic effects as a concept** are genuinely useful for understanding
  how to structure side-effectful code. Worth knowing even if building a
  language around them isn't justified here.
- **The verb/effect separation** is a decent API pattern for library design
  (cf. React hooks, Redux middleware). Not novel enough for a language, but
  a good design principle.
- **Runtime effect tracking** (detecting undeclared effects) was a neat trick
  and demonstrates what you lose without a real type system.

## Verdict

The exploration answered the question. The answer is: algebraic effects are
a powerful language-level concept, but simulating them as a Python library
doesn't buy enough over what Python already offers. And a new language
designed around them faces the same problem every new language faces --
ecosystem bootstrapping -- with the added headwind that LLMs are making
existing languages more productive faster than a new language could catch up.

Closing this exploration.
