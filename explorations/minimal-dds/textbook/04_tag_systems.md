# Chapter 4: Post Tag Systems

## 4.1 Introduction

Tag systems are among the simplest string-rewriting models that achieve computational universality. Introduced by Emil Post in the 1940s, they operate by a monotonously simple rule: read the first symbol, delete a fixed number of symbols from the front, and append a string determined by that first symbol. Despite this extreme simplicity, tag systems can simulate arbitrary Turing machines --- a fact that has made them a key tool in the study of the boundary between decidable and undecidable computation.

This chapter defines tag systems precisely, traces several worked examples, surveys the main universality and decidability results, and connects tag systems to the $(f, x)$ dynamical systems framework developed in earlier chapters.

## 4.2 Definition

**Definition 4.1 (Post Tag System).** A *tag system* is a triple $T = (\Sigma, m, P)$ where:

- $\Sigma$ is a finite alphabet,
- $m \geq 1$ is the *deletion number*,
- $P: \Sigma \to \Sigma^*$ is the *production function*, mapping each symbol to a (possibly empty) string over $\Sigma$.

**Computation step.** Given a string $w = a_1 a_2 \cdots a_n$ with $n \geq m$:

1. Read the first symbol $a_1$.
2. Delete the first $m$ symbols, yielding $a_{m+1} a_{m+2} \cdots a_n$.
3. Append $P(a_1)$, yielding $a_{m+1} a_{m+2} \cdots a_n \cdot P(a_1)$.

**Halting condition.** The system halts when the current string has length less than $m$. In particular, if a production maps some symbol to the empty string $\varepsilon$, the string may shrink and eventually halt.

We write $w \vdash_T w'$ for a single step and $w \vdash_T^* w'$ for the reflexive-transitive closure. The *orbit* of a string $w_0$ is the sequence $w_0, w_1, w_2, \ldots$ where $w_{i+1}$ is obtained from $w_i$ by one step (or the sequence terminates if $w_i$ halts).

**Remark.** A tag system with $m = 1$ is trivial: each step replaces the first symbol with a string but the "queue" never advances faster than it grows. The interesting case is $m \geq 2$, where there is genuine competition between deletion and production.

## 4.3 Worked Example 1: Growth and Cycling

Consider the tag system $T_1 = (\lbrace 0, 1\rbrace , 2, P)$ with:

$$P(0) = \texttt{00}, \quad P(1) = \texttt{1101}$$

Starting from $w_0 = \texttt{10}$:

| Step | String | Length | First symbol | Deleted prefix | Appended |
|------|--------|--------|-------------|----------------|----------|
| 0 | `10` | 2 | `1` | `10` | `1101` |
| 1 | `1101` | 4 | `1` | `11` | `1101` |
| 2 | `011101` | 6 | `0` | `01` | `00` |
| 3 | `110100` | 6 | `1` | `11` | `1101` |
| 4 | `01001101` | 8 | `0` | `01` | `00` |
| 5 | `00110100` | 8 | `0` | `00` | `00` |
| 6 | `11010000` | 8 | `1` | `11` | `1101` |
| 7 | `0100001101` | 10 | `0` | `01` | `00` |
| 8 | `0000110100` | 10 | `0` | `00` | `00` |
| 9 | `0011010000` | 10 | `0` | `00` | `00` |
| 10 | `1101000000` | 10 | `1` | `11` | `1101` |

Several features are visible:

- **Growth.** The string grows when $|P(a)| > m$ for the symbol $a$ being read. Here $|P(1)| = 4 > 2 = m$, so reading a `1` adds net 2 symbols.
- **Shrinkage.** The string neither grows nor shrinks when $|P(a)| = m$. Here $|P(0)| = 2 = m$, so reading a `0` is length-neutral.
- **Complex dynamics.** Despite the simplicity of the rules, the string's evolution is non-trivial: `0`s and `1`s interleave in patterns that are not immediately periodic.

Continuing the trace, one can verify computationally that this system does not halt for the initial string `10`. The orbit grows and exhibits quasi-periodic behavior.

