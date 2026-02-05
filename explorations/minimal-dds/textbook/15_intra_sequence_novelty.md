# Chapter 15: Measuring Novelty Within a Sequence

## 15.1 Introduction

The preceding chapters have focused on dynamics *across time*: how states evolve under iteration, how orbits converge to attractors, how entropy rates characterize the information produced per step. But there is another dimension of novelty that has received less formal attention: **novelty within a single output**.

When an LLM generates a response, that response is itself a sequence of $N$ tokens. Before we ask "how does the $n$-th output differ from the $(n-1)$-th output?" we can ask: "how diverse is the $n$-th output internally?" A sequence that repeats "the the the the" $N/2$ times is grammatically valid but informationally impoverished. A sequence with high internal diversity explores more of the vocabulary and exhibits richer structure.

This chapter develops the theory of **intra-sequence novelty**: metrics that quantify diversity, complexity, and information content within a single finite sequence. We connect these measures to the complexity theory of Chapters 8--10 and to the LLM dynamics of Chapter 14, showing how intra-sequence novelty provides a complementary perspective on the quality-diversity trade-off in generative systems.

---

## 15.2 The Setting

### 15.2.1 Finite Sequences

Let $\Sigma$ be a finite alphabet with $|\Sigma| = V$. A **finite sequence** (or **string**) of length $N$ is an element $w = (w_1, w_2, \ldots, w_N) \in \Sigma^N$. We write $|w| = N$ for the length.

In the LLM context, $\Sigma$ is the token vocabulary (typically $V \approx 32{,}000$ to $128{,}000$), and $w$ is a single generated response.

**Definition 15.1 (Empirical distribution).** Given $w \in \Sigma^N$, the **empirical distribution** (or **type**) of $w$ is the probability distribution $\hat{p}_w$ on $\Sigma$ defined by

$$\hat{p}_w(s) = \frac{|\{i : w_i = s\}|}{N}$$

for each $s \in \Sigma$. This is the relative frequency of symbol $s$ in $w$.

### 15.2.2 Two Notions of Novelty

We distinguish two related but distinct concepts:

1. **Lexical diversity**: How many distinct symbols appear, and how evenly are they distributed? This is captured by type-token ratios and entropy measures.

2. **Structural complexity**: How much internal structure does the sequence have? A sequence of $N$ distinct symbols has high lexical diversity but may have trivial structure (e.g., the alphabet in order). Compression-based measures capture structural complexity.

Both contribute to what we intuitively call "novelty" or "interestingness" of a sequence.

---

## 15.3 Type-Token Measures

### 15.3.1 Type-Token Ratio

The simplest diversity measure counts distinct symbols.

**Definition 15.2 (Type-Token Ratio).** The **type-token ratio** (TTR) of $w \in \Sigma^N$ is

$$\mathrm{TTR}(w) = \frac{|\{w_i : 1 \leq i \leq N\}|}{N} = \frac{\text{number of distinct symbols}}{\text{total symbols}}.$$

**Example 15.3.** Let $\Sigma = \{a, b, c, d\}$ and consider:
- $w_1 = abcdabcd$ (length 8, 4 distinct): $\mathrm{TTR}(w_1) = 4/8 = 0.5$
- $w_2 = aaaaaaaa$ (length 8, 1 distinct): $\mathrm{TTR}(w_2) = 1/8 = 0.125$
- $w_3 = abcdefgh$ over $\Sigma' = \{a,\ldots,h\}$ (length 8, 8 distinct): $\mathrm{TTR}(w_3) = 1.0$

### 15.3.2 The Length Dependence Problem

