# Broekens & Chetouani (2021) — Towards Transparent Robot Learning through TDRL-Based Emotional Expressions

**Journal:** IEEE Transactions on Affective Computing, Vol. 12, No. 2, pp. 352–362, Apr–Jun 2021
**Authors:** Joost Broekens (TU Delft), Mohamed Chetouani (Sorbonne Université / ISIR)
**DOI:** 10.1109/TAFFC.2019.2893348
**IEEE Xplore:** https://ieeexplore.ieee.org/document/8613855/
**Open Access:** https://hal.sorbonne-universite.fr/hal-02422888/document
**Also:** https://ii.tudelft.nl/~joostb/files/broekens%20chetouani%202019%20final.pdf

## Access Status
- Open access via HAL and TU Delft (PDF accessed, binary not parseable)
- Content reconstructed from multiple search sources

## Abstract / Summary

Robots need to adapt and learn novel behavior to function autonomously in society. Robot learning often happens in interaction with or near humans, so the learning process needs to be **transparent**. Reinforcement Learning (RL) has been successful for robot task learning, but the process is often opaque to users, causing confusion about what the robot is trying to do and why.

The authors argue that **simulation and expression of emotion** should make the learning process transparent. They propose that the **TDRL (Temporal Difference Reinforcement Learning) Theory of Emotion** provides sufficient structure for developing emotionally expressive learning robots.

They also argue that **personalized emotion interpretation** is needed for robots to cope with individual expressive differences of users.

## Key Concepts

- **TDRL Theory of Emotion**: Temporal difference (TD) error signal in RL maps onto emotional valence — positive TD error → joy/satisfaction, negative TD error → disappointment/frustration
- **Transparency through emotion**: Rather than explaining RL in abstract terms, let the robot EXPRESS its learning state emotionally — humans naturally understand emotional signals
- **Emotional expressions as social signals**: Robot's facial/bodily expressions communicate its learning progress to human observers
- **Personalized emotion interpretation**: Different humans express and interpret emotions differently — the robot must adapt
- **Bidirectional emotional communication**: Robot expresses emotion about its learning; human responds emotionally; robot adapts

## Relevance to Cybernetics-Agents Research

Fascinating cybernetic angle:
- **TD error as emotion**: The prediction error signal in RL (fundamental to cybernetic feedback) IS the emotional signal. This directly connects to predictive processing / active inference frameworks where prediction error drives both learning and affect.
- **Emotion as communication of internal state**: The robot's emotional expression is essentially making its internal control signals visible — a cybernetic transparency mechanism
- **Social feedback loop**: Human emotional response to robot emotion creates a coupled dynamical system — second-order cybernetics
- **Connects to allostasis**: TD error is about expected vs. actual future reward — this is predictive regulation, not just reactive homeostasis

## Connections
- Salichs & Malfaz (2012) — RL + emotion for decision making
- Aylett et al. (2021) — emotional expressions as social signals
- Cañamero (2021) — embodied robot emotion
- Dancy (2021) — affect-cognition interaction
