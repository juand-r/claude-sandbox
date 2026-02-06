# Chapter 9: Ergodicity and the Ergodic Theorems

## 9.1 The Fundamental Question

We arrive at the central question of ergodic theory — arguably one of the most important questions in all of mathematical physics.

Suppose $(X, \mathcal{B}, \mu)$ is a probability space and $T: X \to X$ is a measure-preserving transformation. Given a measurable function $f: X \to \mathbb{R}$ (an "observable"), we can form its **time average** along the orbit of a point $x$:

$$\bar{f}_n(x) = \frac{1}{n} \sum_{k=0}^{n-1} f(T^k x).$$

We can also form the **space average** (or **ensemble average**) of $f$:

$$\langle f \rangle = \int_X f \, d\mu.$$

The fundamental question is:

> **When does the time average converge to the space average?** That is, when does
> $$\lim_{n \to \infty} \frac{1}{n} \sum_{k=0}^{n-1} f(T^k x) = \int_X f \, d\mu$$
> hold for $\mu$-almost every $x \in X$?

This question has its origins in statistical mechanics. Ludwig Boltzmann, in the late 19th century, proposed what became known as the **ergodic hypothesis**: that a physical system, over sufficient time, visits all accessible states compatible with its energy. If this were true, one could replace the practically impossible computation of a time average (requiring observation of a system for infinite time) with the more tractable computation of a space average (an integral over phase space). We will return to the physical interpretation in Section 9.8.

The mathematical resolution of this question came in the early 1930s, in two landmark theorems:

- **John von Neumann's Mean Ergodic Theorem** (1932): the time averages converge in the $L^2$ norm.
- **George David Birkhoff's Pointwise Ergodic Theorem** (1931): the time averages converge pointwise almost everywhere.

The answer to *when* the limit equals $\int f \, d\mu$ (rather than some other invariant function) turns out to be precisely when the system is **ergodic** — a property we will define and study in detail.

Throughout this chapter, $(X, \mathcal{B}, \mu)$ denotes a probability space (so $\mu(X) = 1$), and $T: X \to X$ is a measure-preserving transformation (so $\mu(T^{-1}A) = \mu(A)$ for all $A \in \mathcal{B}$), unless stated otherwise.


## 9.2 The Koopman Operator

Before stating the ergodic theorems, we introduce an operator that translates the dynamics of $T$ on the space $X$ into linear algebra on function spaces. This perspective, due to B.O. Koopman (1931), is fundamental.

**Definition 9.1** (Koopman operator). Let $T: X \to X$ be a measurable transformation. The **Koopman operator** $U_T: L^2(X, \mu) \to L^2(X, \mu)$ is defined by

$$U_T f = f \circ T.$$

That is, $(U_T f)(x) = f(T(x))$ for all $x \in X$.

When $T$ is measure-preserving, the Koopman operator has several important properties.

**Proposition 9.2.** If $T$ is measure-preserving, then $U_T$ is a linear isometry on $L^2(X, \mu)$. That is, $\|U_T f\|_2 = \|f\|_2$ for all $f \in L^2$.

*Proof.* We compute directly:

$$\|U_T f\|_2^2 = \int_X |f(Tx)|^2 \, d\mu(x) = \int_X |f|^2 \, d(T_* \mu) = \int_X |f|^2 \, d\mu = \|f\|_2^2,$$

where the second equality uses the change-of-variables formula and the third uses the fact that $T_* \mu = \mu$ (i.e., $T$ preserves $\mu$). $\square$

In particular, $U_T$ is a bounded operator with $\|U_T\| = 1$. Note that $U_T$ is an isometry but not necessarily unitary — it is unitary if and only if $T$ is invertible (mod $\mu$). Observe also that

$$U_T^n f = f \circ T^n,$$

so the time average can be written as

$$\bar{f}_n = \frac{1}{n} \sum_{k=0}^{n-1} U_T^k f.$$

This reformulation is the key to von Neumann's approach: the question of convergence of time averages becomes a question about the behavior of the **Cesàro averages** of iterates of a bounded linear operator on a Hilbert space.


## 9.3 Von Neumann's Mean Ergodic Theorem

We now state and prove von Neumann's theorem. The proof is elegant and relies only on the Hilbert space structure of $L^2$.

**Notation.** For a measure-preserving transformation $T$, define the subspace of **$T$-invariant functions**:

$$\mathcal{I} = \{ f \in L^2(X, \mu) : U_T f = f \} = \{ f \in L^2 : f \circ T = f \ \text{a.e.} \}.$$

This is a closed subspace of $L^2$ (as the kernel of the bounded operator $U_T - I$). Let $P: L^2 \to \mathcal{I}$ denote the orthogonal projection onto $\mathcal{I}$.

