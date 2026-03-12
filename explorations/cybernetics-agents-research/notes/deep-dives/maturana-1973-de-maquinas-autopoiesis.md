# Autopoiesis: The Organization of the Living (1973)

## Citation
Maturana, H.R. & Varela, F.J. (1973). *De Maquinas y Seres Vivos: Una teoria sobre la organizacion biologica*. Editorial Universitaria, Santiago.

English translation: "Autopoiesis: the Organization of the Living," reprinted in Maturana & Varela (1980), *Autopoiesis and Cognition: The Realization of the Living*, pp. 59-134. Dordrecht: D. Reidel (Boston Studies in the Philosophy of Science, Vol. 42).

## Related Paper
Varela, F.G., Maturana, H.R. & Uribe, R. (1974). "Autopoiesis: the organization of living systems, its characterization and a model." *Biosystems* 5(4), 187-196. DOI: 10.1016/0303-2647(74)90031-8. Full text PDF: https://monoskop.org/images/d/dd/Varela_Maturana_Uribe_1974_Autopoiesis.pdf

## Context
The 1973 book is the original Spanish-language publication where the term "autopoiesis" was first used in print. The word was coined by Maturana (with input from a friend who suggested the Greek roots) to capture "the central feature of the organization of the living, which is autonomy." The 1974 *Biosystems* paper is the first English-language journal publication of the concept, and includes a computer simulation model.

A second edition preface was later published: Maturana, H.R., Paucar-Caceres, A. & Harnden, R. (2011). "Preface to the Second Edition of De Maquinas y Seres Vivos -- Autopoiesis." *Constructivist Foundations* 6(3), 293-306.

## The Formal Definition of Autopoiesis
An autopoietic machine is a machine organized as a network of processes of production (transformation and destruction) of components that:

1. Through their interactions and transformations continuously regenerate and realize the network of processes that produced them; AND
2. Constitute the machine as a concrete unity in the space in which they exist by specifying the topological domain of its realization as such a network.

(From Maturana & Varela, 1980, p. 78)

### Two Jointly Necessary Conditions
- **Self-regeneration (process closure)**: Components regenerate the network that produces them. Circular causality.
- **Boundary specification (topological closure)**: Components constitute the system as a concrete unity by specifying a physical boundary. The boundary is not externally imposed; it emerges from the same processes it encloses.

## The Six Decisional Rules (Varela, Maturana & Uribe, 1974)
To determine whether a system is autopoietic, an observer must verify six properties by answering six basic questions through observation of the system's domain of existence:

1. **Identifiable boundary**: Can a boundary be identified that separates the system from its environment?
2. **Constitutive elements**: Can constitutive elements of the system be identified?
3. **Mechanistic system**: Is the system a mechanistic system (i.e., does it operate through determinate interactions of components)?
4. **Boundary produced by system**: Are the elements that constitute the boundary produced by interactions of elements of the system?
5. **Components produced by system**: Are the elements that constitute the boundary produced as a result of the production relations of the system?
6. **Condition 4+5 necessary**: If conditions 4 and 5 are not satisfied, is the system not autopoietic?

Note: The precise wording of the six criteria is in the original 1974 paper. The above is reconstructed from secondary sources. The criteria require close observation of "intra-boundary" phenomenology: components' self-production, spatial distribution, and temporal occurrence of interaction events.

## Autopoietic vs. Allopoietic
- **Autopoietic**: The system's sole product is its own organization. A cell produces itself.
- **Allopoietic**: The system produces something other than itself. A factory produces cars, not more factories.

This is the fundamental distinction. Current AI systems are allopoietic -- they produce outputs (text, images, actions) that are not themselves.

## The Computer Simulation (1974 Paper)
Varela, Maturana & Uribe presented a minimal computer model satisfying autopoietic conditions: a 2D cellular automaton with three types of elements (substrate, catalyst, link) where catalysts transform substrates into links, and links form a boundary that entraps catalysts. The system demonstrates self-repair: when the boundary is breached, new links are produced to repair it.

This model is minimal and abstract but demonstrates the formal possibility of autopoietic organization in a non-biological substrate -- though Maturana later insisted that genuine autopoiesis requires molecular-level realization.

## Key Theoretical Claims
- Autopoiesis is the necessary and sufficient condition for the organization of the living
- Organization is invariant (defines identity); structure varies continuously
- Living systems are autonomous -- their organization is self-determined
- Reproduction and evolution are secondary to autopoiesis -- a living system need not reproduce to be alive

## Implications for Agent Autonomy
- The autopoietic definition provides a rigorous criterion for distinguishing genuine autonomy from mere behavioral autonomy
- Current AI agents fail the autopoietic test: they do not produce their own components, do not generate their own boundaries, and are maintained externally
- The 1974 computer simulation suggests autopoiesis might be substrate-independent in principle, but this remains contested
- The distinction between autopoietic and allopoietic is directly relevant to classifying AI agent architectures
