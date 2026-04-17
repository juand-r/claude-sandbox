# Student Notes on Chapter 8: "Probabilistic Grammars and Tightness"

## Overall impression

Excellent chapter. The parallel between Booth-Thompson (PCFGs) and Du et al.
(autoregressive LMs) is well-drawn. The branching-process interpretation of
the first-moment matrix is clear. The "Examples on Both Sides" section
provides concrete intuition.

---

## Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | MEDIUM | Lines 87-91 | Non-tight RNN example: "hidden state $h_t \in \mathbb{R}$ evolves by a one-dimensional ReLU map, with EOS probability $p(\EOS \mid h_t) = 1/(e^{h_t} + 1)$" — the sigmoid function $1/(e^x+1)$ is actually $\sigma(-x)$, not the standard sigmoid $\sigma(x) = 1/(1+e^{-x})$. This is still a valid function (it's the "reverse sigmoid"), but it means EOS probability DECREASES as $h_t$ grows, which is the point. Might be worth a clarifying word. |
| 2 | LOW | Line 112 | "Cotterell et al. [CotterellEtAl2023] situate these definitions..." — this is a survey/tutorial citation, fine as a pointer. |
| 3 | LOW | Chapter | No exercises. |

## Summary

Mathematically sound. The tightness theorem for softmax Transformers (lines
94-102) is well-argued. The $\varepsilon$ lower bound argument is clear and
the connection to the branching-process framework is properly drawn.
