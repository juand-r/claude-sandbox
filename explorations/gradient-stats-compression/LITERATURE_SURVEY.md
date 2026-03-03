# Literature Survey: Gradient Statistics as Communication Compression

**Date:** 2026-03-03

## The Proposed Idea

Instead of sending full gradients between workers in distributed training (expensive), send only
gradient statistics (norm, SNR, layer-wise distribution, variance, Hessian trace) and use them to
reconstruct an approximate gradient direction. This would be a form of extreme gradient compression
where the "compressed representation" is a set of summary statistics rather than a sparsified or
quantized version of the actual gradient vector.

---

## 1. Established Gradient Compression Methods

### 1.1 Quantization

**QSGD** (Alistarh et al., NeurIPS 2017) — [arXiv:1610.02132](https://arxiv.org/abs/1610.02132)
- Stochastically quantizes each gradient component by randomized rounding to a discrete set of
  values, preserving statistical properties (unbiased). Achieves sublinear bits per iteration.
- 1.8x faster ResNet-152 training on 16 GPUs on ImageNet.
- *Difference from proposed idea:* QSGD still transmits a (quantized) representation of every
  gradient coordinate. The proposed idea would transmit only aggregate statistics.

**TernGrad** (Wen et al., 2017)
- Quantizes gradients to {-1, 0, 1} with layer-wise scaling. Special case of QSGD with 3 levels.
- Unbiased, convergence proven under bounded gradient assumption.
- *Difference:* Still transmits one ternary value per coordinate.

**Natural Compression** (Horvath et al., AISTATS 2022) — [MLR](https://proceedings.mlr.press/v190/horvoth22a/horvoth22a.pdf)
- Randomized logarithmic rounding. Reduced training time 26% for ResNet110, 66% for AlexNet
  with no accuracy loss.
- *Difference:* Per-coordinate compression, not statistics-based.

### 1.2 Sparsification

**Deep Gradient Compression (DGC)** (Lin et al., ICLR 2018) — [arXiv:1712.01887](https://arxiv.org/abs/1712.01887)
- Finds 99.9% of gradient exchange is redundant. Only transmits gradients above a threshold.
- 270x-600x compression (ResNet-50: 97MB -> 0.35MB). Uses momentum correction, local gradient
  clipping, momentum factor masking, warm-up training.
- *Difference:* Transmits actual gradient values (the large ones). The proposed idea would not
  transmit any individual gradient values.

**Top-k Sparsification** (various)
- Each worker sends only the k largest-magnitude gradient entries. Very effective for data-parallel
  training (100x+ compression). Sorting overhead is a practical concern.
- Biased compressor, requires error feedback for convergence guarantees.

**Random-k (Rand-k) Sparsification** (Wangni et al., NeurIPS 2018)
- Randomly selects k coordinates. Unbiased but higher variance than Top-k.
- Severe performance degradation in practice compared to Top-k.

**ARC-Top-K** (2025)
- Bridges Rand-k and Top-k. All-Reduce compatible, with convergence guarantees. Reduces
  wall-clock training time by up to 60.7% versus Top-k.

### 1.3 Low-Rank Approximation

**PowerSGD** (Vogels et al., NeurIPS 2019) — [arXiv:1905.13727](https://arxiv.org/abs/1905.13727)
- Low-rank gradient compression via power iteration (subspace iteration). Avoids expensive SVD.
- Warm-starts by reusing the approximation from the previous step. Integrated into PyTorch.
- 120x+ compression. Used at scale by OpenAI (DALL-E) and others.
- *Difference:* Transmits low-rank factors (matrices P, Q where G ~ PQ^T). Still transmits
  O(rank * d) values. The proposed idea would transmit O(L) statistics where L = number of layers.

**PowerSGD+** (2025) — [arXiv:2509.11254](https://www.arxiv.org/pdf/2509.11254)
- Fixes convergence issue in PowerSGD by periodically updating projection subspace via SVD.

**GradZip** (Cho et al., NeurIPS 2019)
- Gradient compression via alternating matrix factorization.

**ATOMO** (Wang et al., NeurIPS 2018) — [arXiv:1806.04090](https://arxiv.org/abs/1806.04090)
- General framework for atomic sparsification. Works on any atomic decomposition (element-wise,
  SVD, Fourier). Given a sparsity budget, finds the minimum-variance unbiased sparsification.
- Shows SVD sparsification can outperform coordinate-wise sparsification.
- *Key insight:* The choice of decomposition basis matters for compression quality.

**GreedyLore** (2025) — [arXiv:2507.08784](https://arxiv.org/html/2507.08784)
- Greedy low-rank gradient compression with novel projector selection and integrated error feedback.
- First greedy low-rank compression with rigorous convergence guarantees.

### 1.4 Sketching-Based Methods

**Sketched SGD** (Ivkin et al., NeurIPS 2019)
- Uses Count Sketch data structures to compress gradients. Scales to 256 workers.
- Sketches are mergeable (linear), enabling efficient aggregation.

**FetchSGD** (Rothchild et al., ICML 2020) — [Semantic Scholar](https://www.semanticscholar.org/paper/06da2e6c52b9fc7abe1b421642c9385bd79b316f)
- Count Sketch for federated learning. Key insight: because Count Sketch is linear, momentum
  and error accumulation can both be done within the sketch on the server side.
- Overcomes sparse client participation challenges.
- *Relevance to proposed idea:* Sketches are a form of summary statistic. However, they still
  encode per-coordinate information (just approximately), not aggregate statistics like norms or SNR.

**Sketch-Fusion** (2023)
- Multi-layer fusion of Count Sketch compression across layers.

---

## 2. SignSGD and 1-Bit Methods

**SignSGD** (Bernstein et al., ICML 2018) — [arXiv:1802.04434](https://arxiv.org/abs/1802.04434)
- Transmits only the sign of each gradient coordinate (1 bit per parameter). 32x compression.
- Distributed version uses majority vote for aggregation.
- Convergence depends on l1/l2 geometry of gradients. Practical momentum variant (Signum)
  matches Adam on ImageNet.
- **Critical limitation:** Can fail to converge on simple convex problems. Biased compressor.
- *Relevance:* SignSGD discards magnitude information entirely, keeping only direction per
  coordinate. The proposed idea would instead discard coordinate-level information entirely,
  keeping only aggregate magnitude/distribution statistics.

**Error Feedback fixes SignSGD** (Karimireddy et al., ICML 2019) — [PDF](http://proceedings.mlr.press/v97/karimireddy19a/karimireddy19a.pdf)
- Shows EF-SGD with arbitrary compression achieves same convergence rate as SGD.
- Error feedback is now understood as essential for biased compressors.

**Flattened 1-bit SGD** (2024) — [arXiv:2405.11095](https://arxiv.org/html/2405.11095)
- Addresses SignSGD failure on sparse gradients via "flattening" technique.
- SGD-like convergence guarantees under mild conditions.

---

## 3. Statistical and Distribution-Aware Gradient Compression

### 3.1 SIDCo: Statistical Gradient Compression (CLOSEST TO PROPOSED IDEA)

**SIDCo** (Abdelmoniem et al., MLSys 2021) — [arXiv:2101.10761](https://arxiv.org/abs/2101.10761)
- **This is the most directly relevant prior work.**
- Models gradients as random variables distributed according to sparsity-inducing distributions
  (SIDs). Empirically validates this by studying statistical characteristics of gradient evolution.
- Uses the fitted distribution to efficiently estimate sparsification thresholds (instead of
  sorting, as in Top-k).
- Speeds up training by up to 41.7% over no-compression baseline.
- *Key difference from proposed idea:* SIDCo uses gradient statistics (distribution fitting)
  to make *local compression decisions* (threshold selection), not as the *compressed
  representation itself*. It still transmits actual gradient values above the threshold. The
  proposed idea would transmit only the statistics and reconstruct gradients from them.

### 3.2 Variance-Based Gradient Compression

**Variance-Based Compression** (OpenReview, 2018) — [OpenReview](https://openreview.net/forum?id=rkEfPeZRb)
- Key observation: gradient updates can be delayed until an unambiguous (high amplitude, low
  variance) gradient has been calculated. Variance can be computed with negligible cost.
- *Relevance:* Uses variance as a signal for *when* to communicate, not as the communication
  content itself.

### 3.3 Partition-Based Gradient Compression

**Partition-Based Compression** (PMC, 2021)
- Divides gradient according to its distribution characteristics. Uses information entropy of
  gradient distribution to select threshold.
- Observes gradient distribution is approximately normal.
- *Relevance:* Exploits distributional knowledge but still transmits actual gradient values.

### 3.4 Learned Gradient Compression (Inter-Node Redundancy)

**LGC** (Abrahamyan et al., IEEE TNNLS 2021) — [arXiv:2103.08870](https://arxiv.org/abs/2103.08870)
- Key insight: gradients across nodes are correlated (inter-node redundancy).
- Trains an autoencoder during early training to capture common gradient information.
- Compresses gradients using learned encoder; server reconstructs with decoder.
- *Relevance:* This is a learned compression scheme that implicitly captures gradient statistics
  in the autoencoder's latent space. The proposed idea would use explicit, interpretable
  statistics instead of learned latent representations.

---

## 4. Gradient SNR and Noise Scale

### 4.1 Gradient Noise Scale / Critical Batch Size

**McCandlish et al. (2018)** — [arXiv:1812.06162](https://arxiv.org/abs/1812.06162)
- Defines the **gradient noise scale**: B_noise = tr(Sigma) / ||G||^2
- This statistic predicts the critical batch size (largest useful batch size) across domains.
- Used in GPT-3 training (Brown et al., 2020).
- *Key relevance:* The gradient noise scale IS a summary statistic of gradient information.
  It captures the ratio of noise to signal in the gradient. However, McCandlish et al. use it
  for batch size selection, not for gradient reconstruction/communication compression.

**Critical Batch Size Revisited** (NeurIPS 2025)
- Shows gradient noise scale underestimates critical batch size by orders of magnitude for LLMs
  (OLMo 1B, 7B). Motivates batch size warmup instead.
- *Caveat for proposed idea:* If gradient noise scale is unreliable for batch size prediction,
  it may also be unreliable as a sufficient statistic for gradient reconstruction.

### 4.2 Gradient SNR for Pruning

**Dynamic Pruning via Gradient SNR** (ICLR 2021) — [Amazon Science](https://assets.amazon.science/13/93/313fb3ff48a1af7e9a2fab004811/dynamic-pruning-of-a-neural-network-via-gradient-signal-to-noise-ratio.pdf)
- Uses gradient SNR to decide which parameters to prune during training.
- SNR computed efficiently from mini-batch during backpropagation.
- *Relevance:* Uses gradient statistics for structural decisions, not communication compression.
  But demonstrates that per-parameter SNR is informative and efficiently computable.

### 4.3 GSNR for Large Batch Training

**Accelerating Large Batch Training via GSNR** (2023) — [arXiv:2309.13681](https://arxiv.org/abs/2309.13681)
- Uses gradient signal-to-noise ratio per weight to modulate learning rates.
- Weights with small GSNR get smaller learning rates (reduces generalization gap).
- Pushes BERT batch size to 128k without accuracy loss.
- *Relevance:* Demonstrates that per-parameter GSNR is a useful and actionable statistic.
  Could be part of the "rich statistics" transmitted in the proposed approach.

---

## 5. Structured / Layer-Wise Compression

### 5.1 L-GreCo (Layer-Wise Adaptive Compression)

**L-GreCo** (Markov et al., MLSys 2024) — [arXiv:2210.17357](https://arxiv.org/abs/2210.17357)
- Applies different compression ratios to different layers based on sensitivity metrics.
- Up to 2.5x training speedup and 5x compression improvement over uniform approaches.
- *Key insight:* Layers differ significantly in sensitivity to compression. This supports the
  proposed idea's inclusion of layer-wise statistics.

### 5.2 LEGACY

**LEGACY** (OpenReview, 2024) — [OpenReview](https://openreview.net/forum?id=Xxpt66OgHI)
- Adaptive compression based on layer size and training phase.
- 7-11% accuracy improvement over uniform Top-0.1% on ImageNet.

### 5.3 ACE (Adaptive Compression)

**ACE** (ScienceDirect, 2024)
- Adapts sparsification ratio to bandwidth conditions.
- Up to 9.39x training speedup.

### 5.4 Beyond Top-K: Structured Sparsification

**Column Masking for Pipeline Parallelism** (OpenReview) — [PDF](https://openreview.net/pdf?id=UyPDg7ksTM)
- Top-K is less effective for pipeline parallelism. Column-masking enables compressing both
  forward and backward passes.

---

## 6. Error Feedback / Error Compensation

**EF-SGD** (Karimireddy et al., ICML 2019) — The foundational result.
- Accumulates compression error and adds it to the next gradient before compression.
- Ensures all gradient information is eventually transmitted (with delay).
- Matches SGD convergence rate with arbitrary compression operators.

**Error Compensated SGD Can Be Accelerated** (Qian et al., NeurIPS 2021) — [OpenReview](https://openreview.net/forum?id=dSqtddFibt2)
- First to show error-compensated compression can be combined with Nesterov acceleration.
- For contraction compressors (Top-K), EC-SGD has same convergence rate as vanilla SGD.

**EC-SGD-DIANA** (2020) — [arXiv:2010.12292](https://arxiv.org/abs/2010.12292)
- Combines error feedback with quantization of gradient differences.
- Converges to exact optimum with constant learning rate.

**Error Feedback Framework** (Stich & Karimireddy, JMLR 2021)
- Unified analysis: SGD is robust to compressed and/or delayed gradient updates.
- Effects of delay/compression become negligible in presence of noise.

*Relevance to proposed idea:* Error feedback would be essential. If gradient statistics are
used to reconstruct an approximate gradient, the reconstruction error must be accumulated and
fed back. The question is whether reconstruction error from statistics-based approaches has
favorable properties for error feedback convergence.

---

## 7. Temporal / Predictive Gradient Compression

**Temporal Predictive Coding** (Edin et al., IEEE 2024) — [arXiv:2410.02478](https://arxiv.org/abs/2410.02478)
- Uses linear predictor on past gradients to predict current gradient.
- Only transmits prediction residual when its norm exceeds a threshold.
- Inspired by predictive coding in image compression.
- *Relevance:* This is conceptually adjacent to the proposed idea. Instead of transmitting
  gradient statistics, it transmits predictor coefficients. Both are forms of "meta-information"
  about the gradient rather than the gradient itself.

**Est-K (Estimated Top-K)** (2021) — [arXiv:2108.07827](https://arxiv.org/pdf/2108.07827)
- Exploits temporal correlation in momentum-SGD. Uses momentum estimator to extrapolate
  gradient from past observations. Reduces Top-K payload by ~40%.

**DIANA** (Mishchenko et al., 2019) — [arXiv:1901.09269](https://arxiv.org/abs/1901.09269)
- Compresses gradient *differences* rather than raw gradients.
- Key insight: gradient differences are typically smaller and more compressible.
- Converges to true optimum in batch mode (unlike QSGD, TernGrad, SignSGD).

---

## 8. Low-Communication / Local SGD Methods

**DiLoCo** (Douillard et al., ICML 2024) — [arXiv:2311.08105](https://arxiv.org/abs/2311.08105)
- Workers train independently for ~500 steps, then synchronize pseudo-gradients.
- 500x less communication than standard data parallelism, matching performance.
- Inner optimizer: AdamW. Outer optimizer: Nesterov momentum.
- *Relevance:* DiLoCo represents an orthogonal approach: reduce communication *frequency*
  rather than *volume per communication*. Could be combined with the proposed idea.

**SparseLoCo** (Sarfi et al., NeurIPS 2025 Workshop) — [arXiv:2508.15706](https://arxiv.org/abs/2508.15706)
- Combines DiLoCo with Top-k sparsification (1-3% density) and 2-bit quantization.
- Outperforms full-precision DiLoCo. Sparse aggregation may actually improve performance.
- *Relevance:* Shows that extreme compression of the pseudo-gradient (which is already
  infrequent) is viable. The proposed idea could be applied to DiLoCo's outer step.

**OpenDiLoCo** (Jaghouar et al., 2024)
- Trained 1B parameter model across continents. 90-95% compute utilization.

---

## 9. Second-Order / Hessian-Aware Methods

**COMPSO** (ACM PPoPP 2025) — [ACM](https://dl.acm.org/doi/10.1145/3710848.3710852)
- Optimizes gradient compression specifically for second-order optimizers.

**Compressed Lazy Hessian** (Neural Networks, 2024)
- Combines cubic Newton methods with compressed, lazily-updated Hessian information.
- Reduces Hessian communication frequency and bits per round.

**Distributed Second-Order Methods** (Islamov et al., ICML 2021) — [PDF](http://proceedings.mlr.press/v139/islamov21a/islamov21a.pdf)
- Fast convergence rates with compressed communication for Newton-type methods.

*Relevance:* These methods show that curvature information can be compressed and communicated.
The proposed idea's inclusion of Hessian trace as a statistic is supported by this line of work,
but existing methods compress the actual Hessian matrix, not just its trace.

---

## 10. Gradient Diversity and Inter-Worker Similarity

**Gradient Diversity** (Yin et al., AISTATS 2018) — [arXiv:1706.05699](https://arxiv.org/abs/1706.05699)
- Defines gradient diversity: how dissimilar concurrent gradients are across workers.
- High diversity enables better parallelism speedups. DropConnect, Langevin dynamics, and
  quantization are provably diversity-inducing.

**ScaleCom** (NeurIPS 2020)
- Exploits inter-worker gradient similarity. Local top-k indices approximate global top-k.

**SGC: Similarity-Guided Compression** (IEEE, 2024)
- Skips aggregating similar gradients, using local values instead.

*Relevance:* If workers' gradients are similar, transmitting statistics that capture this
similarity (e.g., average norm, variance across workers) could be sufficient for reconstruction.

---

## 11. Unified Frameworks and Surveys

**GRACE** (Xu et al., ICDCS 2021) — [Paper](https://sands.kaust.edu.sa/papers/grace.icdcs21.pdf) | [GitHub](https://github.com/sands-lab/grace)
- Unified framework implementing 16 compression methods on TensorFlow and PyTorch.
- Key finding: computational overhead of compression/decompression is non-trivial and may
  render some methods impractical.

**Communication Compression Techniques Survey** (J. Systems Architecture, 2023)
- Comprehensive survey covering quantization, sparsification, low-rank, and sketching.

**Balancing Communication Overhead and Accuracy** (J. Supercomputing, 2025) — [Springer](https://link.springer.com/article/10.1007/s11227-025-07451-z)
- Recent survey on pruning, quantization, sparsification, and low-rank approximation.

**TAGC** (EuroMLSys 2025) — [arXiv:2504.05638](https://arxiv.org/html/2504.05638)
- Transformer-aware gradient compression. Layer-selective compression and dynamic sparsification
  adapted for sharded models.

---

## 12. Analysis: Gap Between Existing Work and the Proposed Idea

### What exists:
1. **Compression of actual gradient values** (Top-k, quantization, low-rank, sketches) — the
   dominant paradigm. All transmit some form of the gradient itself, just lossy.
2. **Use of gradient statistics to make compression decisions** (SIDCo, L-GreCo, variance-based
   methods) — statistics inform *how* to compress, but the compressed message is still actual
   gradient values.
3. **Gradient statistics for training decisions** (GSNR for batch size, SNR for pruning) —
   statistics are computed and used locally, not transmitted.
4. **Learned compression** (LGC autoencoder) — implicitly captures statistics in latent space
   but not interpretable.
5. **Temporal predictive coding** — transmits predictor coefficients (meta-information) rather
   than gradients.

### What the proposed idea would do differently:
The proposed idea is to transmit **only** statistics like:
- Layer-wise gradient norms
- Layer-wise gradient variance
- Per-layer SNR (signal-to-noise ratio)
- Hessian trace estimates
- Gradient distribution parameters (e.g., fitted distribution shape/scale)

And then **reconstruct** an approximate gradient direction on the receiving end.

### This is novel because:
1. **No existing method transmits only aggregate statistics as the compressed representation.**
   All methods transmit some per-coordinate or per-block information.
2. The compression ratio would be extreme: O(L) or O(L * k) where L = number of layers and
   k = number of statistics per layer, versus O(d * r) for low-rank (r = rank, d = dimension)
   or O(d * s) for sparsification (s = sparsity fraction).
3. For a model with 1B parameters and 100 layers, transmitting 10 statistics per layer = 1000
   numbers. That is a 10^6 compression ratio.

### Open problems / challenges:

1. **Is gradient direction recoverable from statistics alone?** This is the fundamental question.
   A gradient norm tells you the magnitude but nothing about direction. Layer-wise norms give
   you relative magnitudes across layers but still no direction information. The critical issue
   is that direction information is inherently high-dimensional — you cannot recover a direction
   in R^d from O(1) statistics without strong priors.

2. **What priors could enable reconstruction?**
   - Temporal continuity: gradient direction changes slowly, so past directions + current
     statistics could constrain the reconstruction.
   - Distributional priors: if gradients follow known distributions (SIDCo shows they follow
     sparsity-inducing distributions), statistics could parameterize the distribution and
     allow sampling or MAP estimation.
   - Structural priors: layer-wise or block-wise structure.

3. **Error feedback with statistics-based reconstruction.** Error feedback requires storing the
   full-dimensional error vector locally. The reconstruction error from statistics-based methods
   would likely be very different in character from sparsification/quantization error. Would
   error feedback still converge?

4. **Interaction with optimization dynamics.** The gradient noise scale work (McCandlish et al.)
   shows that aggregate gradient statistics can predict useful batch sizes, but "Critical Batch
   Size Revisited" (2025) shows this breaks down for LLMs. If simple statistics fail to capture
   gradient structure at scale, the proposed approach may fail similarly.

5. **How to reconstruct direction from norm + distributional information?** One possible approach:
   - Fit per-layer gradient distributions (SIDCo-style)
   - Use fitted parameters as the communication payload
   - Receiver samples from the distribution or uses MAP estimate
   - This is essentially a generative model of gradients parameterized by summary statistics
   - But this would produce independent samples for each coordinate, destroying correlations.

6. **Combining with existing approaches.** The most practical path may be a hybrid:
   - Use statistics to reconstruct a coarse gradient direction
   - Use error feedback to correct over time
   - Possibly combine with very sparse actual gradient values (e.g., top-100 entries + statistics)

7. **Theoretical convergence.** No existing convergence theory covers the case where the
   communicated information is aggregate statistics rather than a (biased or unbiased) estimator
   of the gradient. New theory would be needed.

---

## 13. Summary Table: Existing Methods vs. Proposed Approach

| Method | What is transmitted | Compression ratio | Preserves direction? | Unbiased? |
|--------|-------------------|-------------------|---------------------|-----------|
| Full gradient | All coordinates | 1x | Yes | N/A |
| QSGD | Quantized coordinates | ~8-32x | Approximately | Yes |
| TernGrad | Ternary coordinates | ~16x | Approximately | Yes |
| SignSGD | Sign per coordinate | 32x | Per-coordinate | No |
| Top-k | k largest entries | 100-1000x | Partially | No |
| DGC | Entries above threshold | 270-600x | Partially | No |
| PowerSGD | Low-rank factors | ~120x | Approximately | No |
| Count Sketch | Sketch data structure | ~10-100x | Approximately | Yes |
| DiLoCo | Full pseudo-gradient (infrequent) | 500x (temporal) | Yes | N/A |
| SparseLoCo | Sparse+quantized pseudo-grad | 500x * 50x | Partially | No |
| **Proposed** | **Statistics (norm, SNR, etc.)** | **~10^5-10^6x** | **Must reconstruct** | **Unclear** |

---

## 14. Most Relevant Prior Work (Ranked by Relevance)

1. **SIDCo** — Uses gradient distribution statistics, but for threshold estimation, not as
   the transmitted representation.
2. **Temporal Predictive Coding** — Transmits meta-information (predictor coefficients) rather
   than gradients. Conceptually closest to transmitting "statistics."
3. **LGC (Learned Gradient Compression)** — Uses learned representation (autoencoder latent)
   which implicitly captures statistics. But not interpretable.
4. **Gradient Noise Scale (McCandlish)** — Defines and uses a key gradient statistic (tr(Sigma)/||G||^2)
   for training decisions. Shows statistics are informative.
5. **GSNR for Large Batch Training** — Per-parameter SNR used to modulate optimization.
6. **L-GreCo** — Layer-wise adaptive compression using sensitivity metrics. Shows layer-level
   statistics are useful.
7. **ATOMO** — Framework for choosing optimal decomposition basis. Suggests that the right
   "representation" matters more than the compression ratio.
8. **Error Feedback (Karimireddy et al.)** — Essential mechanism for any biased compression,
   including statistics-based reconstruction.
9. **DiLoCo / SparseLoCo** — Shows extreme communication reduction is possible; could be
   combined with statistics-based compression.
10. **DIANA** — Compressing gradient differences; shows that what you compress (raw vs. difference)
    matters for convergence.

---

## 15. Conclusion and Open Research Directions

The proposed idea of using gradient statistics as the compressed representation is, to the best
of this survey's findings, **novel in its pure form**. No existing method transmits *only*
aggregate statistics and reconstructs gradients from them.

However, the literature strongly suggests several things:

**Supportive evidence:**
- Gradient statistics (norm, variance, SNR, distribution shape) are demonstrably informative
  and efficiently computable (SIDCo, GSNR, McCandlish).
- Layer-wise structure is important and useful for compression decisions (L-GreCo, LEGACY).
- Temporal predictive approaches show that "meta-information" can substitute for raw gradients
  to some degree.
- Error feedback can rescue biased/lossy compression schemes.
- Inter-worker gradient similarity exists and can be exploited.

**Challenging evidence:**
- No existing theory suggests that O(L) statistics can recover a direction in R^d (d >> L).
  This is an information-theoretic barrier.
- The gradient noise scale (the most studied gradient statistic) was recently shown to be
  unreliable for LLMs (Critical Batch Size Revisited, 2025).
- All successful compression methods transmit at least some per-coordinate or per-block
  information. The jump to pure statistics is very large.

**Most promising hybrid approach:**
A practical version might combine:
1. Layer-wise gradient statistics (norms, variance) as a "header"
2. Very sparse actual gradient values (e.g., top-0.01%)
3. Temporal prediction to fill in the rest
4. Error feedback for convergence guarantees

This would be a spectrum between existing methods and the pure statistics-based approach,
allowing empirical investigation of how much the statistics contribute beyond sparsified values.
