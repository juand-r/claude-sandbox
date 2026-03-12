# A Feedback Mechanism With Bounded Confidence-Based Optimization Approach for Consensus Reaching in Multiple Attribute Large-Scale Group Decision-Making

## Citation
Zha, Q., Liang, H., Kou, G., Dong, Y., & Yu, S. (2019). A Feedback Mechanism With Bounded Confidence-Based Optimization Approach for Consensus Reaching in Multiple Attribute Large-Scale Group Decision-Making. *IEEE Transactions on Computational Social Systems*, 6(5), 994-1006. DOI: 10.1109/TCSS.2019.2938258

## Access
- IEEE Xplore: https://ieeexplore.ieee.org/document/8850062
- ResearchGate: https://www.researchgate.net/publication/336092837
- Full text not freely available. No arXiv preprint found.

## Summary

Proposes a consensus model for large-scale group decision-making that uses bounded confidence (agents only consider opinions within a confidence threshold of their own) combined with feedback mechanisms and optimization. The model clusters decision-makers, identifies those furthest from consensus, and provides targeted feedback to guide the group toward agreement.

## Key Contributions

1. **Bounded confidence + feedback**: Combines the Hegselmann-Krause bounded confidence model (agents ignore opinions too different from their own) with an explicit feedback mechanism that suggests preference adjustments to specific agents.

2. **Large-scale optimization**: Addresses the computational challenge of consensus in large groups by using clustering to reduce dimensionality, then optimizing feedback within each cluster.

3. **Multiple attribute decisions**: Extends consensus models beyond single-issue decisions to multi-attribute problems, more realistic for real-world governance scenarios.

## Relevance to Cybernetics Research

- **Feedback as regulation**: The paper's core mechanism is explicitly a feedback loop: measure consensus level, identify deviations, generate corrective signals, apply them, re-measure. This is textbook cybernetic control.
- **Bounded confidence as variety constraint**: The bounded confidence threshold limits which signals an agent will respond to — a form of Ashby's variety filtering. Only "nearby" opinions can influence an agent.
- **Consensus as social homeostasis**: The drive toward consensus is an instance of social homeostasis — the system has mechanisms (feedback) to maintain a desired state (agreement) against perturbations (diverse initial opinions).
- **Distributed governance application**: Large-scale group decision-making is a governance problem. This paper models how distributed agents can reach collective decisions through structured feedback rather than top-down imposition.

## Key Concepts
- Consensus reaching, bounded confidence, feedback mechanisms, large-scale group decision-making, optimization, social homeostasis, Hegselmann-Krause model