## 4.4 Worked Example 2: A Halting Tag System

Consider $T_2 = (\lbrace a, b, c\rbrace , 3, P)$ with:

$$P(a) = \texttt{bc}, \quad P(b) = \texttt{a}, \quad P(c) = \texttt{aaa}$$

Starting from $w_0 = \texttt{aaa}$:

| Step | String | Length | First symbol | Action |
|------|--------|--------|-------------|--------|
| 0 | `aaa` | 3 | `a` | delete `aaa`, append `bc` |
| 1 | `bc` | 2 | --- | **HALT** (length $2 < m = 3$) |

The system halts in one step. The production $P(a) = \texttt{bc}$ has length 2, which is less than $m = 3$, so a net loss of 1 symbol occurs. Starting from a string of length exactly $m$, this guarantees halting.

A more interesting halting example: same alphabet and $m$, but start from $w_0 = \texttt{abcabc}$:

| Step | String | Length | First symbol | Appended |
|------|--------|--------|-------------|----------|
| 0 | `abcabc` | 6 | `a` | `bc` |
| 1 | `abcbc` | 5 | `a` | `bc` |
| 2 | `bcbc` | 4 | `b` | `a` |
| 3 | `ca` | 2 | --- | **HALT** |

This halts in 3 steps. The string length decreases from 6 to 5 to 4 to 2.

## 4.5 Worked Example 3: A Looping Tag System

Consider $T_3 = (\lbrace 0, 1\rbrace , 2, P)$ with:

$$P(0) = \texttt{01}, \quad P(1) = \texttt{10}$$

Both productions have length 2, equal to $m$. Every step preserves the string length. Starting from $w_0 = \texttt{01}$:

| Step | String | First symbol | Appended |
|------|--------|-------------|----------|
| 0 | `01` | `0` | `01` |
| 1 | `01` | `0` | `01` |

The system enters a fixed point immediately: `01` maps to `01`. Now start from $w_0 = \texttt{10}$:

| Step | String | First symbol | Appended |
|------|--------|-------------|----------|
| 0 | `10` | `1` | `10` |
| 1 | `10` | `1` | `10` |

Again a fixed point. Now try $w_0 = \texttt{0110}$:

| Step | String | First symbol | Appended |
|------|--------|-------------|----------|
| 0 | `0110` | `0` | `01` |
| 1 | `1001` | `1` | `10` |
| 2 | `0110` | `0` | `01` |

This is a cycle of period 2: $\texttt{0110} \to \texttt{1001} \to \texttt{0110}$. Since all productions have length $m$, no string can halt or grow; every orbit is eventually periodic with bounded period. This illustrates that length-preserving tag systems have relatively tame dynamics.

## 4.6 Post's Normal Form Theorem (1943)

The original motivation for tag systems comes from Post's study of *canonical systems* --- a general class of string-rewriting systems that Post developed in parallel with Turing's work on computability.

