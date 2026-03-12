# Kawato, Furukawa & Suzuki (1987) — Hierarchical Neural Network Model for Motor Control

## Bibliographic Details
- **Authors:** Mitsuo Kawato, Kenji Furukawa, Ryoji Suzuki
- **Title:** A hierarchical neural-network model for control and learning of voluntary movement
- **Journal:** Biological Cybernetics, Vol. 57, pp. 169-185
- **Year:** 1987
- **DOI:** 10.1007/BF00364149
- **Related:** Kawato & Gomi (1992), "A computational model of four regions of the cerebellum
  based on feedback-error learning," Biol. Cybern. 68, 95-103 (DOI: 10.1007/BF00201431)

## Summary

Kawato and colleagues proposed that the cerebellum acquires internal models of the body and
its controlled objects through motor learning. The model distinguishes between **forward models**
(predicting sensory consequences of actions) and **inverse models** (computing motor commands
to achieve desired outcomes). These are hierarchically arranged, with forward models embedded
in internal feedback loops and inverse models serving as feedforward controllers.

## Key Concepts

### Internal Models
- **Forward model:** predicts sensory consequences of a motor command (input: motor command ->
  output: predicted sensory state). Used for state estimation and prediction.
- **Inverse model:** computes the motor command needed to achieve a desired sensory outcome
  (input: desired state -> output: motor command). Used for feedforward control.
- The cerebellum is proposed as the neural substrate for both types.

### Feedback-Error-Learning
- The key learning mechanism: the output of a feedback controller (which corrects errors in
  real time) serves as the teaching signal for a feedforward controller (the cerebellar inverse model)
- Over time, the feedforward controller learns to anticipate and preempt errors, reducing the
  need for slow feedback correction
- Climbing fiber responses represent motor-command errors from premotor feedback controllers
- Long-term depression in Purkinje cells implements the learning

### Hierarchical Architecture
- Multiple levels of feedback control (spinal, brainstem, cerebral)
- At each level, a cerebellar module learns an inverse model
- Each corticonuclear microcomplex learns predictive and coordinative control for a specific
  controlled object

### Cybernetic Significance
This is deeply cybernetic work:
- **Feedback -> feedforward transition** — the system bootstraps from reactive (feedback) control
  to anticipatory (feedforward) control through learning. This is exactly the kind of adaptation
  Ashby described.
- **Internal models as regulators** — directly related to the Good Regulator Theorem (Conant & Ashby):
  a good controller must contain a model of the system it controls
- **Efference copy / reafference principle** — forward models predict sensory consequences of
  actions, implementing von Holst's reafference principle computationally
- **Hierarchical control** — nested feedback loops at multiple levels, exactly the architecture
  Beer described in the Viable System Model

## Relevance to Our Research

1. **Internal models for agents** — agents need forward models (predict outcomes of actions) and
   inverse models (plan actions to achieve goals). Kawato's framework provides a neurobiological
   grounding for this.
2. **Feedback-to-feedforward learning** — agents that initially rely on slow deliberative reasoning
   could learn to "compile" frequent patterns into fast feedforward responses
3. **Good Regulator connection** — the cerebellar internal model IS the "model of the system"
   required by the Good Regulator Theorem
4. **Hierarchical control** — nested feedback loops at multiple time scales maps directly onto
   multi-level agent architectures
5. **Von Holst bridge** — connects reafference principle to modern computational motor control

## Impact
- Kawato is one of the most prolific authors in Biological Cybernetics (22 papers)
- Internal models framework widely adopted in neuroscience and robotics
- Supported by neurophysiology (monkey experiments) and neuroimaging (human studies)
- Influenced motor control theory, cognitive science, and robot learning

## Access
- Full text behind Springer paywall
- Review available: Kawato (1999) "Internal models for motor control and trajectory planning"
  at https://psychology.nottingham.ac.uk/staff/srj/int/6.%20Forward%20models%20&%20Movement%20control%20mechanisms/Kawato.pdf
- PMC article on evolution of the work: https://link.springer.com/article/10.1007/s00422-021-00904-7
