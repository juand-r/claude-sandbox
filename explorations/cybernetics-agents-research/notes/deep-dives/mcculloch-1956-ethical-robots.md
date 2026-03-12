# McCulloch — "Toward Some Circuitry of Ethical Robots" (1956)

**Author:** Warren S. McCulloch
**Full title:** "Toward Some Circuitry of Ethical Robots or An Observational Science of the Genesis of Social Evaluation in the Mind-Like Behavior of Artifacts"
**Published:** Acta Biotheoretica, Vol. 11, pp. 147-156, 1956
**DOI:** 10.1007/BF01557008
**Full text:** Behind paywall (Springer).

## The Question

Can a machine develop ethical or social values? And if so, what circuit would enable it?

McCulloch argued yes — and proposed a concrete mechanism.

## The Argument

### Learning by Playing
McCulloch described a circuit that could:
1. Be given the rules of a game (like chess) only **ostensibly** — i.e., by playing against opponents
2. Learn which moves are legal (opponents quit when you make an illegal move)
3. Learn which moves lead to winning
4. Develop **shared values** with the other players through this interaction

The key insight: **values emerge from interaction**. The machine doesn't need to be pre-programmed with values. It learns them through social gameplay — through the feedback of other agents quitting, continuing, winning, losing.

### Social Values
McCulloch claimed the values that emerge from this process are **social** in the strongest sense: they are shared by the players. The value doesn't exist in any single player; it exists in the interaction pattern between players.

## Why This Is Remarkable (Written in 1956)

1. **Reinforcement learning from human feedback (RLHF)**: McCulloch described a machine that learns values by playing games against opponents who provide implicit feedback. This is conceptually identical to modern RLHF, where AI models learn from human preference signals.

2. **Emergent social norms**: The idea that shared values emerge from repeated interaction is now studied in multi-agent reinforcement learning (MARL), where agents develop conventions and norms through self-play.

3. **AI alignment**: The paper addresses, in 1956, the core question of AI alignment — how to get machines to have the right values. McCulloch's answer: they learn values through social interaction, not through top-down programming.

4. **Game-theoretic grounding**: Values are grounded in game-playing, connecting ethics to game theory — an approach that modern AI safety researchers also explore.

## Relevance to Agent Architectures

- **Value alignment through interaction**: Agents in a multi-agent system can develop shared norms through repeated interaction, without explicit programming of those norms
- **Social evaluation**: An agent's behavior is "ethical" insofar as it is consistent with the social evaluations that emerge from multi-agent interaction
- **Observation-based learning**: The paper proposes an "observational science" of value genesis — studying how values emerge rather than prescribing them

## Supported By
Signal Corps, Office of Scientific Research (ARDC), Office of Naval Research, Bell Telephone Laboratories.

## Builds On
- McCulloch & Pitts (1943) — the neural net formalism
- McCulloch (1945) — heterarchy of values (values don't need to form a hierarchy)
