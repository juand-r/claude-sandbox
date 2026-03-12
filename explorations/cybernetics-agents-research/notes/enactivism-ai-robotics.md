# Enactivism in AI/Robotics: Concrete Implementations

## Overview

Enactivism holds that cognition arises through dynamic interaction between an organism and its environment -- cognition is "enacted" through sensorimotor processes, not computed over internal representations. This note covers concrete implementations, not just philosophy.

## Key Papers

### 1. Egbert & Barandiaran (2022) - IDSM and Emergent Habits
- "Using enactive robotics to think outside of the problem-solving box: How sensorimotor contingencies constrain the forms of emergent autonomous habits"
- Frontiers in Neurorobotics, 2022
- https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2022.847054/full

#### The Argument Against Problem-Solving
The paper challenges the dominant AI paradigm: intelligence is NOT primarily about solving problems. "The essence of intelligence is to act appropriately when there is no simple pre-definition of the problem" (paraphrasing Winograd and Flores). The question shifts from "how do agents solve problems?" to "how do problems arise for agents in the first place?"

#### IDSM: Iterative Deformable Sensorimotor Medium
The computational substrate for enactive robotics:

- Simulated agents interact with environments through limited sensory channels (visual or auditory)
- Sensorimotor patterns self-reinforce through agent-environment coupling
- **No explicit learning algorithm or fitness function** guides behavior
- Habits emerge as persistent, re-enacted activity patterns

The key: "it is not the materiality of the robot's 'body' that is at stake, but rather the materiality of the sensorimotor mapping, its precarious existence, and its fading structural stability."

#### Results
Simple robots under IDSM control developed emergent habits that clustered by sensory modality. Vision-based habits resembled each other more than audition-based habits. This demonstrates that sensorimotor contingencies (lawful relationships between movement and sensation) fundamentally constrain which behavioral patterns can stabilize.

The sensory structure of an organism directly shapes the repertoire of possible autonomous behaviors -- something functionalist approaches miss entirely.

#### Implications
Robots can exhibit behaviors that emerge from their embodied constitution rather than programmed objectives. Such agents might display greater flexibility precisely because their behavior isn't rigidly optimized for specific external tasks.

### 2. Froese, Iizuka & Di Paolo - Perceptual Crossing
- Froese & Di Paolo (2010), "Modelling social interaction as perceptual crossing"
  - https://www.tandfonline.com/doi/full/10.1080/09540090903197928
- Froese, Iizuka & Ikegami (2014), "Embodied social interaction constitutes social cognition in pairs of humans"
  - Nature Scientific Reports: https://www.nature.com/articles/srep03672

#### The Perceptual Crossing Paradigm
A minimal experimental setup for studying social cognition through interaction:

- Pairs of participants move avatars along a virtual line
- They can make haptic contact with three identical objects
- Two objects embody the other's motions, but only one (the avatar) enables responsive two-way interaction
- The other is a "shadow" or recording

#### Key Finding: Cognition Through Interaction
Participants reliably distinguish the live partner from the recording, even though all objects feel identical in individual encounters. The discrimination capacity **cannot be reduced to the individual agent** -- the interaction process itself is constitutive of social cognition.

#### Evolutionary Robotics Replication
Iizuka and Di Paolo (2007) replicated this with evolved artificial agents using small recurrent neural networks. The evolved agents successfully discriminated between "live" (two-way) and "recorded" (one-way) interaction. Analysis showed the agents did NOT process inputs for signs of social contingency -- they relied on simple sensorimotor couplings that were only stable during genuine mutual interaction.

This is a concrete demonstration that cognitive capacities can be properties of interaction dynamics, not just individual computational processes.

### 3. The iCub Platform for Enactive Cognition
- Sandini, Metta, Vernon - "The iCub Cognitive Humanoid Robot: An Open-System Research Platform for Enactive Cognition"
- https://link.springer.com/chapter/10.1007/978-3-540-77296-5_32

#### Embodiment Specifications
A 53 degree-of-freedom humanoid robot, 94cm tall (size of a 3-year-old child). Capabilities: crawling, sitting up, dexterous manipulation, fully articulated head and eyes. Sensory: visual, vestibular, auditory, haptic.