**Proposition 15.4 (Heaps' Law).** For natural language text, the number of distinct words $V(N)$ in a corpus of $N$ words follows approximately

$$V(N) \approx K \cdot N^\beta,$$

where $K > 0$ and $0 < \beta < 1$ (typically $\beta \approx 0.4$--$0.6$).

*Consequence.* The TTR decreases with sequence length:

$$\mathrm{TTR}(N) = \frac{V(N)}{N} \approx K \cdot N^{\beta - 1} \to 0 \text{ as } N \to \infty.$$

This means TTR is not comparable across sequences of different lengths: a 1000-token sequence will almost always have lower TTR than a 100-token sequence, regardless of their relative diversity.

### 15.3.3 Length-Normalized Variants

To address the length dependence, several normalizations have been proposed:

**Definition 15.5 (Normalized TTR variants).**

1. **Root TTR**: $\mathrm{RTTR}(w) = \dfrac{|\text{types}|}{\sqrt{N}}$

2. **Log TTR**: $\mathrm{LogTTR}(w) = \dfrac{\log|\text{types}|}{\log N}$

3. **Moving-Average TTR (MATTR)**: Fix a window size $k$. Compute TTR for each window of $k$ consecutive tokens. MATTR is the average:
$$\mathrm{MATTR}_k(w) = \frac{1}{N-k+1} \sum_{i=1}^{N-k+1} \mathrm{TTR}(w_i, \ldots, w_{i+k-1}).$$

**Proposition 15.6.** Under Heaps' Law with exponent $\beta$:
- $\mathrm{RTTR}(N) \approx K \cdot N^{\beta - 0.5}$, which still decreases if $\beta < 0.5$.
- $\mathrm{LogTTR}(N) \approx \beta + \frac{\log K}{\log N} \to \beta$ as $N \to \infty$.

Thus LogTTR converges to a constant (the Heaps exponent), making it more suitable for cross-length comparison.

### 15.3.4 Hapax Legomena

**Definition 15.7 (Hapax ratio).** The **hapax legomena** of $w$ are the symbols that appear exactly once. The **hapax ratio** is

$$\mathrm{Hapax}(w) = \frac{|\{s \in \Sigma : |\{i : w_i = s\}| = 1\}|}{N}.$$

A high hapax ratio indicates the sequence is exploring vocabulary rather than reusing a small set of symbols.

---

## 15.4 N-gram Diversity Measures

### 15.4.1 Distinct-n

Token-level measures ignore sequential structure. N-gram measures capture local patterns.

**Definition 15.8 (N-grams and Distinct-n).** For $w \in \Sigma^N$ and $n \geq 1$, the **$n$-grams** of $w$ are the tuples

$$\mathcal{N}_n(w) = \{(w_i, w_{i+1}, \ldots, w_{i+n-1}) : 1 \leq i \leq N - n + 1\}.$$

The **Distinct-n** score is

$$\mathrm{Distinct\text{-}n}(w) = \frac{|\{\text{unique } n\text{-grams}\}|}{|\mathcal{N}_n(w)|} = \frac{|\mathrm{set}(\mathcal{N}_n(w))|}{N - n + 1}.$$

**Example 15.9.** Let $w = abcabcabc$ (length 9).
- $n = 1$: 9 unigrams, 3 unique $\{a, b, c\}$. Distinct-1 $= 3/9 = 0.333$.
- $n = 2$: 8 bigrams $(ab, bc, ca, ab, bc, ca, ab, bc)$, 3 unique. Distinct-2 $= 3/8 = 0.375$.
- $n = 3$: 7 trigrams, 3 unique $(abc, bca, cab)$. Distinct-3 $= 3/7 = 0.429$.

**Remark.** Distinct-n increases with $n$ when the sequence has short repeated patterns but no long repeated patterns. For a sequence with no repeated $n$-grams (maximal diversity), Distinct-n $= 1$.

### 15.4.2 Repetition Rate

**Definition 15.10 (Rep-n).** The **repetition rate at order $n$** is the complement of Distinct-n:

$$\mathrm{Rep\text{-}n}(w) = 1 - \mathrm{Distinct\text{-}n}(w) = \frac{\text{number of repeated } n\text{-grams}}{N - n + 1}.$$

**Theorem 15.11 (Welleck et al., 2020).** In human-written text (e.g., Wikitext-103), sentence-level repetition is rare: Rep-4 $\approx 0.5\%$. In LLM-generated text with greedy or beam-search decoding, Rep-4 can exceed $50\%$, indicating severe degeneration.

This dramatic gap motivates Distinct-n as a diagnostic for text quality.

### 15.4.3 Self-BLEU

**Definition 15.12 (Self-BLEU).** Given a corpus of $M$ generated sequences $\{w^{(1)}, \ldots, w^{(M)}\}$, the **Self-BLEU** score is the average BLEU score of each sequence against the others:

$$\mathrm{Self\text{-}BLEU} = \frac{1}{M} \sum_{i=1}^{M} \mathrm{BLEU}(w^{(i)}, \{w^{(j)} : j \neq i\}).$$

High Self-BLEU indicates the generated sequences are similar to each other (low corpus-level diversity).

**Adaptation to single sequences.** For a single long sequence $w$, partition it into $M$ segments of length $L$: $w = w^{(1)} \| w^{(2)} \| \cdots \| w^{(M)}$. Compute Self-BLEU across segments. High intra-sequence Self-BLEU indicates the sequence repeats itself.

---

## 15.5 Entropy-Based Measures

### 15.5.1 Empirical Entropy

**Definition 15.13 (Unigram entropy).** The **(empirical) unigram entropy** of $w \in \Sigma^N$ is the Shannon entropy of its empirical distribution:

$$H_1(w) = -\sum_{s \in \Sigma} \hat{p}_w(s) \log_2 \hat{p}_w(s),$$

where $0 \log 0 := 0$.

**Proposition 15.14 (Entropy bounds).**
1. $H_1(w) = 0$ if and only if $w$ consists of a single repeated symbol.
2. $H_1(w) \leq \log_2 |\mathrm{supp}(\hat{p}_w)| \leq \log_2 \min(N, V)$.
3. Equality in (2) holds if and only if $\hat{p}_w$ is uniform over its support.

*Proof.* Standard properties of Shannon entropy. $\square$

**Example 15.15.** For $w = abcabcabc$ (9 tokens, each of $a, b, c$ appears 3 times):

$$H_1(w) = -3 \cdot \frac{3}{9} \log_2 \frac{3}{9} = -3 \cdot \frac{1}{3} \log_2 \frac{1}{3} = \log_2 3 \approx 1.585 \text{ bits}.$$

This is the maximum possible for 3 symbols (uniform distribution).

### 15.5.2 Higher-Order Empirical Entropy

**Definition 15.16 (Empirical $n$-gram entropy).** Define the empirical distribution over $n$-grams:

$$\hat{p}_w^{(n)}(g) = \frac{|\{i : (w_i, \ldots, w_{i+n-1}) = g\}|}{N - n + 1}$$

for $g \in \Sigma^n$. The **empirical $n$-gram entropy** is

$$H_n(w) = -\sum_{g \in \Sigma^n} \hat{p}_w^{(n)}(g) \log_2 \hat{p}_w^{(n)}(g).$$

**Proposition 15.17 (Entropy rate estimate).** For large $N$, the **empirical entropy rate** is approximated by

$$h(w) \approx H_n(w) - H_{n-1}(w),$$

the conditional entropy of the $n$-th symbol given the previous $n-1$. This estimates the per-symbol information content.

### 15.5.3 Perplexity

**Definition 15.18 (Empirical perplexity).** The **perplexity** of the empirical unigram distribution is

$$\mathrm{PPL}_1(w) = 2^{H_1(w)}.$$

More generally, $\mathrm{PPL}_n(w) = 2^{H_n(w)/(n)}$ is the per-symbol perplexity at order $n$.

**Interpretation.** Perplexity is the effective vocabulary size: a sequence with perplexity $k$ is "as diverse as" a sequence drawn uniformly from $k$ symbols.

**Example 15.19.** For the uniform distribution over 3 symbols: $H_1 = \log_2 3$, so $\mathrm{PPL}_1 = 3$. For a degenerate sequence of one repeated symbol: $H_1 = 0$, so $\mathrm{PPL}_1 = 1$.

---

## 15.6 Compression-Based Measures

### 15.6.1 Connection to Kolmogorov Complexity

Chapter 8 introduced Kolmogorov complexity $K(w)$: the length of the shortest program that outputs $w$. While $K(w)$ is uncomputable, practical compression algorithms provide upper bounds.

**Proposition 15.20.** For any compressor $C$ (gzip, LZ77, etc.):

$$K(w) \leq |C(w)| + O(1),$$

where $|C(w)|$ is the length of the compressed representation and the $O(1)$ term accounts for the decompressor.

### 15.6.2 Compression Ratio

**Definition 15.21 (Compression ratio).** The **compression ratio** of $w$ under compressor $C$ is

$$\rho_C(w) = \frac{|C(w)|}{|w|}.$$

- $\rho_C(w) \approx 1$: The sequence is incompressible (high complexity, possibly random).
- $\rho_C(w) \ll 1$: The sequence is highly compressible (low complexity, repetitive).

**Proposition 15.22.** For a sequence of $N$ i.i.d. symbols from distribution $p$:

$$\mathbb{E}[\rho_C(w)] \to H(p) / \log_2 |\Sigma| \text{ as } N \to \infty,$$

where $H(p)$ is the entropy of $p$. Optimal compression achieves the entropy rate.

### 15.6.3 Lempel-Ziv Complexity

**Definition 15.23 (LZ complexity).** The **Lempel-Ziv complexity** $c_{LZ}(w)$ is the number of distinct substrings in the LZ76 parsing of $w$: the sequence is parsed left-to-right, and at each step, the longest prefix that has appeared before is identified; the new phrase is that prefix plus one new symbol.

**Example 15.24.** Let $w = abcabcabc$.
- Parse: $a \cdot b \cdot c \cdot ab \cdot ca \cdot bc$ (6 phrases).
- $c_{LZ}(w) = 6$.

For comparison, $w' = aaaaaaaaa$ parses as $a \cdot aa \cdot aaa \cdot aaa$ (or similar), with $c_{LZ}(w') \approx O(\sqrt{N})$.

