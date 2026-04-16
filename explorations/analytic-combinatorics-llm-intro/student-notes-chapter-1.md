# Student Notes on Chapter 1: "What is a Generating Function?"

I'm reading this as a 3rd-year math/CS undergrad who has taken calculus and
linear algebra, maybe a first course in discrete math, but has NOT seen formal
power series, analytic combinatorics, or complex analysis. I know what a ring
is (vaguely) but am not an algebraist.

---

## Overall impression

The chapter is well-paced and the three worked examples (binary strings,
Fibonacci, Catalan) are well-chosen — they build in complexity. But there are
several places where the text skips steps that I cannot reconstruct on my own,
and a few pieces of jargon that assume more background than the preface promises.

---

## Section-by-section notes

### Opening paragraph (lines 3–7)

- "let the algebra of formal power series do the bookkeeping" — I get the gist,
  but I don't yet know what "algebra of formal power series" means. This is a
  forward reference to the definition that follows, which is fine, but a bright
  high school student may stall here.
- "shifting, convolving, differencing" — these are listed as motivating examples
  of sequence operations, but convolution hasn't been defined yet. The word just
  floats past.

### Definition of Q[[z]] (lines 9–11)

- **"Ring"** and **"integral domain"** are used casually. The target reader "knows
  calculus, linear algebra, and a little probability." An integral domain is from
  abstract algebra, which is not in the prerequisites. Either define these terms
  in a sentence, or drop them and just say "the set of all formal power series,
  with addition and multiplication defined by..."
- The multiplication formula $c_n = \sum_{k=0}^n a_k b_{n-k}$ is stated but not
  motivated. **Why** does multiplying two power series give this formula? One
  sentence saying "collect all pairs of terms whose exponents add to $n$" would
  ground it.

### Dense paragraph after the definition (lines 13)

This is the densest paragraph in the chapter and it carries a LOT of weight:
invertibility, shifts, derivatives, and the coefficient extraction operator —
all in one paragraph.

- **Invertibility**: "any series $A(z)$ with $a_0 \ne 0$ is invertible: one
  constructs $A(z)^{-1}$ coefficient by coefficient from the equation
  $A \cdot A^{-1} = 1$." This is a "miracle happens" moment. I believe it but I
  have zero idea how it works. Even one line like "the first coefficient of
  $A^{-1}$ is $1/a_0$, and each subsequent coefficient is determined by requiring
  the convolution product to vanish" would help.
- **Leibniz notation**: The product rule is written as
  $(\cdot\,\cdot)'=(\cdot)'\cdot + \cdot\,(\cdot)'$. This is unusual — most
  students would expect $(fg)' = f'g + fg'$. The dot notation is confusing at
  first glance.
- **Coefficient extraction operator** $[z^n]$: This is introduced in a
  subordinate clause of a long sentence. It deserves its own mini-definition or
  at least a display equation: "$[z^n] A(z)$ denotes the coefficient of $z^n$ in
  $A(z)$, i.e., $a_n$." It's used constantly for the rest of the book.

### Binary strings (lines 15–25)

- **"Multiply both sides by $z^n$ and sum over $n \ge 1$"** — this is THE core
  technique, and it appears here without any explanation of WHY you'd do this.
  A student encountering generating functions for the first time has no
  reason to guess this move. One sentence of motivation would help enormously:
  "The key trick: multiply every term of the recurrence by $z^n$ and sum over
  all valid $n$. This converts a recurrence relation into an equation for the
  generating function."
- **Re-indexing**: The right side goes from $\sum_{n \ge 1} b_{n-1} z^{n-1}$
  to $B(z)$ without showing the substitution $m = n-1$. An undergrad can
  probably follow this, but a high school student might not.
- Otherwise this section is clean and easy to follow. Good first example.

### Fibonacci (lines 27–55)

- The recurrence-to-GF step is clearly explained — better than binary strings,
  actually, since more detail is shown.
- **Factoring the denominator**: "The roots of $1 - z - z^2 = 0$ (equivalently,
  $z^2 + z - 1 = 0$)" — why "equivalently"? One is $-1$ times the other. A
  student might expect the roots to be the same, but they have opposite signs.
  It's correct, just deserves a word of explanation.
- **"one checks that $1/\varphi$ and $1/\hat\varphi$ are the roots"** — this
  "one checks" is asking me to verify a non-trivial algebraic identity. I would
  appreciate seeing it shown, or at least a hint: "$\varphi$ satisfies
  $\varphi^2 = \varphi + 1$, so $1 - 1/\varphi - 1/\varphi^2 = 0$."
