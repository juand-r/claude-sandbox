# Literature Survey: Gradient-Informed Collaborative Training

**Date:** 2026-03-03

## The Proposed Concept

Multiple models train independently on different data. At checkpoints, instead of averaging
weights or predictions, they share **gradient statistics** (gradient directions, curvature info,
Hessian-vector products) to help each other navigate the loss landscape. A model stuck in a
flat region could use gradient curvature info from another model that found a good descent
direction, without copying its weights.

This is distinct from:
- Standard data parallelism (synchronized gradient averaging every step)
- Weight averaging / model merging (FedAvg, model soups)
- Knowledge distillation (sharing soft predictions)

The key novelty is sharing **second-order or directional gradient information** between
independently-training models to inform each other's optimization trajectory.

---

## 1. Closest Existing Work

### 1.1 DiLoCo: Distributed Low-Communication Training of Language Models
**Douillard et al., 2023 (Google DeepMind)** — [arXiv:2311.08105](https://arxiv.org/abs/2311.08105)

**What they did:** Workers train independently with AdamW (inner optimizer) for ~500 steps,
then synchronize by computing "pseudo-gradients" (the difference between locally updated
weights and the original weights). These pseudo-gradients are averaged across workers and
used by an outer Nesterov momentum optimizer to update a shared reference point.

**How it relates:** DiLoCo shares something gradient-like (pseudo-gradients = accumulated
weight deltas) rather than doing raw weight averaging at every step. The outer optimizer
uses momentum over these pseudo-gradients, which captures directional information about
where each worker has been moving.

**How it differs from the proposed idea:** DiLoCo's pseudo-gradients are first-order only — they
contain no curvature information. The outer optimizer treats all workers symmetrically
(averaging). There is no mechanism for one worker's curvature information to help another
worker that is stuck. Workers share the same starting point after each sync.

**Open problems:** Communication is still O(d) per sync (full parameter dimension). No
curvature awareness in the outer optimizer. Workers cannot signal "I found a good direction"
vs. "I'm stuck" — all pseudo-gradients are treated equally.

**Extensions:** OpenDiLoCo (Jaghouar et al., 2024), DiLoCoX (2025) scaled this to billions
of parameters. SPARTA combines DiLoCo with sparse parameter sharing for further gains.

---

### 1.2 SCAFFOLD: Stochastic Controlled Averaging for Federated Learning
**Karimireddy et al., ICML 2020** — [arXiv:1910.06378](https://arxiv.org/abs/1910.06378)

**What they did:** Each client maintains a local "control variate" that tracks the difference
between its local gradient direction and the global gradient direction. During local training,
clients correct their gradient updates using these control variates, counteracting "client drift"
caused by heterogeneous data.

**How it relates:** SCAFFOLD explicitly shares gradient correction information — each client
communicates its control variate (a gradient-direction correction term) to the server. This is
a form of sharing gradient statistics beyond raw weights.

**How it differs from the proposed idea:** SCAFFOLD's corrections are first-order (gradient
direction corrections, no curvature). The goal is correcting for data heterogeneity bias,
not navigating the loss landscape. There is no Hessian or second-order information shared.
All clients aim to converge to the same global optimum, not explore different regions.

**Open problems:** SCAFFOLD removes bias from the dispersion term but not from second-order
terms of the implicit regularizer. No mechanism for one client to help another that is stuck
in a bad region.

---

### 1.3 GIANT: Globally Improved Approximate Newton Method
**Wang et al., NeurIPS 2018** — [arXiv:1709.03528](https://arxiv.org/abs/1709.03528)

**What they did:** Each worker computes a local Approximate Newton (ANT) direction using its
local Hessian and gradient. These local Newton directions are sent to a central driver and
averaged to form a "Globally Improved ANT" (GIANT) direction. The local Hessian is never
explicitly formed — Hessian-vector products via CG are used instead.

**How it relates:** GIANT is perhaps the closest existing method to the proposed idea. Workers
actually compute and share directions that incorporate local curvature information (Newton
directions = H^{-1}g). The aggregated direction benefits from diverse curvature estimates.

**How it differs from the proposed idea:** GIANT averages the Newton directions — all workers
use the same aggregated direction. There is no mechanism for selective sharing (e.g., a stuck
worker requesting curvature info from a successful one). Workers solve the same problem on
different data shards, not independently different problems. Designed for convex ERM, not
the non-convex deep learning landscape.

**Open problems:** Scaling to non-convex deep learning. Selective/adaptive sharing of curvature
info. Handling workers at very different points in parameter space.

---

### 1.4 DANE: Distributed Approximate Newton-type Method
**Shamir et al., 2014**

**What they did:** Each worker computes a local gradient correction based on the difference
between local and global gradients, and solves a local subproblem that incorporates this
correction. Can be seen as a distributed proximal point method.

**How it relates:** DANE shares gradient information (the global gradient) and uses it to correct
local optimization. Extensions (Network-DANE) adapt this to decentralized settings where
nodes share gradient estimates via consensus.

**How it differs:** First-order corrections only. All workers optimize the same objective.
No curvature sharing between workers.

**Open problems:** Communicating local Hessians is O(d^2), which is infeasible for large models.
Network-DANE and variants work around this but lose some curvature benefit.

---

### 1.5 Elastic Averaging SGD (EASGD)
**Zhang et al., NeurIPS 2015** — [arXiv:1412.6651](https://arxiv.org/abs/1412.6651)

**What they did:** Workers are coupled to a center variable by an "elastic force" (a penalty
term). Workers can explore different regions of the loss landscape — the elastic force allows
them to wander away from the center, enabling exploration of different basins of attraction.

**How it relates:** EASGD is the closest work to the "scouting" aspect of the proposed idea.
Workers explicitly explore different regions of the loss landscape, and the elastic coupling
allows information to flow back to the center. More workers = more exploration.

**How it differs from the proposed idea:** EASGD shares weights (through the elastic force
on parameters), not gradient or curvature information. There is no mechanism for a worker
that found a good basin to signal its curvature properties to others. The center variable
just averages, it does not selectively use curvature from the best workers.

**Open problems:** How to identify which worker found the best region? How to share curvature
info about discovered basins rather than just weight positions?

---

### 1.6 Distributed K-FAC
**Ba et al. / Grosse et al.** — [arXiv:1811.12019](https://ar5iv.labs.arxiv.org/html/1811.12019)

**What they did:** Distributed the computation of Kronecker-Factored Approximate Curvature
across multiple workers. Gradient workers compute gradients; stats workers compute
second-order statistics (Kronecker factors); inverse workers compute Fisher block inverses.
Key insight: curvature changes slowly, so stale curvature estimates have minimal impact.

**How it relates:** This is the primary example of distributing curvature computation across
workers. The finding that curvature is slow-changing is directly relevant — it suggests
sharing curvature info at low frequency is viable.

**How it differs from the proposed idea:** All workers train the same model on the same
objective. Curvature computation is distributed for efficiency, not for cross-pollination
between independently-training models. No concept of one model helping another navigate.

**Open problems:** Could the curvature computed by one model (on different data) be useful
for another model on different data? Under what conditions is curvature transferable?

---

### 1.7 Scalable Second-Order Optimization (Shampoo/SP-NGD)
**Gupta et al. / Pauloski et al.** — [arXiv:2002.09018](https://arxiv.org/pdf/2002.09018)

**What they did:** Shampoo uses full-matrix Kronecker-product preconditioners computed from
gradient statistics. Distributed implementations spread the preconditioner computation
across workers. SP-NGD demonstrated scaling K-FAC-style natural gradient to 1024 GPUs,
achieving 75.4% top-1 ImageNet accuracy in 5.5 minutes.

**How it relates:** Demonstrates that second-order preconditioners can be efficiently shared
in distributed settings. The preconditioner itself is derived from accumulated gradient
statistics — a form of curvature information.

**How it differs:** Same-model distributed training, not cross-model information sharing.

---

## 2. Related Concepts in Gradient Sharing and Diversity

### 2.1 Gradient Diversity
**Yin et al., AISTATS 2018** — [proceedings.mlr.press/v84/yin18a](https://proceedings.mlr.press/v84/yin18a.html)

**What they did:** Introduced a formal notion of "gradient diversity" measuring dissimilarity
between concurrent gradient updates. Showed that high gradient diversity enables larger
effective batch sizes and faster distributed training. Proved tight bounds on optimal
batch size as a function of gradient diversity. Showed DropConnect, Langevin dynamics,
and quantization are provably "diversity-inducing."

**How it relates:** Directly relevant — the proposed idea implicitly relies on gradient diversity
across workers (if all workers had identical gradients, sharing would add no information).
Understanding gradient diversity is key to knowing when curvature sharing would help.

**How it differs:** Focuses on standard data-parallel SGD with a single model. Does not
consider sharing curvature or second-order info. Analyzes diversity as a property of the
data/model, not as something to actively exploit across independent training runs.

**Open problems:** Can gradient diversity be leveraged not just for batch size scaling, but
for curvature-informed cross-model communication?

---

### 2.2 Gradient Compression and Sparsification
**Various authors, 2017-2025**

Key methods:
- **Top-k sparsification / gTop-k** (IJCAI 2019): Only communicate the largest gradient components
- **SignSGD**: Communicate only gradient signs
- **PowerSGD** (Vogels et al.): Low-rank gradient compression
- **Error feedback**: Accumulate compression error locally for future correction

**How it relates:** These methods show that gradient information can be heavily compressed
while maintaining convergence. This suggests that sharing gradient statistics between
independent models need not be expensive — even highly compressed directional info
could be useful.

**How it differs:** All designed for same-model data parallelism, not cross-model info sharing.

---

### 2.3 Local SGD / Cooperative SGD
**Koloskova et al., ICML 2020** — [arXiv:2003.10422](https://arxiv.org/abs/2003.10422)

**What they did:** Unified convergence analysis for local SGD variants: workers take multiple
local gradient steps, then synchronize via gossip or averaging. Covers changing topologies,
heterogeneous data, and partial participation.

**How it relates:** Local SGD is the paradigm within which the proposed idea would operate —
workers train locally and communicate periodically. The theoretical framework for analyzing
convergence with infrequent communication is directly applicable.

**How it differs:** Communication in local SGD is weight averaging or gradient averaging,
not curvature sharing.

---

### 2.4 SlowMo: Slow Momentum for Distributed SGD
**Wang et al., ICLR 2020 (Meta)** — [arXiv:1910.00643](https://ar5iv.labs.arxiv.org/html/1910.00643)

**What they did:** After workers perform local SGD or decentralized SGD, a "slow momentum"
update is applied at synchronization points. This momentum acts on the synchronized
model updates, smoothing them over time.

**How it relates:** The slow momentum captures temporal curvature information — it implicitly
encodes second-order dynamics (momentum approximates inverse Hessian scaling in some
settings). This is one step toward curvature-informed synchronization.

**How it differs:** Momentum is computed on the synchronized average, not shared between
independent models. No explicit Hessian or curvature sharing.

---

### 2.5 Gossip SGD / Decentralized Training
**Blot et al. (GoSGD), Daily et al. (GossipGraD)** — [arXiv:1611.09726](https://ar5iv.labs.arxiv.org/html/1611.09726)

**What they did:** Fully decentralized, asynchronous training where peers exchange model
parameters or gradients via gossip protocols. No central server. O(1) communication per
node per round.

**How it relates:** Provides the communication infrastructure for peer-to-peer information
sharing. Could be adapted to share gradient statistics instead of weights.

**How it differs:** Shares weights or raw gradients, not curvature information. All peers
train the same model.

---

## 3. Model Merging and Loss Landscape Connectivity

### 3.1 Linear Mode Connectivity
**Vlaar & Frankle, ICML 2022; Ainsworth et al. (Git Re-Basin), 2022; Wortsman et al. (Model Soups), 2022**

**What they did:** Showed that independently fine-tuned models from the same pretrained
checkpoint often lie in the same basin of the loss landscape — their weight interpolation
has no loss barrier. "Model Soups" demonstrated that averaging fine-tuned models improves
performance. Git Re-Basin showed that even independently trained models can be merged
after permutation alignment.

**How it relates:** This establishes when weight averaging works (same basin) and when it
fails (different basins). The proposed gradient-informed approach would be most valuable
precisely when models are in different basins — where weight averaging fails but curvature
information might still be transferable.

**How it differs:** These methods operate in weight space. The proposed idea operates in
gradient/curvature space, which may be more robust to models being in different basins.

**Key insight for the proposed idea:** If two models are in different basins, their gradients
and curvatures encode information about their respective basins that weight averaging
would destroy. Sharing curvature info could help a model in a bad basin learn about the
geometry of a good basin without being forced to interpolate into it.

---

### 3.2 Branch-Train-Merge (BTM)
**Li et al., NeurIPS 2022** — [arXiv:2208.03306](https://arxiv.org/abs/2208.03306)

**What they did:** Train independent "expert" language models on different data domains
(science, law, etc.) from a common seed. Merge by ensembling or averaging. Extended
by Branch-Train-MiX (BTX, 2024) which trains a MoE router on top.

**How it relates:** BTM is about independent parallel training followed by merging — the same
setting as the proposed idea. The experts train on different data and develop different
specializations.

**How it differs:** Merging is by weight averaging or ensembling, not by sharing gradient
statistics during training. No communication between experts during training at all.

**Open problems:** Could sharing curvature information during BTM training improve the
experts? Could it help them avoid redundant solutions?

---

## 4. Second-Order Optimizers (Single-Model, Relevant for Components)

### 4.1 Sophia: Second-Order Clipped Stochastic Optimization
**Liu et al., ICLR 2024** — [arXiv:2305.14342](https://arxiv.org/abs/2305.14342)

**What they did:** Uses diagonal Hessian estimates (via Hutchinson's or Gauss-Newton-Bartlett)
as a per-parameter learning rate scaler, with element-wise clipping. Achieves 2x speedup
over Adam on LLM pre-training. Only estimates the Hessian every ~10 steps.

**Relevance to proposed idea:** Sophia demonstrates that (a) diagonal Hessian is cheap to
compute (5% overhead), (b) it need not be computed every step, and (c) it dramatically
improves optimization. These three facts make Hessian sharing between models feasible —
if each model computes its diagonal Hessian every few steps anyway, sharing it with peers
is a small additional cost.

---

### 4.2 AdaHessian
**Yao et al., AAAI 2021** — [arXiv:2006.00719](https://arxiv.org/abs/2006.00719)

**What they did:** Uses Hutchinson's method to estimate the diagonal Hessian, applies
exponential moving average smoothing, and block diagonal averaging. 2x FLOPs vs SGD.

**Relevance:** Another demonstration that diagonal Hessian is practical. The EMA smoothing
of Hessian estimates is relevant — shared Hessian info from peers could be incorporated
similarly.

---

### 4.3 Recovering the Hessian from Gradients
**Anonymous, arXiv January 2026** — [arXiv:2601.18546](https://arxiv.org/html/2601.18546)

**What they did:** Showed that by adding controlled noise to targets, the gradient covariance
can be calibrated to recover the true Hessian. Demonstrated that the commonly used
"empirical Fisher" (unnormalized gradient covariance) does NOT equal the Hessian in general.

**How it relates:** Directly relevant — if models can recover Hessian information from
gradient statistics alone, then sharing gradient statistics between models is implicitly
sharing curvature information. This could be a mechanism for the proposed idea: rather
than explicitly computing and sharing Hessians, share gradient statistics from which
peers can extract curvature.

**Open problems:** Can this extraction work across models at different points in parameter
space? The calibration assumes specific noise injection — is it practical in a multi-model
setting?

---

### 4.4 Hessian-Free Optimization
**Martens, ICML 2010** — [cs.toronto.edu](https://www.cs.toronto.edu/~jmartens/docs/Deep_HessianFree.pdf)

**What they did:** Used conjugate gradient with Hessian-vector products (computed via
autodiff at gradient cost) to perform approximate Newton steps without forming the Hessian.

**Relevance:** HVP computation is O(gradient), making it practical to compute and share.
Hessian-vector products in specific directions could be the "curvature info" that models
share with each other in the proposed scheme.

---

## 5. Federated Learning with Curvature

### 5.1 DP-FedSOFIM
**2026** — [arXiv:2601.09166](https://arxiv.org/html/2601.09166)

**What they did:** Server constructs a Fisher Information Matrix from aggregated (noisy)
client gradients and uses it as a natural gradient preconditioner. Clients never compute
second-order statistics — curvature is inferred server-side from the aggregated gradients.

**How it relates:** This is a concrete example of extracting curvature from shared gradients
in a federated setting. The server acts as an intermediary that converts first-order
shared information into second-order preconditioning.

**How it differs:** Clients share raw gradients, not curvature. The curvature extraction
happens centrally, not peer-to-peer. Still aimed at same-model convergence.

---

### 5.2 FedCurv / Fisher-based Federated Methods

**What they did:** Use the Fisher information matrix to identify "important" parameters
for each client, preventing catastrophic forgetting during federated training. Parameters
with high Fisher values (high curvature) are preserved more aggressively.

**How it relates:** Uses curvature (Fisher) to guide what information is preserved across
communication rounds. Different clients contribute different curvature information based
on their local data.

**How it differs:** Curvature is used for regularization (EWC-style), not for optimization
direction guidance.

---

### 5.3 FedNova: Normalized Averaging
**Wang et al., NeurIPS 2020** — [arXiv:2007.07481](https://arxiv.org/pdf/2007.07481)

**What they did:** Clients normalize their gradient updates by the number of local steps
taken before sharing. Separates gradient direction from magnitude, fixing the "objective
inconsistency" problem in heterogeneous federated learning.

**How it relates:** FedNova explicitly manipulates gradient direction and magnitude separately,
which is a primitive form of the gradient-statistics sharing in the proposed idea.

**How it differs:** Only first-order normalization. No curvature sharing.

---

## 6. Adjacent Paradigms

### 6.1 Population Based Training (PBT)
**Jaderberg et al., 2017 (DeepMind)** — [arXiv:1711.09846](https://ar5iv.labs.arxiv.org/html/1711.09846v1)

**What they did:** Train a population of models in parallel with different hyperparameters.
Periodically, poorly-performing models copy weights from better-performing models
("exploit") and perturb their hyperparameters ("explore").

**How it relates:** PBT is about parallel models helping each other, but through weight
copying and hyperparameter exploration. The "exploit" step is the crude version of what
the proposed idea aims to achieve more surgically through curvature sharing.

**How it differs:** Copies entire weight vectors, not gradient/curvature info. No mechanism
for learning about the loss landscape geometry from peers.

---

### 6.2 Lookahead Optimizer
**Zhang et al., NeurIPS 2019** — [arXiv:1907.08610](https://arxiv.org/abs/1907.08610)

**What they did:** Maintains "fast weights" (exploring) and "slow weights" (averaging).
Fast weights take k steps of inner optimization, then slow weights interpolate toward
the fast weights. Creates an exploration-exploitation dynamic within a single model.

**How it relates:** The dual-weight system is analogous to the proposed idea's structure:
independent exploration followed by information sharing. The slow weights perform
a form of "conservative averaging" of the fast weights' exploration.

**How it differs:** Single model, single data stream. No curvature sharing. The slow
weights average positions, not gradient statistics.

**Potential connection:** Could the proposed idea be seen as a multi-model Lookahead
where instead of interpolating weights, models share curvature information from their
explorations?

---

### 6.3 Deep Mutual Learning
**Zhang et al., CVPR 2018**

**What they did:** Multiple models train simultaneously and teach each other via
KL-divergence matching of their output distributions. No pre-trained teacher needed.

**How it relates:** Collaborative training where models share information (predictions)
during training. Bidirectional, peer-to-peer.

**How it differs:** Shares predictions (output distributions), not gradient statistics.
Operates in function space, not optimization space. No curvature or Hessian involved.

---

### 6.4 Swarm Learning
**Warnat-Herresthal et al., Nature 2021**

**What they did:** Decentralized ML using blockchain coordination. No central server.
Models merge parameters via peer-to-peer protocols with elected leaders.

**How it relates:** Decentralized collaborative training infrastructure. Could be adapted
to share gradient statistics instead of parameters.

**How it differs:** Shares model parameters, not curvature information.

---

## 7. Gap Analysis: What Does NOT Exist

After thorough search, the following specific elements of the proposed idea appear to be **novel**
or at least **not well-explored**:

### 7.1 Selective Curvature Sharing Based on Optimization State
No existing method allows a model to say "I'm stuck in a flat region, send me curvature info
from someone who found a good descent direction." Current methods treat all workers
symmetrically. **Adaptive, state-dependent sharing of second-order information is an open
problem.**

### 7.2 Hessian-Vector Product Exchange Between Models at Different Points
Existing distributed second-order methods (K-FAC, GIANT, DANE) compute curvature at the
same point or nearby points. **Sharing HVPs between models at substantially different
parameter-space locations is unexplored.** It is unclear whether curvature information
transfers meaningfully across distant points in the loss landscape.

### 7.3 Curvature-Informed Model Scouting
EASGD allows workers to explore different basins, but the only information flowing back is
the parameter values. PBT copies weights from good models. **No existing method uses
curvature reports from scouts to guide other models' optimization without copying weights.**

### 7.4 Gradient Covariance as a Communication Channel
The January 2026 paper on recovering Hessians from gradient covariance opens the possibility
of sharing gradient statistics that implicitly encode curvature. **Using gradient covariance
as the communication medium between independently-training models is unexplored.**

### 7.5 Second-Order Federated Learning with Non-Identical Models
Most federated second-order methods (GIANT, FedSOFIM, FedCurv) assume all clients train
the same model architecture. **Sharing curvature information between different
architectures or models at very different training stages is completely open.**

---

## 8. Key Open Questions and Challenges

1. **Curvature transferability:** Under what conditions is Hessian/curvature information from
   one model (at point A in parameter space, trained on data D1) useful to another model
   (at point B, trained on data D2)? The answer likely depends on how similar A and B are,
   and how related D1 and D2 are.

2. **Communication cost:** Full Hessian is O(d^2), infeasible. Diagonal Hessian is O(d),
   same as gradients. HVPs in k directions is O(kd). What is the minimum curvature
   information that provides benefit?

3. **Staleness of curvature:** Distributed K-FAC showed curvature changes slowly. But does
   this hold for curvature computed by a DIFFERENT model on DIFFERENT data?

4. **Aggregation of curvature from diverse sources:** How to combine Hessian estimates from
   models that may be in different basins? Simple averaging may not make sense for
   second-order info the way it does for gradients.

5. **When to share vs. when to ignore:** A model in a good basin should probably not be
   disturbed by curvature info from a model in a bad basin. How to determine whose
   curvature is valuable?

6. **Theoretical convergence:** No convergence theory exists for methods that share
   second-order information between models at different parameter-space locations.

7. **Non-convexity:** Most distributed second-order methods have theory only for convex
   problems. Deep learning is non-convex. Curvature information in non-convex settings
   (saddle points, negative curvature) is much more complex.

---

## 9. Summary Table

| Method | Year | What is shared | First/Second order | Same model? | Explores different regions? |
|--------|------|---------------|-------------------|-------------|---------------------------|
| AllReduce SGD | - | Gradients | 1st | Yes | No |
| FedAvg | 2017 | Weights | - | Yes | No (converge to same) |
| SCAFFOLD | 2020 | Gradient corrections | 1st | Yes | No |
| DiLoCo | 2023 | Pseudo-gradients | 1st | Yes | Partially (local steps) |
| EASGD | 2015 | Weights (elastic) | - | Yes | Yes (by design) |
| GIANT | 2018 | Newton directions | 2nd | Yes | No |
| Distributed K-FAC | 2018 | Curvature factors | 2nd | Yes | No |
| SlowMo | 2020 | Momentum updates | ~1.5th | Yes | Partially |
| PBT | 2017 | Full weights (copy) | - | Same arch | Yes |
| Deep Mutual Learning | 2018 | Predictions (KL) | - | Same/diff | No |
| BTM | 2022 | Nothing during training | - | Same arch | Yes (different data) |
| **Proposed idea** | - | **Gradient stats, HVPs, curvature** | **2nd** | **Independent** | **Yes** |

---

## 10. Most Promising Building Blocks for the Proposed Idea

1. **DiLoCo's outer optimizer** — could be extended to use curvature-aware updates instead
   of Nesterov momentum on pseudo-gradients.

2. **GIANT's local Newton directions** — instead of averaging Newton directions, selectively
   share them based on optimization progress.

3. **Sophia's diagonal Hessian** — cheap (5% overhead), infrequent (every ~10 steps),
   and highly informative. Natural candidate for what to share.

4. **EASGD's exploration mechanism** — the elastic force framework could be augmented
   with curvature reports from explorers.

5. **The Hessian-from-gradients technique (2026)** — could allow implicit curvature sharing
   through gradient statistics without explicit Hessian computation.

6. **Gradient diversity theory** — provides the framework for understanding when sharing
   is beneficial (high diversity = high potential benefit).

---

## References

- Ba et al. (2018). Distributed Second-Order Optimization Using K-FAC. [arXiv:1811.12019](https://ar5iv.labs.arxiv.org/html/1811.12019)
- Blot et al. (2016). Gossip training for deep learning. [arXiv:1611.09726](https://ar5iv.labs.arxiv.org/html/1611.09726)
- Douillard et al. (2023). DiLoCo: Distributed Low-Communication Training. [arXiv:2311.08105](https://arxiv.org/abs/2311.08105)
- Jaderberg et al. (2017). Population Based Training. [arXiv:1711.09846](https://ar5iv.labs.arxiv.org/html/1711.09846v1)
- Karimireddy et al. (2020). SCAFFOLD. [arXiv:1910.06378](https://arxiv.org/abs/1910.06378)
- Koloskova et al. (2020). Unified Theory of Decentralized SGD. [arXiv:2003.10422](https://arxiv.org/abs/2003.10422)
- Li et al. (2022). Branch-Train-Merge. [arXiv:2208.03306](https://arxiv.org/abs/2208.03306)
- Liu et al. (2023). Sophia Optimizer. [arXiv:2305.14342](https://arxiv.org/abs/2305.14342)
- Martens (2010). Deep Learning via Hessian-Free Optimization. [ICML 2010](https://www.cs.toronto.edu/~jmartens/docs/Deep_HessianFree.pdf)
- Wang et al. (2018). GIANT. [arXiv:1709.03528](https://arxiv.org/abs/1709.03528)
- Wang et al. (2020). FedNova. [arXiv:2007.07481](https://arxiv.org/pdf/2007.07481)
- Wang et al. (2020). SlowMo. [arXiv:1910.00643](https://ar5iv.labs.arxiv.org/html/1910.00643)
- Warnat-Herresthal et al. (2021). Swarm Learning. [Nature](https://www.nature.com/articles/s41586-021-03583-3)
- Yao et al. (2021). AdaHessian. [arXiv:2006.00719](https://arxiv.org/abs/2006.00719)
- Yin et al. (2018). Gradient Diversity. [AISTATS](https://proceedings.mlr.press/v84/yin18a.html)
- Zhang et al. (2015). Elastic Averaging SGD. [arXiv:1412.6651](https://arxiv.org/abs/1412.6651)
- Zhang et al. (2018). Deep Mutual Learning. [CVPR 2018](https://openaccess.thecvf.com/content_cvpr_2018/papers/Zhang_Deep_Mutual_Learning_CVPR_2018_paper.pdf)
- Zhang et al. (2019). Lookahead Optimizer. [arXiv:1907.08610](https://arxiv.org/abs/1907.08610)
- Anonymous (2026). Recovering the Hessian from Gradients. [arXiv:2601.18546](https://arxiv.org/html/2601.18546)
- DP-FedSOFIM (2026). [arXiv:2601.09166](https://arxiv.org/html/2601.09166)
