# Wiener and Communication Theory (Relation to Shannon)

## The Two 1948 Publications

In 1948, two foundational texts were published almost simultaneously:

1. **Wiener:** *Cybernetics, or Control and Communication in the Animal and
   the Machine* (Hermann & Cie, Paris / Technology Press, MIT)
2. **Shannon:** "A Mathematical Theory of Communication" (Bell System
   Technical Journal)

Both initiated new scientific frameworks — cybernetics and information theory —
and both have been far-reaching in technological development.

## The Shannon-Wiener Relationship

### Mutual Credit

Shannon emphasized that communication theory owes a great debt to Wiener for
much of its basic philosophy. Wiener, on the other hand, pointed out that
Shannon's early work on switching and mathematical logic antedated his own
interest in the field, and generously credited Shannon for independent
development of fundamental aspects such as the introduction of entropic ideas.

### Division of Labor

- **Shannon** was primarily concerned with engineering communication —
  channel capacity, coding, compression
- **Wiener** was more concerned with biological applications — central
  nervous system phenomena, sensory processing, homeostasis

### Common Ancestor: Boltzmann

Von Neumann pointed out that both connect back to Boltzmann's observation
(1894) that entropy is related to "missing information." Shannon's work
also connects to Nyquist (1924) and Hartley (1928), both at Bell Labs.

## Wiener's Information Measure

In the Yellow Peril (1949), Wiener described information as "the mathematical
likelihood of a particular message emerging from a larger measure or
probability of possible messages." This parallels Shannon's entropy:

H = -sum p(x) log p(x)

Wiener arrived at similar formulations through his work on communication
and filtering, while Shannon arrived through his work on coding and
channel capacity.

### Key Difference

Wiener defined the amount of information as the *negative* of entropy
(negentropy), emphasizing that information is the opposite of disorder.
Shannon defined entropy directly as information content. The mathematics
is equivalent; the sign convention and philosophical interpretation differ.

## Warren Weaver's Role

Shannon's work might not have become as famous without Warren Weaver, who:
- Wrote "The Mathematics of Communication" for Scientific American
- Later expanded it as "Recent Contributions to the Mathematical Theory
  of Communication" (ETC: A Review of General Semantics, Vol. 10, No. 4,
  Summer 1953, pp. 261-281)
- Re-interpreted Shannon's mathematical framework for a broader audience

## "Cybernetics in History"

This essay appears as Chapter I of *The Human Use of Human Beings* (1950),
not as a standalone paper. Wiener explored the broader implications of the
theory of messages, encompassing language, machinery control, computing,
psychology, and scientific methodology. It was reprinted in *Multimedia:
From Wagner to Virtual Reality* (Packer & Jordan, 2001).

## Wiener's "Cybernetics" Essay in Scientific American (1948)

A popularization of cybernetic ideas published in Scientific American,
Vol. 179, No. 5 (November 1948). This brought cybernetics to a general
scientific audience.

## Relevance to AI Agent Architectures

- **Information as the fundamental currency** — both Wiener and Shannon
  established that information, not energy, is the key quantity in
  communication and control systems
- **Channel capacity** — limits on how much information an agent can
  process per unit time (bounded rationality)
- **Entropy and uncertainty** — Shannon entropy measures uncertainty
  in agent observations; Wiener's negentropy measures how much
  information reduces uncertainty
- **Coding theory** — how agents should encode/compress information
  for efficient communication and storage
- **The cybernetics-information theory bridge** — Wiener showed that
  control IS communication; Shannon showed that communication has
  fundamental limits. Together: agent behavior is fundamentally
  constrained by information-theoretic limits.
