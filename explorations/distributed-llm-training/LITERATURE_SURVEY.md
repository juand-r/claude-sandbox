# Literature Survey: Gradient-Informed Collaborative Training & Gradient Statistics as Communication Compression

## The Two Ideas

### Idea 1: Gradient-Informed Collaborative Training
N models train independently on different data. At checkpoints, instead of averaging weights or predictions, they share *gradient statistics* (directions, curvature info, Hessian-vector products) to help each other navigate the loss landscape. A model stuck in a flat region could use curvature info from a model that found a good descent direction, without copying its weights.

### Idea 2: Gradient Statistics as Communication Compression
Instead of sending full gradients between workers (expensive), send only gradient statistics (norm, SNR, layer-wise distribution, variance) and use them to reconstruct an approximate gradient direction.

---

## Related Work

### A. Gradient Diversity & Distributed SGD

**Gradient Diversity (Yin et al., 2018, AISTATS)**
- Introduced a measure of dissimilarity between concurrent gradient updates
- Showed that high gradient diversity enables better mini-batch SGD scaling
- Key insight: diverse gradients across workers = more information per communication round
- **Difference from our idea:** They measure diversity but don't use it to *guide* other workers. It's an analytical tool, not a training signal.
- https://arxiv.org/abs/1706.05699

**Cooperative SGD (Wang & Joshi, 2021, JMLR)**
- Unified framework subsuming Local SGD, EASGD, decentralized parallel SGD
- Workers do local updates, periodically synchronize via weight averaging
- **Difference from our idea:** Synchronization is via weight/model averaging, not gradient statistics sharing. Workers don't inform each other about promising directions.
- https://jmlr.org/papers/volume22/20-147/20-147.pdf

### B. Distributed Second-Order Methods

**Distributed Approximated Hessian (Arnold & Wang, 2017)**
- Compute rank-m approximation of inverse Hessian using differences in gradients/parameters across workers
- Distributed Newton-Raphson method
- **Difference from our idea:** They use gradient differences to approximate a global Hessian. Our idea is about one worker's curvature info helping *another* worker that's in a different part of the landscape. They assume workers are near each other; we don't.
- https://arxiv.org/abs/1709.05069

**Distributed K-FAC / Scalable Shampoo (Anil et al., 2020)**
- Kronecker-factored approximate curvature for distributed training
- Dedicated workers for computing curvature statistics
- Significant wall-time speedups over first-order methods
- **Difference from our idea:** K-FAC/Shampoo compute curvature for a single model's optimization. Not about sharing curvature between independent models in different landscape regions.
- https://arxiv.org/abs/2002.09018

**SHED: Federated Learning with Hessian Eigenvector Sharing (2023)**
- Newton-type algorithm for federated learning
- Clients share incremental Hessian eigendecompositions
- Achieves super-linear convergence
- **Closest to our idea for Idea 1.** Shares second-order info between workers. But assumes workers optimize the same objective on different data partitions (standard FL), not independent models scouting different landscape regions.
- https://www.sciencedirect.com/science/article/pii/S0005109823006271

**HessFormer (2025)**
- First framework for distributed stochastic Lanczos quadrature on large Transformers
- Enables computing full Hessian spectrum for >7B parameter models
- Infrastructure contribution: makes distributed Hessian computation practical
- **Relevant as enabling technology:** if we want to share curvature info, we need to compute it efficiently.
- https://arxiv.org/abs/2505.11564

**AdaHessian + EASGD**
- Second-order optimizer using Hutchinson's method for diagonal Hessian approximation
- Combined with elastic averaging for distributed training
- Argument: second-order methods reduce communication rounds (fewer but better steps)
- **Difference:** Uses curvature to improve each worker's own updates, not to share landscape info between workers.

### C. Gradient Compression

**Deep Gradient Compression (Lin et al., 2017)**
- 99.9% of gradient exchange is redundant
- 270x-600x compression via top-k sparsification + momentum correction + error feedback
- **Difference from Idea 2:** DGC compresses the actual gradient values. Our idea is to send statistics *about* the gradient (norm, SNR, layer distribution) as a compressed representation. DGC preserves direction; statistics-based compression would reconstruct an approximate direction from summary stats.
- https://arxiv.org/abs/1712.01887

**SIDCo: Statistical-based Gradient Compression (Abdelmoniem et al., 2021)**
- Models gradients as random variables with sparsity-inducing distributions (SIDs)
- Uses statistical properties to derive compression thresholds
- **Closest to Idea 2.** They use statistical characterization of gradients for compression. But they still send selected gradient values (sparsified), not the statistics themselves as a reconstruction basis.
- https://arxiv.org/abs/2101.10761

