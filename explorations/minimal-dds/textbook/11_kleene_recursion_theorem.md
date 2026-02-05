# Chapter 11: Kleene's Recursion Theorem and Fixed Points of Program Transformations

## 11.1 Introduction

Kleene's recursion theorem is one of the most surprising results in computability theory. It says, roughly, that for any computable way of transforming programs, there exists a program that is a *fixed point* of that transformation --- not in the sense that the program text is unchanged, but in the sense that the transformed program computes the same function as the original.

This result has far-reaching consequences. It explains why quines (self-printing programs) must exist in any sufficiently powerful programming language, why self-replicating programs (viruses) are inevitable, why Rice's theorem holds, and why certain self-referential strategies are available in algorithmic learning theory. In the context of discrete dynamical systems with evolving rules --- the $(f, x) \mapsto (\varphi(f, x), f(x))$ framework of earlier chapters --- it guarantees the existence of "self-consistent" rules that no meta-rule can escape.

This chapter develops the necessary background (Gödel numbering, the s-m-n theorem), states and proves the recursion theorem, and works through its principal applications.

## 11.2 Setup: Acceptable Numberings and the s-m-n Theorem

### 11.2.1 Gödel Numbering

Fix a standard model of computation (Turing machines, register machines, lambda calculus --- the choice does not matter). Every program in this model can be encoded as a natural number. Such an encoding is called a *Gödel numbering* or *acceptable numbering* of programs.

**Definition 11.1 (Partial Computable Function).** For each $e \in \mathbb{N}$, we write $\varphi_e$ for the partial function $\mathbb{N} \rightharpoonup \mathbb{N}$ computed by the program with index (Gödel number) $e$. The family $\{\varphi_e\}_{e \in \mathbb{N}}$ is called an *acceptable numbering* of the partial computable functions.

Some conventions:

- $\varphi_e(x)\!\downarrow$ means the computation of program $e$ on input $x$ halts (is defined).
- $\varphi_e(x)\!\uparrow$ means it diverges (is undefined).
- $\varphi_e = \varphi_{e'}$ means the two programs compute the same partial function: for all $x$, $\varphi_e(x)\!\downarrow = \varphi_{e'}(x)\!\downarrow$ or both diverge.
- $W_e = \text{dom}(\varphi_e) = \{x : \varphi_e(x)\!\downarrow\}$ is the domain of program $e$.

**Remark.** Many different indices compute the same function. The map $e \mapsto \varphi_e$ is surjective onto the partial computable functions but far from injective: every partial computable function has infinitely many indices.

### 11.2.2 The s-m-n Theorem (Parameter Theorem)

The s-m-n theorem (also called the parameter theorem or parametrization theorem) is a basic structural property of acceptable numberings. It says that "hard-coding" an input into a program can itself be done computably.

**Theorem 11.2 (s-m-n Theorem; Kleene 1943).** There exists a total computable function $s: \mathbb{N}^2 \to \mathbb{N}$ such that for all $e, x, y \in \mathbb{N}$:

$$\varphi_{s(e, x)}(y) = \varphi_e(x, y).$$

More generally, for any $m, n \geq 1$, there exists a total computable injection $s^m_n$ such that

$$\varphi_{s^m_n(e, x_1, \ldots, x_m)}(y_1, \ldots, y_n) = \varphi_e(x_1, \ldots, x_m, y_1, \ldots, y_n).$$

*Interpretation.* Suppose program $e$ takes two inputs $(x, y)$. Then $s(e, x)$ is the index of a new program that has $x$ "baked in" and only needs the second input $y$. The function $s$ is a compiler that performs partial evaluation, and it is itself total and computable.

**Example 11.3.** Suppose $\varphi_e(x, y) = x + y$. Then $\varphi_{s(e, 3)}(y) = 3 + y$. The index $s(e, 3)$ is the Gödel number of a program that adds 3 to its input.

## 11.3 Kleene's Second Recursion Theorem

### 11.3.1 Statement

