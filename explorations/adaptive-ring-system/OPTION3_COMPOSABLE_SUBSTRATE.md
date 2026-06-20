# Option 3 --- A Composable-Primitive Substrate (design / launch doc)

Status: **design, awaiting go-ahead on the primitive choice.** This begins the
deliberate "option 3" pivot flagged in `REPORT.md` section 7 and `TRAJECTORY.md`.
It is a *new substrate*, not a modification of the ring system; it reuses the
ring system's hard-won lessons but replaces the building block.

## 1. Why

The ring system climbs the whole ladder --- persistence, heredity, adaptation,
emergent spatial structure, open-ended novelty --- but **walls at complexity**
(E13--E15, R4). The cause is specific and now well established: the elementary
8-bit CA rule is **not composable**. Stacking ECA rules does not yield
incrementally-better behaviour, so selection saturates at shallow complexity even
when complexity is directly rewarded (E15). To test whether *open-ended
complexity growth* is achievable at all, we need a primitive whose compositions
vary smoothly and richly with length.

## 2. What to keep (the transferable lessons)

These were substrate-independent and should carry over:

- **Heredity is the master key** --- nothing works until genomes reliably
  persist. The new substrate must make heredity cheap (likely built-in copying,
  Tierra/Avida-style, rather than emergent-from-chaos).
- **Locality matters** --- a spatial medium gave coexistence, ecology, and made
  structure legible. Keep an optional 2-D torus.
- **Self-templating / functional reproduction** --- tying reproduction to a
  ring's *function* gave emergent selection. The analog here is self-replication.
- **Measure against nulls; match metric to type** (R1). Reuse the analysis
  discipline; add a real complexity metric (e.g. logical depth / task repertoire,
  not just compressibility).

## 3. Design goals

1. **Composability** --- adding instructions can incrementally change behaviour,
   so selection has a gradient to climb toward complex function.
2. **Expressiveness** --- Turing-ish; able in principle to compute non-trivial
   functions and to copy itself.
3. **Self-reference** --- a ring can read/write rings (including itself), so
   "rings transform rings" and self-replication both have meaning.
4. **Minimal** --- the smallest instruction set that gives 1--3; resist
   feature creep.
5. **Comparable** --- keep a logic-task harness like E15 so we can directly ask
   "does complexity grow where ECA could not?"

## 4. Candidate primitives (with trade-offs)

- **(A) Linear VM / Avida-adjacent assembly.** A ring is a program of
  instructions over a small register/stack machine; execution can copy code into
  a neighbour (replication) and compute logic tasks. *Pros:* the most validated
  route to evolved self-replication and rising complexity in ALife; directly
  comparable to E15's task framing; composability is natural (longer programs do
  more). *Cons:* self-replication must usually be **seeded** (random programs
  almost never replicate); heavier to implement; needs an instruction set chosen
  with care.
- **(B) Combinatory logic / term rewriting (SKI, lambda).** *Pros:* maximally
  composable --- composition *is* function application; elegant and minimal.
  *Cons:* evolving a specific function or a self-replicator is a rugged search;
  spatial embedding and "data" are less natural; harder to define a smooth task
  gradient.
- **(C) Tag systems / Post rewriting / string rewriting (L-systems).** *Pros:*
  very small spec; rewriting composes; growth is natural. *Cons:* expressiveness
  and self-replication are awkward to steer; weak control over a fitness
  gradient.
- **(D) Small register/stack machine without a copy loop**, transformation-only
  (B's program runs with A as data). *Pros:* closest to the ring system's
  "B transforms A". *Cons:* without built-in copy, heredity is again hard ---
  re-creates the ring system's core problem.

## 5. Recommendation

**Option (A), a minimal Avida-adjacent linear VM, seeded with an ancestor
replicator.** Rationale: it is the only candidate with a track record of
producing *both* sustained self-replication *and* rising functional complexity
under selection, and it keeps the E15 task comparison exact. (B) is more elegant
but its rugged landscape risks reproducing the E15 plateau for a different
reason, which would not cleanly answer the question. We can revisit (B) as a
second substrate if (A) shows complexity does grow and we want to test
generality.

## 6. Minimal first milestone (the decisive experiment)

1. Implement the VM + instruction set; unit-test each instruction.
2. Hand-write an **ancestor self-replicator**; verify it copies itself into a
   neighbour and populates an empty world (the Tierra "Ameba" check).
3. Add mutation (copy errors) + a hard population cap + death; confirm
   evolution runs without collapsing.
4. Add a **logic-task reward** (the E15 analog) and measure **complexity over
   time** (program length that is *used*, and task repertoire) against the ECA
   ceiling. *Decisive question:* does complexity grow and keep growing, or
   plateau as in E15?

A positive result would show the ring-system ceiling was a property of the
*primitive*, not of the broader setup; a negative result (plateau even here)
would be a strong statement that open-ended complexity needs more than
composability.

## 7. Risks

- **Bootstrapping:** random programs ~never self-replicate; we seed an ancestor
  (standard practice; means "open-ended from scratch" is not claimed).
- **Scope:** a VM + instruction set + tasks is a real project; keep the
  instruction set minimal and resist Avida feature-parity.
- **Performance:** executing many programs per tick is heavier than the ECA
  sweep; start small (e.g. a few hundred rings, short programs).
- **Honesty:** "complexity grew" must be measured as *used* computation (task
  repertoire / logical depth), not raw genome length, to avoid the E14 trap of
  rewarding junk.

## 8. Open decision (need a steer)

Primitive choice: **(A) linear VM** is my recommendation. If you prefer the more
elegant but riskier **(B) combinators**, or want me to keep it as close as
possible to the ring system **(D)**, say so --- it determines the whole build.
Default if you don't weigh in: proceed with (A).