**SignSGD (Bernstein et al., 2018)**
- Extreme compression: send only gradient signs (1 bit per parameter)
- Works with majority vote across workers
- **Relation to Idea 2:** Can be seen as sending one specific statistic (sign) instead of full gradients. Our idea generalizes this: what if you send richer statistics (norm, SNR, per-layer info) that allow better reconstruction?

**GComp: Near-Lossless Gradient Compression (2024)**
- Uses statistical characteristics of gradients for near-lossless compression
- https://dl.acm.org/doi/10.1145/3698038.3698541

### D. Curvature-Aware Model Merging

**CAMEx: Curvature-Aware Merging of Experts (2025)**
- Merges expert models using Fisher Information to account for parameter space geometry
- **Relevant connection:** Instead of merging weights in Euclidean space, uses curvature to determine which parameters matter. Could inform our idea: when combining info from different workers, weight by curvature importance.
- https://arxiv.org/abs/2502.18821

### E. Population-Based Training

**PBT (Jaderberg et al., 2017, DeepMind)**
- Multiple workers train with different hyperparameters
- Periodically copy weights from best performers, mutate hyperparameters
- **Difference:** PBT copies weights wholesale. Our idea shares gradient/curvature information without copying weights. PBT changes hyperparameters; we propose changing optimization direction.

### F. Loss Landscape Connectivity

**FedVG: Gradient-Guided Aggregation (2025)**
- Uses gradient analysis to evaluate client updates during local training
- Aggregation weights based on how beneficial updates are to the global model
- **Relevant:** Uses gradient statistics to decide how to combine worker contributions, not just averaging. Closest in spirit to using gradient info for informed collaboration.

---

## What's Novel in Our Ideas

### Idea 1: Gradient-Informed Collaborative Training
**What exists:**
- Sharing weights/model averages (Local SGD, FedAvg, PBT)
- Sharing gradient values (data parallelism, gradient compression)
- Sharing curvature info for the *same* optimization (K-FAC, SHED)

**What doesn't exist (the gap):**
- Using one model's curvature/gradient direction info to help *another model in a different landscape region*
- The "scouting" metaphor: model A explores region X, finds a promising direction via Hessian-vector products, communicates this to model B which is stuck in region Y
- Key assumption that differs: models are NOT near each other in parameter space. Standard distributed methods assume workers are optimizing the same model or nearby copies. Our idea is about heterogeneous landscape exploration.

**Open problems:**
1. How to make gradient/curvature information from one landscape region useful in another? Gradient directions are local — a good direction at point A may be meaningless at point B.
2. What's the right representation to communicate? Full Hessian eigenvectors? Top-k curvature directions? Gradient SNR?
3. When is this better than just running independent models and picking the best? (Our rank stability analysis suggests it may not help when configs are well-separated.)
4. Does this help more in rugged landscapes (e.g., RL) than smooth ones (e.g., supervised LM training)?

### Idea 2: Gradient Statistics as Communication Compression
**What exists:**
- Sparsification (top-k, random-k)
- Quantization (1-bit SignSGD, ternary quantization)
- Statistical modeling for compression thresholds (SIDCo)
- Low-rank approximation

**What doesn't exist (the gap):**
- Using a *rich set* of gradient statistics (norm, SNR, per-layer norms, variance, Hessian trace) as the compressed representation itself
- Reconstructing approximate gradient direction from these summary statistics rather than from sparsified/quantized gradient values
- The statistics we already compute (38 features) as a natural compression vocabulary

**Open problems:**
1. Can you actually reconstruct a useful gradient direction from summary statistics? The information loss may be too severe — knowing the norm and per-layer distribution doesn't tell you *which* parameters to update.
2. What's the theoretical compression ratio vs. convergence tradeoff?
3. Could this work as a "meta-gradient" — not reconstructing the exact gradient but inferring the right *type* of update from statistics?

---

## Assessment

**Idea 1** is more novel and has a clearer gap in the literature. The closest work (SHED, FedVG) shares second-order info between workers, but always assumes workers are optimizing the same objective near each other. The scouting/exploration angle — models in different landscape regions helping each other — appears genuinely unexplored.

**Idea 2** is less promising upon reflection. The gradient compression literature is mature and the fundamental challenge (you need to know which parameters to update, not just aggregate statistics) may be a dealbreaker. Existing methods (top-k + error feedback) are already extremely effective (600x compression). Hard to see how statistics-only would compete.

**Recommendation:** Focus on Idea 1. The open question is whether gradient/curvature information transfers meaningfully between different landscape regions. This is testable with our existing infrastructure.
