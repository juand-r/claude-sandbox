# Von Foerster (1973) — On Constructing a Reality

**Full Citation:** Von Foerster, H. (1973). "On Constructing a Reality." In W.F.E. Preiser (Ed.), *Environmental Design Research*, Volume 2 (pp. 35–46). Stroudsberg: Dowden, Hutchinson & Ross. Reprinted in *Understanding Understanding* (2003), Springer, pp. 211–227.

**Source:** Full text PDF from pespmc1.vub.ac.be; extracted via pdftotext.

---

## 1. The Central Postulate

"The environment as we perceive it is our invention."

Von Foerster supports this with four demonstrations, a neurophysiological analysis, and an ethical argument.

## 2. The Four Demonstrations

### (a) The Blind Spot
The retina has no photoreceptors where the optic nerve exits (the disc). When an image falls on this spot, we do not see darkness — we perceive NOTHING. The blindness is not perceived at all — "neither as something present, nor as something absent." What is perceived is perceived "blotch-less."

**Implication:** The nervous system does not report absences. It fills in. We do not see our own blind spots.

### (b) Scotoma
Patients with occipital brain lesions lose portions of their visual field but are not initially aware of the loss. They cannot perceive the absence of perception. Only motor dysfunction reveals the deficit.

Two metaphors: "Perceiving is Doing" and "If I don't see I am blind, I am blind; but if I see I am blind, I see."

### (c) Alternates (Word Repetition)
A single word played on loop is perceived clearly — then abruptly shifts to a different word (an "alternate"), then another, then another. From the word "Cogitate," 758 alternates were reported (including: "agitate," "can't you stay," "gravity," "marmalade").

**Implication:** The percept is not determined by the stimulus. The organism constructs different perceptions from identical physical input.

### (d) Comprehension (Cat Auditory Learning)
A cat learning that a tone means food: initially, the auditory cortex shows pure noise in response to the tone. Only when the cat "comprehends" (associates tone with food) does the neural activity reorganize into a signal. Sensation becomes comprehensible only through sensorimotor coordination.

**Implication:** "No tone is perceived as long as this tone is uninterpretable." The cat's perception of "beep, beep, beep" is actually "food, food, food."

## 3. The Principle of Undifferentiated Encoding

This is von Foerster's key neurophysiological principle:

> "The response of a nerve cell does not encode the physical nature of the agents that caused its response. Encoded is only 'how much' at this point on my body, but not 'what'."

- A retinal rod absorbs electromagnetic radiation and produces periodic discharges commensurate with the INTENSITY of radiation — but contains no clue that it was electromagnetic radiation.
- The same is true for ALL sensory receptors: taste, touch, smell, heat, cold, sound — they are all "blind" to the QUALITY of stimulation, responsive only to QUANTITY.

**The consequence:** "Out there" there is no light and no color — only electromagnetic waves. No sound and no music — only air pressure variations. No heat or cold — only moving molecules. "The tremendous variety of this colorful world" is conjured up by the brain.

## 4. Cognition = Computing a Reality

Von Foerster paraphrases the Problem of Cognition:

**COGNITION = computing a reality** (note the indefinite article "a")

He defends the use of "a" over "the": the "A-school" holds that sensations in correlation GENERATE an experience ("here is a table"), while the "The-school" holds that sensations CONFIRM a pre-existing reality.

He then refines through recursion:
- Cognition = computing descriptions of a reality
- But descriptions are operated on to produce further descriptions
- So: cognition = computing descriptions of descriptions of descriptions...
- Which is: **never-ending recursive processes of computation**

## 5. The Neurophysiological Architecture

### Evolution of the Computing Machinery
1. **Independent effectors** (protozoa): sensory-motor units directly coupled — perturbation causes contraction, displacement causes further perturbation. Already recursive.
2. **Separated sensation and action:** sensors connected to effectors by axons (degenerated muscle fibers). Introduces the concept of "signal."
3. **Internuncial neuron:** a cell between sensory and motor units, responsive to electrical activity. Introduces **computation** and non-trivial behavior.

