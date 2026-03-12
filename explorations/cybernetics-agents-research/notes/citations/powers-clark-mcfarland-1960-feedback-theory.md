# Powers, Clark & McFarland (1960) — A General Feedback Theory of Human Behavior

**Full Citation:** Powers, W.T., Clark, R.K., & McFarland, R.L. (1960). "A General Feedback Theory of Human Behavior." *Perceptual and Motor Skills*, 11, 71-88 (Part I) and 309-323 (Part II).

**Cited in our notes:** powers-pct.md (as the founding paper of PCT)

**Source:** Available via [IAPCT](https://www.iapct.org/publications/other/a-general-feedback-theory-of-human-behavior-part-i-and-part-ii/). Referenced through secondary sources and IAPCT website.

---

## 1. Historical Context

This is the first formal publication of what would become Perceptual Control Theory (PCT). Powers described it as "the beginnings of my contributions to applying control theory to behavior." Clark and McFarland worked with Powers from 1953 to 1960 at the Veterans Administration Research Hospital, Chicago, and Northwestern University Medical School.

The paper was written at a time when behaviorism dominated psychology and cybernetics was still young (Wiener's *Cybernetics* was only 12 years old). It proposed a radical alternative to the stimulus-response framework by placing feedback control — not input-output processing — at the center of behavioral explanation.

## 2. Core Argument

### The Thesis
Human behavior is organized as negative feedback control. The controlled variable is NOT the behavioral output but the **perceptual input** — a sensed function of the environment. Behavior varies as the means of keeping perception stable.

### The Key Inversion
Standard psychology (and early cybernetics): environment → sensory processing → behavioral output.

Powers et al.: the organism controls its sensory input by varying its behavioral output. The causal arrow points BOTH ways (circular causation), and what is maintained constant is the input, not the output.

### Hierarchical Organization
The paper proposed that control is organized hierarchically — higher-level systems set the reference signals for lower-level systems. Each level controls its own type of perception. This was the kernel of the 11-level hierarchy Powers would develop fully in *Behavior: The Control of Perception* (1973).

## 3. The Mathematical Framework

Each control unit consists of:
- **Input function:** Transforms environmental variable into perceptual signal p
- **Comparator:** Computes error e = r - p (reference minus perception)
- **Output function:** Generates behavioral output proportional to (or integrating) the error
- **Feedback through environment:** Output affects the environment, which affects the input

The controlled variable q.i satisfies: when loop gain is high, q.i ≈ r/K (where K is the input function gain). The system maintains q.i near the value specified by the reference signal, regardless of disturbances.

## 4. Relation to Rosenblueth, Wiener & Bigelow (1943)

Powers et al. built directly on the 1943 paper's classification of purposeful behavior. But they went further:

| Rosenblueth et al. (1943) | Powers et al. (1960) |
|--------------------------|---------------------|
| Behavior can be purposeful (feedback-driven) | All behavior IS feedback-driven |
| Feedback corrects errors in output | Feedback controls input (perception) |
| Classification scheme | Quantitative model |
| Feedback as one category of behavior | Feedback as THE mechanism of all behavior |

## 5. Significance for Our Research

### The First Hierarchical Control Model of Behavior
This paper introduced the idea that complex behavior emerges from hierarchically organized simple control loops — an architecture that maps directly onto:
- Beer's VSM (hierarchically organized control with each level having its own controlled variable)
- Ashby's multistable system (independent subsystems with limited interconnection)
- Modern agent architectures with hierarchical goals

### Control of Input vs. Control of Output
This distinction is still underappreciated in AI/RL:
- **RL controls output:** Find the best policy (action mapping)
- **PCT controls input:** Maintain desired perceptual states through whatever actions work
- This leads to fundamentally different architectures and different kinds of robustness

### No World Model Required
PCT robots operate without world models, inverse kinematics, or trajectory planning. They simply close feedback loops around perceptual variables. This challenges the Richens et al. (2025) claim that capable agents must contain world models — but the two can be reconciled: PCT agents handle single-task regulation well (where world models are unnecessary per Richens' Theorem 2), but multi-goal generalization may still require implicit world models.

## 6. Key References from This Paper

- **Rosenblueth, A., Wiener, N., & Bigelow, J. (1943). "Behavior, Purpose and Teleology."** — Direct ancestor.
- **Ashby, W.R. (1952). *Design for a Brain*.** — Ultrastability as the mechanism for parameter adaptation.
- **Wiener, N. (1948). *Cybernetics*.** — The formal framework for feedback and communication.
- **MacKay, D.M. (1956).** — Information-theoretic approaches to brain function that influenced Powers.

---

*Notes compiled 2026-03-12 from IAPCT website, secondary sources, and our existing PCT notes.*