**Theorem 11.4 (Kleene's Second Recursion Theorem; Kleene 1938, 1952).** Let $f: \mathbb{N} \to \mathbb{N}$ be any total computable function. Then there exists an index $e \in \mathbb{N}$ such that

$$\varphi_e = \varphi_{f(e)}.$$

In words: for any computable transformation of programs, there is a program that is a fixed point of that transformation in the *extensional* sense --- the program and its transform compute the same partial function.

### 11.3.2 Proof

The proof is short but uses a clever diagonal trick combined with the s-m-n theorem.

**Proof.** Define a computable function $d$ as follows. Given input $x$, the function $d$ does:

1. Compute $s(x, x)$ --- this is the index of the program $\varphi_x$ with its first argument specialized to $x$.
2. Apply $f$ to the result: compute $f(s(x, x))$.
3. Return the index $f(s(x, x))$.

So $d(x) = f(s(x, x))$. Since $s$ and $f$ are total computable, $d$ is total computable. Let $d_0$ be an index for the function $d$, meaning $\varphi_{d_0}(x) = d(x) = f(s(x, x))$ for all $x$.

But actually, we need $d$ to *simulate* the program $f(s(x, x))$ rather than merely return its index. More precisely, define $d$ so that:

$$\varphi_{d_0}(x, y) = \varphi_{f(s(x,x))}(y).$$

That is, $d_0$ is a program of two arguments: given $(x, y)$, it computes $s(x, x)$, applies $f$ to get an index $f(s(x, x))$, and then runs that program on $y$.

Now set:

$$e = s(d_0, d_0).$$

We verify this is a fixed point. For any $y$:

$$\varphi_e(y) = \varphi_{s(d_0, d_0)}(y) = \varphi_{d_0}(d_0, y) = \varphi_{f(s(d_0, d_0))}(y) = \varphi_{f(e)}(y).$$

The first equality is the definition of $e$. The second is the s-m-n theorem. The third is the definition of $d_0$. The fourth substitutes $e = s(d_0, d_0)$ back.

Since this holds for all $y$, we have $\varphi_e = \varphi_{f(e)}$. $\square$

### 11.3.3 Dissecting the Proof

The proof has the structure of a diagonalization that "undoes itself." Compare it with the proof of the undecidability of the halting problem, which constructs a program that does the *opposite* of what a purported decider predicts. Here, instead of contradicting, we construct a program that *agrees* with its own transform.

The key insight is the self-application $s(x, x)$. The program indexed by $s(x, x)$ behaves like "$\varphi_x$ applied to itself" --- reminiscent of the $\lambda$-calculus combinator $\omega = \lambda x. x\, x$. The fixed-point construction builds a form of self-reference without any explicit self-reference in the programming language.

## 11.4 Rogers's Fixed-Point Theorem

The following equivalent formulation, due to Rogers (1967), rephrases the result slightly.

**Theorem 11.5 (Rogers's Fixed-Point Theorem).** Let $f: \mathbb{N} \to \mathbb{N}$ be any total computable function. Then there exists $n \in \mathbb{N}$ with $\varphi_n = \varphi_{f(n)}$.

This is identical in content to Theorem 11.4. Rogers's contribution was to place the result in a broader framework of numbering theory and to show that the existence of fixed points *characterizes* acceptable numberings: an effective numbering of the partial computable functions is acceptable if and only if it satisfies the recursion theorem (Rogers 1958).

**Theorem 11.6 (Myhill--Shepherdson; Rogers 1958).** A numbering $\{\psi_e\}_{e \in \mathbb{N}}$ of the partial computable functions has the fixed-point property (i.e., every total computable $f$ has an index $n$ with $\psi_n = \psi_{f(n)}$) if and only if it is an acceptable numbering.

## 11.5 What the Theorem Does NOT Say

A common misunderstanding deserves emphasis.

**The theorem does not claim $e = f(e)$.** It claims $\varphi_e = \varphi_{f(e)}$. The indices $e$ and $f(e)$ are in general different natural numbers --- they are different programs. What the theorem guarantees is that these two different programs compute the same function.

- **Intensional fixed point:** $e = f(e)$. The program index itself is unchanged.
- **Extensional fixed point:** $\varphi_e = \varphi_{f(e)}$. The computed function is unchanged.

Kleene's theorem provides extensional fixed points. Intensional fixed points need not exist. For instance, $f(e) = e + 1$ has no intensional fixed point (no $e$ satisfies $e = e + 1$), but it does have an extensional one: there exists $e$ with $\varphi_e = \varphi_{e+1}$.

## 11.6 Worked Examples

### 11.6.1 Example 1: A Concrete Fixed Point

Let $f(e) = 2e + 7$. This is a total computable function. The recursion theorem guarantees there exists $e$ with $\varphi_e = \varphi_{2e+7}$.

We cannot easily exhibit a specific numerical value of $e$ without committing to a particular Gödel numbering, but the theorem assures us the number exists. Intuitively: among the infinitely many indices for every partial computable function, at least one index $e$ is "aligned" so that $2e + 7$ is another index for the same function.

### 11.6.2 Example 2: Quine Construction

A *quine* is a program that, when run with no input, outputs its own source code (its own Gödel number, in our formalism).

**Claim.** In any acceptable numbering, there exists an index $e$ such that $\varphi_e(x) = e$ for all $x$ (i.e., $\varphi_e$ is the constant function with value $e$).

**Proof using the recursion theorem.** Define a total computable function $f$ as follows: given an index $i$, let $f(i)$ be the index of the program that, on any input $x$, outputs $i$. That is:

$$\varphi_{f(i)}(x) = i \quad \text{for all } x.$$

The function $f$ is total computable: we can effectively construct, from any number $i$, a program that ignores its input and prints $i$.

By the recursion theorem, there exists $e$ with $\varphi_e = \varphi_{f(e)}$. But $\varphi_{f(e)}$ is the constant function that always outputs $e$. Therefore $\varphi_e(x) = e$ for all $x$.

The program $e$ outputs its own index on every input. In particular, on input 0 (or with no input), it prints $e$ --- its own source code. This is a quine. $\square$

**Explicit construction (without invoking the full theorem).** Following the proof of Theorem 11.4 directly:

1. Define $\varphi_{d_0}(x, y) = \varphi_{f(s(x,x))}(y) = s(x, x)$. That is, $d_0$ is a program that, given $(x, y)$, computes $s(x, x)$ and returns it. (Here $f$ maps $i$ to a program printing $i$, so $\varphi_{f(s(x,x))}(y) = s(x,x)$.)
2. Set $e = s(d_0, d_0)$.
3. Then $\varphi_e(y) = \varphi_{s(d_0, d_0)}(y) = \varphi_{d_0}(d_0, y) = s(d_0, d_0) = e$.

This mirrors the structure of real quines in programming languages. In Python, for instance:

```python
s = 's = %r\nprint(s %% s)'
print(s % s)
```

The string `s` plays the role of $d_0$, and the substitution `s % s` plays the role of $s(d_0, d_0)$ --- applying the template to itself.

### 11.6.3 Example 3: A Fixed Point of "Double the Program"

Consider a computable function $f$ that takes a program index $e$ and produces a new program $f(e)$ that runs $\varphi_e$ twice: $\varphi_{f(e)}(x) = \varphi_e(\varphi_e(x))$ (composition of $\varphi_e$ with itself, where the result is undefined if either application diverges).

The recursion theorem gives us $e^*$ with $\varphi_{e^*} = \varphi_{f(e^*)}$. This means:

$$\varphi_{e^*}(x) = \varphi_{e^*}(\varphi_{e^*}(x)) \quad \text{for all } x.$$

What functions satisfy $g(x) = g(g(x))$ for all $x$? Any function satisfying $g(g(x)) = g(x)$ works --- that is, any *idempotent* function. Examples include:

- The identity: $g(x) = x$.
- Any constant function: $g(x) = c$.
- Any projection onto a fixed set: $g(x) = x$ if $x \in S$, $g(x) = c \in S$ otherwise, provided $g(c) = c$.
- The everywhere-undefined function: $g(x)\!\uparrow$ for all $x$.

The theorem guarantees that at least one index $e^*$ for such an idempotent function exists as a fixed point of $f$.

### 11.6.4 Example 4: Self-Referential Programs

The recursion theorem can be used to construct programs that "know their own index." Suppose we want a program $e$ that, on input $x$, outputs the pair $(e, x)$ --- it reports its own index together with its input.

Define $f(i)$ to be the index of the program: "on input $x$, output $(i, x)$." Then $\varphi_{f(i)}(x) = (i, x)$, and $f$ is total computable. The recursion theorem gives $e$ with $\varphi_e = \varphi_{f(e)}$, so $\varphi_e(x) = (e, x)$.

This is the standard way to build self-referential programs in computability theory: you write the program *as if* you had access to your own index as a parameter, and then invoke the recursion theorem to "close the loop."

## 11.7 Applications

### 11.7.1 Application 1: Self-Replicating Programs (Viruses)

A *self-replicating program* (or virus, in the informal sense) is a program that produces a copy of itself as output, possibly interleaved with other behavior.

More precisely, let $\text{write}(i)$ be a computable function that returns the index of a program that writes $i$ to some specified location. Define $f(i) = \text{write}(i)$. Then $f$ is total computable, and the recursion theorem gives $e$ with $\varphi_e = \varphi_{f(e)} = \varphi_{\text{write}(e)}$. The program $e$ writes its own index --- it copies itself.

The existence of self-replicating programs is thus a mathematical inevitability in any sufficiently expressive computational model. This observation has been attributed to von Neumann (in the context of self-reproducing automata) and was made rigorous by the recursion theorem. Adleman (1988) explicitly connected the recursion theorem to computer viruses.

### 11.7.2 Application 2: Rice's Theorem

**Theorem 11.7 (Rice 1953).** Let $\mathcal{A}$ be a set of partial computable functions that is non-trivial (i.e., $\mathcal{A} \neq \emptyset$ and $\mathcal{A}$ does not contain all partial computable functions). Then the index set

$$A = \{e \in \mathbb{N} : \varphi_e \in \mathcal{A}\}$$

is not computable (not decidable).

**Proof using the recursion theorem.** Suppose for contradiction that $A$ is decidable. Since $\mathcal{A}$ is non-trivial, choose indices $a$ and $b$ such that $\varphi_a \in \mathcal{A}$ and $\varphi_b \notin \mathcal{A}$.

Define the total computable function:

$$f(e) = \begin{cases} b & \text{if } e \in A, \\ a & \text{if } e \notin A. \end{cases}$$

This is computable because we assumed $A$ is decidable.

By the recursion theorem, there exists $e^*$ with $\varphi_{e^*} = \varphi_{f(e^*)}$.

- If $e^* \in A$, then $f(e^*) = b$, so $\varphi_{e^*} = \varphi_b \notin \mathcal{A}$, contradicting $e^* \in A$.
- If $e^* \notin A$, then $f(e^*) = a$, so $\varphi_{e^*} = \varphi_a \in \mathcal{A}$, contradicting $e^* \notin A$.

Either case is a contradiction, so $A$ is not decidable. $\square$

This is one of the cleanest proofs of Rice's theorem. The recursion theorem provides the fixed point that the diagonalization needs.

### 11.7.3 Application 3: Fixed Points in Learning Theory

In *algorithmic learning theory* (also called inductive inference), a learner $M$ receives an enumeration of the values of a total function $f$ and must, in the limit, output an index $e$ such that $\varphi_e = f$. The recursion theorem enables the construction of *self-referential learners* --- learners that can refer to their own future output.

Case (1994) showed that self-referential learners (those that exploit the recursion theorem to access their own index) can identify strictly more function classes than non-self-referential ones. The key idea: a learner that "knows its own program" can reason about what it would do in hypothetical situations, gaining an advantage that provably cannot be replicated without self-reference.

**Theorem 11.8 (Case 1994).** There exist classes of computable functions that are identifiable in the limit by a self-referential learner but not by any non-self-referential learner.

This shows that the recursion theorem is not merely a curiosity --- it provides genuine computational power in the context of learning.

## 11.8 The Recursion Theorem for Dynamical Systems

### 11.8.1 Meta-Rules and Fixed Points

Recall the framework from earlier chapters: a discrete dynamical system with evolving rules is a pair $(f, x)$ that evolves by

$$(f, x) \longmapsto (\varphi(f, x),\; f(x)),$$

where $\varphi$ is a *meta-rule* that updates the function component $f$ based on the current state.

If we focus on the function component alone, the meta-rule defines a transformation $T: f \mapsto \varphi(f, x)$ (parametrized by the state $x$, but let us first consider the state-independent case $T: f \mapsto \varphi(f)$).

**Theorem 11.9 (Fixed Points of Meta-Rules).** Let $\varphi$ be any computable meta-rule, viewed as a total computable function on program indices: $\varphi: \mathbb{N} \to \mathbb{N}$ maps the index of $f$ to the index of the "updated" function. Then there exists an index $e^*$ such that

$$\varphi_{e^*} = \varphi_{\varphi(e^*)}.$$

That is, $f^* = \varphi_{e^*}$ is an extensional fixed point of the meta-rule: applying $\varphi$ to $f^*$ yields a program that computes the same function as $f^*$.

*Proof.* This is an immediate application of Kleene's recursion theorem (Theorem 11.4) with $f = \varphi$. $\square$

### 11.8.2 Consequences for the $(f, x)$ Framework

In the full framework $(f, x) \mapsto (\varphi(f, x), f(x))$, the meta-rule depends on the current state. If we fix a state $x_0$ and define $T_{x_0}(f) = \varphi(f, x_0)$, then for each $x_0$ there is a fixed point $f^*_{x_0}$. But the more interesting observation is global:

**Observation 11.10.** For any computable meta-rule $\varphi$, there exist "self-consistent" functions $f^*$ such that $\varphi(f^*, x) = f^*$ (extensionally) for *every* state $x$, provided $\varphi$ does not depend on $x$ when restricted to such $f^*$.

In the general state-dependent case, self-consistency becomes: the function $f^*$ is such that the meta-rule, evaluated at any state the system actually visits along the orbit of $f^*$, returns (an index of) $f^*$. Formally, if $(f^*, x_0) \mapsto (f^*, f^*(x_0)) \mapsto (f^*, f^*(f^*(x_0))) \mapsto \cdots$, then $f^*$ is a true fixed point in the sense that the function component never changes.

These fixed points are *unavoidable*: no matter how cleverly $\varphi$ is designed, it cannot escape having extensional fixed points. This is a fundamental structural constraint on any computable system of evolving rules.

**Example 11.11.** Consider the meta-rule "given program $e$, produce the program that runs $\varphi_e$ and then adds 1 to the result." Formally, $\varphi_{\text{meta}}(e)$ is the index of the program $x \mapsto \varphi_e(x) + 1$.

One might think this meta-rule has no fixed point --- after all, it always increments the output. But the recursion theorem says otherwise. There exists $e^*$ with $\varphi_{e^*} = \varphi_{\text{meta}(e^*)}$, meaning $\varphi_{e^*}(x) = \varphi_{e^*}(x) + 1$ for all $x$ in the domain. The only way this can hold is if $\varphi_{e^*}(x)$ is *undefined* for all $x$ --- the fixed point is the everywhere-undefined (nowhere-halting) function. The meta-rule does have a fixed point; it is just the trivial one $\varphi_{e^*} = \bot$.

This example illustrates an important subtlety: the recursion theorem guarantees existence of fixed points but says nothing about their computability or non-triviality. The fixed point may be the everywhere-undefined function.

### 11.8.3 From Extensional to Intensional Fixed Points in Finite Systems

In the computability-theoretic setting (countably infinite function space), only extensional fixed points are guaranteed. But in the finite discrete dynamical systems studied in earlier chapters, the function space $S^S$ is finite. Every function $T: S^S \to S^S$ on a finite set must have a periodic orbit, and in particular:

**Proposition 11.12.** If $|S|$ is finite, then any meta-rule $T: S^S \to S^S$ has an *intensional* fixed point or a finite cycle. In particular, there exists $k \geq 1$ and $f^* \in S^S$ such that $T^k(f^*) = f^*$.

When $T$ has an actual fixed point ($k = 1$), we get $T(f^*) = f^*$: the function is unchanged even as a syntactic object (since in a finite setting, the function *is* the object --- there is no distinction between a function and its index).

This is stronger than what Kleene's theorem provides. Finiteness buys us intensional fixed points for free.

## 11.9 Limitations and Caveats

1. **Extensional only.** In the computable setting, the fixed point satisfies $\varphi_e = \varphi_{f(e)}$ but generally $e \neq f(e)$. The program *text* changes; only the *behavior* is preserved.

2. **No control over which fixed point.** The proof gives a specific $e$, but there may be many fixed points of $f$, and the theorem does not let us choose one with desirable properties (e.g., a total function, an efficient program).

3. **The fixed point may be trivial.** As Example 11.11 showed, the fixed point may be the everywhere-undefined function. The theorem does not guarantee interesting or useful fixed points.

4. **Requires totality of $f$.** The standard recursion theorem assumes $f$ is total computable. There are extensions to partial functions (the recursion theorem with parameters), but the basic statement requires totality.

5. **Non-constructive flavor.** While the proof is constructive (it gives an explicit $e = s(d_0, d_0)$), computing $e$ requires knowing the index $d_0$, which depends on the Gödel numbering. In practice, the theorem is used as an existence result.

## 11.10 Summary

| Concept | Statement |
|---|---|
| s-m-n theorem | $\varphi_{s(e,x)}(y) = \varphi_e(x,y)$; parameter specialization is computable |
| Kleene's recursion theorem | For total computable $f$, $\exists\, e$: $\varphi_e = \varphi_{f(e)}$ |
| Fixed point type | Extensional ($\varphi_e = \varphi_{f(e)}$), not intensional ($e = f(e)$) |
| Quines | Exist in every acceptable numbering; follow from the recursion theorem |
| Rice's theorem | No non-trivial extensional property of programs is decidable |
| Finite DDS | Meta-rules on finite $S^S$ always have intensional fixed points or cycles |

The recursion theorem tells us something deep about the nature of computation: self-reference is inescapable. Any computable system that transforms programs must have programs that are invariant (up to extensional equivalence) under that transformation. For the study of discrete dynamical systems with evolving rules, this means that every meta-rule $\varphi$ has unavoidable fixed points --- functions that $\varphi$ cannot change.

## References

- Adleman, L. M. (1988). An abstract theory of computer viruses. *Advances in Cryptology --- CRYPTO '88*, LNCS 403, pp. 354--374.
- Case, J. (1994). Infinitary self-reference in learning theory. *Journal of Experimental and Theoretical Artificial Intelligence*, 6(1), 3--16.
- Cutland, N. J. (1980). *Computability: An Introduction to Recursive Function Theory*. Cambridge University Press.
- Kleene, S. C. (1938). On notation for ordinal numbers. *Journal of Symbolic Logic*, 3(4), 150--155.
- Kleene, S. C. (1943). Recursive predicates and quantifiers. *Transactions of the AMS*, 53(1), 41--73.
- Kleene, S. C. (1952). *Introduction to Metamathematics*. North-Holland.
- Kiselyov, O. (2002). Kleene's second recursion theorem: A functional pearl. Unpublished manuscript.
- Rice, H. G. (1953). Classes of recursively enumerable sets and their decision problems. *Transactions of the AMS*, 74(2), 358--366.
- Rogers, H., Jr. (1958). Gödel numberings of partial recursive functions. *Journal of Symbolic Logic*, 23(3), 331--341.
- Rogers, H., Jr. (1967). *Theory of Recursive Functions and Effective Computability*. McGraw-Hill. Reprinted by MIT Press, 1987.
- Soare, R. I. (1987). *Recursively Enumerable Sets and Degrees*. Springer-Verlag.