- **Partial fractions**: This is a major "miracle happens" moment. The
  decomposition
  $$F(z) = \frac{1}{\sqrt{5}} \cdot \frac{1}{1-\varphi z} - \frac{1}{\sqrt{5}} \cdot \frac{1}{1-\hat\varphi z}$$
  appears fully formed with no derivation. I know partial fractions from
  calculus, but the specific coefficients $\pm 1/\sqrt{5}$ are not derived.
  The text just says "Partial fractions decompose $F(z)$ as" and gives the
  answer. This is one of the biggest gaps in the chapter. At minimum, show
  the setup: write $F(z) = A/(1-\varphi z) + B/(1-\hat\varphi z)$, multiply
  through, and solve for $A$ and $B$.
- **"Expanding each geometric series"** — I need to realize that
  $1/(1-\varphi z) = \sum_{n \ge 0} (\varphi z)^n = \sum \varphi^n z^n$.
  This is probably fine for someone who read the binary strings section
  carefully, since $1/(1-2z) = \sum 2^n z^n$ was just shown. But making the
  connection explicit ("each factor is a geometric series, just as in the
  binary-string example") would help.

### Catalan numbers (lines 57–83)

- **From recurrence to GF equation**: The text says "The right-hand side is a
  convolution: $[z^{n-1}](C(z)^2) = \sum_{k=0}^{n-1} C_k C_{n-1-k}$." I
  can sort of see this, but it's not obvious. The convolution formula from the
  definition gives $[z^m](C^2) = \sum_{k=0}^m C_k C_{m-k}$, so we need
  $m = n-1$. OK. But then the text says "multiplying by $z^{n-1}$ and summing
  over $n \ge 1$." Wait — for binary strings and Fibonacci, we multiplied by
  $z^n$. Now we multiply by $z^{n-1}$? This is inconsistent and confusing.

  Actually, I think a cleaner route is: multiply both sides of
  $C_n = \sum_{k=0}^{n-1} C_k C_{n-1-k}$ by $z^n$ and sum over $n \ge 1$.
  Left side: $C(z) - C_0 = C(z) - 1$. Right side: $z \cdot C(z)^2$
  (because $\sum_{n \ge 1} z^n \sum_{k=0}^{n-1} C_k C_{n-1-k} = z \sum_{n \ge 1} z^{n-1} [z^{n-1}] C(z)^2 = z \cdot C(z)^2$).
  So $C(z) - 1 = z C(z)^2$, giving $C(z) = 1 + z C(z)^2$.

  The text's approach via multiplying by $z^{n-1}$ is algebraically equivalent
  but harder to follow because it breaks the pattern established in the
  previous two examples. I'd prefer the $z^n$ approach for consistency.

- **Sign choice**: "The plus sign gives $C(0) = 2/0$, which is undefined" —
  this is informal. $C(z) = (1 + \sqrt{1-4z})/(2z)$; as $z \to 0$, numerator
  $\to 2$ and denominator $\to 0$. But we're working with formal power series,
  not limits! The correct argument is: expand $(1+\sqrt{1-4z})/(2z)$ as a
  series — the $z^0$ term would require the constant term of the numerator
  ($= 2$) divided by the factor of $z$ in the denominator, which gives no
  valid power series. This could be stated more carefully.

- **Generalized binomial theorem**: "$\sqrt{1-4z} = \sum_{n \ge 0}
  \binom{1/2}{n}(-4z)^n$." The generalized binomial coefficient
  $\binom{1/2}{n}$ is **never defined** in this chapter (or anywhere before
  it). This is a significant gap. The standard definition is:
  $$\binom{\alpha}{n} = \frac{\alpha(\alpha-1)\cdots(\alpha-n+1)}{n!}$$
  for real $\alpha$. Without this, the formula is a black box.

- **"After simplification, one finds $[z^n] C(z) = \frac{1}{n+1}\binom{2n}{n}$"**
  — the entire derivation is hidden behind "after simplification." A student
  who tries to verify this will need to expand $\binom{1/2}{n}$, simplify the
  falling factorial, and recognize the resulting expression as
  $\frac{1}{n+1}\binom{2n}{n}$. This is a nontrivial calculation. At minimum,
  the intermediate step $\binom{1/2}{n} = \frac{(-1)^{n-1}}{2^{2n-1} n} \binom{2n-2}{n-1}$ or similar should be shown, or the reader should be
  explicitly told "the algebra is carried out in Exercise X."

### OGF vs EGF (lines 85–106)

- **Long sentence**: The sentence starting "the product structure of
  permutations (concatenating two permutations of disjoint sets..." is 5 lines
  long. It's grammatically correct but very hard to parse. Breaking it into
  two sentences would help.
- **Why binomial convolution?** The explanation is compressed. The key idea
  ("we must choose which $k$ of the $n$ labels go to the $A$-part, hence the
  $\binom{n}{k}$ factor") deserves its own sentence rather than being embedded
  in a parenthetical.
- **Notation $[z^n/n!]$**: Used in the permutation example (line 103) without
  definition. Does it mean "$n!$ times the coefficient of $z^n$"? That's what
  the context implies, but it's not stated. I think it means "the coefficient
  of $z^n/n!$", which is the same as $n! \cdot [z^n]$. Either way, define it.
- **Radius of convergence**: The permutation example says the OGF "has zero
  radius of convergence." But radius of convergence is a concept from Chapter 2,
  which the student hasn't read yet. At minimum, add "(a concept we define
  precisely in Chapter 2; for now, it means the series diverges for all
  nonzero $z$)."

### Cross-reference error (line 106)

- "The symbolic method, developed in Chapter~2, makes this assignment
  systematic" — but Chapter 2 is "Just Enough Complex Analysis" and Chapter 3
  is "The Symbolic Method." **This is a cross-reference error.** Should be
  Chapter 3.

### Road map (lines 108–111)

- "The next chapter" is Chapter 2 (complex analysis) — correct.
- "Chapter~3 introduces the symbolic method" — correct.
- "Chapters~3 and~4" in the Fibonacci discussion (line 55) — says "singularities
  of generating functions control asymptotics, a theme developed fully in
  Chapters 3 and 4." But the singularity analysis theme is developed in
  Chapters 2 and 4 (complex analysis + transfer theorem), not in Chapter 3
  (symbolic method). Should this say "Chapters 2 and 4"?

---

## Missing elements

1. **No exercises.** The other chapters have exercises. Chapter 1 has none.
   Even two simple ones would ground the material: "Find the OGF for the
   sequence $a_n = 3^n$" and "Use the generating function method to solve
   $a_n = 2a_{n-1} + 1$, $a_0 = 0$."

2. **No explicit recipe.** The "multiply by $z^n$ and sum" technique is the
   core method of this chapter, but it's never stated as a general procedure.
   Something like:

   > **Recipe.** To convert a recurrence $a_n = (\text{expression in } a_{n-1},
   > a_{n-2}, \ldots)$ into a functional equation for $A(z) = \sum a_n z^n$:
   > multiply both sides by $z^n$, sum over all valid $n$, and recognize each
   > side as an expression involving $A(z)$.

   would help enormously.

3. **Convolution is under-motivated.** The product formula
   $c_n = \sum_k a_k b_{n-k}$ is stated as a definition but never explained
   intuitively. One sentence: "When you multiply $A(z) \cdot B(z)$ and collect
   all terms contributing to $z^n$, you get $a_0 b_n + a_1 b_{n-1} + \cdots +
   a_n b_0$, because $z^k \cdot z^{n-k} = z^n$" would make it click.

4. **The generalized binomial coefficient needs a definition.** It's used
   crucially in the Catalan section and will reappear in later chapters.

5. **The permutation EGF example uses undefined notation** ($[z^n/n!]$) and
   an undefined concept (radius of convergence).

---

## Ranked list of issues by severity

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | HIGH | Fibonacci, line 48-49 | Partial fractions: result stated with no derivation |
| 2 | HIGH | Catalan, line 75 | Generalized binomial coefficient $\binom{1/2}{n}$ never defined |
| 3 | HIGH | Catalan, line 76 | "After simplification" hides entire derivation |
| 4 | HIGH | Line 106 | Cross-reference error: symbolic method is Ch 3 not Ch 2 |
| 5 | MEDIUM | Lines 9-13 | "Ring", "integral domain" assume algebra background |
| 6 | MEDIUM | Line 13 | Invertibility of power series asserted but not shown |
| 7 | MEDIUM | Line 17 | "Multiply by $z^n$ and sum" technique needs motivation |
| 8 | MEDIUM | Catalan, lines 63-65 | Multiply by $z^{n-1}$ vs $z^n$ inconsistency |
| 9 | MEDIUM | Line 103 | $[z^n/n!]$ notation used without definition |
| 10 | MEDIUM | Line 99 | Radius of convergence referenced before defined |
| 11 | LOW | Line 55 | "Chapters 3 and 4" should be "Chapters 2 and 4" |
| 12 | LOW | Line 13 | Leibniz rule in dot notation is cryptic |
| 13 | LOW | Chapter | No exercises |
| 14 | LOW | Chapter | No explicit "recipe" for the recurrence-to-GF method |

---

## Summary

The chapter is well-written and covers the right material in the right order.
The three examples are well-chosen. But there are three significant "miracle
happens" moments (partial fractions in Fibonacci, generalized binomial
coefficients in Catalan, "after simplification" in Catalan) where the reader
is given a result without seeing how it's obtained. There is also a
cross-reference error (Ch 2 vs Ch 3 for the symbolic method). Fixing issues
#1-4 and #7 would make this chapter genuinely self-contained for the target
audience.