**Theorem 15.25 (Lempel-Ziv theorem).** For a stationary ergodic source with entropy rate $h$:

$$\frac{c_{LZ}(w) \log N}{N} \to h \text{ almost surely as } N \to \infty.$$

Thus normalized LZ complexity converges to the entropy rate.

### 15.6.4 Normalized Compression Distance

**Definition 15.26 (NCD).** For two sequences $w_1, w_2$ and compressor $C$, the **normalized compression distance** is

$$\mathrm{NCD}(w_1, w_2) = \frac{|C(w_1 \| w_2)| - \min(|C(w_1)|, |C(w_2)|)}{\max(|C(w_1)|, |C(w_2)|)}.$$

This measures similarity: $\mathrm{NCD} \approx 0$ if $w_1, w_2$ share much structure; $\mathrm{NCD} \approx 1$ if they are unrelated.

**Application.** To measure self-similarity within a sequence $w$, split it into halves $w = w_1 \| w_2$ and compute $\mathrm{NCD}(w_1, w_2)$. Low NCD indicates the two halves are similar (internal repetition).

---

## 15.7 The Quality-Diversity Frontier

### 15.7.1 The Trade-off

High intra-sequence novelty is not intrinsically desirable. Consider two extremes:

1. **Random sequence**: Draw each $w_i$ uniformly from $\Sigma$. This achieves $\mathrm{TTR} \approx 1$ (for $N \ll V$), $H_1 \approx \log_2 V$, and $\rho_C \approx 1$. But the sequence is meaningless noise.

