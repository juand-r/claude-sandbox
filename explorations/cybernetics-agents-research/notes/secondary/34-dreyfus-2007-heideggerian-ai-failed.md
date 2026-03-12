# Dreyfus (2007) — Why Heideggerian AI Failed and How Fixing It Would Require Making It More Heideggerian

## Citation

Dreyfus, H. L. (2007). Why Heideggerian AI Failed and How Fixing It Would Require Making It More Heideggerian. *Philosophical Psychology*, 20(2), 247–268. DOI: 10.1080/09515080701239510

Also published in: Dreyfus, H. L. (2012). In *Artificial Intelligence*, Vol. 171, Issues 18–19, pp. 1137–1160. DOI: 10.1016/j.artint.2007.10.009

Available: https://cspeech.ucd.ie/Fred/docs/WhyHeideggerianAIFailed.pdf

## Core Thesis

All attempts at AI — from classical GOFAI through Brooks's behavior-based robotics to Wheeler's embodied-embedded cognition — have failed because they rely on some form of **representation**. Genuine intelligence requires nonrepresentational, embodied, skillful coping with a meaningful world. Building a truly Heideggerian AI would require abandoning representations entirely, which may be impossible with current computational substrates.

## Key Arguments

### 1. The Frame Problem as Fundamental

The frame problem — how to determine what is relevant in any given situation — is not a technical glitch but a deep symptom of the representational approach. If you represent the world symbolically, you need rules for determining which representations are relevant when. But those rules themselves need context to apply, leading to infinite regress.

GOFAI tried to solve this with "frames" and "scripts" — pre-packaged bundles of relevance. This never scaled. The frame problem was never solved; it was abandoned.

### 2. Critique of Brooks's Subsumption Architecture

Rodney Brooks's behavior-based robots were explicitly anti-representational: no internal world models, no symbolic reasoning, just layers of sensorimotor behaviors. Dreyfus's verdict: Brooks solved the frame problem by **eliminating significance entirely**. His robots respond to fixed features of the environment via reflex-like responses. They have no sense of what matters, no learning, no skill acquisition. They are "empiricist/behaviorist" — stimulus triggers response, end of story.

### 3. Critique of Agre's "Pengi"

Phil Agre's "Pengi" system used "deictic representations" — representations that referred to the functional role of objects (e.g., "the-thing-I'm-pushing") rather than to object identity. Dreyfus praised the insight but critiques the execution: Pengi had no skill, no learning, and its deictic representations were still representations. The system's relevance was still pre-programmed by the designer, not discovered by the agent.

### 4. Critique of Wheeler's Embodied-Embedded Approach

Michael Wheeler's synthesis attempted to combine action-oriented representations with embodied, situated cognition. Dreyfus argues Wheeler simply reintroduced the frame problem in a new guise: how does the system determine which action-oriented representations are relevant? Wheeler acknowledged the problem but offered no solution.

### 5. The Heideggerian Alternative

For Heidegger, intelligent beings do not primarily relate to the world through representations but through **skillful coping** — ready-to-hand engagement where things show up as meaningful affordances, not as objects to be represented. A hammer in use is not an object with properties; it is an extension of one's purposive activity. You don't represent the hammer; you hammer.

Genuine intelligence involves:
- **Absorbed coping**: Acting without reflective awareness of objects or rules
- **Solicitations**: The world pulls you toward actions based on your embodied skills and concerns
- **The intentional arc**: A feedback loop between perception, action, and the skill-body that integrates past experience into present readiness

### 6. Freeman's Neurodynamics as Hope

Dreyfus finds hope in Walter Freeman's neurodynamic models: self-organizing neural systems that use attractor dynamics to determine relevance without explicit representations. The brain doesn't search through representations for relevant ones; it settles into attractor basins shaped by experience. This is closer to Heidegger's vision.

## Relevance to Agent Design

### The Representation Question for LLMs

This paper poses a sharp challenge to current LLM-based agents:

1. **LLMs are maximally representational**: Everything is tokens, embeddings, attention weights. If Dreyfus is right that intelligence requires nonrepresentational engagement, then LLMs are categorically the wrong substrate for intelligence.

2. **But LLMs might sidestep the frame problem**: LLMs do not use explicit symbolic representations with explicit relevance rules. Their "relevance" is implicit in learned attention patterns and activation dynamics. In some ways, this is closer to Freeman's neurodynamics than to GOFAI. Dreyfus might argue they are still representational (they still process symbols), but the representation is subsymbolic and learned, not hand-coded.

3. **The tool-use question**: When an LLM agent uses tools, is this more like ready-to-hand or present-at-hand engagement? If the agent smoothly integrates tool outputs into its ongoing reasoning without explicit reflection on the tool-as-object, this is closer to ready-to-hand. If it treats tools as objects with documented APIs that must be explicitly invoked, this is present-at-hand — exactly what Dreyfus critiques.

### The Cybernetic Connection

Dreyfus's account has deep parallels with cybernetics:
- **Absorbed coping** is control without explicit representation — like a thermostat or a homeostatic system
- **The intentional arc** is a feedback loop between perception, action, and embodied skill
- **Solicitations** are like affordances detected by a controller tuned to relevant disturbances
- **Freeman's attractor dynamics** are self-organizing systems in the cybernetic tradition

But Dreyfus goes beyond cybernetics in insisting that the embodied, phenomenological dimension is essential — not just a nice-to-have but a necessary condition for genuine intelligence.

### The Uncomfortable Implication

If Dreyfus is right, then building genuinely intelligent agents may require:
- Bodies that physically engage with the world
- Needs and concerns that make things matter
- Skills acquired through practice, not programmed
- A capacity for absorbed, nonrepresentational coping

This is a much harder engineering challenge than building better prompt architectures.

## Relation to Other Notes

- Clark (2013): Predictive processing — potentially a representational framework that Dreyfus would critique, though its status is debated
- Gallagher (2017): Enactivist interventions — shares Dreyfus's anti-representationalism
- Froese (2012): The cybernetics-to-enactivism lineage
- Brooks subsumption architecture: One of Dreyfus's explicit targets
- Barandiaran et al. (2009): Provides the formal account of agency Dreyfus gestures toward
