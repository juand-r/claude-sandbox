# Chapter 3: Sliding Block Codes and the Curtis-Hedlund-Lyndon Theorem

## 3.1 Introduction

The central objects of symbolic dynamics are shift spaces (subshifts) and the maps between them. In the previous chapters we defined shift spaces as closed, shift-invariant subsets of $\Sigma^\mathbb{Z}$ (or $\Sigma^\mathbb{N}$). The natural question is: **what are the "right" morphisms between these objects?**

The answer turns out to be remarkably clean. The Curtis-Hedlund-Lyndon theorem (1969) says that the structure-preserving maps between shift spaces are precisely the **sliding block codes**: maps defined by applying a fixed local rule uniformly across every position. This is one of the foundational results of symbolic dynamics, and it connects the topological viewpoint (continuity + shift-commutation) to the combinatorial viewpoint (local rules on finite windows).

This chapter develops the theory of sliding block codes, states and sketches the proof of the Curtis-Hedlund-Lyndon theorem, and explores consequences including factor maps, conjugacies, automorphisms, and the connection to cellular automata and autoregressive language models.

---

## 3.2 Sliding Block Codes: Definition

Let $\Sigma$ and $\Gamma$ be finite alphabets. Let $X \subseteq \Sigma^\mathbb{Z}$ and $Y \subseteq \Gamma^\mathbb{Z}$ be subshifts.

**Definition 3.2.1 (Block map).** A function $f: \Sigma^{m+a+1} \to \Gamma$, where $m, a \geq 0$, is called a **local rule** (or **block map**) with **memory** $m$ and **anticipation** $a$. The quantity $r = \max(m, a)$ is called the **radius** of the block map. When $m = a = r$, the domain is $\Sigma^{2r+1}$ and we say the block map has **symmetric radius** $r$.

**Definition 3.2.2 (Sliding block code).** Given a local rule $f: \Sigma^{m+a+1} \to \Gamma$ with memory $m$ and anticipation $a$, the **sliding block code** (or **$\infty$-block map**) induced by $f$ is the map $\Phi: \Sigma^\mathbb{Z} \to \Gamma^\mathbb{Z}$ defined by

$$[\Phi(x)]_i = f(x_{i-m}, x_{i-m+1}, \ldots, x_i, \ldots, x_{i+a})$$

for all $i \in \mathbb{Z}$ and all $x \in \Sigma^\mathbb{Z}$.

In words: to compute the $i$-th coordinate of the output, we look at a window of $m + a + 1$ symbols centered (with possible asymmetry) at position $i$ in the input, and apply the fixed local rule $f$.

If $\Phi(X) \subseteq Y$, we say $\Phi$ is a sliding block code **from $X$ to $Y$** and write $\Phi: X \to Y$.

**Remark.** Every sliding block code with memory $m$ and anticipation $a$ can be **recoded** as one with symmetric radius $r = \max(m, a)$ by simply ignoring extra coordinates in the local rule. A more useful recoding trick (the **higher block presentation**, see Section 3.7) shows that every sliding block code can be recoded as a **1-block map** (memory 0, anticipation 0) after passing to a higher-block shift.

---

## 3.3 Examples

### Example 3.3.1: XOR map (2-block code)

Let $\Sigma = \Gamma = \lbrace 0, 1\rbrace $. Define the local rule $f: \lbrace 0,1\rbrace ^2 \to \lbrace 0,1\rbrace $ by

$$f(a, b) = a \oplus b$$

where $\oplus$ denotes addition mod 2 (XOR). This has memory $m = 0$ and anticipation $a = 1$ (equivalently, memory 1 and anticipation 0, depending on convention). The induced sliding block code $\Phi: \lbrace 0,1\rbrace ^\mathbb{Z} \to \lbrace 0,1\rbrace ^\mathbb{Z}$ is

$$[\Phi(x)]_i = x_i \oplus x_{i+1}.$$

**Worked computation.** Let $x = \ldots 0\, 0\, 1\, 1\, 0\, 1\, 0\, 0 \ldots$ (with positions labeled $\ldots, -1, 0, 1, 2, 3, 4, 5, 6, \ldots$). Then:

| $i$          | 0 | 1 | 2 | 3 | 4 | 5 |
|:-------------|:-:|:-:|:-:|:-:|:-:|:-:|
| $x_i$        | 0 | 1 | 1 | 0 | 1 | 0 |
| $x_{i+1}$    | 1 | 1 | 0 | 1 | 0 | 0 |
| $[\Phi(x)]_i$| 1 | 0 | 1 | 1 | 1 | 0 |