2. **Deterministic repetition**: $w = ssss\ldots$ for some $s \in \Sigma$. This achieves $\mathrm{TTR} = 1/N \to 0$, $H_1 = 0$, $\rho_C \to 0$. The sequence is predictable and boring.

Neither extreme is desirable for language generation. The goal is to achieve high diversity **subject to coherence constraints**.

### 15.7.2 Pareto Optimality

**Definition 15.27 (Quality-diversity Pareto frontier).** Let $Q(w)$ be a quality measure (e.g., fluency, coherence, task performance) and $D(w)$ a diversity measure (e.g., Distinct-2, entropy). A sequence $w^*$ is **Pareto optimal** if there is no $w$ with $Q(w) \geq Q(w^*)$ and $D(w) \geq D(w^*)$ with at least one strict inequality.

The set of Pareto optimal sequences forms a **frontier** in $(Q, D)$ space. Different decoding strategies (greedy, beam search, nucleus sampling) trace different points on or below this frontier.

**Theorem 15.28 (Holtzman et al., 2020, informal).** Nucleus (top-$p$) sampling achieves a better quality-diversity trade-off than beam search or pure sampling. Specifically:
- Beam search maximizes $Q$ but achieves low $D$ (degeneration).
- Pure sampling achieves high $D$ but low $Q$ (incoherence).
- Nucleus sampling with appropriate $p$ approximates the Pareto frontier.

### 15.7.3 Entropy Bounds in Human Text

**Observation 15.29 (Holtzman et al., 2020).** Human-written text maintains entropy within a "Goldilocks zone": neither too high (incoherent) nor too low (repetitive). Empirically, the per-token entropy of human text lies in a narrow band across domains and styles.

LLM-generated text that violates these bounds---either by entropy collapse (repetition) or entropy explosion (incoherence)---is perceived as low quality.

---

## 15.8 Connection to Logical Depth

### 15.8.1 Review of Logical Depth

Chapter 9 introduced Bennett's **logical depth**: the computational time required to produce a string from its shortest description. Intuitively:

