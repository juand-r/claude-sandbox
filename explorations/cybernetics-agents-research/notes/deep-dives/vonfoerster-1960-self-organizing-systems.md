# Von Foerster (1960) — On Self-Organizing Systems and Their Environments

## Citation
Von Foerster, H. (1960). "On Self-Organizing Systems and Their Environments." In M. C. Yovits & S. Cameron (Eds.), *Self-Organizing Systems*, Pergamon Press, pp. 31-50. Reprinted in *Understanding Understanding* (Springer, 2003), ch. 1.

## Source Status
Full text available via Semantic Scholar PDF and Springer. Originally an address at the Interdisciplinary Symposium on Self-Organizing Systems, Chicago, IL.

## Core Argument

### The Provocation: "There Are No Self-Organizing Systems"

Von Foerster opens with a deliberate paradox: he proves by reductio ad absurdum that no system can be truly "self-organizing" in isolation. If a closed system reduces its own entropy (increases its own order), it violates the Second Law of Thermodynamics. Therefore, any system that appears to self-organize must be exchanging energy or information with an environment.

The term "self-organizing system" is a misnomer unless understood as shorthand for "a system that organizes itself *in relation to its environment*." The environment is not optional scenery — it is constitutive of the self-organizing process.

### Redundancy as Measure of Order

Von Foerster adopts Shannon's redundancy R as his formal measure of internal order:

```
R = 1 - H / H_max
```

Where:
- H = Shannon entropy of the system
- H_max = maximum possible entropy (complete disorder)

Properties:
- H = H_max => R = 0 (no order, maximum disorder)
- H = 0 => R = 1 (perfect order — given one element, all others are determined)

He prefers redundancy over negentropy because negentropy always assumes finite values even for maximally disordered systems, making it a poor discriminator. Redundancy is zero when there is no order and unity when order is complete.

### The Self-Organization Criterion

A system is self-organizing iff:

```
dR/dt > 0
```

The redundancy (internal order) is increasing over time.

### The "Order from Noise" Principle

This is von Foerster's principal contribution beyond Schrodinger's two principles:
- Schrodinger's "order from order" (algorithmic, crystalline)
- Schrodinger's "order from disorder" (statistical, thermodynamic)
- **Von Foerster's "order from noise"** (self-organizational)

Random perturbations ("noise") cause a system to explore its state space more widely. This increases the probability that it will fall into the basin of a strong attractor. Paradoxically, the larger the noise, the faster the self-organization — because the system traverses more of its state space and finds attractors sooner.

### The Magnetic Cubes Thought Experiment

The canonical illustration: magnetized cubes in a box, each magnetized on two faces. When the box is shaken (noise is introduced), the cubes spontaneously form ordered configurations because the magnetic interactions between faces create an "energy landscape" with deep wells corresponding to ordered states. Shaking moves the cubes out of shallow wells and into deeper ones. More shaking => faster discovery of deep wells.

This is essentially simulated annealing before the concept was formalized in computational optimization (Kirkpatrick et al., 1983).

### Important Caveat (Vallee)

Noise does not create order ex nihilo. It acts as a "structure displayer" — it reveals pre-existing order embedded in the system's interaction dynamics (e.g., magnetic interactions among components). The structure must already be latent in the system's interaction potentials for noise to display it.

### Internal and External Demons

To compute R properly, one must account for the coupling between system entropy and environment entropy. Von Foerster introduces:
- The **internal demon**: the agent responsible for changes in the system's entropy
- The **external demon**: the agent responsible for changes in the environment's entropy

Self-organization requires that these are coupled: the system's entropy decrease is compensated by the environment's entropy increase, satisfying the Second Law globally.

## Relevance to Agent Architectures

### Direct Relevance

1. **Exploration vs. exploitation**: The order-from-noise principle is a precursor to the exploration/exploitation tradeoff in RL. "Noise" = exploration; "attractor" = exploitation of a found policy. Von Foerster's insight that *more noise speeds up self-organization* maps to the idea that higher exploration temperatures early in training lead to faster convergence.

2. **Simulated annealing**: The magnetic cubes example is literally simulated annealing. The connection to cooling schedules in SA and to epsilon-decay in epsilon-greedy RL is direct.

3. **Environment-dependence of agents**: Von Foerster's insistence that no system self-organizes in isolation maps directly to the observation that agents cannot learn without an environment. The "environment" is constitutive, not incidental. This is structurally identical to the active inference framework where agent and environment are coupled via a generative model.

4. **Redundancy as a measure of agent competence**: An agent that has "learned" a domain has high redundancy — given one observation, it can predict others. This is compression, generalization, and model-building all at once.

### The Latent Structure Caveat

The Vallee caveat is important for agents: noise/exploration only helps if there is latent structure to discover. In domains with no exploitable regularities, exploration is just random walk. This connects to the "no free lunch" theorem — you need inductive biases (latent structure) for learning to work.

## Key Quotes and Formulations

- "There are no such things as self-organizing systems!" (opening provocation)
- The self-organization criterion: dR/dt > 0
- Order from noise principle: random perturbations accelerate attractor discovery
- No self-organization without environment coupling (Second Law argument)

## Links
- Semantic Scholar PDF: https://pdfs.semanticscholar.org/2384/d37ee804cfed6b56cc286d407ffec3bcc3b3.pdf
- Springer chapter: https://link.springer.com/chapter/10.1007/0-387-21722-3_1
