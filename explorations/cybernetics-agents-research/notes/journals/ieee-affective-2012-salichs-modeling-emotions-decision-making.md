# Salichs & Malfaz (2012) — A New Approach to Modeling Emotions and Their Use on a Decision-Making System for Artificial Agents

**Journal:** IEEE Transactions on Affective Computing, Vol. 3, No. 1, pp. 56–68, Jan–Mar 2012
**Authors:** Miguel A. Salichs, María Malfaz
**DOI:** 10.1109/T-AFFC.2011.32
**IEEE Xplore:** https://ieeexplore.ieee.org/document/6035666/

## Access Status
- Full text NOT accessed (IEEE paywall, sci-hub blocked)
- No preprint found on arxiv; may be on ResearchGate

## Abstract / Summary

Presents a biologically-inspired decision-making system for autonomous agents (physical and virtual) based on **drives, motivations, and emotions**. The agent has needs/drives that must stay within a certain range; motivations are what moves the agent to satisfy a drive. The agent's well-being is a function of its drives, and the goal is to optimize it.

Three artificial emotions implemented: **happiness, sadness, and fear**. Key novelty: each emotion is treated separately with its own generation method and functional role, rather than being defined as a unified whole. The system does not require predefined emotional triggers — agents learn emotional associations autonomously through experience (reinforcement learning).

## Key Concepts

- **Drives and homeostasis**: Agent has internal needs that must be maintained within acceptable ranges — directly analogous to homeostatic regulation
- **Motivations**: What moves the agent to satisfy a drive — connects to cybernetic goal-seeking
- **Well-being function**: Scalar function of drive states the agent optimizes
- **Fear modeled as worst historical Q-value** for a state — the agent remembers dangerous locations
- **Emergent emotional learning**: No predefined emotion-trigger mappings; learned through RL
- **Happiness/sadness**: Related to whether drives are being satisfied or frustrated

## Relevance to Cybernetics-Agents Research

This is a core paper for our project. The drives-motivations-emotions architecture is essentially a cybernetic control system with:
- Homeostatic drives (reference signals, error signals)
- Emotion as a functional regulatory layer modulating behavior
- Well-being as an aggregate error signal
- Reinforcement learning as the adaptation mechanism

Directly connects to Ashby's homeostatic framework and to modern allostatic ideas — the agent doesn't just react to current drive states but learns predictive associations (fear of states that led to poor outcomes).

## Connections
- Cañamero (2021) — embodied robot emotion models
- Dancy (2021) — cognitive architecture with physiology and affect
- Broekens & Chetouani (2021) — TDRL and emotion in robot learning
