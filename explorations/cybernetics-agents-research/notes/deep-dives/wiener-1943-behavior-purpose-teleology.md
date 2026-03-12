# Behavior, Purpose and Teleology (1943)

**Authors:** Arturo Rosenblueth, Norbert Wiener, Julian Bigelow
**Published:** Philosophy of Science, Vol. 10, No. 1, pp. 18-24 (1943)
**DOI:** 10.1086/286788 (also 10.2307/184878)
**Access:** PDF available at https://courses.media.mit.edu/2004spring/mas966/rosenblueth_1943.pdf

## Context and Origin

This paper originated from WWII anti-aircraft fire control work. Warren Weaver of the
National Defense Research Council brought the authors together to work on targeting and
controlling anti-aircraft guns. Each member contributed something crucial to the idea of
information feedback.

The collaboration's origin: Wiener was attempting to develop an Anti-Aircraft Predictor.
When tracking a flying aircraft, you make observations to predict future position. Wiener
realized the *pilot's* response to gunfire must also be part of the prediction — leading to
a cycle of adjustments and re-adjustments. This feedback loop insight became foundational.

## Core Arguments

### Classification of Behavior

The paper proposes a **behavioristic** (black-box) approach to studying natural events:
- **Output** = any change produced in surroundings by the object
- **Input** = any event external to the object that modifies it

They classify behavior hierarchically:

```
Behavior
├── Active (output energized by object itself)
│   ├── Non-purposeful (random)
│   └── Purposeful (directed toward a goal)
│       ├── Non-feedback (no course correction)
│       └── Feedback (negative feedback = teleological)
│           ├── Non-predictive (acts on present error)
│           ├── First-order predictive (extrapolates)
│           └── Higher-order predictive (extrapolates extrapolations)
└── Passive
```

### Key Claim: Purpose = Negative Feedback

The revolutionary claim: "all purposeful behavior may be considered to require
negative feedback." Purpose is not a mystical property of living things — it is a
structural feature of any system (biological or mechanical) that uses error-correction
to move toward a goal.

### Teleology Rehabilitated

Before this paper, "teleology" (explanation by final causes/purposes) was considered
unscientific. Rosenblueth, Wiener, and Bigelow argue that teleological behavior can be
defined rigorously in terms of feedback mechanisms, making it fully compatible with
mechanistic science.

### Pathological Feedback

The paper describes what happens when feedback is excessive or delayed:
purpose tremor in neurological conditions (cerebellar disease). The system oscillates
around its goal instead of converging. This is the cybernetic explanation of ataxia.

## Relevance to AI Agent Architectures

This paper is the conceptual ancestor of:
1. **Goal-directed agents** — any agent architecture with a goal and error signal
2. **Feedback loops in RL** — reward signals as negative feedback toward desired behavior
3. **Hierarchical prediction** — higher-order predictive behavior maps to model-based planning
4. **The agent-environment loop** — the input/output behavioristic framing
5. **Failure modes** — oscillation around goals (purpose tremor) maps to instability in
   control-based agents, reward hacking, and mode collapse

## The Taylor Debate (1950)

Richard Taylor critiqued this paper in "Comments on a mechanistic conception of
purposefulness" (Philosophy of Science, 1950). Rosenblueth and Wiener responded with
"Purposeful and Non-Purposeful Behavior" (1950). Taylor then wrote a rejoinder.

The debate centered on whether feedback-based definitions truly capture "purpose" or
merely describe a mechanism that *mimics* purpose.

## Notable Quotes

From the paper's framework: the distinction between active/passive, purposeful/random,
and feedback/non-feedback behavior provides a taxonomy that remains applicable to
modern AI systems classification.
