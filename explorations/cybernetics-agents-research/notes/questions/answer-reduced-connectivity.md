# Answer: Has Ashby's "Reduced Connectivity Improves Adaptation" Been Validated?

**Question**: Ashby claimed that reduced internal connectivity improves adaptation. Does modern neural network research support or contradict this?

---

## Finding: Partially Vindicated, But the Story Is Complex

### Ashby's Original Claim

In *Design for a Brain*, Ashby showed that a "multistable" brain with barriers between subsystems adapts more efficiently than a richly interconnected one. The argument: full connectivity means a disturbance in one subsystem destabilizes all others, forcing the entire system to re-adapt. Reduced connectivity isolates subsystems, allowing them to adapt independently.

### Modern Evidence: Sparse Networks

There is a substantial and growing body of research showing that **sparse neural networks can match or approach the performance of dense networks** while being dramatically more efficient:

1. **Scalable Training with Adaptive Sparse Connectivity** (Mocanu et al., Nature Communications, 2018): Replacing fully-connected layers with sparse ones before training reduced parameters quadratically with "no decrease in accuracy." Networks designed as sparse scale-free graphs achieved comparable performance with far fewer connections.

2. **Lottery Ticket Hypothesis** (Frankle & Carlin, ICLR 2019): Dense networks contain sparse subnetworks that, when trained in isolation, match the full network's performance. This suggests that most connections are not needed.

3. **Network Pruning**: Compression of RL networks in Atari environments shows that up to 95% of parameters can be pruned without significant quality loss, leading to 80x size reductions (Nature Scientific Reports, 2025).

4. **Biological Parallels**: Mammalian brains exhibit both sparse activity (only a small fraction of neurons active at any time) and sparse connectivity (each neuron connected to a limited number of others). This is consistent with Ashby's argument.

5. **Generalization benefits**: LeCun et al. (1990) observed that sparse connectivity improves generalization in convolutional neural networks. This is explained by bias-variance tradeoff: constraining degrees of freedom reduces overfitting.

### Mixture of Experts: Modularity at Scale

The most striking modern vindication of Ashby's principle is the **Mixture of Experts (MoE)** architecture:

- MoE networks contain thousands of expert sub-networks, but only a small subset (typically 1-2) is activated for any given input.
- This represents "conditional computation" -- the network is modular by design, with experts specializing in different domains.
- DeepSeek-V3 (2024) demonstrated that MoE with fine-grained experts could match frontier dense models at a fraction of training cost.
- Meta's NLLB project found experts naturally aligned with language families -- spontaneous specialization through reduced cross-expert connectivity.
- The sparsely-gated MoE (Shazeer et al., 2017) achieved "greater than 1000x improvements in model capacity with only minor losses in computational efficiency."

This is precisely Ashby's insight: by creating barriers between subsystems (experts), each subsystem can specialize and adapt more efficiently than a fully interconnected system.

### Where the Analogy Gets Complicated

1. **Transformers are densely connected**: The dominant architecture in modern AI (transformers) uses dense attention mechanisms where every token can attend to every other token. This rich connectivity is central to their success. Ashby would predict this should impede adaptation -- and in some sense it does (transformers are expensive and require massive data).

2. **Dense pretraining, sparse deployment**: The emerging pattern is to train dense models and then sparsify them, or to use MoE to achieve effective sparsity. This is more nuanced than "reduced connectivity is always better."

3. **Recurrent networks**: Analysis of sparse recurrent neural networks shows they evolve toward "structurally balanced configurations" during sparsification -- universal structural patterns emerge (Nature Communications Physics, 2023). This supports Ashby's intuition about self-organization in modular systems.

### Assessment

Ashby's insight is **substantially vindicated** by modern research, though the mechanism is more nuanced than he could have anticipated:

- Sparse networks can match dense ones while being far more efficient.
- MoE architectures are essentially Ashby's "multistable systems" at scale -- modular, specialized subsystems with limited cross-connectivity.
- The Lottery Ticket Hypothesis suggests dense networks contain effective sparse subnetworks.
- However, dense connectivity during training may still be valuable even if the final system is sparse.

The reports are right to highlight this as an important cybernetic insight, but they should connect it more explicitly to the MoE literature, which provides the strongest modern evidence.

## Sources

- Mocanu, D. et al. (2018). "Scalable Training of Artificial Neural Networks with Adaptive Sparse Connectivity." *Nature Communications*. [Nature](https://www.nature.com/articles/s41467-018-04316-3)
- Shazeer, N. et al. (2017). "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer." [arXiv:1701.06538](https://arxiv.org/abs/1701.06538)
- Universal Structural Patterns in Sparse RNNs (2023). *Communications Physics*. [Nature](https://www.nature.com/articles/s42005-023-01364-0)
- "Sparse Activity and Sparse Connectivity in Supervised Learning." JMLR 14. [PDF](https://www.jmlr.org/papers/volume14/thom13a/thom13a.pdf)
- Neural network compression for RL (2025). *Scientific Reports*. [Nature](https://www.nature.com/articles/s41598-025-93955-w)
- MoE in LLMs survey (2025). [arXiv:2507.11181](https://arxiv.org/html/2507.11181v1)
