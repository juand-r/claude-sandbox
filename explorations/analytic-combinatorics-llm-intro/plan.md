# Plan: Expository Introduction to Analytic Combinatorics and LLMs

## Goal

Write a long, self-contained expository book-style introduction (LaTeX, compiled
to PDF) that takes a mathematically mature undergraduate or early graduate
student from basics (generating functions, a little complex analysis) all the
way to the 2024-2026 research literature on analytic combinatorics and large
language models.

**Target reader.** Knows calculus, linear algebra, elementary probability, has
seen complex numbers. Does **not** know analytic combinatorics, formal language
theory, or any deep learning.

**Source material.**
- `source_lit_review.md` — the literature review note from the RACA dashboard.
- `source_lit_deep_dive.md` — the deep dive note expanding each section
  narratively.

## Structure (five parts, nineteen chapters)

### Part I — Foundations of Analytic Combinatorics
1. **What is a generating function?** Formal power series as bookkeeping
   devices. Fibonacci, binary strings, Catalan numbers. The shift
   operation. Why turning a sequence into a function helps.
2. **Just enough complex analysis.** Complex numbers, analytic functions,
   power series and radius of convergence, Cauchy's integral formula for
   coefficients, poles and branch points — the minimum needed for §4.
3. **The symbolic method.** Combinatorial classes, size functions, the
   translation dictionary for sum / product / sequence / set / cycle.
   Worked examples: binary strings, plane trees, integer compositions.
4. **Singularity analysis.** Exponential growth = $1/R$, the transfer
   theorem $[z^n](1-z/\rho)^{-\alpha} \sim n^{\alpha-1}\rho^{-n}/\Gamma(\alpha)$,
   dominant singularities, why the *type* matters.
5. **Algebraic generating functions and the $n^{-3/2}$ law.** Chomsky–
   Schützenberger, square-root branch points, the universal asymptotic
   for unambiguous context-free languages.

### Part II — Languages, Automata, and Probability
6. **Formal languages and the Chomsky hierarchy.** Regular, context-free,
   context-sensitive; finite-state automata; what grammars generate.
7. **Weighted finite automata and rational power series.** Matrix-valued
   transitions, rational GFs $\alpha^\top(I - zA)^{-1}\beta$, the
   Kleene–Schützenberger theorem.
8. **Probabilistic grammars and tightness.** PCFGs, the Booth–Thompson
   consistency condition, Chi (1999), Du et al. (2023) measure-theoretic
   tightness — why $F(1) = 1$ matters.
9. **Entropy rate and the identity $h = \log(1/R)$.** Stationary sources,
   Shannon–McMillan–Breiman, typical sets as counting GFs.

### Part III — Large Language Models as Mathematical Objects
10. **Autoregressive language models as distributions over $\Sigma^*$.**
    Tokenization, softmax, EOS, factorization. Transformers are tight.
11. **Formal language theory of transformers.** Hahn (2020), Merrill &
    Sabharwal, Strobl et al. survey, $\mathsf{TC}^0$ ceilings, Rizvi et al.
    simulation of WFAs, chain of thought breaking the ceiling.
12. **WFA approximations of LLMs.** Lecorvé–Motlicek, Suresh et al.,
    Schwartz–Thomson–Smith rational recurrences, Rabusseau–Li–Precup, the
    Lacroce operator-theoretic program.

### Part IV — Sampling, Statistical Mechanics, and Phase Transitions
13. **Boltzmann sampling.** The Duchon–Flajolet–Louchard–Schaeffer
    framework, $\Gamma A(x)$ samplers, tuning $x$ to control size,
    singular samplers.
14. **Gibbs measures and temperature decoding.** The LLM energy
    $E(w) = -\log\mu(w)$, temperature sampling as a Gibbs measure,
    the identification $x = e^{-1/T}$, ARM-EBM duality (Blondel et al.),
    Kempton–Burrell local normalization distortion.
15. **Phase transitions in LLM output.** Nakaishi et al., Arnold et al.,
    coalescence of singularities as the analytic face of a phase
    transition.

### Part V — Zipf, the Frontier, and the Ten Open Problems
16. **Zipf's law and token distributions.** Piantadosi, Goldwater–
    Griffiths–Johnson, Berman's combinatorial derivation, Mikhaylovskiy's
    temperature-window result.
17. **Motif statistics and analytic information theory.** Szpankowski,
    Jacquet–Szpankowski, Nicodème–Salvy–Flajolet. What it means to "do
    Szpankowski for LLMs".
18. **Ten open problems at the frontier.** The ten gaps identified in
    the literature review.
19. **A research roadmap.** Where a student could plausibly start:
    the WFA pipeline as the most tractable entry point.

## Technical setup

- `documentclass: book`, 11pt, a4paper.
- Packages: `amsmath`, `amssymb`, `amsthm`, `hyperref`, `geometry`,
  `microtype`. No tikz, no graphics.
- Theorem environments defined in `preamble.tex`; no per-chapter
  redefinitions.
- Citations: `\cite{CamelCaseAuthorYear}`. Bibliography assembled at
  assembly time from the keys that actually get used.
- One file per part (`partI.tex` through `partV.tex`), included from
  `book.tex`. Bibliography in `bibliography.tex`.

## Process

1. Write skeleton: `book.tex`, `preamble.tex`, empty `partX.tex` stubs.
2. Launch five subagents in parallel, one per part, each given:
   - The shared style and LaTeX constraints.
   - The relevant sections of the two source notes.
   - Its chapter list with a rough target length.
   - Instructions to write directly to `partX.tex` and return a list of
     used citation keys.
3. Assemble: scan all part files for `\cite{...}` keys, build
   `bibliography.tex` mapping each key to a reference.
4. Compile with `pdflatex` two or three passes (for cross-refs + TOC +
   hyperref). Fix errors.
5. Read through once more, note gaps and rough transitions, revise.
6. Commit and push to
   `claude/analytic-combinatorics-llm-intro-kD3yi`.

## Progress log

- `[2026-04-15]` Plan drafted. Source material in place. Skeleton next.