- **Shallow strings**: Either simple (short description, fast to compute) or random (long description, fast to "compute" by just listing).
- **Deep strings**: Require significant computation to produce, even from the shortest description. They are "neither simple nor random."

### 15.8.2 Depth as Structured Novelty

**Proposition 15.30 (Informal).** A sequence with high intra-sequence novelty (high entropy, low compression) can be either:
1. **Random**: High Kolmogorov complexity, low logical depth.
2. **Structured-complex**: Moderate Kolmogorov complexity, high logical depth.

True "creativity" or "interestingness" corresponds to case (2): the sequence is neither trivially compressible nor trivially generated.

**Example 15.31.** Consider:
- $w_1 = $ a random bit string of length 1000. High entropy, high $K$, but depth $\approx 0$ (just output the bits).
- $w_2 = $ the first 1000 digits of $\pi$. Moderate entropy, low $K$ (short program: "compute $\pi$"), but high depth (computing $\pi$ takes time).
- $w_3 = $ "0000...0" (1000 zeros). Low entropy, low $K$, low depth.

Logical depth distinguishes $w_1$ (random, shallow) from $w_2$ (structured, deep).

### 15.8.3 Implications for LLM Outputs

A high-quality LLM output should have:
- Moderate-to-high entropy (not degenerate).
- Moderate Kolmogorov complexity (not incompressible noise).
- High logical depth (structured, meaningful).

Current intra-sequence novelty metrics (TTR, Distinct-n, compression ratio) capture the first two but not the third. Developing practical proxies for logical depth in generated text remains an open problem.

---

## 15.9 Connection to Computational Mechanics

### 15.9.1 Epsilon-Machines and Statistical Complexity

Chapter 10 introduced the **epsilon-machine**: the minimal deterministic automaton that generates a stationary process with the same statistical structure as the observed data. The **statistical complexity** $C_\mu$ is the entropy of the epsilon-machine's state distribution.

### 15.9.2 Statistical Complexity of a Finite Sequence

For a finite sequence $w$, we can estimate statistical complexity by:

1. Inferring an epsilon-machine from $w$ (e.g., via the CSSR algorithm).
2. Computing the entropy of the inferred causal states.

**Definition 15.32 (Empirical statistical complexity).** Let $\hat{\epsilon}(w)$ be an epsilon-machine inferred from $w$, with causal state distribution $\hat{\pi}$. The **empirical statistical complexity** is

$$\hat{C}_\mu(w) = H(\hat{\pi}).$$

### 15.9.3 Excess Entropy

**Definition 15.33 (Excess entropy).** The **excess entropy** (or **predictive information**) of a process is

$$E = I(W_{\text{past}}; W_{\text{future}}) = \lim_{L \to \infty} [H(W_1^L) - L \cdot h],$$

where $h$ is the entropy rate. For a finite sequence, this is estimated by:

$$\hat{E}(w) = H_L(w) - L \cdot \hat{h}(w),$$

where $H_L$ is the block entropy and $\hat{h}$ is the estimated entropy rate.

**Interpretation.** Excess entropy measures the total amount of structure in the process---how much knowing the past helps predict the future, beyond the per-symbol entropy rate. High excess entropy indicates long-range correlations and complex structure.

### 15.9.4 Complexity vs. Entropy

**Proposition 15.34.** For finite sequences:
- **Random sequences**: High entropy rate $h$, low statistical complexity $C_\mu$, low excess entropy $E$.
- **Periodic sequences**: Low $h$, low $C_\mu$, low $E$.
- **Complex structured sequences**: Moderate $h$, high $C_\mu$, high $E$.

This echoes the logical depth distinction: complex sequences are neither too ordered nor too random.

---

## 15.10 Practical Metrics for LLM Evaluation

### 15.10.1 Standard Metrics

Based on the theoretical framework, we recommend the following metrics for evaluating intra-sequence novelty in LLM outputs:

| Metric | Formula | Measures | Range |
|--------|---------|----------|-------|
| Distinct-1 | unique unigrams / total | Vocabulary diversity | [0, 1] |
| Distinct-2 | unique bigrams / total | Local pattern diversity | [0, 1] |
| Distinct-4 | unique 4-grams / total | Phrase-level diversity | [0, 1] |
| Rep-4 | 1 - Distinct-4 | Repetition rate | [0, 1] |
| $H_1$ | Unigram entropy | Information content | [0, log V] |
| $\rho_{\text{gzip}}$ | Compression ratio | Structural complexity | (0, 1+] |

