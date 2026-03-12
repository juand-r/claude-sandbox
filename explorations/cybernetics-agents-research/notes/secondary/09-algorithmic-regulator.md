# The Algorithmic Regulator

## Citation
Ruffini, G. (2025). "The Algorithmic Regulator." arXiv:2510.10300. Also published in *Entropy*, 28(3), 257.

## Summary

Reformulates the Good Regulator Theorem using Algorithmic Information Theory (AIT / Kolmogorov complexity). The original Conant-Ashby theorem is proven only in limited settings; this paper extends it into a quantitative, distribution-free claim applicable to individual sequences, not just stochastic ensembles. Connects to the Free Energy Principle and predictive brain theories.

## Key Arguments

1. **AIT reformulation.** Replaces Shannon information (statistical, ensemble-based) with Kolmogorov complexity (algorithmic, individual-sequence). This makes the Good Regulator Theorem applicable without assuming linearity, stochastic models, or specific architectures.

2. **Quantitative and testable.** The reformulation turns "every good regulator must be a model of its system" from a qualitative slogan into a quantitative claim about the algorithmic complexity of regulators relative to their regulated systems.

3. **Distribution-free.** Works for individual sequences, not just probability distributions — important for real-world AI systems operating on specific inputs rather than statistical ensembles.

4. **Connects to FEP.** The paper bridges the Good Regulator Theorem to the Free Energy Principle, showing both are about the same fundamental constraint: effective regulation requires internal models that compress environmental regularities.

## Connection to Our Research

- **Formalizing the cybernetics-AI bridge.** This paper provides the mathematical machinery to connect Ashby/Conant's qualitative cybernetic insight to information-theoretic analysis of AI agents. If an LLM agent is a "good regulator" of its task environment, it must encode a compressed model of that environment — and we can quantify how good that model is.
- **Kolmogorov complexity and LLMs.** There's a natural connection: LLMs are essentially compression algorithms (predicting next tokens = compressing text). The Algorithmic Regulator framing suggests that an LLM's regulatory capacity is bounded by its compression quality.
- **Beyond statistical guarantees.** Most ML theory operates on statistical (ensemble) guarantees. The AIT approach provides guarantees for individual sequences — relevant for AI safety where we care about specific failure cases, not just average performance.

## Key References to Chase

1. **Conant, R.C. & Ashby, W.R. (1970).** "Every good regulator..." — The original theorem.
2. **Friston, K. (2010).** "The free-energy principle: a unified brain theory?" — Connection to predictive processing.
3. **Solomonoff, R. (1964).** Algorithmic probability — foundation for the AIT approach.
