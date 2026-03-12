# Answer: What Is the Empirical Track Record of Active Inference Agents?

**Question**: Do active inference agents compete with standard RL or LLM agents on practical benchmarks? How strong is the Free Energy Principle as a foundation for AI?

---

## Finding: Active Inference Remains Largely Unproven on Standard Benchmarks

The reports present Friston's Free Energy Principle (FEP) and active inference as "the most ambitious contemporary attempt to build a unified theory of adaptive behavior on explicitly cybernetic foundations." This claim deserves serious scrutiny.

### What Exists

1. **Mountain Car**: The foundational comparison paper ("Reinforcement Learning or Active Inference?", Friston et al., PLoS ONE) demonstrated that active inference can solve the mountain-car problem, reproducing policies that match RL and dynamic programming solutions. This is a toy problem.

2. **Atari (VERSES AI)**: VERSES AI claims results on the Atari 10k benchmark showing their active inference approach is "markedly better, faster, and cheaper" than RL and transformers. They started with Pong in early 2024 and expanded from there. However, these claims come from the company's blog, not peer-reviewed publications with full reproducibility details. The Atari 10k benchmark uses only 10,000 environment interactions -- a sample-efficiency test where active inference's Bayesian approach might naturally excel. Performance on the full Atari suite (57 games, standard training budgets) has not been demonstrated.

3. **DishBrain (2022)**: Friston and colleagues at Cortical Labs showed lab-grown neurons learning to play Pong, demonstrating free energy minimization in biological neurons. This is a neuroscience result, not an AI benchmark.

### What Does Not Exist

- **No comprehensive head-to-head comparisons** between active inference and state-of-the-art deep RL (PPO, SAC, TD3, DreamerV3) on standard benchmarks (full Atari-57, MuJoCo continuous control, DMControl).
- **No active inference agent competing on any LLM agent benchmark** (SWE-bench, WebArena, AgentBench).
- **No production deployment** of active inference agents in any commercial application.
- VERSES AI has been promising benchmark results since 2024; as of early 2026, comprehensive published results remain limited.

### The Falsifiability Problem

The FEP itself faces a well-documented criticism: it is widely acknowledged to be **an unfalsifiable mathematical tautology**, including by Friston himself. Key criticisms:

- Byrnes (LessWrong, 2022): "Anything that you can derive from FEP, you can derive directly from the same underlying premises... without ever mentioning FEP."
- A recent paper ("The Emperor's New Pseudo-Theory", 2025, ResearchGate) argues FEP "repackages ordinary feedback control as 'active inference'" and "interprets all outcomes -- regardless of direction -- as evidence in its favor."
- Andrews (2021, PMC): FEP is "good science and questionable philosophy," with the scope and universality claims going well beyond what the mathematics supports.
- Stegemann (Neo-Cybernetics, Medium): FEP commits "a category error by inadmissibly transferring concepts from physics and epistemology to biology."

Proponents respond that FEP is a mathematical principle (like the principle of least action in physics), not an empirical theory. Active inference -- the process theory derived from FEP -- *is* falsifiable. This distinction is valid but does not resolve the practical question: does the framework produce better agents?

### Assessment

The reports' enthusiasm for active inference as "the most promising path to cybernetics-informed AI" is **not supported by current empirical evidence**. The framework has theoretical elegance and offers natural solutions to exploration-exploitation tradeoffs, but:

1. It has not demonstrated competitive performance on standard AI benchmarks at scale.
2. The flagship company (VERSES AI) has been making claims about upcoming results for years without delivering comprehensive published comparisons.
3. The FEP foundation is criticized as unfalsifiable, meaning the framework can "explain" any result post-hoc without making useful predictions.

The reports should have been more honest about this gap between theoretical promise and empirical reality.

## Sources

- Friston, K. et al. "Reinforcement Learning or Active Inference?" PLoS ONE, 4(7), e6421. [RepEc](https://ideas.repec.org/a/plo/pone00/0006421.html)
- VERSES AI. "Mastering Atari Games with Natural Intelligence." [Blog](https://www.verses.ai/blog/mastering-atari-games-with-natural-intelligence)
- VERSES AI. "On Upcoming 2024 Benchmark Work from VERSES." [Blog](https://verses.ai/rd-blog/on-upcoming-2024-benchmark-work-from-verses)
- Byrnes, S. "Why I'm not into the Free Energy Principle." [LessWrong](https://www.lesswrong.com/posts/MArdnet7pwgALaeKs/why-i-m-not-into-the-free-energy-principle)
- "The Emperor's New Pseudo-Theory." [ResearchGate](https://www.researchgate.net/publication/390546288)
- Andrews, M. (2021). "The Free Energy Principle: Good Science and Questionable Philosophy." *Entropy*, 23(2), 238. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7922226/)
- Stegemann, W. "Why Karl Friston is wrong: Teleology is metaphysics." [Medium/Neo-Cybernetics](https://medium.com/neo-cybernetics/why-friston-is-wrong-teleology-is-metaphysics-fb9c6011c043)
