# Active Inference for Self-Organizing Multi-LLM Systems

## Citation
Prakki, R. (2024). "Active Inference for Self-Organizing Multi-LLM Systems: A Bayesian Thermodynamic Approach to Adaptation." arXiv:2412.10425.

## Summary

Integrates active inference (based on the Free Energy Principle) as a "cognitive layer" above LLM-based agents. Rather than improving the LLM itself, the framework dynamically adjusts prompts and search strategies through principled information-seeking behavior — minimizing variational free energy to balance exploration and exploitation.

## Key Arguments

1. **Active inference as meta-controller for LLMs.** The LLM is treated as a specialized component; active inference provides the decision-making brain that selects which prompts and search strategies to use. This separates adaptation from model training.

2. **Free energy decomposition drives behavior:**
   - **Accuracy term**: How well beliefs match observations
   - **Complexity term**: Divergence between learned and prior beliefs
   - **Expected Free Energy** balances information gain (epistemic drive) and pragmatic value (goal achievement)

3. **Emergent exploration-exploitation.** The agent naturally prioritizes information-gathering actions early (when uncertainty is high), then shifts to exploitation — this emerges from the math, not hand-coded.

4. **State space design:**
   - 33 prompt states × 11 search states × 3 information levels
   - 7 observation modalities (accuracy, relevance, comprehensiveness, etc.)
   - Learning via Dirichlet-parameterized observation model updates

## Relevant Formalisms

- **Variational free energy**: F = -accuracy + complexity (bound on surprisal)
- **Expected free energy**: G = -information_gain - pragmatic_value
- **Observation model (A matrices)**: Likelihood tensors mapping hidden states to observations
- **Transition model (B matrices)**: State transition dynamics
- **Preference structure (C matrix)**: Encodes desired observations
- **Update rule**: a_m^(t+1) = a_m^t + η·(o_m ⊗ q(s))·(A_m > 0)

## Connection to Our Research

This paper is the most concrete implementation of cybernetic principles in an LLM agent architecture:

- **Free Energy Principle as cybernetics 2.0**: FEP can be seen as a mathematical formalization of Ashby's ultrastability — the system adjusts its parameters (beliefs/policies) to keep free energy (surprisal) within viable bounds. The "essential variables" are the system's model accuracy and goal achievement.
- **Homeostasis via free energy minimization**: The agent maintains viability by minimizing surprise — directly analogous to cybernetic homeostasis maintaining essential variables.
- **VSM mapping**:
  - S1 (operations) = LLM execution
  - S2 (coordination) = prompt/search selection via active inference
  - S3 (control) = free energy monitoring
  - S4 (intelligence) = epistemic exploration drive
  - S5 (policy) = preference structure (C matrix)
- **Requisite variety**: The 33×11×3 state space represents the agent's variety for matching environmental complexity. Active inference naturally manages variety through the complexity term (penalizing unnecessary model complexity).
- **Good Regulator**: The learned A matrices (observation model) constitute an internal model of the environment — the agent becomes a model of its task domain through Bayesian updating.

## Key References to Chase

1. **Friston, K. et al. (2017).** "The graphical brain: Belief propagation and active inference." — Foundation for the computational framework.
2. **Fields, C. et al. (2023).** "Control flow in active inference systems." — Thermodynamic foundations connecting FEP to physical information processing costs.
3. **Champion, T. et al. (2023).** "Reframing the Expected Free Energy: Four Formulations and a Unification." — Mathematical unification of different EFE formulations.