So $\Phi(x) = \ldots 1\, 0\, 1\, 1\, 1\, 0 \ldots$ in positions $0, \ldots, 5$.

Note that $\Phi$ is a 2-to-1 map on $\lbrace 0,1\rbrace ^\mathbb{Z}$: for any output $y$, choosing $x_0 \in \lbrace 0,1\rbrace $ determines the rest of $x$ uniquely. This map is also known as **elementary cellular automaton Rule 102** (see Section 3.10).

### Example 3.3.2: Majority vote map (radius-1)

Let $\Sigma = \Gamma = \lbrace 0, 1\rbrace $. Define $f: \lbrace 0,1\rbrace ^3 \to \lbrace 0,1\rbrace $ by

$$f(a, b, c) = \text{majority}(a, b, c) = \begin{cases} 1 & \text{if } a + b + c \geq 2, \\ 0 & \text{otherwise.} \end{cases}$$

This has symmetric radius $r = 1$. The induced map is

$$[\Phi(x)]_i = \text{majority}(x_{i-1}, x_i, x_{i+1}).$$

**Worked computation.** Let $x = \ldots 0\, 1\, 1\, 0\, 0\, 1\, 1\, 1 \ldots$ at positions $0, \ldots, 7$.

| $i$           | 1 | 2 | 3 | 4 | 5 | 6 |
|:------------- |:-:|:-:|:-:|:-:|:-:|:-:|
| $(x_{i-1}, x_i, x_{i+1})$ | $(0,1,1)$ | $(1,1,0)$ | $(1,0,0)$ | $(0,0,1)$ | $(0,1,1)$ | $(1,1,1)$ |
| $[\Phi(x)]_i$ | 1 | 1 | 0 | 0 | 1 | 1 |

This map acts as a "smoothing" or "noise reduction" operator: isolated 0s surrounded by 1s become 1, and vice versa. It is **not** invertible. As a cellular automaton, this is **Rule 232**.

### Example 3.3.3: Higher-order block code and the golden mean shift

Let $X \subseteq \lbrace 0,1\rbrace ^\mathbb{Z}$ be the **golden mean shift**: the subshift defined by the forbidden word $\mathcal{F} = \lbrace 11\rbrace $, so no two consecutive 1s appear. Let $\Gamma = \lbrace a, b, c\rbrace $ and define $f: \lbrace 0,1\rbrace ^2 \to \lbrace a, b, c\rbrace $ by

$$f(0,0) = a, \quad f(0,1) = b, \quad f(1,0) = c, \quad f(1,1) = \text{(never occurs in } X\text{)}.$$

The induced map $\Phi: X \to \Gamma^\mathbb{Z}$ sends the golden mean shift to the subshift $Y \subseteq \lbrace a,b,c\rbrace ^\mathbb{Z}$ whose allowed transitions are $a \to a$, $a \to b$, $b \to c$, $c \to a$, $c \to b$ (one can verify: after a $b$, the underlying pair was $(0,1)$, so the next symbol in $X$ must be $0$, giving either $(1,0) \mapsto c$). This is the **higher block presentation** of the golden mean shift; it converts a subshift defined by forbidden words into an **edge shift** (a 1-step shift of finite type).

---

## 3.4 Continuity and Shift-Commutation

We equip $\Sigma^\mathbb{Z}$ with the **product topology** (equivalently, the topology induced by the metric $d(x,y) = 2^{-\min\lbrace |i| : x_i \neq y_i\rbrace }$). In this topology, two sequences are close if they agree on a large window around the origin.

**Proposition 3.4.1.** Every sliding block code $\Phi: \Sigma^\mathbb{Z} \to \Gamma^\mathbb{Z}$ is:

1. **Continuous** in the product topology.
2. **Shift-commuting**: $\Phi \circ \sigma = \sigma \circ \Phi$, where $\sigma$ is the left shift $[\sigma(x)]_i = x_{i+1}$.

*Proof sketch.* (1) Fix $\Phi$ with memory $m$ and anticipation $a$. If $x$ and $y$ agree on positions $\lbrace -N, \ldots, N\rbrace $, then $\Phi(x)$ and $\Phi(y)$ agree on positions $\lbrace -N+m, \ldots, N-a\rbrace $. So agreement on a large window in the input implies agreement on a large window in the output, which is exactly continuity in the product topology.

(2) We compute directly:

