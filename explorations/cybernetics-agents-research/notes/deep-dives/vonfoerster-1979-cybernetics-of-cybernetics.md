# Von Foerster (1974/1979) — Cybernetics of Cybernetics

## Citation

Two distinct publications share this title:

1. **The 1974 Book**: Von Foerster, H. et al. (1974). *Cybernetics of Cybernetics, or, the Control of Control and the Communication of Communication*. BCL Report 73.38, Biological Computer Laboratory, University of Illinois, Urbana, IL. 2nd ed. 1995, Future Systems, Minneapolis, 497 pp.

2. **The 1979 Paper**: Von Foerster, H. (1979). "Cybernetics of Cybernetics." In K. Krippendorff (Ed.), *Communication and Control in Society*, Gordon and Breach, New York, pp. 5-8. Reprinted in *Understanding Understanding* (Springer, 2003), ch. 13.

## Source Status
- 1979 paper full text: https://cepa.info/fulltexts/1707.pdf
- Also available at: https://sites.evergreen.edu/arunchandra/wp-content/uploads/sites/395/2018/05/cybernetics.pdf
- 1974 book: not freely available online. Physical copies exist in libraries.

## The 1974 Book

### What It Was

The book was not a monograph by von Foerster alone. It was a collaborative production from his "Cybernetics of Cybernetics" seminar at UIUC — a collection of papers by distinguished cyberneticians with graphic commentaries and original texts and definitions composed by students. It was catalogued as BCL Report 73.38.

This was itself an exercise in second-order cybernetics: the course was about cybernetics, and the course's product (the book) was itself a cybernetic system — a self-referential artifact where the study of cybernetics produced a cybernetic object.

### Historical Note on the Title

The phrase "cybernetics of cybernetics" emerged from a collaboration between von Foerster and Margaret Mead. Glanville notes: "Mead provoked the approach, but in actuality von Foerster gave her the title and the briefing for her keynote." With Mead unreachable due to fieldwork, von Foerster titled the paper himself, "a title that perhaps emphasised his concerns more than Mead's."

## The 1979 Paper: Core Content

### The Fundamental Distinction

Von Foerster defines:
- **First-order cybernetics**: the cybernetics of observed systems
- **Second-order cybernetics**: the cybernetics of observing systems

This is not a slogan. It is a formal distinction with mathematical and logical consequences.

### First-Order Cybernetics

The observer stands outside the system. The system is modeled as:

```
input -> [black box] -> output
```

The observer describes the system's behavior without the observer's properties entering the description. The descriptions are "objective" in the classical sense. The observer is a transparent recording device.

This is the cybernetics of Wiener, Ashby, and the early Macy conferences. It produced: feedback control theory, information theory, automata theory, game theory.

### Second-Order Cybernetics

The observer is recognized as part of the system being observed. This creates self-reference: the description includes the describer. The model is:

```
observer <-> system <-> observer
```

Or more precisely, the observer IS part of the system, and the "system" includes the observer's act of observation. This creates circular causality with no external vantage point.

### The Two Circularities

1. **Circularity of the observed system**: e.g., thermostat — sensor causes heater to switch, heater causes sensor to change. Circular causality with no primary cause. This is already handled by first-order cybernetics.

2. **Circularity of the act of observing**: the observer observes systems that include the observer. The observation changes what is observed, which changes the observer, which changes the observation... This is the specifically second-order problem.

### Consequences

1. **Closure**: The system of observation is operationally closed. No external reference point.
2. **Recursion**: Descriptions are descriptions of descriptions. Computations compute computations.
3. **Undecidability**: Certain questions become formally undecidable within the system.
4. **Responsibility**: The observer who cannot claim objectivity must take responsibility for their descriptions.

### Double Closure

Von Foerster formalized cognitive/communicative systems through **double closure**, topologically represented as a torus:

- **First closure**: the process of making a distinction (Spencer-Brown's mark)
- **Second closure**: the process by which the distinction becomes a stable, memorable entity — a concept that "remembers itself"

Communication is formally defined as "the eigenbehavior of a recursively operating system that is doubly closed onto itself."

## Relevance to Agent Architectures

### The Core Mapping

| First-Order Cybernetics | Second-Order Cybernetics |
|---|---|
| External observer designs agent | Agent must model itself as part of its environment |
| Agent modeled as input -> output | Agent-environment modeled as circular, coupled system |
| Objective evaluation metrics | Metrics are part of the system being measured |
| RLHF: human provides external signal | Self-play / self-improvement: agent evaluates itself |
| Open-loop planning | Closed-loop, reflexive planning |

### Agent Self-Models

Second-order cybernetics is directly relevant to agents that must model themselves:
- **Meta-learning**: learning to learn = computing computations
- **Self-evaluation**: the agent evaluates its own outputs (second-order observation)
- **Constitutional AI**: the agent applies principles to itself (self-reference)
- **Recursive self-improvement**: the hallmark of second-order cybernetic systems

### The Objectivity Problem in AI Evaluation

Von Foerster's critique of objectivity maps to a real problem in AI: evaluation metrics are not external to the system. When we evaluate a language model on benchmarks, the benchmarks were created by humans using language, and the model was trained on human language — the evaluation is not independent of the system being evaluated. This is structurally identical to the second-order cybernetics problem.

### Double Closure in Transformers

A transformer has something like double closure:
- First closure: attention (making distinctions between tokens)
- Second closure: layer-to-layer processing (stabilizing distinctions into representations)

The output is an eigenbehavior of this doubly-closed recursive process.

## Key Formulations

- First-order: cybernetics of observed systems; second-order: cybernetics of observing systems
- The observer is part of the system — this is not optional philosophy but a structural fact
- Double closure (torus topology) as the condition for stable cognition/communication
- Communication = eigenbehavior of a doubly-closed recursive system
