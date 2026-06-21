# References & Related Work

Background literature for the phenomena explored in this project, and why each
is relevant. These frame the concepts and (for E18) the spiral model; they are
not inputs to the simulations. The same list appears at the bottom of
`artifact.html`. Citation details are from memory --- verify before formal use.

### Cellular automata (the transformation primitive)

- **Wolfram, "Statistical mechanics of cellular automata," Rev. Mod. Phys. 55
  (1983); *A New Kind of Science* (2002).** Elementary CA and the 0--255 rule
  numbering used as each ring's transformation rule.
- **Cook, "Universality in elementary cellular automata," Complex Systems 15
  (2004).** Rule 110 is Turing-complete --- a single ECA rule can compute --- yet
  a single 8-bit rule is still not a *composable* substrate (E15, the complexity
  ceiling).
- **Langton, "Computation at the edge of chaos," Physica D 42 (1990).** The
  order/chaos boundary; frames E9's edge-of-chaos sweet spot (structured
  sustained novelty).

### Heredity, mutation, self-organization

- **Eigen, "Selforganization of matter and the evolution of biological
  macromolecules," Naturwissenschaften 58 (1971).** Quasispecies and the error
  threshold: why "zero mutation does not exist" yet too much mutation dissolves
  heredity (E3; the mutation/heredity tension that runs through the project).
- **Maturana & Varela, *Autopoiesis and Cognition* (1980).** Autopoiesis ---
  active self-maintenance --- the property probed (and not found) for the
  emergent domains in E5/E5b.
- **Kauffman, *The Origins of Order* (1993); autocatalytic sets.** Mutual-
  production cycles; frames the E1 finding that transformation builds hubs but
  suppresses directed cycles, and the autopoiesis question.

### Cyclic competition and spatial pattern (E11/E16/E18)

- **May & Leonard, "Nonlinear aspects of competition between three species,"
  SIAM J. Appl. Math. 29 (1975).** Foundational rock-paper-scissors dynamics.
- **Kerr, Riley, Feldman & Bohannan, "Local dispersal promotes biodiversity in
  a real-life game of rock-paper-scissors," Nature 418 (2002).** Local
  interaction maintains coexistence; mirrors our finding that spatial separation
  (not self-maintenance) sustains the ecology (E5, E16).
- **Reichenbach, Mobilia & Frey, "Mobility promotes and jeopardizes
  biodiversity in rock-paper-scissors games," Nature 448 (2007).** The
  spiral-wave result: spirals need an intermediate *mobility* (exchange) term.
  Exactly the model in E18, and why the no-mobility E16/E17 produced none.
- **Turing, "The chemical basis of morphogenesis," Phil. Trans. R. Soc. B 237
  (1952).** Reaction-diffusion pattern formation; the lineage of emergent
  spatial patterns from local rules.

### Artificial life / evolution of complexity (E13--E15, option 3)

- **Ray, "An approach to the synthesis of life" (Tierra), Artificial Life II
  (1991).** Self-replicating machine-code organisms seeded from an ancestor; the
  template for the option-3 plan (self-replication must usually be seeded).
- **Lenski, Ofria, Pennock & Adami, "The evolutionary origin of complex
  features," Nature 423 (2003) (Avida).** Complex functions evolve when rewarded
  via logic tasks on a composable instruction set; motivates E15's task and the
  option-3 composable substrate.

### Methods

- **Moran, "Notes on continuous stochastic phenomena," Biometrika 37 (1950).**
  Moran's I spatial autocorrelation --- used early, then flagged as wrong for
  categorical rule fields (Reflection R1).