$$[\Phi(\sigma(x))]_i = f((\sigma x)_{i-m}, \ldots, (\sigma x)_{i+a}) = f(x_{i-m+1}, \ldots, x_{i+a+1})$$

$$[\sigma(\Phi(x))]_i = [\Phi(x)]_{i+1} = f(x_{(i+1)-m}, \ldots, x_{(i+1)+a}) = f(x_{i-m+1}, \ldots, x_{i+a+1}).$$

These are equal for all $i$, so $\Phi \circ \sigma = \sigma \circ \Phi$. $\square$

The remarkable content of the Curtis-Hedlund-Lyndon theorem is that the converse holds.

---

## 3.5 The Curtis-Hedlund-Lyndon Theorem

**Theorem 3.5.1 (Curtis-Hedlund-Lyndon, 1969).** Let $X \subseteq \Sigma^\mathbb{Z}$ and $Y \subseteq \Gamma^\mathbb{Z}$ be subshifts, and let $\Phi: X \to Y$ be a map. Then $\Phi$ is a sliding block code if and only if:

1. $\Phi$ is **continuous** (with respect to the product topology), and
2. $\Phi$ **commutes with the shift**: $\Phi \circ \sigma = \sigma \circ \Phi$.

The forward direction is Proposition 3.4.1. The content is the reverse: every continuous, shift-commuting map is induced by a local rule.

**Proof sketch of the reverse direction.**

Assume $\Phi: X \to Y$ is continuous and shift-commuting. We must show that there exist $m, a \geq 0$ and a local rule $f: \Sigma^{m+a+1} \to \Gamma$ such that $[\Phi(x)]_i = f(x_{i-m}, \ldots, x_{i+a})$ for all $x \in X$ and all $i$.

**Step 1: Reduce to the zeroth coordinate.** By shift-commutation, it suffices to show that $[\Phi(x)]_0$ depends only on finitely many coordinates of $x$. Indeed, once we know that $[\Phi(x)]_0 = f(x_{-m}, \ldots, x_a)$ for some function $f$, then

$$[\Phi(x)]_i = [\sigma^{-i}(\Phi(x))]_0 = [\Phi(\sigma^{-i}(x))]_0 = f((\sigma^{-i} x)_{-m}, \ldots, (\sigma^{-i} x)_a) = f(x_{i-m}, \ldots, x_{i+a})$$

where we used shift-commutation in the second equality.

**Step 2: Compactness argument.** Consider the map $\pi_0 \circ \Phi: X \to \Gamma$, where $\pi_0$ projects onto the zeroth coordinate. This is a continuous function from $X$ to the discrete space $\Gamma$. For each $\gamma \in \Gamma$, the preimage $(\pi_0 \circ \Phi)^{-1}(\gamma)$ is clopen (both open and closed) in $X$.

