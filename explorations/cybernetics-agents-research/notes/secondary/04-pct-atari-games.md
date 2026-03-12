# High Performance on Atari Games Using Perceptual Control Architecture Without Training

## Citation
Gulrez, T. & Mansell, W. (2022). "High Performance on Atari Games Using Perceptual Control Architecture Without Training." *Journal of Intelligent & Robotic Systems*, 106, 47. arXiv:2108.01895.

## Summary

Demonstrates that a Perceptual Control Theory (PCT) agent achieves human-level performance on Atari paddle games (Breakout, Pong) with zero training — no gradient descent, no reward signal, no data. The PCT architecture uses hierarchical closed-loop error correction where each level controls a perceptual variable by setting reference values for the level below.

## Key Arguments

1. **PCT needs no training.** Unlike DRL methods requiring millions of training frames (Rainbow: 200M, DQN: 10M), the PCTagent uses a hand-designed 4-level perceptual hierarchy with all gains set to 1. It works immediately.

2. **Results match or exceed DRL:**
   - Breakout: PCTagent ~400-862 vs. Rainbow 120, DQN 401, Human Record 864
   - Pong: PCTagent 18-21 vs. Rainbow/DQN 21

3. **Unified architecture across games.** The same model (with appropriate perceptual variable definitions) works for both Breakout and Pong. DRL models must be retrained per game.

4. **Control hierarchy:**
   - Level 1 (top): Distance between paddle and ball
   - Level 2: Directional control
   - Level 3: Paddle position tracking
   - Level 4 (bottom): Button-press frequency with velocity limiting

## Relevant Formalisms

- **PCT control loop**: Each level computes error e = reference - perception, outputs action to reduce error. Output of higher level sets reference for lower level.
- **No planning, no prediction**: The system reacts to current perceptual error. "Output signals from control units set reference values at lower hierarchy levels, allowing actions to vary dynamically without planning or learning."
- **Gain parameters**: All set to k=1 without optimization — the architecture does the work, not parameter tuning.

## Connection to Our Research

This is the strongest empirical demonstration that cybernetic control architectures can compete with modern ML:

- **PCT vs. RL**: PCT achieves comparable results through hierarchical error correction rather than reward maximization. This is a fundamentally different paradigm — control of perception vs. optimization of reward.
- **Hierarchy maps to agent architecture**: The 4-level PCT hierarchy (distance → direction → position → action) parallels the hierarchical decomposition in agents like Tree of Thought (abstract goal → sub-goals → concrete actions).
- **No training = no alignment problem**: A PCT agent doesn't learn goals from data — goals are set as reference signals. This has implications for AI safety: goal specification is explicit, not emergent from training.
- **Powers' hierarchy ↔ Agent levels**: Powers' original PCT hierarchy (intensity → sensation → configuration → transition → sequence → ... → system concepts) could map onto increasingly abstract levels of agent reasoning.
- **Limitation**: The architecture works for paddle games because the perceptual hierarchy can be hand-designed. For complex environments, the open question is whether PCT hierarchies can be learned — bridging PCT and deep learning.

## Key References to Chase

1. **Powers, W.T. (1973/2005).** *Behavior: The Control of Perception.* — The foundational PCT text (already in our primary notes).
2. **Powers, W.T. (2008).** *Living Control Systems III.* — Later developments of PCT hierarchy.
3. **Marken, R.S. & Mansell, W. (2013).** "Perceptual control as a unifying concept in psychology." — PCT as theoretical framework for understanding behavior.