### 15.10.2 Implementation

```python
import math
import gzip
from collections import Counter
from typing import List

def distinct_n(tokens: List[str], n: int) -> float:
    """Compute Distinct-n score."""
    if len(tokens) < n:
        return 0.0
    ngrams = [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    return len(set(ngrams)) / len(ngrams)

def unigram_entropy(tokens: List[str]) -> float:
    """Compute empirical unigram entropy in bits."""
    counts = Counter(tokens)
    total = len(tokens)
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def compression_ratio(text: str) -> float:
    """Compute gzip compression ratio."""
    original = text.encode('utf-8')
    compressed = gzip.compress(original)
    return len(compressed) / len(original)

def lz_complexity(tokens: List[str]) -> int:
    """Compute Lempel-Ziv complexity (number of phrases)."""
    seen = set()
    complexity = 0
    current = []
    for token in tokens:
        current.append(token)
        current_tuple = tuple(current)
        if current_tuple not in seen:
            seen.add(current_tuple)
            complexity += 1
            current = []
    if current:  # Handle remaining tokens
        complexity += 1
    return complexity

def novelty_report(tokens: List[str]) -> dict:
    """Compute comprehensive novelty metrics."""
    text = ' '.join(tokens)
    return {
        'length': len(tokens),
        'vocab_size': len(set(tokens)),
        'ttr': len(set(tokens)) / len(tokens),
        'distinct_1': distinct_n(tokens, 1),
        'distinct_2': distinct_n(tokens, 2),
        'distinct_4': distinct_n(tokens, 4),
        'rep_4': 1 - distinct_n(tokens, 4),
        'entropy_h1': unigram_entropy(tokens),
        'perplexity': 2 ** unigram_entropy(tokens),
        'compression_ratio': compression_ratio(text),
        'lz_complexity': lz_complexity(tokens),
    }
```

### 15.10.3 Interpreting the Metrics

**Guidelines for LLM-generated text:**

1. **Distinct-2 < 0.5**: Likely degenerate (excessive repetition).
2. **Distinct-2 > 0.9**: Possibly incoherent or enumeration-like.
3. **Rep-4 > 10%**: Significant phrase repetition; investigate.
4. **Compression ratio < 0.3**: Highly repetitive structure.
5. **Compression ratio > 0.8**: Little structure; possibly random or very diverse.

Human text typically achieves Distinct-2 $\approx 0.8$--$0.95$ and compression ratio $\approx 0.3$--$0.5$.

---

## 15.11 Connection to Model Collapse

### 15.11.1 Intra-Sequence Novelty During Collapse

Chapter 14 (Section 14.5) described **model collapse**: when models are trained on their own outputs, diversity progressively decreases. This manifests in intra-sequence metrics:

**Proposition 15.35 (Novelty decay under collapse).** Let $M_n$ be the model at generation $n$ in a self-consuming loop. As $n$ increases:
1. $\mathrm{Distinct\text{-}k}(M_n) \to 0$ for $k \geq 2$.
2. $H_1(M_n) \to 0$.
3. $\rho_C(M_n) \to 0$.

The outputs converge to repetitive, low-entropy sequences.

### 15.11.2 Diversity as Collapse Diagnostic

Monitoring intra-sequence novelty provides early warning of model collapse:

- Track Distinct-2 and $H_1$ across training generations.
- Significant drops indicate onset of collapse.
- Intervention (fresh data injection) can be triggered when metrics fall below thresholds.

---

## 15.12 Open Questions

**Question 15.36 (Practical depth estimation).** Can we develop efficient estimators for logical depth or depth-like quantities that distinguish "structured complex" from "random" sequences in LLM outputs?

**Question 15.37 (Novelty vs. coherence).** Is there a formal relationship between intra-sequence novelty and inter-sequence coherence (e.g., in a conversation)? Can high intra-sequence diversity compensate for low inter-sequence diversity, or vice versa?

**Question 15.38 (Optimal decoding).** Given a quality function $Q$ and a diversity function $D$, what decoding strategy achieves the Pareto frontier? Can this be characterized analytically for simple models?

**Question 15.39 (Multi-scale novelty).** Novelty can be measured at multiple scales: token, phrase, sentence, paragraph, document. How do these scales interact? Can a document have high paragraph-level diversity but low sentence-level diversity?

