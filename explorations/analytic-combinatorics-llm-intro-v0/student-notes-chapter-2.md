# Student Notes on Chapter 2: "Just Enough Complex Analysis"

Reading as a 3rd-year math/CS undergrad who has taken calculus and linear
algebra, maybe seen complex numbers in a course but has not taken a full
complex analysis course.

---

## Overall impression

The chapter does a good job of being honest about what it's doing: "here is the
minimum you need." The classification of singularities at the end is the real
payoff, and it's clearly stated. But there are a few errors and some places
where the reasoning jumps further than the student can follow.

---

## Section-by-section notes

### Opening paragraph (lines 1-13)

Clear and well-framed. The invitation to skim if you already know complex
analysis is helpful. No issues.

### Complex Numbers and Convergence (lines 15-42)

Standard review material. The geometric series identity is stated without
proof (fine for this audience — it's telescoping). No issues.

### Power Series and Radius of Convergence (lines 44-84)

**Issue 1 (math error, line 61): "ratio test" should be "root test."**

The proof sketch says: "The formula follows from comparing
$|a_n z^n|^{1/n} = |a_n|^{1/n}|z|$ with the ratio test." But taking $n$-th
roots and comparing with $1$ is the **root test** (Cauchy's root test), not
the ratio test. The ratio test compares $|a_{n+1}/a_n|$ with $1$. This is a
clear error.

**Issue 2 (minor inaccuracy, line 67): $|a_n|^{1/n} \to R^{-1}$.**

The text says: "in the sense that $|a_n|^{1/n} \to R^{-1}$." But
Cauchy-Hadamard uses $\limsup$, not $\lim$. The limit might not exist in
general (the sequence $|a_n|^{1/n}$ could oscillate). For the combinatorial
sequences in this book the limit always exists, so this is fine in practice,
but stating $\limsup$ would be more correct.

The Fibonacci example (line 80) says "the poles are at the roots of
$1-z-z^2 = 0$, namely $z = (-1 \pm \sqrt{5})/2$." This is correct and
consistent with Ch1's treatment.

### Analytic Functions (lines 86-107)

The three-way equivalence (complex-differentiable = infinitely differentiable
+ Cauchy-Riemann = locally representable by convergent power series) is stated
as a fact to take on faith. This is the right call for a "just enough" chapter.

Missing: the word "singularity" is used constantly from this point on but is
never defined. I would appreciate a one-line definition somewhere:

> A **singularity** of $f$ is a point $z_0$ at which $f$ fails to be
> holomorphic — it cannot be represented by a convergent power series in any
> neighborhood of $z_0$.

### The Geometric Series as Prototype (lines 109-131)

Good section. The key insight — that $1/(1-z)$ is holomorphic on
$\mathbb{C} \setminus \{1\}$ but the power series only works on $|z| < 1$ —
is well-stated.

**Issue 3 (clarity, line 118): "extends analytically" is undefined.**

The text says "$1/(1-z)$ extends analytically well beyond the disk of
convergence." The concept of analytic continuation hasn't been defined. A
student who hasn't taken complex analysis won't know what this means. A
parenthetical would help: "(meaning the function $1/(1-z)$ is perfectly
well-defined and holomorphic at, say, $z = 2$, even though the series
$\sum z^n$ diverges there)."

**Issue 4 (clarity, lines 126-128): "the radius of convergence... equals the
distance from $z_0$ to the nearest singularity."**

This is stated as a general principle but is actually a theorem (essentially
the definition of radius of convergence combined with the fact that power
series define holomorphic functions on their disk of convergence). It works
because the power series at $z_0$ converges on the largest disk around $z_0$
on which $f$ is holomorphic. Stating it flat is OK for this audience, but a
one-line parenthetical like "(this is because a power series converges on
exactly the largest disk around its center on which the function remains
holomorphic)" would demystify it.

### Cauchy's Integral Formula (lines 132-162)

The formula and its derivation from Cauchy's derivative formula are clearly
presented.

**Issue 5 (clarity, lines 153-155): "On a circle of radius $r > 1$ (say)"
could confuse.**

We just finished discussing $1/(1-z)$, which has a singularity at $z = 1$.
Then the text says "On a circle of radius $r > 1$ (say)..." — which sounds
like we're taking a contour beyond the singularity of the example we just
discussed. The text is speaking generally, not about $1/(1-z)$, but the
transition is jarring. Adding "(for a function whose singularities all lie
outside $|z| = r$)" would eliminate the confusion.

### Classifying Singularities (lines 164-217)

**Issue 6 (clarity, line 168): $\rho > 0$ assumes the dominant singularity is
a positive real number.**

The text says "Let $\rho > 0$ be the location of the dominant singularity."
But singularities can be complex! For instance, $1/(1+z^2)$ has singularities
at $z = \pm i$, which are not positive reals. The text is tacitly restricting
to the case where the dominant singularity is on the positive real axis, which
is the typical case for combinatorial generating functions with non-negative
coefficients (by the Pringsheim-Vivanti theorem: if $a_n \ge 0$ and $R$ is
finite, then $z = R$ is a singularity). This should be stated:

> For generating functions with non-negative coefficients — which is the case
> for all counting problems — the dominant singularity always lies on the
> positive real axis. We write $\rho$ for this point.

**Poles subsection (lines 172-183):**

"$1/(1-z/\rho)^k = \sum_{n \ge 0} \binom{n+k-1}{k-1} \rho^{-n} z^n$" — this
is the negative-binomial series. It could be derived from the generalized
binomial theorem $(1-w)^{-k} = \sum \binom{n+k-1}{k-1} w^n$, with
$w = z/\rho$. The formula is stated without proof, which is OK since the
generalized binomial theorem was just developed in Ch1. But a one-line
"(setting $\alpha = -k$ and $w = -z/\rho$ in the generalized binomial
theorem of Chapter 1)" would close the loop.

