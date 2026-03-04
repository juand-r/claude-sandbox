# Research Takeaways

Notes from the deep research report on Minimal-Lang's design space.

## The Big Validations

1. **The 4-layer architecture is novel as a unified system.** Every layer has
   precedent (Rails for convention-over-config, Haskell for deriving, Alloy
   for domain modeling, Drools for business rules), but nobody has combined
   all four in one language. This is genuinely new territory.

2. **Algebraic effects are the right foundation for pluggable verbs.** This
   was a hunch; the research confirms it. The verb IS the effect, the backend
   IS the handler. Koka and Unison already prove this works. Key advantage:
   intermediate functions don't need to know about effects -- a function
   calling `store(user)` doesn't need to reference the Postgres backend.
   This is exactly what we want.

3. **The LLM era makes this timely.** GitClear's data (211M lines) shows
   current languages + AI tools produce measurably worse code: 4x code clones,
   doubled reverts, collapsed refactoring. The argument: eliminate boilerplate
   at the language level, don't generate it.

## The Big Warnings

### 1. Escape hatches are existential, not optional

Dark died partly because users couldn't escape. MDA died from the cliff
problem. Every successful derivation system (Spring Boot, Prisma, CSS cascade)
succeeds because its override path is clear, graduated, and discoverable.

**The hardest engineering won't be making 50-line declarations work. It will
be making line 4,387 of 5,000 derived lines changeable without understanding
lines 1-4,386.**

The research proposes 4 graduated levels:
- L1: Configuration (change a parameter, not the implementation)
- L2: Hooks (inject logic at extension points)
- L3: Implementation override (replace derived impl with raw code)
- L4: Full external escape (external service handles it)

React's `dangerouslySetInnerHTML` is instructive: name it to discourage
overuse. CSS `!important` is the anti-pattern: unconstrained escape that
everyone uses, destroying the abstraction.

### 2. Continuous derivation, not generate-once

Rails scaffolding generates code you then edit. It drifts from the schema.
Prisma and Hasura continuously derive -- output always reflects current
source of truth. We MUST use continuous derivation, which means:
- Derived code is NEVER hand-edited
- Customizations live in separate override layers
- The separation must be strict and enforced

### 3. The 80/20 trap (Cognitive Technical Debt)

"LLMs are incredible at synthesizing that first 80%. But when the AI
generates a complex routine you don't understand, you're taking out a
high-interest loan of cognitive technical debt." -- Raji Abraham, 2026

This applies to our derivation engine too. If the system derives 5,000
lines and something breaks at line 4,387, the developer has a problem.
Inspectability isn't a nice-to-have, it's load-bearing infrastructure.

### 4. The domain scope question

The 100:1 ratio is achievable for CRUD-centric web applications (Hasura
already does it). It drops sharply for general-purpose computation.

**We must define our domain boundary explicitly rather than claiming
universality.** The 4GL movement failed exactly because they were
domain-limited but pretended otherwise.

This is an uncomfortable truth. The language is probably best suited for
data-centric web/API applications initially. Claiming it replaces C or
Rust for systems programming would be dishonest.

### 5. Training data bootstrapping

LLMs perform dramatically worse on new languages (documented across 111
papers). Our syntax should stay close to well-represented language families
(TypeScript/Python/ML) to avoid this penalty.

This is a real constraint on syntax design. We can't be too exotic.

## Design Adjustments

### Inspectability: Terraform-plan model

The research converges on multiple transparency levels:
- Summary dashboard (like `rails routes`)
- Diff view (like `terraform plan` -- show what CHANGED since last derivation)
- Line-mapped view (like Compiler Explorer/Godbolt)
- Interactive explorer (like GraphQL Playground)

Most users need "User entity -> CRUD API + validation + DB schema" at a
glance, drilling down only when debugging.

Proposed: `explain` command at multiple granularities:
```
explain User              -- summary of all derived artifacts
explain User.store        -- show the derived SQL + migration
explain checkout          -- show expanded behavior with all verb resolutions
explain checkout --diff   -- show what changed since last version
```

### Override model: CSS cascade layers

CSS `@layer` is the best existing model for override precedence:
- Layers are declared upfront in order
- Higher layers override lower, regardless of specificity within a layer
- Backward compatibility with non-layered code is explicit

For us:
```
layer derived       -- system-generated defaults (lowest priority)
layer configured    -- user configuration adjustments
layer custom        -- user-written overrides
layer escape        -- raw backend code (highest priority, most visible)
```

### Type system: bidirectional + row polymorphism

Pure Hindley-Milner produces cryptic errors and doesn't work well with
subtyping/unions. The recommendation:
- Bidirectional checking (better errors)
- Structural typing (entity declarations naturally describe structure)
- Row polymorphism (for entity extension)
- Lightweight refinement types for validation (smart constructors, not SMT)
- ~90% inference, annotations available for documentation

F#'s approach: `type EmailAddress = private EmailAddress of string` with
smart constructors. Makes invalid states unrepresentable.

### Error model: context-dependent policies

When `validate cart is not empty` fails, the right behavior depends:
- HTTP handler -> return 400
- Batch job -> log and skip
- Test -> fail with description
- REPL -> print and continue

Result types with happy-path sugar (Gleam's `use`, Zig's `try`).
Strict separation of validation errors (domain, expected, user-facing)
from runtime errors (infrastructure, unexpected, developer-facing).

**No exceptions.** They hide failure modes, produce incomprehensible
stack traces through generated code, and make reasoning impossible.

### Testing: property-based by default

Property-based testing is natural for derived code. `store User` implies
the roundtrip property: "for all valid Users, store then fetch returns
the same User." The system auto-generates these.

Responsibility split:
- Humans test: business logic (L2) and intent correctness (L3)
- System tests: derivation correctness (L4 -> derived)

Design by Contract (Eiffel): preconditions, postconditions, invariants
as part of the code. If the system derives `store`, it auto-generates
`require: user.isValid()` and `ensure: fetch(user.id) == user`.

## Inform 7 Warning

"Inform has proven to be easy to read but hard to write."

Our Layer 3 verb-based intent must use CONSTRAINED natural language --
a fixed vocabulary -- not open-ended English parsing. The verbs are
keywords, not parsed natural language.

## What's Actually Novel

The unified layering with controlled derivation and principled override
across the entire stack. No existing system provides a coherent chain
from domain declaration -> behavioral intent -> pure logic -> escape
hatches in one language.

Each layer also serves a different stakeholder:
- Layer 4: architects
- Layer 3: product owners
- Layer 2: business analysts / domain experts
- Layer 1: engineers

This is interesting and I hadn't thought about it that way.
