# Option 3 (revised) --- A Composable Primitive *Within* the Ring Architecture

Status: **DONE (M1--M3 complete). Result in EXPERIMENTS.md E21 / Reflection R5.**
Outcome: a composable primitive is *necessary but not sufficient*. Within the
ring architecture complexity still does not grow --- a working program rewrites
its own genome under self-application, so it is self-destructive and the
self-templating gate blocks it. Only with **program/data separation** (faithful
copy + program acting on a separate data tape) does used-computation climb past
the ECA plateau. The controlled experiment thus isolates the deepest cause as
the ring's **program/data conflation**, and shows open-ended complexity requires
the von Neumann / Avida architecture (the original "option ii"), now empirically
justified. Implementation: `composable.py`.

Status (historical): **design agreed (variant i); implementing.** Supersedes the
original Avida-clone recommendation. The goal is a *controlled* test of the R4
hypothesis: change **only the primitive** (the per-step transformation
operation), holding the ring architecture fixed, and ask whether complexity can
then grow where the elementary-CA primitive plateaued (E13--E15).

## 1. Why this design (vs. an Avida clone)

An Avida-adjacent VM would largely re-derive a known result (complexity evolves
when rewarded; Lenski et al. 2003) and would throw away the project's two best
results: the **ring substrate** and **emergent heredity** (E6/E10 --- heredity
the system discovers via self-templating, not a hardwired copy loop). Instead we
keep all of that and replace just the building block. A positive result then
cleanly attributes the E13 ceiling to the *primitive*; a negative result says
composability alone is insufficient. Either is a real finding, not a replication.

## 2. What is kept (unchanged from the ring system)

- Rings transform rings via PULL/PUSH; **local addressing** + **mobility**
  (spatial); the snapshot tick.
- **Emergent heredity via self-templating** (E6): a ring reproduces in
  proportion to how well its own program preserves its own genome.
- Variable-length genomes + indel mutation (from `growth.py`), so program length
  can grow or shrink.
- Analysis discipline: nulls, categorical metrics (R1), and a *used-computation*
  complexity metric (not raw length --- E14 junk trap).

## 3. What changes: the primitive

Replace the single 8-bit ECA rule with a **short straight-line program of
composable bit operations**. "B transforms A" = run B's program on A's genome
(as a bit-tape). The genome is a variable-length bitstring:

```
[ header (fixed) | program (variable) ]
  header: PULL(8) PUSH(8) CTRL(8)   CTRL = spawn,death,mut(2),type(2),spare
  program: a sequence of 4-bit opcodes (the rest of the genome)
```

**Instruction set** (4-bit opcode; straight-line, bounded runtime = program
length; pointer `p` over the tape, wraps mod L):

| op | name   | effect                                             |
|----|--------|----------------------------------------------------|
| 0  | NOP    | --                                                 |
| 1  | FWD    | p += 1                                              |
| 2  | BACK   | p -= 1                                              |
| 3  | FLIP   | tape[p] ^= 1                                        |
| 4  | COPY   | tape[p+1] = tape[p]                                 |
| 5  | XORB   | tape[p] ^= tape[p-1]                                |
| 6  | SKIPZ  | if tape[p]==0: skip next instruction               |
| 7  | SKIPNZ | if tape[p]==1: skip next instruction               |
| 8--15 | NOP (reserved for later ops)                              |

Rationale: this set **composes richly and (relatively) smoothly** --- adding an
instruction makes a targeted, conditional edit that builds on prior pointer
state, so longer programs realize more input/output behaviour incrementally.
Contrast ECA, where each rule is a fixed chaotic whole-tape map and stacking
them stays chaotic (E15). Straight-line + conditional SKIP gives expressiveness
without halting problems (no loops -> runtime bounded by program length).

Self-templating, reproduction (copy + indel mutation), death, spawn, type/RPS,
local addressing, mobility all work exactly as in the ring engine --- only the
"apply rule" step is replaced by "run program".

## 4. The decisive experiment (with the E14 lesson designed in)

Complexity will collapse to the floor unless something makes it pay (E14). So:

1. **Persistent complexity reward.** A fixed task: program applied to K fixed
   input tapes must match targets produced by a fixed nontrivial "secret"
   program. Reproduction probability scales with `task_fit^power` (a *standing*
   pressure, like Avida's metabolic bonus), combined with the self-templating
   gate so heredity is retained.
2. **Controls (predict the outcomes):**
   - *no-reward control* -> program length should collapse (parsimony, E14).
   - *ECA-primitive control* -> the E15 plateau (~2 effective rules).
3. **Measure complexity over time** as **used-instruction count** (instructions
   that actually affect the output on the task inputs --- not raw length) and
   **task repertoire**, vs. the controls.

**Success criterion:** used-instruction count (and task-fit) rises and *stays*
clearly above the no-reward control and the ECA plateau, across >=3 seeds.
**Kill criterion:** if no self-replicating/self-consistent population sustains
for ~1000 ticks after a few tuning attempts, stop and report the negative.

## 5. Build phases (each a checkpoint; tests before moving on)

- **M1 --- the VM.** Encode/decode genome; `run(program, tape)`; unit-test every
  instruction and a few hand-written programs; a "composability" sanity check
  (compositions vary richly, not chaotically).
- **M2 --- dynamics.** Drop the VM into the ring tick (transform = run program);
  reproduction via self-templating + indel; confirm a population persists and is
  heritable (self-preservation rises, as E6) with no transformation collapse.
- **M3 --- the experiment.** Add the task reward + controls; measure complexity
  over time; report against the ceiling.

## 6. Risks

- **Scope:** a VM + dynamics + task + metrics is multi-session; M1--M3 are hard
  checkpoints, and the kill criterion bounds the downside.
- **Smoothness not guaranteed:** the chosen instruction set is a *hypothesis*
  about composability; if its landscape is also rugged (plateau like E15), that
  itself is an informative result about what "composable" requires.
- **Performance:** running a program per transformation per tick is heavier than
  the ECA sweep; start small (few hundred rings, short programs, modest grid).
- **Honesty:** report *used* computation, not raw length; keep the no-reward and
  ECA controls in every comparison.

## 7. Out of scope (deliberately)

Turing-complete loops / self-copying-via-program (we keep reproduction built into
the ring substrate, so the program need not copy itself); Avida feature-parity;
claims of "open-ended from scratch" (the population is seeded random, and a
viable region must be found by selection, not assumed).