**Theorem 9.3** (Von Neumann's Mean Ergodic Theorem, 1932). Let $(X, \mathcal{B}, \mu)$ be a probability space, $T: X \to X$ measure-preserving, and $f \in L^2(X, \mu)$. Then

$$\frac{1}{n} \sum_{k=0}^{n-1} U_T^k f \xrightarrow{L^2} Pf \quad \text{as } n \to \infty,$$

where $P$ is the orthogonal projection onto the subspace $\mathcal{I}$ of $T$-invariant functions.

*Proof.* The idea is to decompose $L^2$ into two subspaces on which the convergence is easy to check separately.

**Step 1: Orthogonal decomposition.** We claim that

$$L^2(X, \mu) = \mathcal{I} \oplus \overline{\mathcal{C}},$$

where

$$\mathcal{C} = \{ g - U_T g : g \in L^2(X, \mu) \}$$

is the space of **coboundaries**, and $\overline{\mathcal{C}}$ is its closure in $L^2$.

To establish this, it suffices to show that $\mathcal{I} = \mathcal{C}^\perp$ (since $L^2 = \mathcal{C}^\perp \oplus \overline{\mathcal{C}}$ for any subspace $\mathcal{C}$).

First, suppose $f \in \mathcal{I}$, so $U_T f = f$. For any $g \in L^2$,

$$\langle f, g - U_T g \rangle = \langle f, g \rangle - \langle f, U_T g \rangle.$$

Now we use the fact that $U_T$ is an isometry with adjoint $U_T^*$ satisfying $\langle U_T^* f, g \rangle = \langle f, U_T g \rangle$. Since $T$ is measure-preserving, $U_T^* U_T = I$ (on $L^2$), and one can check that $U_T^* f = f$ whenever $U_T f = f$. (Indeed, $\|U_T f - f\| = 0$ implies $\langle U_T f, f \rangle = \|f\|^2$, and then $\|f - U_T^* f\|^2 = \|f\|^2 - 2\text{Re}\langle f, U_T^* f\rangle + \|U_T^* f\|^2 = \|f\|^2 - 2\text{Re}\langle U_T f, f\rangle + \|U_T^* f\|^2$. Since $U_T^* U_T = I$, we have $\|U_T^* f\|^2 \leq \|f\|^2$ (as $U_T^*$ is a contraction), and $\text{Re}\langle U_T f, f\rangle = \|f\|^2$, giving $\|f - U_T^* f\|^2 \leq 0$.)

So $U_T^* f = f$, and therefore $\langle f, U_T g \rangle = \langle U_T^* f, g \rangle = \langle f, g \rangle$. Thus $\langle f, g - U_T g \rangle = 0$. Since $g$ was arbitrary, $f \perp \mathcal{C}$.

Conversely, suppose $f \perp \mathcal{C}$. Then for every $g \in L^2$, $\langle f, g - U_T g \rangle = 0$, i.e., $\langle f, g \rangle = \langle f, U_T g \rangle = \langle U_T^* f, g \rangle$. Since this holds for all $g$, we get $U_T^* f = f$. Then $\|U_T f - f\|^2 = \|U_T f\|^2 - 2\text{Re}\langle U_T f, f\rangle + \|f\|^2 = \|f\|^2 - 2\text{Re}\langle f, U_T^* f\rangle + \|f\|^2 = 2\|f\|^2 - 2\|f\|^2 = 0$ (using $\|U_T f\| = \|f\|$ and $U_T^* f = f$). So $U_T f = f$, i.e., $f \in \mathcal{I}$.

This establishes $\mathcal{I} = \mathcal{C}^\perp$, and therefore $L^2 = \mathcal{I} \oplus \overline{\mathcal{C}}$.

**Step 2: Convergence on each subspace.** Write $f = f_{\text{inv}} + h$, where $f_{\text{inv}} = Pf \in \mathcal{I}$ and $h \in \overline{\mathcal{C}}$. Then

$$\frac{1}{n} \sum_{k=0}^{n-1} U_T^k f = \frac{1}{n} \sum_{k=0}^{n-1} U_T^k f_{\text{inv}} + \frac{1}{n} \sum_{k=0}^{n-1} U_T^k h = f_{\text{inv}} + \frac{1}{n} \sum_{k=0}^{n-1} U_T^k h,$$

since $U_T^k f_{\text{inv}} = f_{\text{inv}}$ for all $k$ (because $f_{\text{inv}}$ is $T$-invariant). So it suffices to show that $\frac{1}{n}\sum_{k=0}^{n-1} U_T^k h \to 0$ in $L^2$ for all $h \in \overline{\mathcal{C}}$.

**Case (a): $h = g - U_T g$ is an exact coboundary.** Then

$$\sum_{k=0}^{n-1} U_T^k h = \sum_{k=0}^{n-1} (U_T^k g - U_T^{k+1} g) = g - U_T^n g,$$

a telescoping sum. Therefore

$$\left\| \frac{1}{n} \sum_{k=0}^{n-1} U_T^k h \right\|_2 = \frac{1}{n}\|g - U_T^n g\|_2 \leq \frac{2\|g\|_2}{n} \to 0.$$

**Case (b): $h \in \overline{\mathcal{C}}$ is a general element.** Given $\varepsilon > 0$, choose a coboundary $h_0 = g_0 - U_T g_0$ with $\|h - h_0\|_2 < \varepsilon$. Since $U_T$ is an isometry, $\|\frac{1}{n}\sum_{k=0}^{n-1} U_T^k\| \leq 1$ (as an operator on $L^2$). Therefore

$$\left\| \frac{1}{n} \sum_{k=0}^{n-1} U_T^k h \right\|_2 \leq \left\| \frac{1}{n} \sum_{k=0}^{n-1} U_T^k h_0 \right\|_2 + \left\| \frac{1}{n} \sum_{k=0}^{n-1} U_T^k (h - h_0) \right\|_2 \leq \frac{2\|g_0\|_2}{n} + \varepsilon.$$

For $n$ large enough, the first term is less than $\varepsilon$, so the whole expression is less than $2\varepsilon$. Since $\varepsilon$ was arbitrary, $\frac{1}{n}\sum_{k=0}^{n-1} U_T^k h \to 0$ in $L^2$. $\square$

**Remark 9.4.** Von Neumann's theorem is really a theorem in functional analysis: it holds for any isometry on a Hilbert space. The dynamics enter only through the identification of $\mathcal{I}$ with the invariant functions. This level of generality is both a strength and a weakness — the theorem tells us that time averages converge *in norm*, but it says nothing about convergence at individual points. For that, we need Birkhoff's deeper result.


## 9.4 The Maximal Ergodic Theorem

Before proving Birkhoff's theorem, we need a crucial technical tool. The maximal ergodic theorem controls the size of the set where partial time averages are large. The proof we give is due to A. Garsia (1965) and is notable for its brevity and elegance.

**Notation.** For $f \in L^1(X, \mu)$ and $n \geq 1$, define the partial sums

$$S_n f(x) = \sum_{k=0}^{n-1} f(T^k x), \qquad S_0 f(x) = 0,$$

and the **maximal function**

$$M_N f(x) = \max_{1 \leq n \leq N} S_n f(x).$$

**Theorem 9.5** (Maximal Ergodic Theorem). Let $T$ be a measure-preserving transformation on $(X, \mathcal{B}, \mu)$ and let $f \in L^1(X, \mu)$. For each $N \geq 1$, define

$$E_N = \{ x \in X : M_N f(x) > 0 \} = \left\{ x \in X : \max_{1 \leq n \leq N} S_n f(x) > 0 \right\}.$$

Then

$$\int_{E_N} f \, d\mu \geq 0.$$

*Proof (Garsia).* Fix $N \geq 1$. Define $f^* = M_N f = \max_{1 \leq n \leq N} S_n f$. Note that $E_N = \{f^* > 0\}$ and $f^* \geq S_n f$ for $1 \leq n \leq N$, with $f^* \geq S_1 f = f$.

We claim:

$$f \geq f^* - f^* \circ T. \tag{$*$}$$

To prove ($*$), note that for each $n$ with $1 \leq n \leq N$,

$$S_n f(x) = f(x) + S_{n-1} f(Tx).$$

For $n \geq 2$, $S_{n-1} f(Tx) \leq M_N f(Tx) = f^*(Tx)$ (since $n - 1 \leq N - 1 < N$ and $M_N f$ takes the maximum over indices up to $N$; more precisely, $S_{n-1}f(Tx) = \sum_{k=0}^{n-2} f(T^{k+1}x) \leq \max_{1 \leq j \leq N} S_j f(Tx) = f^*(Tx)$). Also $S_1 f(x) = f(x) = f(x) + 0 \leq f(x) + f^*(Tx)$ (since $f^* \geq 0$ on $E_N$ and $f^* \geq S_1 f = f$ everywhere; actually we need to be slightly more careful).

Let us redo this cleanly. For $1 \leq n \leq N$:
- If $n = 1$: $S_1 f(x) = f(x) \leq f(x) + f^*(Tx)$ since $f^*(Tx) \geq 0$ when $Tx \in E_N$, and $f^*(Tx) \geq S_0 f(Tx) = 0$... but $f^*$ might be negative.

Let us use a cleaner version of Garsia's argument. Define

$$f^*(x) = \max(0, S_1 f(x), S_2 f(x), \ldots, S_N f(x)) = \max_{0 \leq n \leq N} S_n f(x) \geq 0.$$

Now $f^* \geq 0$ everywhere, and $E_N = \{f^* > 0\}$. For $1 \leq n \leq N$:

$$S_n f(x) = f(x) + S_{n-1} f(Tx) \leq f(x) + f^*(Tx),$$

since $S_{n-1} f(Tx) \leq \max_{0 \leq j \leq N} S_j f(Tx) = f^*(Tx)$ (note $n - 1$ ranges from $0$ to $N - 1$, and $f^*$ takes the max over $0$ to $N$, so indeed $S_{n-1} f(Tx) \leq f^*(Tx)$). Also $S_0 f(x) = 0 \leq f(x) + f^*(Tx)$ is not necessarily true, but we do not need it: we only need

$$f^*(x) = \max_{0 \leq n \leq N} S_n f(x) \leq \max\!\big(0,\; f(x) + f^*(Tx)\big) \leq f(x) + f^*(Tx),$$

where the last inequality uses the fact that $f^*(Tx) \geq 0$. (The first inequality holds because each $S_n f(x) \leq f(x) + f^*(Tx)$ for $n \geq 1$, and $S_0 f(x) = 0$.)

Wait — to be fully precise: if $f^*(x) = 0$, the inequality $f^*(x) \leq f(x) + f^*(Tx)$ might fail if $f(x) + f^*(Tx) < 0$. But $f^*(Tx) \geq 0$, so $f(x) + f^*(Tx) \geq f(x)$, and we would need $f(x) \geq 0$, which need not hold. However, if $f^*(x) = 0$, then $x \notin E_N$, and we only integrate over $E_N$ anyway.

So: on $E_N$, we have $f^*(x) > 0$, which means $f^*(x) = \max_{1 \leq n \leq N} S_n f(x)$, and for each such $n$, $S_n f(x) = f(x) + S_{n-1}f(Tx) \leq f(x) + f^*(Tx)$. Therefore

$$f^*(x) \leq f(x) + f^*(Tx) \qquad \text{for all } x \in E_N.$$

Rearranging: $f(x) \geq f^*(x) - f^*(Tx)$ for $x \in E_N$. Since $f^* \geq 0$ everywhere and $f^*(x) > 0$ on $E_N$:

$$\int_{E_N} f \, d\mu \geq \int_{E_N} \big(f^* - f^* \circ T\big) \, d\mu = \int_{E_N} f^* \, d\mu - \int_{E_N} f^*(Tx) \, d\mu.$$

Now, $\int_{E_N} f^* \, d\mu = \int_X f^* \, d\mu$ since $f^* = 0$ on $X \setminus E_N$ (by definition, $f^* \geq 0$ and $f^* = 0$ outside $E_N$). Also, $\int_{E_N} f^*(Tx) \, d\mu \leq \int_X f^*(Tx) \, d\mu = \int_X f^* \, d\mu$, where the equality uses the fact that $T$ is measure-preserving. Therefore

$$\int_{E_N} f \, d\mu \geq \int_X f^* \, d\mu - \int_X f^* \, d\mu = 0. \quad \square$$

**Remark 9.6.** The maximal ergodic theorem is sometimes stated in the following equivalent form. Define $E^* = \{x : \sup_{n \geq 1} S_n f(x) > 0\}$. Since $E^* = \bigcup_{N=1}^\infty E_N$ and $E_1 \subseteq E_2 \subseteq \cdots$, continuity of the measure gives $\int_{E^*} f \, d\mu = \lim_{N \to \infty} \int_{E_N} f \, d\mu \geq 0$.

More precisely, for any $\alpha \in \mathbb{R}$, applying the theorem to $f - \alpha$ (which is still in $L^1$), we obtain the following useful corollary.

**Corollary 9.7** (Maximal Ergodic Inequality). Let $f \in L^1(X, \mu)$ and $\alpha \in \mathbb{R}$. Define

$$E_\alpha = \left\{ x \in X : \sup_{n \geq 1} \frac{1}{n} S_n f(x) > \alpha \right\}.$$

Then $\int_{E_\alpha} f \, d\mu \geq \alpha \cdot \mu(E_\alpha)$.

*Proof.* Apply Remark 9.6 to the function $g = f - \alpha$. Note that $S_n g = S_n f - n\alpha$, so $\sup_n \frac{1}{n} S_n g(x) > 0$ if and only if $\sup_n \frac{1}{n} S_n f(x) > \alpha$. Thus $\{x : \sup_n S_n g(x) > 0\} = E_\alpha$, and $\int_{E_\alpha} g \, d\mu \geq 0$ gives $\int_{E_\alpha} f \, d\mu \geq \alpha \cdot \mu(E_\alpha)$. $\square$


## 9.5 Birkhoff's Pointwise Ergodic Theorem

We now prove the most important theorem of ergodic theory.

**Theorem 9.8** (Birkhoff's Pointwise Ergodic Theorem, 1931). Let $(X, \mathcal{B}, \mu)$ be a probability space, $T: X \to X$ a measure-preserving transformation, and $f \in L^1(X, \mu)$. Then:

**(i)** The limit

$$\bar{f}(x) = \lim_{n \to \infty} \frac{1}{n} \sum_{k=0}^{n-1} f(T^k x)$$

exists for $\mu$-almost every $x \in X$.

**(ii)** The limit function $\bar{f}$ is $T$-invariant: $\bar{f}(Tx) = \bar{f}(x)$ a.e.

**(iii)** $\bar{f} \in L^1(X, \mu)$ and $\int_X \bar{f} \, d\mu = \int_X f \, d\mu$.

*Proof.*

**Part (ii)** is immediate once the limit exists: if $\bar{f}(x) = \lim_n \frac{1}{n}\sum_{k=0}^{n-1} f(T^k x)$, then

$$\bar{f}(Tx) = \lim_n \frac{1}{n} \sum_{k=0}^{n-1} f(T^{k+1} x) = \lim_n \frac{1}{n} \sum_{k=1}^{n} f(T^k x) = \lim_n \frac{1}{n}\sum_{k=0}^{n-1} f(T^k x) = \bar{f}(x),$$

where the third equality uses the fact that $\frac{1}{n}(S_n f(x) - f(x) + f(T^n x)) \to \bar{f}(x)$ since $\frac{f(x)}{n} \to 0$ and $\frac{f(T^n x)}{n} \to 0$ (the latter requires a small argument, but follows from the fact that $f \in L^1$ implies $\frac{f(T^n x)}{n} \to 0$ a.e. — this is a consequence of the almost-everywhere convergence itself, or can be seen from the Borel-Cantelli lemma; for now we note that the shift of indices does not affect the Cesàro limit when it exists).

**Part (i): The limit exists a.e.** This is the hard part. We use the maximal ergodic theorem.

Define the upper and lower time averages:

$$\overline{f}(x) = \limsup_{n \to \infty} \frac{1}{n} S_n f(x), \qquad \underline{f}(x) = \liminf_{n \to \infty} \frac{1}{n} S_n f(x).$$

Clearly $\underline{f}(x) \leq \overline{f}(x)$ for all $x$. The limit $\bar{f}(x)$ exists if and only if $\underline{f}(x) = \overline{f}(x)$. We will show that $\underline{f}(x) = \overline{f}(x)$ for $\mu$-a.e. $x$.

For rational numbers $\alpha < \beta$, define

$$A_{\alpha, \beta} = \{ x \in X : \underline{f}(x) < \alpha < \beta < \overline{f}(x) \}.$$

Then

$$\{ x : \underline{f}(x) < \overline{f}(x) \} = \bigcup_{\alpha < \beta, \; \alpha, \beta \in \mathbb{Q}} A_{\alpha, \beta}.$$

It suffices to show that $\mu(A_{\alpha, \beta}) = 0$ for every pair of rationals $\alpha < \beta$.

The sets $A_{\alpha, \beta}$ are $T$-invariant: if $x \in A_{\alpha, \beta}$, then $\overline{f}(Tx) = \overline{f}(x)$ and $\underline{f}(Tx) = \underline{f}(x)$ (by the same index-shifting argument as in Part (ii)), so $Tx \in A_{\alpha, \beta}$.

Now fix $\alpha < \beta$ in $\mathbb{Q}$. We apply Corollary 9.7 twice.

**Applying the maximal inequality to get an upper bound.** On the set $A_{\alpha, \beta}$, we have $\overline{f}(x) > \beta$, so $A_{\alpha, \beta} \subseteq E_\beta = \{x : \sup_n \frac{1}{n} S_n f(x) > \beta\}$. But we want to work on $A_{\alpha, \beta}$ itself. Since $A_{\alpha, \beta}$ is $T$-invariant, we can restrict our attention to it.

Let $g = f - \beta$. On $A_{\alpha,\beta}$, $\overline{f}(x) > \beta$ means $\limsup_n \frac{1}{n} S_n g(x) > 0$, so $\sup_n \frac{1}{n} S_n g(x) > 0$, so $A_{\alpha, \beta} \subseteq \{x : \sup_n \frac{1}{n} S_n g(x) > 0\} = E_0(g)$.

By the maximal ergodic inequality (Corollary 9.7 with $\alpha = 0$ applied to $g$):

$$\int_{E_0(g)} g \, d\mu \geq 0,$$

and since $A_{\alpha,\beta} \subseteq E_0(g)$... but this is not quite enough, because $E_0(g)$ might be larger than $A_{\alpha,\beta}$.

Let us use a cleaner approach. We work directly with Corollary 9.7 applied to the restriction of the system to the invariant set $A_{\alpha, \beta}$.

Since $A_{\alpha, \beta}$ is $T$-invariant and measurable, $T$ restricts to a measure-preserving transformation on $A_{\alpha, \beta}$ (with the restricted measure — or more precisely, $T^{-1}(A_{\alpha,\beta}) = A_{\alpha,\beta}$ since the set is $T$-invariant).

On $A_{\alpha,\beta}$, we have $\overline{f}(x) > \beta$, so $\sup_n \frac{1}{n} S_n f(x) > \beta$. Apply Corollary 9.7 to $f$ restricted to $A_{\alpha,\beta}$ with the threshold $\beta$: the set $\{x \in A_{\alpha,\beta} : \sup_n \frac{1}{n} S_n f(x) > \beta\} = A_{\alpha,\beta}$ (since every point in $A_{\alpha,\beta}$ has $\overline{f}(x) > \beta$). Thus:

$$\int_{A_{\alpha,\beta}} f \, d\mu \geq \beta \cdot \mu(A_{\alpha,\beta}). \tag{1}$$

Similarly, on $A_{\alpha,\beta}$, $\underline{f}(x) < \alpha$, so $\liminf_n \frac{1}{n} S_n f(x) < \alpha$, which means $\limsup_n \frac{1}{n} S_n(-f)(x) > -\alpha$, hence $\sup_n \frac{1}{n} S_n(-f)(x) > -\alpha$. Applying Corollary 9.7 to $-f$ on $A_{\alpha,\beta}$ with threshold $-\alpha$:

$$\int_{A_{\alpha,\beta}} (-f) \, d\mu \geq -\alpha \cdot \mu(A_{\alpha,\beta}),$$

i.e.,

$$\int_{A_{\alpha,\beta}} f \, d\mu \leq \alpha \cdot \mu(A_{\alpha,\beta}). \tag{2}$$

Combining (1) and (2):

$$\beta \cdot \mu(A_{\alpha,\beta}) \leq \int_{A_{\alpha,\beta}} f \, d\mu \leq \alpha \cdot \mu(A_{\alpha,\beta}).$$

Since $\beta > \alpha$, this implies $(\beta - \alpha) \mu(A_{\alpha,\beta}) \leq 0$, and since $\beta - \alpha > 0$, we conclude $\mu(A_{\alpha,\beta}) = 0$.

Since this holds for all rational $\alpha < \beta$, $\mu(\{x : \underline{f}(x) < \overline{f}(x)\}) = 0$, so the limit $\bar{f}(x) = \lim_n \frac{1}{n} S_n f(x)$ exists $\mu$-a.e.

**Part (iii): $\bar{f} \in L^1$ and $\int \bar{f} = \int f$.** By Fatou's lemma applied to the non-negative functions $\frac{1}{n}|S_n f|$:

$$\int_X |\bar{f}| \, d\mu \leq \liminf_{n \to \infty} \frac{1}{n} \int_X |S_n f| \, d\mu \leq \liminf_{n \to \infty} \frac{1}{n} \sum_{k=0}^{n-1} \int_X |f \circ T^k| \, d\mu = \|f\|_1,$$

where we used the fact that $\|f \circ T^k\|_1 = \|f\|_1$ (since $T$ is measure-preserving). So $\bar{f} \in L^1$ and $\|\bar{f}\|_1 \leq \|f\|_1$.

For the equality of integrals, note that $|\frac{1}{n} S_n f(x)| \leq \frac{1}{n} \sum_{k=0}^{n-1} |f(T^k x)|$, and the right-hand side converges a.e. to $\overline{|f|}(x) \in L^1$ by Part (i) applied to $|f|$. So $\{\frac{1}{n}S_n f\}$ is dominated by an $L^1$ function (eventually, and can be handled carefully). More directly, by the $T$-invariance of $\mu$:

$$\int_X \frac{1}{n} S_n f \, d\mu = \frac{1}{n} \sum_{k=0}^{n-1} \int_X f \circ T^k \, d\mu = \frac{1}{n} \sum_{k=0}^{n-1} \int_X f \, d\mu = \int_X f \, d\mu$$

for every $n$. Now, define $g_n = \frac{1}{n} S_n f$. We have $g_n \to \bar{f}$ a.e. and $|g_n| \leq \frac{1}{n}\sum_{k=0}^{n-1} |f| \circ T^k$. We need to apply dominated convergence. Define $h_n = \frac{1}{n}\sum_{k=0}^{n-1} |f| \circ T^k$, which converges a.e. to $\overline{|f|}$. We have $|g_n| \leq h_n$, but $h_n$ is not a fixed dominating function.

Instead, we use a truncation argument. For $M > 0$, let $f_M = \max(-M, \min(f, M))$ be the truncation of $f$ at level $M$. Then $|f_M| \leq M$, so $|\frac{1}{n} S_n f_M| \leq M$, and by the dominated convergence theorem:

$$\int_X \bar{f}_M \, d\mu = \lim_{n \to \infty} \int_X \frac{1}{n} S_n f_M \, d\mu = \int_X f_M \, d\mu.$$

Now let $M \to \infty$. Since $f_M \to f$ in $L^1$ and $\|\bar{f}_M - \bar{f}\|_1 \leq \|f_M - f\|_1 \to 0$ (by the bound $\|\bar{g}\|_1 \leq \|g\|_1$ from above, applied to $g = f_M - f$), we get $\int \bar{f}_M \to \int \bar{f}$ and $\int f_M \to \int f$, so $\int \bar{f} = \int f$. $\square$

**Remark 9.9.** The relationship between the two ergodic theorems is worth noting. Von Neumann's theorem gives $L^2$ convergence, which is weaker than pointwise a.e. convergence in general (the two are not directly comparable, but $L^2$ convergence implies convergence in measure). Birkhoff's theorem gives the stronger pointwise convergence, but requires a harder proof. Historically, Birkhoff proved his theorem slightly before von Neumann published, though von Neumann had communicated his result earlier — leading to some priority disputes. Both theorems are fundamental, and in many applications the $L^2$ version suffices.


## 9.6 Ergodicity

We now define the central concept of this chapter — and arguably of the entire subject.

**Definition 9.10.** A measure-preserving transformation $T: (X, \mathcal{B}, \mu) \to (X, \mathcal{B}, \mu)$ is **ergodic** if every $T$-invariant measurable set has measure $0$ or $1$. That is, if $A \in \mathcal{B}$ and $T^{-1}(A) = A$, then $\mu(A) = 0$ or $\mu(A) = 1$.

Informally, ergodicity means the system cannot be decomposed into two non-trivial invariant pieces. The dynamics is "indecomposable" from the measure-theoretic point of view.

**Remark 9.11.** Some authors use the weaker condition $\mu(T^{-1}A \triangle A) = 0 \Rightarrow \mu(A) \in \{0, 1\}$ (invariance mod $\mu$). For most purposes these are equivalent. We will use strict invariance $T^{-1}A = A$ in the definition, noting that the equivalence with the "mod $\mu$" version is straightforward when the system is defined on a complete measure space.

The following theorem gives several equivalent characterizations of ergodicity. This is a result of fundamental importance — it tells us precisely when time averages equal space averages.

**Theorem 9.12** (Equivalent characterizations of ergodicity). Let $T: (X, \mathcal{B}, \mu) \to (X, \mathcal{B}, \mu)$ be a measure-preserving transformation on a probability space. The following are equivalent:

**(a)** $T$ is ergodic: every $T$-invariant set $A \in \mathcal{B}$ (i.e., $T^{-1}A = A$) satisfies $\mu(A) = 0$ or $\mu(A) = 1$.

**(b)** Every $T$-invariant function in $L^1(X, \mu)$ is constant a.e. That is, if $f \in L^1$ and $f \circ T = f$ a.e., then $f$ is constant a.e.

**(c)** For every $f \in L^1(X, \mu)$:
$$\lim_{n \to \infty} \frac{1}{n} \sum_{k=0}^{n-1} f(T^k x) = \int_X f \, d\mu \qquad \text{for } \mu\text{-a.e. } x.$$

**(d)** For all measurable sets $A, B \in \mathcal{B}$:
$$\lim_{n \to \infty} \frac{1}{n} \sum_{k=0}^{n-1} \mu(T^{-k}A \cap B) = \mu(A)\mu(B).$$

*Proof.*

**(a) $\Rightarrow$ (b).** Suppose $T$ is ergodic and $f \circ T = f$ a.e. with $f \in L^1$. We first handle the case $f$ real-valued. For any $c \in \mathbb{R}$, the set $A_c = \{x : f(x) \leq c\}$ satisfies

$$T^{-1}(A_c) = \{x : f(Tx) \leq c\} = \{x : f(x) \leq c\} = A_c \quad \text{(a.e.)}.$$

More precisely, $\mu(T^{-1}(A_c) \triangle A_c) = 0$, so by adjusting on a null set (or using the "mod $\mu$" version of ergodicity), $\mu(A_c) \in \{0, 1\}$. Define

$$c^* = \inf\{c \in \mathbb{R} : \mu(A_c) = 1\}.$$

For $c > c^*$, $\mu(A_c) = 1$, so $f \leq c$ a.e. For $c < c^*$, $\mu(A_c) = 0$, so $f > c$ a.e. Taking a sequence $c_n \downarrow c^*$, we get $f \leq c^*$ a.e., and taking $c_n \uparrow c^*$, we get $f \geq c^*$ a.e. Therefore $f = c^*$ a.e. (The value $c^*$ is finite since $f \in L^1$.)

For complex-valued $f$, apply the above to the real and imaginary parts.

**(b) $\Rightarrow$ (a).** Suppose every $T$-invariant $L^1$ function is constant a.e. Let $A$ be a $T$-invariant set. Then $f = \mathbf{1}_A$ is a $T$-invariant $L^1$ function (since $\mathbf{1}_A \circ T = \mathbf{1}_{T^{-1}A} = \mathbf{1}_A$). By (b), $\mathbf{1}_A$ is constant a.e., so $\mathbf{1}_A = 0$ a.e. or $\mathbf{1}_A = 1$ a.e., i.e., $\mu(A) = 0$ or $\mu(A) = 1$.

**(b) $\Rightarrow$ (c).** By Birkhoff's theorem (Theorem 9.8), the time average $\bar{f}(x) = \lim_n \frac{1}{n}\sum_{k=0}^{n-1} f(T^k x)$ exists a.e., is $T$-invariant, and satisfies $\int \bar{f} = \int f$. By (b), $\bar{f}$ is constant a.e. Since $\int \bar{f} = \int f$, this constant must equal $\int f \, d\mu$.

**(c) $\Rightarrow$ (b).** Suppose $f \in L^1$ and $f \circ T = f$ a.e. Then $\frac{1}{n}\sum_{k=0}^{n-1} f(T^k x) = f(x)$ a.e. for all $n$. By (c), this equals $\int f \, d\mu$ a.e. So $f(x) = \int f \, d\mu$ for a.e. $x$.

**(c) $\Rightarrow$ (d).** Apply (c) to $f = \mathbf{1}_A$, where $A \in \mathcal{B}$:

$$\frac{1}{n} \sum_{k=0}^{n-1} \mathbf{1}_A(T^k x) \to \mu(A) \qquad \text{a.e.}$$

Multiply both sides by $\mathbf{1}_B(x)$ and integrate:

$$\frac{1}{n} \sum_{k=0}^{n-1} \int_X \mathbf{1}_A(T^k x) \mathbf{1}_B(x) \, d\mu(x) \to \mu(A) \cdot \mu(B).$$

The left side equals $\frac{1}{n}\sum_{k=0}^{n-1} \mu(T^{-k}A \cap B)$ (since $\mathbf{1}_A(T^k x)\mathbf{1}_B(x) = \mathbf{1}_{T^{-k}A \cap B}(x)$). The convergence of the integral is justified by dominated convergence (the integrands are bounded by $1$). This gives (d).

**(d) $\Rightarrow$ (a).** Let $A$ be $T$-invariant, i.e., $T^{-1}A = A$. Apply (d) with $B = A$:

$$\frac{1}{n} \sum_{k=0}^{n-1} \mu(T^{-k}A \cap A) = \frac{1}{n} \sum_{k=0}^{n-1} \mu(A \cap A) = \mu(A) \to \mu(A)\mu(A) = \mu(A)^2.$$

So $\mu(A) = \mu(A)^2$, which implies $\mu(A) = 0$ or $\mu(A) = 1$. $\square$

**Remark 9.13.** The equivalence (a) $\Leftrightarrow$ (c) is the key takeaway of this chapter. It says:

> *The time average of any observable equals its space average (for a.e. initial condition) if and only if the system is ergodic.*

This is the precise mathematical content of Boltzmann's ergodic hypothesis (in its modern formulation).

Condition (d) is often called **Cesàro mixing** or **ergodicity in the sense of mixing on average**. It says that, on average, the sets $T^{-k}A$ become independent of any fixed set $B$. This is weaker than (strong) mixing, which requires $\mu(T^{-n}A \cap B) \to \mu(A)\mu(B)$ without the Cesàro averaging.


## 9.7 Examples of Ergodic Systems

We now prove ergodicity for several fundamental examples introduced in Chapter 8.

### 9.7.1 Irrational Rotation

Let $X = \mathbb{R}/\mathbb{Z} \cong [0, 1)$ with Lebesgue measure $\mu$, and let $T_\alpha(x) = x + \alpha \pmod{1}$, where $\alpha \in \mathbb{R} \setminus \mathbb{Q}$.

**Theorem 9.14.** The irrational rotation $T_\alpha$ is ergodic with respect to Lebesgue measure.

*Proof.* We use Fourier analysis. We show that characterization (b) holds: every $T_\alpha$-invariant $L^2$ function is constant a.e. (Since $L^2 \subset L^1$ on a probability space, this suffices.)

Let $f \in L^2(\mathbb{R}/\mathbb{Z})$ satisfy $f \circ T_\alpha = f$ a.e. Expand $f$ in a Fourier series:

$$f(x) = \sum_{n \in \mathbb{Z}} \hat{f}(n) e^{2\pi i n x}, \qquad \hat{f}(n) = \int_0^1 f(x) e^{-2\pi i n x} \, dx.$$

The condition $f(x + \alpha) = f(x)$ a.e. gives, at the level of Fourier coefficients:

$$\hat{f}(n) e^{2\pi i n \alpha} = \hat{f}(n) \qquad \text{for all } n \in \mathbb{Z}.$$

This is because $(f \circ T_\alpha)\hat{\;}(n) = e^{2\pi i n \alpha} \hat{f}(n)$.

For $n \neq 0$, $e^{2\pi i n \alpha} \neq 1$ (since $\alpha$ is irrational and $n \neq 0$, we have $n\alpha \notin \mathbb{Z}$). Therefore $\hat{f}(n) = 0$ for all $n \neq 0$.

So $f(x) = \hat{f}(0) = \int_0^1 f \, dx$ a.e. That is, $f$ is constant a.e. $\square$

**Remark 9.15.** This proof breaks down completely when $\alpha = p/q$ is rational. In that case, $e^{2\pi i n \alpha} = 1$ whenever $q \mid n$, so there exist non-constant invariant functions — for instance, $f(x) = e^{2\pi i q x}$. We will see below that rational rotations are indeed not ergodic.


### 9.7.2 The Doubling Map

Let $X = [0, 1)$ with Lebesgue measure $\mu$, and $T(x) = 2x \pmod{1}$.

**Theorem 9.16.** The doubling map is ergodic with respect to Lebesgue measure.

*Proof.* We again use Fourier analysis. Suppose $f \in L^2([0,1))$ is $T$-invariant: $f(2x \bmod 1) = f(x)$ a.e.

We compute the Fourier coefficients of $f \circ T$:

$$(f \circ T)\hat{\;}(n) = \int_0^1 f(2x \bmod 1) e^{-2\pi i n x} \, dx.$$

Split the integral into $[0, 1/2)$ and $[1/2, 1)$. On $[0, 1/2)$, $2x \bmod 1 = 2x$; substituting $u = 2x$:

$$\int_0^{1/2} f(2x) e^{-2\pi i n x} \, dx = \frac{1}{2} \int_0^1 f(u) e^{-\pi i n u} \, du.$$

On $[1/2, 1)$, $2x \bmod 1 = 2x - 1$; substituting $u = 2x - 1$:

$$\int_{1/2}^1 f(2x - 1) e^{-2\pi i n x} \, dx = \frac{1}{2} \int_0^1 f(u) e^{-\pi i n (u+1)} \, du = \frac{e^{-\pi i n}}{2} \int_0^1 f(u) e^{-\pi i n u} \, du.$$

Adding:

$$(f \circ T)\hat{\;}(n) = \frac{1 + e^{-\pi i n}}{2} \int_0^1 f(u) e^{-\pi i n u} \, du.$$

Now $\frac{1 + e^{-\pi i n}}{2} = \begin{cases} 1 & \text{if } n \text{ is even} \\ 0 & \text{if } n \text{ is odd}\end{cases}$.

So for $n$ even, say $n = 2m$:

$$(f \circ T)\hat{\;}(2m) = \int_0^1 f(u) e^{-2\pi i m u} \, du = \hat{f}(m).$$

And for $n$ odd: $(f \circ T)\hat{\;}(n) = 0$.

The condition $f \circ T = f$ a.e. means $(f \circ T)\hat{\;}(n) = \hat{f}(n)$ for all $n$. This gives:

- For $n$ odd: $\hat{f}(n) = 0$.
- For $n$ even, $n = 2m$: $\hat{f}(2m) = \hat{f}(m)$.

The second relation, applied repeatedly, gives $\hat{f}(m) = \hat{f}(2m) = \hat{f}(4m) = \hat{f}(8m) = \cdots = \hat{f}(2^k m)$ for all $k \geq 0$.

If $m \neq 0$, then $|2^k m| \to \infty$, but $\hat{f}(n) \to 0$ as $|n| \to \infty$ by the Riemann-Lebesgue lemma (since $f \in L^1$, and in particular $f \in L^2$ implies $\sum |\hat{f}(n)|^2 < \infty$, hence $\hat{f}(n) \to 0$). Therefore $\hat{f}(m) = 0$ for all $m \neq 0$.

We also need to handle the case where $m$ is even: write $m = 2^j m'$ with $m'$ odd. Then $\hat{f}(m) = \hat{f}(m')$ (by iterating $\hat{f}(2m) = \hat{f}(m)$ a total of $j$ times). But $m'$ is odd, so $\hat{f}(m') = 0$. Hence $\hat{f}(m) = 0$ for all $m \neq 0$.

So $f(x) = \hat{f}(0)$ a.e., and $T$ is ergodic. $\square$


### 9.7.3 Bernoulli Shifts

Let $\Sigma = \{0, 1, \ldots, k-1\}^{\mathbb{N}}$ be the one-sided shift space on $k$ symbols (with the product $\sigma$-algebra), equipped with the product measure $\mu = p^{\mathbb{N}}$ where $p = (p_0, p_1, \ldots, p_{k-1})$ is a probability vector ($p_i > 0$, $\sum p_i = 1$). The **shift map** $\sigma: \Sigma \to \Sigma$ is defined by $(\sigma(\omega))_n = \omega_{n+1}$.

Recall that the **cylinder sets**

$$[a_0, a_1, \ldots, a_{m-1}] = \{\omega \in \Sigma : \omega_0 = a_0, \omega_1 = a_1, \ldots, \omega_{m-1} = a_{m-1}\}$$

form a semi-algebra generating $\mathcal{B}$, and $\mu([a_0, \ldots, a_{m-1}]) = p_{a_0} p_{a_1} \cdots p_{a_{m-1}}$.

**Theorem 9.17.** The Bernoulli shift $(\Sigma, \mu, \sigma)$ is ergodic.

*Proof.* We verify characterization (d) of ergodicity for cylinder sets, which suffices since cylinders generate the $\sigma$-algebra (and both sides of (d) extend by standard measure-theoretic approximation arguments).

Let $A = [a_0, \ldots, a_{m-1}]$ and $B = [b_0, \ldots, b_{\ell-1}]$ be cylinder sets, specifying coordinates $0, \ldots, m-1$ and $0, \ldots, \ell-1$ respectively. Note that

$$\sigma^{-k}(A) = \{\omega : \omega_{k} = a_0, \omega_{k+1} = a_1, \ldots, \omega_{k+m-1} = a_{m-1}\},$$

which specifies coordinates $k, k+1, \ldots, k+m-1$.

For $k \geq \ell$, the sets $\sigma^{-k}(A)$ and $B$ specify disjoint sets of coordinates, so by independence of coordinates under the product measure:

$$\mu(\sigma^{-k}A \cap B) = \mu(\sigma^{-k}A) \cdot \mu(B) = \mu(A) \cdot \mu(B).$$

So for $n > \ell$:

$$\frac{1}{n}\sum_{k=0}^{n-1} \mu(\sigma^{-k}A \cap B) = \frac{1}{n}\sum_{k=0}^{\ell-1} \mu(\sigma^{-k}A \cap B) + \frac{1}{n}\sum_{k=\ell}^{n-1} \mu(A)\mu(B).$$

The first sum contributes at most $\ell/n \to 0$, and the second sum equals $\frac{n - \ell}{n}\mu(A)\mu(B) \to \mu(A)\mu(B)$.

Therefore $\frac{1}{n}\sum_{k=0}^{n-1}\mu(\sigma^{-k}A \cap B) \to \mu(A)\mu(B)$.

To extend from cylinders to arbitrary measurable sets: let $A, B \in \mathcal{B}$. Given $\varepsilon > 0$, approximate $A$ and $B$ by finite unions of cylinders $A'$ and $B'$ with $\mu(A \triangle A') < \varepsilon$ and $\mu(B \triangle B') < \varepsilon$. Since

$$|\mu(\sigma^{-k}A \cap B) - \mu(\sigma^{-k}A' \cap B')| \leq \mu(A \triangle A') + \mu(B \triangle B') < 2\varepsilon$$

(using the fact that $\mu(\sigma^{-k}(A \triangle A')) = \mu(A \triangle A')$ since $\sigma$ preserves $\mu$), and (d) holds for $A', B'$, a routine $3\varepsilon$-argument shows (d) holds for $A, B$. $\square$

**Remark 9.18.** In fact, the Bernoulli shift is **mixing** (not just ergodic): $\mu(\sigma^{-n}A \cap B) \to \mu(A)\mu(B)$ as $n \to \infty$, without the need for Cesàro averaging. This is stronger than what we needed. We will discuss mixing in Chapter 10.


### 9.7.4 Non-Example: Rational Rotation

Let $T_{p/q}(x) = x + p/q \pmod{1}$ where $p/q$ is a rational number in lowest terms with $q \geq 2$.

**Proposition 9.19.** The rational rotation $T_{p/q}$ is NOT ergodic with respect to Lebesgue measure.

*Proof.* We exhibit a $T_{p/q}$-invariant set of intermediate measure. Consider the set

$$A = \bigcup_{j=0}^{q-1} \left[\frac{j}{q}, \frac{j}{q} + \frac{1}{2q}\right).$$

This is a union of the "first halves" of the intervals $[j/q, (j+1)/q)$ for $j = 0, \ldots, q-1$. We have $\mu(A) = q \cdot \frac{1}{2q} = \frac{1}{2}$.

Since $T_{p/q}$ permutes the intervals $[j/q, (j+1)/q)$ (it maps the $j$-th interval to the $(j+p \bmod q)$-th interval), and $A$ consists of the first half of each such interval, $A$ is $T_{p/q}$-invariant. So $\mu(A) = 1/2 \notin \{0, 1\}$, and $T_{p/q}$ is not ergodic.

Alternatively: $f(x) = e^{2\pi i q x}$ satisfies $f(x + p/q) = e^{2\pi i q(x + p/q)} = e^{2\pi i qx} e^{2\pi i p} = f(x)$, so $f$ is a non-constant $T_{p/q}$-invariant function. $\square$

**Remark 9.20.** Geometrically, rational rotation partitions the circle into finitely many orbits, each of length $q$. The dynamics on each orbit is periodic. One can decompose the system into $q$ invariant subsets (or, thinking continuously, into invariant "strips"), showing the system is far from indecomposable.


## 9.8 Unique Ergodicity

So far, Birkhoff's theorem tells us that time averages converge *almost everywhere*. But "almost everywhere" depends on the measure, and there may be exceptional points. In some situations, we can do better.

**Definition 9.21.** A continuous map $T: X \to X$ on a compact metrizable space $X$ is **uniquely ergodic** if there is exactly one $T$-invariant Borel probability measure on $X$.

**Theorem 9.22** (Unique ergodicity and uniform convergence). Let $T: X \to X$ be a continuous map on a compact metrizable space $X$, and let $\mu$ be a $T$-invariant Borel probability measure. The following are equivalent:

**(a)** $T$ is uniquely ergodic (with unique invariant measure $\mu$).

**(b)** For every continuous function $f \in C(X)$:
$$\frac{1}{n} \sum_{k=0}^{n-1} f(T^k x) \to \int_X f \, d\mu \qquad \text{uniformly in } x \in X.$$

**(c)** For every continuous function $f \in C(X)$:
$$\frac{1}{n} \sum_{k=0}^{n-1} f(T^k x) \to \int_X f \, d\mu \qquad \text{for every } x \in X.$$

Note the strength of this result: convergence holds for *every* point, not just almost every point. There is no exceptional set.

*Proof.*

**(a) $\Rightarrow$ (b).** Suppose for contradiction that the convergence is not uniform for some $f \in C(X)$. Then there exist $\varepsilon > 0$, a sequence $n_j \to \infty$, and points $x_j \in X$ such that

$$\left|\frac{1}{n_j} \sum_{k=0}^{n_j - 1} f(T^k x_j) - \int f \, d\mu \right| \geq \varepsilon. \tag{$\dagger$}$$

Define the probability measures $\nu_j = \frac{1}{n_j}\sum_{k=0}^{n_j-1} \delta_{T^k x_j}$ (empirical measures along orbits). By the Banach-Alaoglu theorem (or equivalently, Prokhorov's theorem, since $X$ is compact), the sequence $\{\nu_j\}$ has a weak-$*$ convergent subsequence $\nu_{j_i} \rightharpoonup \nu$ for some Borel probability measure $\nu$ on $X$.

We claim $\nu$ is $T$-invariant. For any $g \in C(X)$:

$$\int g \, d(T_* \nu_j) = \int g \circ T \, d\nu_j = \frac{1}{n_j}\sum_{k=0}^{n_j - 1} g(T^{k+1}x_j) = \frac{1}{n_j}\sum_{k=1}^{n_j} g(T^k x_j).$$

The difference between this and $\int g \, d\nu_j$ is at most $\frac{2\|g\|_\infty}{n_j} \to 0$. So $T_* \nu_j$ and $\nu_j$ have the same weak-$*$ limit, hence $T_* \nu = \nu$.

By unique ergodicity, $\nu = \mu$. But then $\int f \, d\nu_j \to \int f \, d\nu = \int f \, d\mu$, i.e., $\frac{1}{n_{j_i}}\sum_{k=0}^{n_{j_i}-1} f(T^k x_{j_i}) \to \int f \, d\mu$, contradicting ($\dagger$).

**(b) $\Rightarrow$ (c).** Trivial (uniform convergence implies pointwise convergence).

**(c) $\Rightarrow$ (a).** Suppose $\nu$ is any $T$-invariant probability measure. For any $f \in C(X)$, by (c), $\frac{1}{n}\sum_{k=0}^{n-1} f(T^k x) \to \int f \, d\mu$ for every $x$. Integrating against $\nu$ and using $T$-invariance of $\nu$:

$$\int f \, d\nu = \int \frac{1}{n}\sum_{k=0}^{n-1} f(T^k x) \, d\nu(x) \to \int \left(\int f \, d\mu\right) d\nu = \int f \, d\mu.$$

(The exchange of limit and integral is justified by dominated convergence since $|f| \leq \|f\|_\infty$.) Since $\int f \, d\nu = \int f \, d\mu$ for all $f \in C(X)$, the Riesz representation theorem gives $\nu = \mu$. $\square$


### 9.8.1 Irrational Rotations Are Uniquely Ergodic

**Theorem 9.23.** The irrational rotation $T_\alpha: x \mapsto x + \alpha \pmod{1}$ on $\mathbb{R}/\mathbb{Z}$ is uniquely ergodic, with Lebesgue measure as its unique invariant measure.

*Proof.* Let $\nu$ be any $T_\alpha$-invariant Borel probability measure on $\mathbb{R}/\mathbb{Z}$. We show $\nu$ is Lebesgue measure by computing its Fourier-Stieltjes coefficients.

For $n \in \mathbb{Z}$, define

$$\hat{\nu}(n) = \int_0^1 e^{-2\pi i n x} \, d\nu(x).$$

Since $\nu$ is $T_\alpha$-invariant, $(T_\alpha)_*\nu = \nu$, so

$$\hat{\nu}(n) = \int_0^1 e^{-2\pi i n x} \, d\nu(x) = \int_0^1 e^{-2\pi i n (x + \alpha)} \, d\nu(x) = e^{-2\pi i n \alpha} \hat{\nu}(n).$$

For $n \neq 0$, $e^{-2\pi i n \alpha} \neq 1$ (since $\alpha$ is irrational), so $\hat{\nu}(n) = 0$.

For $n = 0$, $\hat{\nu}(0) = \nu(\mathbb{R}/\mathbb{Z}) = 1$.

Since $\hat{\nu}(n) = \hat{\lambda}(n)$ for all $n$ (where $\lambda$ is Lebesgue measure: $\hat{\lambda}(0) = 1$ and $\hat{\lambda}(n) = 0$ for $n \neq 0$), we conclude $\nu = \lambda$ by the uniqueness theorem for Fourier-Stieltjes coefficients of measures on $\mathbb{R}/\mathbb{Z}$. $\square$


### 9.8.2 Weyl's Equidistribution Theorem

As a beautiful application of unique ergodicity, we obtain a classical result in number theory.

**Theorem 9.24** (Weyl's Equidistribution Theorem, 1916). If $\alpha$ is irrational, then the sequence $\{n\alpha\}_{n=0}^\infty$ (where $\{y\} = y - \lfloor y \rfloor$ denotes the fractional part) is **equidistributed modulo 1**. That is, for every interval $[a, b] \subseteq [0, 1]$:

$$\lim_{N \to \infty} \frac{1}{N} \#\{0 \leq n < N : \{n\alpha\} \in [a, b]\} = b - a.$$

*Proof.* Apply Theorem 9.22(b) to $T_\alpha(x) = x + \alpha \pmod{1}$, which is uniquely ergodic with invariant measure $\mu = \lambda$ (Lebesgue measure), and to $x_0 = 0$. For $f = \mathbf{1}_{[a,b]}$ ... but $f$ is not continuous. However, for continuous $f$, Theorem 9.22 gives

$$\frac{1}{N}\sum_{n=0}^{N-1} f(\{n\alpha\}) = \frac{1}{N}\sum_{n=0}^{N-1} f(T_\alpha^n(0)) \to \int_0^1 f(x) \, dx$$

uniformly in the starting point (and in particular for $x_0 = 0$).

To handle indicator functions, approximate $\mathbf{1}_{[a,b]}$ from above and below by continuous functions: for any $\varepsilon > 0$, there exist continuous $g_\varepsilon \leq \mathbf{1}_{[a,b]} \leq h_\varepsilon$ with $\int (h_\varepsilon - g_\varepsilon) < \varepsilon$. Then

$$\int g_\varepsilon \leq \liminf_{N} \frac{1}{N}\sum_{n=0}^{N-1} \mathbf{1}_{[a,b]}(\{n\alpha\}) \leq \limsup_N \frac{1}{N}\sum_{n=0}^{N-1} \mathbf{1}_{[a,b]}(\{n\alpha\}) \leq \int h_\varepsilon,$$

and both $\int g_\varepsilon$ and $\int h_\varepsilon$ tend to $b - a$ as $\varepsilon \to 0$. $\square$

**Remark 9.25.** Weyl originally proved this using exponential sum estimates. The ergodic-theoretic proof given here, while requiring more machinery, is arguably more conceptual: equidistribution is simply a consequence of the dynamics being uniquely ergodic.


## 9.9 Physical Interpretation and Significance

### 9.9.1 The Ergodic Hypothesis

The word "ergodic" was coined by Boltzmann (from the Greek *ergon* = work and *hodos* = path) in the context of statistical mechanics. The setup is as follows.

Consider a classical mechanical system of $N$ particles in a box. The state of the system is described by a point $x$ in a $6N$-dimensional phase space $\Gamma$ (three position coordinates and three momentum coordinates per particle). The system evolves according to Hamilton's equations, generating a flow $\phi_t: \Gamma \to \Gamma$.

Liouville's theorem (from Hamiltonian mechanics) states that this flow preserves the Lebesgue measure on $\Gamma$ (or more precisely, the measure induced by the symplectic structure). Since the total energy $H(x) = E$ is conserved, the system actually moves on the energy surface $\Sigma_E = \{x \in \Gamma : H(x) = E\}$, and the flow preserves a natural measure on $\Sigma_E$ (the microcanonical measure).

Boltzmann's ergodic hypothesis (in its modern formulation) asserts:

> *The flow $\phi_t$ on $\Sigma_E$ is ergodic with respect to the microcanonical measure.*

If this holds, then for any observable $f$ (temperature, pressure, etc.), the time average

$$\lim_{T \to \infty} \frac{1}{T} \int_0^T f(\phi_t(x)) \, dt$$

equals the ensemble average $\int_{\Sigma_E} f \, d\mu$ for a.e. initial condition $x$. This is precisely Birkhoff's theorem combined with ergodicity.

### 9.9.2 Why This Matters

The practical significance is immense:

1. **Time averages are what we measure.** An experimentalist measuring the pressure of a gas is effectively computing a time average (averaged over the measurement time, which is enormously long compared to molecular timescales).

2. **Ensemble averages are what we can compute.** Statistical mechanics gives us tools (partition functions, etc.) to compute integrals over phase space.

3. **Ergodicity bridges the gap.** If the system is ergodic, these two quantities agree, providing the theoretical foundation for statistical mechanics.

### 9.9.3 Limitations

The ergodic hypothesis, despite its foundational importance, has significant limitations:

1. **Not all systems are ergodic.** The KAM theorem (Kolmogorov-Arnold-Moser) shows that many Hamiltonian systems with few degrees of freedom are *not* ergodic: they possess invariant tori that partition phase space into invariant regions of positive measure.

2. **Ergodicity may be too slow.** Even when a system is ergodic, the convergence of time averages to space averages may be so slow as to be physically irrelevant. The system may have multiple timescales, and on observable timescales, different regions of phase space may be effectively disconnected (a phenomenon related to *metastability*).

3. **Hard systems.** Proving ergodicity for realistic physical systems is extremely difficult. The ergodicity of hard sphere gases was a major open problem for decades. Sinai proved the case of two disks on a torus (1970), and Ya. Sinai and N. Chernov, along with others, made progress on more general cases, but a complete proof for $N$ hard spheres remains incomplete for large $N$.

4. **Beyond ergodicity.** For many applications in statistical mechanics, one needs stronger properties than ergodicity — such as mixing, or quantitative estimates on rates of mixing (decay of correlations). We will explore mixing in Chapter 10.

Despite these caveats, the ergodic theorems remain cornerstones of both pure mathematics and mathematical physics. They provide the conceptual framework within which we understand the relationship between microscopic dynamics and macroscopic observables.


## 9.10 Summary

Let us collect the main ideas of this chapter.

1. **Von Neumann's theorem** establishes $L^2$-convergence of time averages to the projection onto the invariant subspace. The proof is a clean application of Hilbert space geometry.

2. **Birkhoff's theorem** establishes pointwise a.e. convergence of time averages to a $T$-invariant function $\bar{f}$, with $\int \bar{f} = \int f$. The proof uses the maximal ergodic theorem.

3. **Ergodicity** is the condition under which the invariant function $\bar{f}$ is forced to be the constant $\int f \, d\mu$. It is equivalent to: no non-trivial invariant sets, no non-constant invariant functions, and the Cesàro mixing condition.

4. We verified ergodicity for **irrational rotations** (Fourier analysis), the **doubling map** (Fourier analysis + Riemann-Lebesgue), and **Bernoulli shifts** (independence of coordinates).

5. **Unique ergodicity** is a topological strengthening: it guarantees convergence for *every* point, not just almost every point. Irrational rotations are uniquely ergodic, yielding Weyl's equidistribution theorem.

6. The physical significance: ergodicity justifies the replacement of time averages by ensemble averages, the foundational step of statistical mechanics.

In Chapter 10, we will study stronger forms of "mixing" — strong mixing and weak mixing — which refine the ergodic hierarchy and have deep connections to spectral theory.


## Exercises

**Exercise 9.1.** Let $T$ be a measure-preserving transformation on $(X, \mathcal{B}, \mu)$. Show that $T$ is ergodic if and only if: for every $f \in L^2(X, \mu)$ with $f \circ T = f$ a.e., $f$ is constant a.e. (That is, characterization (b) of Theorem 9.12 holds with $L^2$ in place of $L^1$.)

**Exercise 9.2.** Let $T_\alpha$ be an irrational rotation on $\mathbb{R}/\mathbb{Z}$. Using the ergodic theorem (not Weyl's theorem directly), prove that for any Riemann-integrable function $f: [0,1] \to \mathbb{R}$:

$$\lim_{N \to \infty} \frac{1}{N} \sum_{n=0}^{N-1} f(\{n\alpha\}) = \int_0^1 f(x) \, dx.$$

**Exercise 9.3** (Ergodicity of a product). Let $T_1: (X_1, \mu_1) \to (X_1, \mu_1)$ and $T_2: (X_2, \mu_2) \to (X_2, \mu_2)$ be ergodic measure-preserving transformations. Define $T = T_1 \times T_2: X_1 \times X_2 \to X_1 \times X_2$ by $T(x_1, x_2) = (T_1 x_1, T_2 x_2)$, preserving $\mu_1 \times \mu_2$.

(a) Show by example that $T$ need not be ergodic. (*Hint*: consider $T_1 = T_2$ = irrational rotation by $\alpha$. What invariant sets does $T_1 \times T_2$ have?)

(b) Show that if $T_1$ is ergodic and $T_2$ is weak mixing (defined as: $T_2 \times T_2$ is ergodic), then $T_1 \times T_2$ is ergodic. You may assume results about weak mixing from Chapter 10 if needed, or prove it directly.

**Exercise 9.4** (A non-ergodic system). Let $T: [0,1] \to [0,1]$ be the "tent map" restricted to $[0, 1/2]$: $T(x) = 2x$ for $x \in [0, 1/4]$ and $T(x) = 1 - 2x$ for $x \in [1/4, 1/2]$. Note $T$ maps $[0, 1/2]$ to itself, and also $[1/2, 1]$ to itself (define $T$ appropriately on $[1/2, 1]$). Show that $T$ is not ergodic with respect to Lebesgue measure on $[0,1]$.

**Exercise 9.5** (Maximal inequality and weak type bound). Using the maximal ergodic theorem, prove the following: for $f \in L^1(X, \mu)$, $T$ measure-preserving, and $\lambda > 0$:

$$\mu\left(\left\{x : \sup_{n \geq 1} \frac{1}{n}\left|\sum_{k=0}^{n-1} f(T^k x)\right| > \lambda \right\}\right) \leq \frac{3}{\lambda}\|f\|_1.$$

(*Hint*: Apply Corollary 9.7 to $f - \lambda/3$ and to $-f - \lambda/3$, then handle the region where partial sums oscillate.)

**Exercise 9.6** (Computing time averages). Let $T(x) = 2x \pmod{1}$ on $[0,1)$ with Lebesgue measure.

(a) Compute $\lim_{n \to \infty} \frac{1}{n}\sum_{k=0}^{n-1} \cos(2\pi T^k(x))$ for a.e. $x$.

(b) Compute $\lim_{n \to \infty} \frac{1}{n}\sum_{k=0}^{n-1} \mathbf{1}_{[0, 1/3)}(T^k(x))$ for a.e. $x$.

(c) For $x = 1/3$, verify your answer to (b) by directly analyzing the orbit of $1/3$ under the doubling map.

**Exercise 9.7** (Unique ergodicity and minimality). A continuous map $T: X \to X$ on a compact space is called **minimal** if every orbit is dense: $\overline{\{T^n x : n \geq 0\}} = X$ for all $x \in X$.

(a) Show that if $T$ is uniquely ergodic and $\mu$ has full support (i.e., $\mu(U) > 0$ for every nonempty open $U$), then $T$ is minimal.

(b) Give an example of a minimal homeomorphism that is not uniquely ergodic. (*This is harder — you may describe the construction without full details. See Furstenberg's example on the torus.*)

(c) Show that irrational rotations on $\mathbb{R}/\mathbb{Z}$ are minimal.

**Exercise 9.8** (Ergodicity via invariant functions — a direct approach). Let $T(x) = 2x \pmod{1}$ on $[0,1)$. Give an alternative proof of ergodicity that does not use Fourier analysis, using the following outline:

(a) Show that if $A$ is a $T$-invariant measurable set, then for every dyadic interval $I = [j/2^n, (j+1)/2^n)$, $\mu(A \cap I) = \mu(A) \cdot \mu(I)$. (*Hint*: What does $T^{-n}$ do to dyadic intervals?)

(b) Conclude that $\mu(A \cap J) = \mu(A) \cdot \mu(J)$ for every interval $J \subseteq [0,1)$.

(c) Deduce that $\mu(A) = 0$ or $1$.

**Exercise 9.9** (Convergence of ergodic averages for the doubling map). Let $T(x) = 2x \pmod 1$ and consider $f(x) = x$.

(a) Compute $\int_0^1 f \, dx$. What does the ergodic theorem predict about $\frac{1}{n}\sum_{k=0}^{n-1} T^k(x)$ for a.e. $x$?

(b) Write a careful argument (or numerical computation) to verify the prediction for $x = \sqrt{2} - 1$, at least numerically.

(c) Find a specific $x$ for which the time average does NOT converge to $\int f \, d\mu$. Why does this not contradict the ergodic theorem?


## References

- G.D. Birkhoff. "Proof of the ergodic theorem." *Proceedings of the National Academy of Sciences*, 17(12):656–660, 1931.

- J. von Neumann. "Proof of the quasi-ergodic hypothesis." *Proceedings of the National Academy of Sciences*, 18(1):70–82, 1932.

- A.M. Garsia. "A simple proof of E. Hopf's maximal ergodic theorem." *Journal of Mathematics and Mechanics*, 14(3):381–382, 1965.

- P. Walters. *An Introduction to Ergodic Theory*. Graduate Texts in Mathematics, vol. 79. Springer-Verlag, 1982.

- K. Petersen. *Ergodic Theory*. Cambridge Studies in Advanced Mathematics, vol. 2. Cambridge University Press, 1983.

- M. Einsiedler and T. Ward. *Ergodic Theory: with a view towards Number Theory*. Graduate Texts in Mathematics, vol. 259. Springer, 2011.

- P.R. Halmos. *Lectures on Ergodic Theory*. Mathematical Society of Japan, 1956. Reprinted by Chelsea, 1960.


## Recommended Reading

For a first reading of the ergodic theorems, **Walters** (Chapters 1 and 2) is clear and well-organized. **Petersen** gives a more thorough treatment with excellent motivation. For readers interested in the number-theoretic applications (Weyl's theorem and beyond), **Einsiedler and Ward** is outstanding. **Halmos** is a classic — short, elegant, and still worth reading for its clarity of exposition, though some notation is dated. For the original papers, Birkhoff (1931) and von Neumann (1932) are historically significant and surprisingly readable.

For the physical context and the ergodic hypothesis in statistical mechanics, the survey by Gallavotti and others in *Statistical Mechanics* (Springer, various editions) provides an accessible discussion, as does the treatment in Arnol'd and Avez, *Ergodic Problems of Classical Mechanics* (1968).
