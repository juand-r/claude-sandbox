# Cutting-Edge Artificial Life Systems (2020-2026)

A concise research survey of recent developments in ALife.

---

## 1. Flow Lenia - Continuous ALife with Mass Conservation

Flow Lenia (Plantec et al., 2023; Best Paper, ALIFE 2023) extends the Lenia continuous cellular automaton family by adding a mass conservation constraint. In standard Lenia, spatially localized patterns (SLPs) are fragile -- perturbations can cause them to vanish, and each creature requires specific global update rules, preventing multi-species coexistence. Flow Lenia solves both problems: mass conservation makes creatures intrinsically robust (they cannot simply dissipate), and parameter localization embeds update-rule parameters into the CA state itself, so different "species" with different local rules can cohabit one simulation. This also enables environmental features like food consumption -- creatures must eat to avoid mass decay. An extended journal version appeared in *Artificial Life* (MIT Press, 2025). The key practical insight is that conservation laws dramatically simplify the search for interesting patterns, removing the need to explicitly optimize for spatial localization.

**Refs:** [Flow Lenia (arXiv 2212.07906)](https://arxiv.org/abs/2212.07906) | [MIT Press journal version](https://direct.mit.edu/artl/article/31/2/228/130572/Flow-Lenia-Emergent-Evolutionary-Dynamics-in-Mass) | [Project site](https://sites.google.com/view/flowlenia/)

---

## 2. ASAL (Sakana AI) - Foundation Models for ALife Discovery

ASAL -- Automated Search for Artificial Life (Kumar, Lu, Kirsch, Tang, Stanley, Isola, Ha; Dec 2024) is the first system to use vision-language foundation models (e.g., CLIP) to automatically discover ALife simulations. It operates in three modes: (1) supervised target search (find simulations matching text prompts), (2) open-endedness search (maximize temporal novelty in FM embedding space), and (3) illumination search (discover a diverse archive of distinct simulations). ASAL works across multiple substrates -- Boids, Particle Life, Game of Life, Lenia, and Neural Cellular Automata -- without substrate-specific engineering. A notable contribution is "Particle Life++," an extended Particle Life where particle colors change dynamically, enabling combinatorial explosion in interaction dynamics and open-ended ecosystem formation. The broader significance is methodological: FMs provide a human-aligned metric space for evaluating "interestingness," replacing ad-hoc fitness functions.

**Refs:** [ASAL paper (arXiv 2412.17799)](https://arxiv.org/abs/2412.17799) | [Sakana AI blog](https://sakana.ai/asal/) | [GitHub](https://github.com/SakanaAI/asal)

---

## 3. Particle-Based ALife - Recent Systems

Three developments stand out. First, **Particle Lenia** (Google Research) bridges Lenia and particle systems by reformulating continuous CA dynamics as interactions between point particles with an energy-based formulation; it scales naturally to 3D and produces diverse emergent behaviors even with uniform parameters. Second, **ALIEN** (Artificial LIfe ENvironment, v4.0-5.0) is a CUDA-powered 2D particle engine simulating millions of particles in real-time with SPH fluid dynamics, neural-network-orchestrated cell functions (sensors, muscles, constructors), genomes, and self-replication; its "Emerging Ecosystems" video won the Virtual Creatures Competition 2024. Third, the ASAL work introduced **Particle Life++** as mentioned above, extending the popular Particle Life model with dynamic color-changing rules. The overall trend is toward GPU-accelerated, large-scale particle simulations with richer per-particle state (neural controllers, genomes) rather than simple attraction/repulsion rules.

**Refs:** [Particle Lenia (Google Research)](https://google-research.github.io/self-organising-systems/particle-lenia/) | [ALIEN project](https://www.alien-project.org/) | [ALIEN GitHub](https://github.com/chrxh/alien)

---

## 4. Neural Cellular Automata - Recent Developments

Since the foundational "Growing Neural Cellular Automata" (Mordvintsev et al., 2020, Distill), NCA research has expanded rapidly. Key 2024-2025 developments include: **Scaling** -- NCAs have been limited to ~128x128 grids due to quadratic memory/time scaling; a 2025 paper pairs NCA with implicit neural decoders to generate full-HD output in real time while preserving self-organizing properties. **Conditional morphogenesis** (Dec 2024) -- class-conditional vectors injected into the perception loop guide development from a single pixel through symmetry breaking to refined target shapes, achieving 96.3% digit recognition accuracy. **ARC-AGI reasoning** (2025) -- NCAs with hidden memory states ("Engram-NCA") are applied to the ARC-AGI abstract reasoning benchmark, connecting morphogenesis to general intelligence. **Multi-texture synthesis** (2025, Scientific Reports) -- a single compact NCA generates multiple textures via internal genomic signals. A comprehensive review (Hartl et al., Sept 2025, arXiv) surveys NCA applications to biology, bioengineering, and drug discovery. The frontier is hybrid NCA-diffusion architectures and universal NCAs capable of simulating arbitrary CA rules.

**Refs:** [Growing NCA (Distill 2020)](https://distill.pub/2020/growing-ca/) | [NCA review (arXiv 2509.11131)](https://arxiv.org/abs/2509.11131) | [NCA for ARC-AGI](https://arxiv.org/html/2506.15746) | [Conditional NCA (arXiv 2512.08360)](https://www.arxiv.org/pdf/2512.08360)

---

## 5. Computational Mechanics (Crutchfield) - Detecting Emergent Computation

Crutchfield's computational mechanics framework, centered on epsilon-machines (minimal predictive models of stochastic processes), remains the primary rigorous tool for detecting emergent computation in CAs. The most significant recent development building on this framework is Rosas et al. (Feb 2024), "Software in the Natural World," which combines epsilon-machine theory with automata theory to characterize emergent macroscopic computation -- defining informational, causal, and computational closure as three levels of emergence (featured in Quanta Magazine, June 2024). Grassberger (Jan 2024, revised Nov 2025) published a critical analysis of recent Jurgens & Crutchfield papers on mixed-state epsilon-machines, clarifying connections to the forward algorithm and proposing alternative complexity measures. While no major new Crutchfield-authored papers on CA-specific computational mechanics appeared in 2023-2025, the framework is increasingly adopted by the broader emergence/complexity community as the standard formalism for asking "is this system computing?"

**Refs:** [Software in the Natural World (arXiv 2402.09090)](https://arxiv.org/abs/2402.09090) | [Quanta article](https://www.quantamagazine.org/the-new-math-of-how-large-scale-order-emerges-20240610/) | [Grassberger critique (arXiv 2401.03279)](https://arxiv.org/abs/2401.03279) | [Crutchfield publications](https://csc.ucdavis.edu/~cmg/compmech/pubs.htm)

---

## 6. Key Open Problems and State of the Field (2024-2025)

The *Artificial Life* journal published a **Special Issue on Open-Ended Evolution** (Vol 30, Issue 3, 2024), the field's central unsolved problem: no artificial system yet exhibits indefinitely increasing complexity and adaptive novelty comparable to biological evolution. Bedau et al.'s 14 grand challenges (2000) remain largely open -- especially the origin-of-life transition, open-ended evolution, and the life-mind relationship. Current active fronts include: (1) formalizing and measuring open-endedness (no consensus on metrics), (2) bridging ALife and foundation models (ASAL being the first major result), (3) scaling simulations while preserving emergence (GPU acceleration enabling millions of particles but unclear if scale alone yields qualitative novelty), (4) connecting ALife to origin-of-life chemistry and synthetic biology, and (5) ethics of increasingly lifelike systems. ALIFE 2024 (Copenhagen, theme: "Exploring New Frontiers") and ALIFE 2025 (Kyoto, theme: "Ciphers of Life") reflect the field's shift toward information-theoretic and FM-augmented approaches. The journal's impact factor (1.5) and h5-index (18) indicate a small but active community.

**Refs:** [OEE Special Issue](https://direct.mit.edu/artl/article/30/3/300/123431/Editorial-Introduction-to-the-2024-Special-Issue) | [ALIFE 2025](https://2025.alife.org/) | [Artificial Life journal](https://direct.mit.edu/artl)

---

## 7. Practical Lessons - Compute, Grid Sizes, Rule Complexity

**Grid sizes:** Most Lenia/NCA research uses 128x128 to 256x256 grids. Scaling beyond this hits quadratic memory costs for grid-based CAs. The Blazor Lenia implementation supports 24x24 to 128x128 on CPU; serious research uses GPU. ALIEN simulates millions of particles via CUDA but requires NVIDIA compute capability 6.0+.

**Compute:** Lenia's bottleneck is large-kernel convolutions -- FFT-based GPU implementations (cuLenia) are essential for grids above ~128x128. Half-precision (FP16) roughly doubles throughput vs FP32 with acceptable quality. NCA training is expensive due to long unrolled trajectories; inference is cheap. ASAL requires FM inference (CLIP) in the optimization loop, adding significant cost per evaluation.

**Rule complexity:** Lenia uses ~130 parameters per species and produces rich behavior. Flow Lenia adds mass-conservation constraints but similar parameter counts. NCA update rules are small neural networks (typically a few thousand parameters per cell, shared). ALIEN uses 100+ configurable simulation parameters. The recurring lesson is that modest rule complexity (hundreds of parameters, not millions) suffices for rich emergence -- the key ingredients are conservation laws, local interaction with global consequences, and sufficient simulation scale/time.

**Practical recommendations:** Start with 128x128 grids on GPU for Lenia/NCA experiments. Use FFT convolutions. For particle systems, budget for 10K-1M particles with CUDA. Expect hours of GPU time for NCA training, minutes for Lenia pattern search, days for ASAL-style FM-guided exploration across substrates.

**Refs:** [cuLenia paper](https://hal.science/hal-05005838v1/file/speeding-up-lenia-a-comparative-study-between-cuda-and-existing-implementations.pdf) | [Lenia GitHub](https://github.com/Chakazul/Lenia) | [ALIEN GitHub](https://github.com/chrxh/alien)

---

*Report compiled 2026-03-23. Sources verified via web search.*