**Theorem 4.2 (Post's Normal Form Theorem, 1943).** Every Post canonical system can be reduced to a tag system (possibly over a larger alphabet).

More precisely, any computation that can be expressed as a sequence of string productions in a canonical system can be simulated by a tag system, at the cost of increasing the alphabet size. Post's original formulation used "normal systems," which are a special case of canonical systems where productions are constrained to delete a prefix and append a suffix --- exactly the structure of a tag system.

Post arrived at tag systems in the 1920s and struggled with the question of their decidability for over two decades before publishing in 1943. His frustration with the problem --- he called it his "principal unsolved problem" --- is documented in his correspondence and was only resolved after his death (Post, 1943).

## 4.7 Turing-Completeness of Tag Systems

### Minsky's Theorem (1961)

**Theorem 4.3 (Minsky, 1961).** For any $m \geq 2$, tag systems with deletion number $m$ are Turing-complete.

*Sketch of proof.* Minsky showed how to encode the configuration of a Turing machine as a tag string and simulate each transition by a sequence of tag steps.

The key idea is as follows. A Turing machine configuration consists of a state $q$, a tape content, and a head position. This is encoded as a string over an enlarged alphabet where:

1. The tape content to the right of the head is encoded as a sequence of "data symbols" using a block code (each tape symbol is represented by a fixed-length block of tag symbols).
2. The state and the symbol currently under the head are encoded jointly as a special "state-symbol" marker at the front of the string.
3. The tape content to the left of the head is encoded at the end of the string.

A single Turing machine step is simulated by multiple tag steps that:
- Read the state-symbol marker at the front of the string.
- Use the production rules to output the appropriate new marker (encoding the new state and the symbol to write) plus routing symbols.
- The deletion of $m$ symbols from the front "advances" through the encoded tape, effectively moving the head.

The encoding requires an alphabet whose size depends on the number of Turing machine states and tape symbols, but $m$ can remain fixed. The overhead is polynomial in the description of the Turing machine. $\square$

### The Cocke--Minsky Theorem (1964)

**Theorem 4.4 (Cocke--Minsky, 1964).** 2-tag systems (tag systems with deletion number $m = 2$) are universal.

This is a strengthening of Theorem 4.3: the deletion number need not be arbitrary but can be fixed at 2, the smallest non-trivial value. The proof proceeds by showing that any tag system with $m > 2$ can be simulated by a 2-tag system over a larger alphabet, combined with Minsky's theorem.

The universality of 2-tag systems makes them one of the simplest known Turing-complete formalisms, alongside two-state three-symbol Turing machines and Rule 110 cellular automata.

## 4.8 Cyclic Tag Systems

**Definition 4.5 (Cyclic Tag System).** A *cyclic tag system* is a tag system variant defined by a finite sequence of productions $P_0, P_1, \ldots, P_{k-1}$ over the alphabet $\lbrace 0, 1\rbrace $. The system operates on binary strings as follows:

At step $t$:
1. Read and delete the first symbol of the string.
2. If the first symbol was `1`, append $P_{t \bmod k}$.
3. If the first symbol was `0`, append nothing.

The production applied at each step cycles through the list $P_0, P_1, \ldots, P_{k-1}, P_0, P_1, \ldots$ regardless of the symbol read.

**Example.** Let $k = 3$ with productions $P_0 = \texttt{11}$, $P_1 = \texttt{10}$, $P_2 = \varepsilon$ (empty). Starting from $w_0 = \texttt{11}$:

| Step $t$ | String | First symbol | Production $P_{t \bmod 3}$ | Append? | Result |
|-----------|--------|-------------|---------------------------|---------|--------|
| 0 | `11` | `1` | $P_0 = \texttt{11}$ | yes | `111` |
| 1 | `111` | `1` | $P_1 = \texttt{10}$ | yes | `1110` |
| 2 | `1110` | `1` | $P_2 = \varepsilon$ | yes (nothing) | `110` |
| 3 | `110` | `1` | $P_0 = \texttt{11}$ | yes | `1011` |
| 4 | `1011` | `1` | $P_1 = \texttt{10}$ | yes | `01110` |
| 5 | `01110` | `0` | $P_2 = \varepsilon$ | no | `1110` |

Note step 5: the first symbol is `0`, so nothing is appended regardless of the production.

Cyclic tag systems were introduced by Matthew Cook in connection with his proof that the elementary cellular automaton Rule 110 is Turing-complete (Cook, 2004). The proof proceeds in two stages:

1. Show that cyclic tag systems are Turing-complete (by simulating arbitrary 2-tag systems).
2. Show that Rule 110 can simulate cyclic tag systems.

Cyclic tag systems serve as a bridge because their purely periodic control structure is well-suited for embedding in the spatially periodic patterns of cellular automata.

## 4.9 The Collatz Connection

De Mol (2008) observed a striking connection between certain tag systems and Collatz-like iterations in number theory.

The Collatz function $C: \mathbb{N} \to \mathbb{N}$ is defined by:

$$C(n) = \begin{cases} n/2 & \text{if } n \text{ is even} \\ 3n + 1 & \text{if } n \text{ is odd} \end{cases}$$

Consider a 2-tag system over $\lbrace a, b\rbrace $ with $P(a) = \texttt{b}$ (length 1, causing the string to shrink) and $P(b) = \texttt{aab}$ (length 3, causing the string to grow). If we track the length $\ell$ of the string:

- When the first symbol is $a$: new length $= \ell - 2 + 1 = \ell - 1$.
- When the first symbol is $b$: new length $= \ell - 2 + 3 = \ell + 1$.

The *pattern* of $a$s and $b$s at the head of the string determines a sequence of increments and decrements that, when analyzed modulo arithmetic, produces dynamics analogous to iterated Collatz-type maps. De Mol showed that proving termination (or non-termination) for certain tag systems is equivalent to resolving Collatz-type conjectures, thereby connecting string rewriting to deep open problems in number theory.

This provides another lens on why tag system behavior is hard to predict: even the question "does the string length remain bounded?" can encode unsolved problems.

## 4.10 The Decidability Boundary

The halting problem for tag systems asks: given a tag system $T$ and an initial string $w$, does the computation starting from $w$ eventually halt?

**Theorem 4.6 (Undecidability, from Minsky 1961 / Cocke--Minsky 1964).** The halting problem for 2-tag systems is undecidable.

This follows immediately from universality: if we could decide halting for 2-tag systems, we could decide the halting problem for Turing machines.

The interesting question is: *how small* can a tag system be while remaining undecidable?

De Mol (2007) investigated this boundary systematically. For 2-tag systems over a binary alphabet $\lbrace 0, 1\rbrace $, there are only finitely many possible production tables (up to production length bounds). De Mol showed:

- Many small 2-tag systems have decidable behavior (they always halt, always loop, or can be analyzed by tracking string length).
- The smallest known undecidable 2-tag systems require relatively few production rules but with productions of moderate length.
- There exist 2-tag systems whose behavior is unknown for specific inputs --- systems that may halt, loop, or grow without bound, and current techniques cannot determine which.

The precise boundary remains open, but the general picture is clear: the threshold of undecidability occurs at remarkably small system sizes, consistent with the theme that computational universality requires very little structure.

## 4.11 Connection to the $(f, x)$ Framework

A tag system fits naturally into the dynamical systems framework of Chapter 1.

In a standard tag system, the state is the current string $x \in \Sigma^*$, and the transition function $f$ is determined by the fixed triple $(\Sigma, m, P)$. Thus a tag system is a dynamical system of the form:

$$x_{n+1} = f(x_n)$$

where $f$ is the tag-step function. The "program" $f$ (encoded by the production table $P$) is fixed; only the "data" $x$ evolves. In our $(f, x)$ notation, the system is:

$$(f, x) \to (f, f(x))$$

with $f$ constant --- the simplest case of the general framework.

A *self-modifying tag system* would be one in which the production table is encoded within the string itself, so that applying the current rules transforms both the "data" portion and the "rule" portion of the string. In $(f, x)$ notation:

$$(f, x) \to (f', x')$$

where $f'$ is extracted from the string $x'$. This is not merely a theoretical curiosity: it corresponds to a system whose rewriting rules are part of its own substrate, analogous to self-modifying code or --- more relevantly --- to an LLM whose prompt contains instructions that are themselves rewritten by the generation process.

Such self-modifying tag systems inherit the universality of ordinary tag systems but add a layer of meta-level dynamics: the function itself undergoes evolution, not just the data. The dynamical questions from Chapter 1 (transient length, cycle structure, attractor complexity) become substantially harder, because the "program" is no longer a fixed point of the meta-rule $\varphi$; it co-evolves with the data.

## 4.12 Connection to Autoregressive Language Models

There is a suggestive structural parallel between tag systems and autoregressive language generation with a finite context window.

| Tag System | Autoregressive LLM |
|---|---|
| Finite alphabet $\Sigma$ | Token vocabulary $V$ |
| Current string $w$ | Context window contents |
| Read first symbol $a$ | Attend to context (especially early tokens) |
| Delete first $m$ symbols | Sliding window drops oldest $m$ tokens |
| Append $P(a)$ | Generate and append new tokens |
| Production table $P$ | Model weights (fixed during inference) |

In both systems, the core loop is: *read context, discard old material, produce new material*. The production function $P$ in a tag system is a lookup table; in an LLM, it is a neural network --- vastly more expressive, but playing the same structural role.

The analogy has limits. An LLM attends to its entire context window (not just the first token), and its "production" depends on the full context via attention, not on a single symbol lookup. Nevertheless, the tag system abstraction captures the essential tension: the system's future behavior is determined by a finite window of past output, with old information irreversibly discarded. This is precisely the regime where complex, hard-to-predict dynamics arise --- as the universality results of this chapter confirm.

## 4.13 Summary

Tag systems illustrate a recurring theme in the theory of computation: extremely simple rewriting rules can generate behavior that is computationally universal and therefore undecidable. The key results form a clear logical chain:

1. **Post (1943):** Canonical systems reduce to tag systems.
2. **Minsky (1961):** Tag systems with $m \geq 2$ are Turing-complete.
3. **Cocke--Minsky (1964):** Even 2-tag systems suffice for universality.
4. **Cook (2004):** Cyclic tag systems mediate between 2-tag systems and cellular automata.
5. **De Mol (2007, 2008):** The decidability boundary is surprisingly low, and tag system dynamics connect to Collatz-type problems in number theory.

For our purposes, tag systems serve as a bridge between the abstract $(f, x)$ dynamics of Chapter 1 and the concrete mechanics of string rewriting. They are the simplest non-trivial model in which "read, delete, append" produces universal computation --- and they suggest that the same dynamical pattern, scaled up with neural networks, may account for some of the surprising capabilities of autoregressive language models.

## References

- Cocke, J. and Minsky, M. (1964). "Universality of Tag Systems with P = 2." *Journal of the ACM*, 11(1), 15--20.
- Cook, M. (2004). "Universality in Elementary Cellular Automata." *Complex Systems*, 15(1), 1--40.
- De Mol, L. (2007). "Tag Systems and Collatz-like Functions." *Theoretical Computer Science*, 390(1), 92--101.
- De Mol, L. (2008). "Closing the Circle: An Analysis of Emil Post's Early Work." *Bulletin of Symbolic Logic*, 12(2), 267--289.
- Minsky, M. (1961). "Recursive Unsolvability of Post's Problem of 'Tag' and Other Topics in Theory of Turing Machines." *Annals of Mathematics*, 74(3), 437--455.
- Post, E. L. (1943). "Formal Reductions of the General Combinatorial Decision Problem." *American Journal of Mathematics*, 65(2), 197--215.
- Wolfram, S. (2002). *A New Kind of Science*. Wolfram Media. Chapter 3: "The World of Simple Programs."

---

## Recommended Reading

For historical context and Post's contributions:

- **Davis, M.** (1965). *The Undecidable*. Raven Press. Contains Post's original 1943 paper along with other foundational papers in computability. Essential primary source.

- **De Mol, L.** (2008). "Closing the Circle: An Analysis of Emil Post's Early Work." Provides excellent historical analysis of how Post arrived at tag systems and their place in the development of computability theory.

For universality proofs:

- **Minsky, M.** (1967). *Computation: Finite and Infinite Machines*. Prentice-Hall. Chapter 14 gives a readable account of tag system universality with full details.

- **Rogozhin, Y.** (1996). "Small Universal Turing Machines." *Theoretical Computer Science*, 168(2), 215--240. Context on the quest for minimal universal systems, of which tag systems are a key example.

For connections to cellular automata:

- **Cook, M.** (2004). The original proof that Rule 110 is universal, via cyclic tag systems. Technical but foundational.

For the decidability boundary and open problems:

- **De Mol, L.** (2007). Explores the connection between tag systems and Collatz-type problems, showing that seemingly simple systems encode deep number-theoretic questions.

For broader context on string rewriting:

- **Book, R. and Otto, F.** (1993). *String-Rewriting Systems*. Springer. Comprehensive treatment of rewriting systems, with tag systems as a special case.