### The Principle of Undifferentiated Encoding (detail)
- Neurons fire with magnitude independent of stimulus type — only frequency varies with intensity.
- There are ~100 million sensory receptors (external environment) but ~10 trillion synapses (internal environment).
- **We are 100,000 times more receptive to changes in our internal than in our external environment.**

### Retinal Computation Example
Von Foerster describes a two-layer neural network in the retina:
- Each receptor connects to three computing neurons: two excitatory synapses on the neuron directly below, one inhibitory synapse on each neighbor.
- Under uniform illumination: zero response (excitation and inhibition cancel).
- At an edge: the neuron at the boundary receives two excitatory but only one inhibitory signal — it fires.
- The network **computes edges**, independent of illumination intensity, independent of location.
- This is the computation of ABSTRACTS — "edge" is not in the stimulus, it is computed.

### Double Closure (The Torus)
The full nervous system has double closure:
1. **Horizontal closure:** sensory surface → neural computation → motor surface → (via environment) → sensory surface. External feedback loop.
2. **Vertical closure:** neural computation → neuropituitary → steroids into synaptic gaps → modifying the computation itself. Internal modulation loop.

Von Foerster represents this topologically as a **torus** (doughnut). The system recursively operates not only on what it "sees" but on its own operators.

### The Postulate of Cognitive Homeostasis
> "The nervous system is organized (or organizes itself) so that it computes a stable reality."

This postulate stipulates **autonomy** = self-regulation = regulation of regulation. The doubly-closed torus regulates its own regulation.

## 6. The Social Argument: Solipsism Overcome

The gentleman with the bowler hat insists he is the sole reality. But his imaginary universe contains apparitions that may make the same claim. By the **Principle of Relativity** (a hypothesis that doesn't hold for two instances together cannot hold for either), solipsism fails when we posit another autonomous organism.

This is not a logical necessity — it is a CHOICE. If I reject the Principle of Relativity, I am the center, my language is monologue, my logic is mono-logic. If I adopt it, neither I nor the other is the center. There must be a third reference point: the RELATION between Thou and I.

**"Reality = Community"**

## 7. The Two Imperatives

- **The Ethical Imperative:** "Act always so as to increase the number of choices."
- **The Aesthetical Imperative:** "If you desire to see, learn how to act."

These follow from the argument: autonomy implies responsibility. If I am the only one who decides how I act, I am responsible for my actions. The popular game of making someone else responsible ("heteronomy") is incompatible with the neurophysiological evidence.

## 8. Implications for Agent World-Models

### The "World Model" Is Computed, Not Received
An agent's world model is not a representation of an external world — it is the result of recursive computation by the agent's own architecture. The model IS the agent's way of organizing its sensorimotor experience.

### Undifferentiated Encoding in AI
Current AI systems also have undifferentiated encoding at some level: all inputs become vectors of numbers. The "quality" of the input (text vs. image vs. audio) is imposed by the architecture's interpretive structure, not by the input itself.

### The 100,000:1 Ratio
Von Foerster's insight that internal processing dwarfs external input applies directly to LLMs: the model's internal weights (~billions of parameters) vastly exceed any prompt's information content. The model's response is determined primarily by its internal structure, not by the input — exactly as constructivism predicts.

### Double Closure in Agent Architectures
Current agent architectures typically have only single closure (perception-action loops). The "vertical" closure — the system modifying its own computational parameters based on its own operation — is largely absent. Meta-learning and self-modification architectures attempt to add this second closure.

### Reality = Community
For multi-agent systems: "reality" is not what any single agent computes but what emerges from the relations between agents. Shared world models are negotiated, not discovered.

---

*Notes compiled 2026-03-12 from full text PDF (pespmc1.vub.ac.be, pdftotext extraction).*