**Square-root branch points (lines 185-198):**

**Issue 7 (leap, lines 188-190):** "Computing the coefficient
$\binom{1/2}{n}(-1)^n$ by Stirling's formula yields
$[z^n]\sqrt{1-z/\rho} = -\frac{1}{2\sqrt{\pi}} n^{-3/2} \rho^{-n}
(1+O(1/n))$."

This is stated as a computation but the computation is not shown. In Ch1 we
derived $\binom{1/2}{n} = (-1)^{n-1}/(2^{2n-1}n)\binom{2n-2}{n-1}$. To get
from there to the $n^{-3/2}$ formula requires applying Stirling's
approximation to $\binom{2n-2}{n-1}$, which gives $\binom{2n-2}{n-1} \sim
4^{n-1}/\sqrt{\pi n}$. The student has no way to fill this in without knowing
Stirling. It's a leap.

However: Ch4 will prove the transfer theorem, of which this is a special case.
So perhaps just say "a result we will derive carefully in Chapter 4" instead
of "by Stirling's formula."

**Logarithmic singularities (lines 200-208):**

**Issue 8 (garbled comparison, lines 203-204):** "The correction factor is
$1/n$, slower to decay than any negative power with exponent greater than
$-1$ but faster than a constant."

This is confusing. Let me parse it:
- "slower to decay than any negative power with exponent greater than $-1$"
  — exponents greater than $-1$ include $-1/2$, $0$, $1$, etc. But $n^{-1/2}$
  decays SLOWER than $n^{-1}$, not faster. So $1/n$ is FASTER than
  $n^{-1/2}$, which contradicts "slower."
- "but faster than a constant" — yes, $1/n \to 0$ while a constant doesn't.

I think the intended meaning is: $1/n$ decays faster than any $n^{\alpha}$
with $\alpha > -1$ (since $n^{\alpha} \to \infty$ for $\alpha > 0$ and
$n^{\alpha} \to 1$ for $\alpha = 0$), and slower than any $n^{\alpha}$ with
$\alpha < -1$ (like $n^{-3/2}$). But the text has it backwards or phrased
confusingly.

Suggested rewrite: "The correction factor $1/n$ sits between a constant (no
decay) and the $n^{-3/2}$ of a square-root branch point."

**Essential singularities (lines 210-217):**

**Issue 9 (jargon, line 212):** "governed by Picard's theorem" — unexplained.
Picard's theorem (near an essential singularity, the function hits every
complex value infinitely often, with at most one exception) is deep and not
needed. Dropping the reference to Picard would be cleaner. Just say "they
blow up in a highly irregular fashion."

### The Big Picture (lines 219-242)

**Issue 10 (cross-reference error, line 234):** "using the symbolic method
from Chapter~1" — but Chapter 1 is "What is a Generating Function?" and the
symbolic method is Chapter 3 ("The Symbolic Method"). Should say "Chapter~3"
or "Chapters~1 and~3."

The summary is otherwise clear and correctly states the three-step workflow.

---

## Missing elements

1. **No definition of "singularity."** The word is used dozens of times but
   never formally defined. A one-line definition after the analytic functions
   section would fill this gap.

2. **"Analytic continuation" mentioned but undefined** (line 118). A
   parenthetical explanation would suffice.

3. **No exercises.** Suggested:
   - "Find the radius of convergence of $\sum z^n/n^2$ and identify the type
     of singularity at $z = 1$."
   - "Show that $1/(1-z)^3$ has a pole of order 3 at $z = 1$ and verify that
     $[z^n](1/(1-z)^3) = \binom{n+2}{2}$."
   - "What is the radius of convergence of $\sum n! z^n$? Does the function
     have a singularity at $z = R$?"

---

## Ranked issues by severity

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | HIGH | Line 61 | "ratio test" should be "root test" (math error) |
| 2 | HIGH | Line 234 | "Chapter~1" should be "Chapter~3" (cross-ref error) |
| 3 | MEDIUM | Lines 188-190 | Square-root coefficient: "by Stirling" is an unjustified leap |
| 4 | MEDIUM | Lines 203-204 | Logarithmic decay comparison is garbled |
| 5 | MEDIUM | Line 168 | $\rho > 0$ assumes positive real singularity without saying so |
| 6 | MEDIUM | Lines 153-155 | "$r > 1$ (say)" confusing after $1/(1-z)$ discussion |
| 7 | LOW | Line 67 | $|a_n|^{1/n} \to R^{-1}$ should technically be $\limsup$ |
| 8 | LOW | Line 212 | "Picard's theorem" is unexplained jargon |
| 9 | LOW | Chapter | No definition of "singularity" |
| 10 | LOW | Chapter | "Analytic continuation" mentioned but undefined |
| 11 | LOW | Chapter | No exercises |

---

## Summary

The chapter is well-scoped and honest about what it's doing. The singularity
classification at the end is the core payoff and is clearly presented. There
are two clear errors ("ratio test" for "root test," Chapter 1 for Chapter 3),
one garbled sentence about logarithmic decay, and one unjustified leap (the
$n^{-3/2}$ formula for square-root singularities, attributed to Stirling but
not derived). The missing definition of "singularity" is a gap that should be
filled since the entire chapter depends on the concept. Fixing issues #1-6
and adding the singularity definition would make this chapter fully
self-contained for the stated audience.
