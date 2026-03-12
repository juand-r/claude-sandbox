# Constant et al. (2018) — A Variational Approach to Niche Construction

**Paper:** Constant, A., Ramstead, M.J.D., Veissière, S.P.L., Campbell, J.O., &
Friston, K.J. (2018). "A variational approach to niche construction." *Journal
of the Royal Society Interface*, 15(141), 20170685.
**URL:** https://royalsocietypublishing.org/doi/10.1098/rsif.2017.0685
**PMC:** https://pmc.ncbi.nlm.nih.gov/articles/PMC5938575/

---

## Summary

This paper applies the Free Energy Principle to **niche construction** — the
process by which organisms modify their environments, thereby steering their own
evolutionary trajectory. It proposes that niche construction is a form of active
inference operating at evolutionary timescales.

## Core Argument

### Niche Construction as Active Inference

Organisms do not just adapt to their environment (natural selection). They also
modify their environment to suit themselves (niche construction). Under the FEP,
both are aspects of the same process: minimizing free energy across the
organism-environment boundary.

- **Natural selection** = variational inference on the environment side (the niche
  selects for organisms that fit)
- **Niche construction** = active inference on the organism side (organisms act to
  make the niche fit them)

Both serve to minimize the joint free energy of the organism-niche system.

### Organism-Environment Coupling via Markov Blankets

The organism and its niche are coupled through a Markov blanket of sensory and
active states. The dynamics on both sides are gradient flows on variational free
energy. Crucially, the paper argues that "the agent and eco-niche share the same
Markov blanket and, therefore, mathematically speaking, must be inferring each
other."

This bidirectional inference is the key insight: not just the organism models the
environment, but the environment (through niche construction) comes to reflect
the organism.

### The Variational Ratchet

The "variational ratchet" mechanism:

1. Organisms modify their environment (niche construction)
2. These modifications encode information ("epistemic resources")
3. Future organisms use this information to reduce uncertainty
4. This enables more effective niche construction
5. Repeat

This creates a cumulative, directional process — each generation inherits not
just genes but a modified environment that makes inference easier. The ratchet
tightens over time.

### Offloading Computation into the Environment

A key practical insight: by modifying the environment, organisms can reduce the
complexity of their internal models. Instead of maintaining complex internal
representations, they "upload" information into the niche.

This reduces:
- **Model complexity** (simpler internal models needed)
- **Metabolic cost** (less neural computation)
- **Uncertainty** (environmental cues disambiguate)

## Examples

### Capuchin Monkey Nut-Cracking

Previous generations leave oily residues, nutshells, and anvil stones at
nut-cracking sites. Juvenile monkeys use these environmental cues to learn
nut-cracking skills more effectively than from observation alone. The
environment functions as an epistemic scaffold.

### Human Culture

Cultural artifacts (tools, symbols, institutions) are niche-constructed epistemic
resources. They encode behavioral regularities and reduce the computational
burden on individuals. Written language, mathematical notation, and computational
tools are all niche construction that simplifies inference.

## Cybernetic Connections

### Extended Regulation

Niche construction extends the regulatory capacity of the organism beyond its
body. This is related to:
- **Ashby's requisite variety:** By modifying the environment, the organism
  effectively increases its variety without increasing internal complexity
- **Beer's VSM:** Organizations (viable systems) construct their environments
  to make regulation tractable

### Circular Causation

The organism-niche feedback loop is the paradigmatic cybernetic circular causal
system: organism modifies niche, niche constrains organism, organism modifies
niche further. There is no privileged causal direction.

### Good Regulator Extended

If the organism must be a model of its environment (Good Regulator), then by
constructing its environment, the organism makes the environment easier to model.
The organism doesn't just model the world — it shapes the world to be more
model-able.

## Implications for Agent Design

1. **Environment design is part of agent design:** Agents should be designed
   together with their environments, not in isolation.

2. **Epistemic scaffolding:** Agents can offload computation into their
   environment (external memory, structured workspaces, tool creation).

3. **Cumulative improvement:** Agent-environment systems should be designed to
   enable cumulative improvement over time (the ratchet effect).

4. **Multi-generational learning:** Information persists in the environment
   across agent lifetimes, enabling cultural evolution.

5. **Reduced model complexity:** By structuring their environment, agents can
   operate with simpler internal models.

## Related Work

- Ramstead, Constant, Badcock & Friston (2019): "Variational ecology and the
  physics of sentient systems" — extends the framework to ecology.
- Constant, Ramstead et al. (2019): Further work on cultural affordances and
  regimes of attention.

## Status

Freely available on PMC.