**Question 15.40 (Semantic vs. lexical).** Our metrics are largely lexical. How can we measure **semantic novelty**---diversity in meaning rather than surface form? Embedding-based metrics (e.g., variance of sentence embeddings) are one approach, but their relationship to information-theoretic quantities is unclear.

---

## 15.13 Summary

| Concept | Metric | Captures |
|---------|--------|----------|
| Vocabulary exploration | TTR, Hapax ratio | Number of distinct symbols |
| Local pattern diversity | Distinct-n | Uniqueness of n-grams |
| Repetition | Rep-n, Self-BLEU | Degree of self-copying |
| Information content | Entropy $H_1$, $H_n$ | Bits per symbol |
| Structural complexity | Compression ratio, LZ complexity | Non-random patterns |
| Long-range structure | Statistical complexity, Excess entropy | Memory in the process |
| "Interestingness" | Logical depth (theoretical) | Computation required to generate |

Intra-sequence novelty complements the dynamical systems perspective of earlier chapters. Where Chapters 1--14 ask "how does the system evolve over time?", this chapter asks "how rich is each individual state?" Together, they provide a comprehensive framework for analyzing the outputs of generative systems.

The key insight is that novelty alone is insufficient: random sequences have maximum novelty but zero value. The goal is **structured novelty**---high diversity within the constraints of coherence, grammar, and meaning. This is the "creative zone" between order and chaos, the edge where interesting computation happens.

---

## References

- Bennett, C. H. (1988). Logical depth and physical complexity. In *The Universal Turing Machine: A Half-Century Survey*, pp. 227--257. Oxford University Press.

- Crutchfield, J. P. and Young, K. (1989). Inferring statistical complexity. *Physical Review Letters*, 63(2):105--108.

- Heaps, H. S. (1978). *Information Retrieval: Computational and Theoretical Aspects*. Academic Press.

- Holtzman, A., Buys, J., Du, L., Forbes, M., and Choi, Y. (2020). The curious case of neural text degeneration. In *ICLR 2020*.

- Li, J., Galley, M., Brockett, C., Gao, J., and Dolan, B. (2016). A diversity-promoting objective function for neural conversation models. In *NAACL-HLT 2016*.

- Lempel, A. and Ziv, J. (1976). On the complexity of finite sequences. *IEEE Transactions on Information Theory*, 22(1):75--81.

- Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3):379--423.

- Shumailov, I., et al. (2024). The curse of recursion: Training on generated data makes models forget. *arXiv preprint* arXiv:2305.17493.

- Welleck, S., Kulikov, I., Roller, S., Dinan, E., Cho, K., and Weston, J. (2020). Neural text generation with unlikelihood training. In *ICLR 2020*.

- Ziv, J. and Lempel, A. (1977). A universal algorithm for sequential data compression. *IEEE Transactions on Information Theory*, 23(3):337--343.

---

## Exercises

**Exercise 15.1.** Compute Distinct-1, Distinct-2, and $H_1$ for the following sequences over $\Sigma = \{a, b, c\}$:
(a) $w_1 = abcabcabcabc$
(b) $w_2 = aaaaaaaaaaaa$
(c) $w_3 = abcbcacabacb$

**Exercise 15.2.** Prove that for any sequence $w$ of length $N$ over alphabet $\Sigma$:
$$\mathrm{Distinct\text{-}1}(w) = \mathrm{TTR}(w).$$

**Exercise 15.3.** Show that if $w$ is a periodic sequence with period $p$ (i.e., $w_i = w_{i+p}$ for all $i$), then for $n \leq p$:
$$\mathrm{Distinct\text{-}n}(w) \leq \frac{p}{N - n + 1}.$$

**Exercise 15.4.** The **Rényi entropy** of order $\alpha$ is defined as:
$$H_\alpha(w) = \frac{1}{1-\alpha} \log_2 \sum_{s \in \Sigma} \hat{p}_w(s)^\alpha.$$
Show that $\lim_{\alpha \to 1} H_\alpha(w) = H_1(w)$ (Shannon entropy).

**Exercise 15.5.** Implement the `novelty_report` function and compute metrics for:
(a) A paragraph from a news article.
(b) The same paragraph repeated 5 times.
(c) 100 tokens sampled uniformly from English words.
Compare and interpret the results.

**Exercise 15.6.** (Research) Find an LLM-generated text that has high Distinct-2 but low human-judged quality. What other metrics might detect this failure mode?