The sets of the form $C(i_1, \ldots, i_k; a_1, \ldots, a_k) = \lbrace x \in X : x_{i_j} = a_j \text{ for all } j\rbrace $ (cylinder sets) form a basis for the topology on $X$. Since $(\pi_0 \circ \Phi)^{-1}(\gamma)$ is open, it is a union of cylinder sets. Since $X \subseteq \Sigma^\mathbb{Z}$ is compact (as a closed subset of the compact space $\Sigma^\mathbb{Z}$, by Tychonoff's theorem), and $(\pi_0 \circ \Phi)^{-1}(\gamma)$ is closed (hence compact), it can be covered by **finitely many** cylinder sets.

Each cylinder set depends on finitely many coordinates. A finite union of such sets depends on finitely many coordinates. Since $\Gamma$ is finite, taking the union over all $\gamma$, we find a finite set of coordinates $\lbrace -m, -m+1, \ldots, a\rbrace $ (after relabeling) such that $[\Phi(x)]_0$ depends only on $x_{-m}, \ldots, x_a$.

**Step 3: Define the local rule.** For each word $w = w_{-m} \cdots w_a \in \mathcal{B}_{m+a+1}(X)$ (the set of $(m+a+1)$-blocks appearing in $X$), pick any $x \in X$ with $x_{-m} \cdots x_a = w$ and define $f(w) = [\Phi(x)]_0$. By Step 2, this is well-defined (independent of the choice of $x$). Then $\Phi$ is the sliding block code induced by $f$. $\square$

**Remark on the domain.** The theorem requires the domain $X$ to be a subshift (in particular, compact). This is essential: on non-compact subsets of $\Sigma^\mathbb{Z}$, there exist continuous shift-commuting maps that are not sliding block codes.

---

## 3.6 Why the Theorem Matters

The Curtis-Hedlund-Lyndon theorem says that the category of subshifts with continuous shift-commuting maps is the same as the category of subshifts with sliding block codes. This has several important consequences:

1. **Complete characterization of morphisms.** We do not need to search for exotic continuous shift-commuting maps; they are all given by local rules on finite windows. The theory is entirely combinatorial.

2. **Computability.** To specify a map between subshifts, it suffices to give a finite lookup table (the local rule). This makes the theory computationally tractable.

3. **Composition.** The composition of two sliding block codes is again a sliding block code (with radius at most the sum of the radii). This follows immediately from the topological characterization: a composition of continuous maps is continuous, and a composition of shift-commuting maps is shift-commuting.

4. **Foundation for classification.** It provides the correct notion of isomorphism (conjugacy) between subshifts, which underlies the entire classification theory of symbolic dynamics.

---

## 3.7 Factor Maps and Conjugacies

**Definition 3.7.1.** Let $X$ and $Y$ be subshifts.

- A **factor map** is a surjective sliding block code $\Phi: X \to Y$. We say $Y$ is a **factor** of $X$, and $X$ is an **extension** of $Y$.

- A **conjugacy** is a bijective sliding block code $\Phi: X \to Y$ whose inverse $\Phi^{-1}: Y \to X$ is also a sliding block code. Two subshifts are **conjugate** if there exists a conjugacy between them.

**Remark.** If $\Phi$ is a bijective sliding block code, then $\Phi^{-1}$ is automatically a sliding block code. This follows because $\Phi$ is a continuous bijection from the compact space $X$ to the Hausdorff space $Y$, hence a homeomorphism, and $\Phi^{-1}$ commutes with the shift (since $\Phi$ does). By the Curtis-Hedlund-Lyndon theorem, $\Phi^{-1}$ is a sliding block code. So in the definition of conjugacy, it suffices to require bijectivity.

Conjugacy is the correct notion of **isomorphism** for subshifts. Two conjugate subshifts are "the same" dynamical system up to a re-encoding of symbols. Any dynamical invariant (topological entropy, zeta function, etc.) is preserved by conjugacy.

**Example 3.7.2.** Every subshift of finite type is conjugate to an edge shift (a 1-step SFT) via a higher block code. This is the standard recoding trick: if $X$ is an $M$-step SFT over $\Sigma$, define the new alphabet $\tilde{\Sigma} = \mathcal{B}_M(X)$ (the set of allowed $M$-blocks), and the 1-block conjugacy sends each $M$-block to its corresponding symbol in $\tilde{\Sigma}$.

---

## 3.8 Endomorphisms and Automorphisms of the Full Shift

The set of all sliding block codes from a full shift $\Sigma^\mathbb{Z}$ to itself has rich algebraic structure.

**Definition 3.8.1.** Let $\Sigma$ be a finite alphabet with $|\Sigma| \geq 2$.

- $\text{End}(\Sigma^\mathbb{Z})$ denotes the set of all sliding block codes $\Phi: \Sigma^\mathbb{Z} \to \Sigma^\mathbb{Z}$. Under composition, this is a **monoid** (associative with identity, where the identity is the 0-block code $[\Phi(x)]_i = x_i$).

- $\text{Aut}(\Sigma^\mathbb{Z})$ denotes the set of all **invertible** sliding block codes (conjugacies from $\Sigma^\mathbb{Z}$ to itself). Under composition, this is a **group**, called the **automorphism group** of the full shift.

**Basic elements of $\text{Aut}(\Sigma^\mathbb{Z})$:**

- The **shift** $\sigma$ itself (a 0-block code after re-indexing; it is the conjugacy induced by the identity local rule but with a coordinate offset).
- **Symbol permutations**: for any permutation $\pi: \Sigma \to \Sigma$, the 0-block code $[\Phi(x)]_i = \pi(x_i)$ is an automorphism.
- **Marker automorphisms** and more exotic constructions.

**Theorem 3.8.2 (Hedlund, 1969).** For $|\Sigma| \geq 2$, the group $\text{Aut}(\Sigma^\mathbb{Z})$ is countably infinite. It contains:
- The shift $\sigma$ (of infinite order),
- All finite symmetric groups $S_n$ for $n \leq |\Sigma|$ (via symbol permutations),
- Free groups and free products,
- Every finite group as a subgroup (Ryan's theorem, 1972).

The structure of $\text{Aut}(\Sigma^\mathbb{Z})$ remains deeply mysterious. For example, it is unknown whether $\text{Aut}(\lbrace 0,1\rbrace ^\mathbb{Z})$ is generated by $\sigma$ together with all involutions.

**Example 3.8.3.** For $\Sigma = \lbrace 0, 1\rbrace $, the map $\Phi$ defined by $[\Phi(x)]_i = x_i \oplus x_{i+1}$ from Example 3.3.1 is an endomorphism (it maps $\lbrace 0,1\rbrace ^\mathbb{Z}$ to itself) but **not** an automorphism, since it is 2-to-1.

The map $\Psi$ defined by $[\Psi(x)]_i = 1 - x_i$ (symbol swap) is an automorphism of order 2.

---

## 3.9 One-Sided Sliding Block Codes (Causal Maps)

In many applications, we are interested in maps that depend only on the past and present, not the future.

**Definition 3.9.1.** A **one-sided sliding block code** (or **causal sliding block code**) is a sliding block code with anticipation $a = 0$. That is, $[\Phi(x)]_i = f(x_{i-m}, \ldots, x_i)$ for some local rule $f: \Sigma^{m+1} \to \Gamma$.

Equivalently, the output at position $i$ depends only on the input at positions $\leq i$.

On the one-sided shift space $\Sigma^\mathbb{N}$ (sequences indexed by $\mathbb{N} = \lbrace 0, 1, 2, \ldots\rbrace $), the Curtis-Hedlund-Lyndon theorem holds in the same form, and all sliding block codes $\Phi: X \to Y$ between one-sided subshifts $X \subseteq \Sigma^\mathbb{N}$, $Y \subseteq \Gamma^\mathbb{N}$ are necessarily causal: $[\Phi(x)]_i$ can depend on $x_0, \ldots, x_{i+a}$ for some fixed $a$, and by re-indexing this is equivalent to a causal map on a higher block presentation.

**Remark.** One-sided sliding block codes are strictly less expressive than two-sided ones. For example, the map $[\Phi(x)]_i = x_{i+1}$ (a "look-ahead" by one step) is a perfectly valid two-sided sliding block code but is not causal.

---

## 3.10 Connection to Cellular Automata

**Definition 3.10.1.** A **(one-dimensional) cellular automaton** (CA) is a sliding block code $\Phi: \Sigma^\mathbb{Z} \to \Sigma^\mathbb{Z}$ from the full shift to itself.

By the Curtis-Hedlund-Lyndon theorem, this is equivalent to: a CA is a continuous, shift-commuting map from $\Sigma^\mathbb{Z}$ to itself. Thus:

$$\lbrace \text{cellular automata on } \Sigma\rbrace  = \text{End}(\Sigma^\mathbb{Z}).$$

This is the endomorphism monoid of the full shift, as defined in Section 3.8.

**Wolfram's elementary cellular automata** are exactly the sliding block codes $\Phi: \lbrace 0,1\rbrace ^\mathbb{Z} \to \lbrace 0,1\rbrace ^\mathbb{Z}$ with symmetric radius $r = 1$. There are $2^{2^3} = 256$ such local rules $f: \lbrace 0,1\rbrace ^3 \to \lbrace 0,1\rbrace $, conventionally numbered 0 through 255. For instance:

- **Rule 102**: $f(a,b,c) = b \oplus c$. This is the XOR map from Example 3.3.1 (after a shift in indexing).
- **Rule 232**: $f(a,b,c) = \text{majority}(a,b,c)$. This is the majority vote from Example 3.3.2.
- **Rule 110**: Known to be Turing-complete (Cook, 2004).

The perspective of cellular automata as endomorphisms of the full shift provides a rich algebraic and topological framework for their study, going beyond the purely computational viewpoint.

---

## 3.11 Connection to Autoregressive Language Models

An **autoregressive language model** (such as a transformer-based LLM) generates a sequence of tokens $x_0, x_1, x_2, \ldots$ from a finite vocabulary $\Sigma$ (the "token alphabet") by the rule

$$x_{t+1} \sim P(\cdot \mid x_{\max(0, t-k+1)}, \ldots, x_t)$$

where $k$ is the **context window** length. If we ignore the stochastic sampling and consider the deterministic **greedy decoding** map (always pick the most likely next token), this becomes a deterministic function

$$x_{t+1} = f(x_{\max(0, t-k+1)}, \ldots, x_t)$$

for some fixed $f: \Sigma^{\leq k} \to \Sigma$. Once the sequence is long enough that $t \geq k - 1$, this is exactly a **one-sided sliding block code** with memory $m = k - 1$ and anticipation $a = 0$:

$$[\Phi(x)]_i = f(x_{i-k+1}, \ldots, x_i).$$

More precisely:

| Symbolic dynamics concept | LLM concept |
|:---|:---|
| Alphabet $\Sigma$ | Token vocabulary |
| One-sided shift space $\Sigma^\mathbb{N}$ | Space of all token sequences |
| Memory $m = k - 1$ | Context window minus 1 |
| Anticipation $a = 0$ | Causal (autoregressive) generation |
| Local rule $f$ | Deterministic decoding of the model |
| Sliding block code $\Phi$ | One step of autoregressive generation |

This correspondence is exact in the deterministic case and approximate in the stochastic case (where the model samples rather than taking the argmax). The subshift generated by iterating $\Phi$ from a prompt is the **orbit** of the prompt under the dynamical system defined by $\Phi$.

Key differences from the classical theory:
1. LLMs operate on **one-sided** sequences (causal generation), not two-sided.
2. The local rule $f$ is astronomically complex (billions of parameters), whereas classical symbolic dynamics studies simple local rules.
3. The stochastic case (nonzero temperature) leads to random dynamical systems and stationary measures on shift spaces, not deterministic orbits.

Nevertheless, the sliding block code framework provides the correct mathematical scaffolding for understanding the structure of autoregressive generation.

---

## 3.12 Summary of Key Results

| Concept | Definition |
|:---|:---|
| Sliding block code | $[\Phi(x)]_i = f(x_{i-m}, \ldots, x_{i+a})$ for a fixed local rule $f$ |
| Curtis-Hedlund-Lyndon | Continuous + shift-commuting $\iff$ sliding block code |
| Factor map | Surjective sliding block code |
| Conjugacy | Bijective sliding block code (inverse is automatic) |
| $\text{End}(\Sigma^\mathbb{Z})$ | Monoid of CAs = endomorphisms of the full shift |
| $\text{Aut}(\Sigma^\mathbb{Z})$ | Group of invertible CAs = automorphisms of the full shift |
| Causal SBC | Anticipation $a = 0$; relevant to autoregressive models |

---

## References

- **Curtis, A., Hedlund, G. A., and Lyndon, R. C.** The result is attributed to all three; the published proof appears in Hedlund (1969).
- **Hedlund, G. A.** (1969). Endomorphisms and automorphisms of the shift dynamical system. *Mathematical Systems Theory*, 3(4), 320--375.
- **Lind, D. and Marcus, B.** (2021). *An Introduction to Symbolic Dynamics and Coding*, 2nd edition. Cambridge University Press. (Chapter 6 covers sliding block codes; Chapter 1 covers shift spaces.)
- **Kurka, P.** (2003). *Topological and Symbolic Dynamics*. Cours Specialises, Societe Mathematique de France. (Chapter 4 treats cellular automata as endomorphisms.)
- **Ryan, J. P.** (1972). The shift and commutativity. *Mathematical Systems Theory*, 6(1--2), 82--85.
- **Cook, M.** (2004). Universality in elementary cellular automata. *Complex Systems*, 15(1), 1--40.

---

## Recommended Reading

For the core theory:

- **Lind & Marcus (2021)**, Chapter 6, gives the definitive modern treatment of sliding block codes, including full proofs and many exercises. This is the standard reference.

- **Hedlund (1969)** is the original source and remains highly readable. It establishes the foundational results on endomorphisms and automorphisms of shift spaces.

For cellular automata:

- **Wolfram, S.** (2002). *A New Kind of Science*. Wolfram Media. Controversial but influential; contains extensive empirical study of elementary cellular automata.

- **Ilachinski, A.** (2001). *Cellular Automata: A Discrete Universe*. World Scientific. Comprehensive treatment of cellular automata from multiple perspectives.

For deeper algebraic structure:

- **Ceccherini-Silberstein, T. and Coornaert, M.** (2010). *Cellular Automata and Groups*. Springer. Explores the connection between CAs and group theory, generalizing beyond $\mathbb{Z}$ actions.

- **Boyle, M., Lind, D., and Rudolph, D.** (1988). "The automorphism group of a shift of finite type." *Transactions of the AMS*, 306(1), 71--114. Deep results on $\text{Aut}(X)$ for SFTs.

For connections to computation and language:

- **Kari, J.** (2005). "Theory of cellular automata: A survey." *Theoretical Computer Science*, 334(1-3), 3--33. Emphasizes decidability questions and the computational perspective.