#### Enactive Cognitive Architecture
The iCub uses enactive principles for developmental learning:
- Skills acquired through sensorimotor interaction with humans, not pre-programming
- Linguistic behaviors emerge from "interaction games" with human partners
- Successfully learned linguistic skills including negation through embodied interaction with naive participants
- Can autonomously switch between behaviors (interactive drumming, peek-a-boo) based on social cues

#### Developmental Approach
Rather than programming fixed behaviors, the iCub develops through ontogenetic learning -- acquiring capabilities through experience, like a child. This operationalizes the enactive principle that cognition develops through history of structural coupling.

### 4. Froese & Ziemke (2009) - Enactive AI Framework
- "Enactive artificial intelligence: Investigating the systemic organization of life and mind"
- Artificial Intelligence, vol. 173, pp. 466-500

#### Distinction: Embodied vs. Enactive AI
- **Embodied AI**: physical/sensorimotor embodiment, structural coupling through sensors and actuators
- **Enactive AI**: additionally requires that the system self-regulate its internal processes and external interactions to remain viable

The gap: embodied AI gives robots bodies, but enactive AI requires that those bodies matter to the robot -- that the robot's continued operation depends on maintaining viability through its interactions. Current robots do not qualify as truly embodied in the enactive sense.

Di Paolo's observation: "something fundamental is still missing" from embodied AI. The missing element is **autonomy** -- the system generating its own concerns rather than serving externally-imposed objectives.

### 5. Bio A.I. Editorial (Safron, Hipolito, Clark, 2023)
- "Editorial: Bio A.I. - from embodied cognition to enactive robotics"
- Frontiers in Neurorobotics, 2023
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10682788/

Synthesizes 16 papers exploring how enactivist principles can advance AI beyond cognitivist deep learning. Proposes seven mechanisms for biological intelligence:

1. **Distributed attractor dynamics**: implicit representation through action-perception cycles
2. **Latent workspaces**: reduced-dimension manifolds with partially disentangled features
3. **Homeostatic grounding**: subcortical predictive modeling coupling agents to survival needs
4. **Value-canalized control**: striatal-cortical loops conditioning perception on likely action patterns
5. **Spatiotemporal trajectories**: hippocampal/entorhinal re-representation
6. **Local object models**: cortical columns achieving functional closure over action-perception cycles
7. **Symbolic capacities**: language as probable motor patterns enabling recursive self-modeling

Warning: don't assume biological features automatically improve AI performance. The value is in the principles, not in superficial biomimicry.

## Cybernetic Connections

### Autopoiesis (Maturana & Varela)
Enactivism descends directly from autopoietic theory. The enactive agent must be organizationally closed -- its processes produce the components that maintain those processes. In robotics, this translates to self-maintaining sensorimotor patterns (habits in the IDSM sense).

### Ashby's Requisite Variety
The IDSM results show that sensory modality constrains the variety of possible behaviors. This is Ashby's insight applied to embodiment: the variety of available actions is determined by the variety of the sensor-effector system, not by abstract computational capacity.

### Operational Closure (von Foerster)
The perceptual crossing experiments demonstrate operational closure in social cognition: the cognitive capacity is a property of the closed interaction loop, not of either participant individually. This is second-order cybernetics applied to multi-agent interaction.

### PCT (Powers)
Enactive robotics shares PCT's emphasis on control of perception rather than control of output. The IDSM agent doesn't plan actions -- it maintains sensorimotor patterns. This is controlling the perceptual variable (sensorimotor contingency), not the motor output.

## Implications for AI Agent Design

1. **Against the representationalist assumption**: Current AI agents (LLM-based) are fundamentally representationalist -- they manipulate symbolic representations. Enactivism suggests this is the wrong foundation. But enactive principles can still inform agent design even within representationalist systems (e.g., emphasizing agent-environment coupling over internal reasoning).

2. **Habits over plans**: Rather than explicit planning (chain-of-thought, tree-of-thought), enactive design suggests agents should develop stable patterns of interaction that persist through structural coupling with their environment. This is closer to tool-use patterns that emerge from experience than to explicit reasoning chains.

3. **Autonomy requires precariousness**: An agent is truly autonomous only if its continued operation depends on maintaining its own viability. Current AI agents have no stake in their own continuation -- they can be stopped and restarted without consequence. Enactivism says this is why they lack genuine cognition.

4. **Social cognition through interaction**: The perceptual crossing results suggest that multi-agent coordination might be better achieved through dynamic interaction patterns than through explicit communication protocols. This connects to stigmergy (see stigmergy-multiagent.md).
