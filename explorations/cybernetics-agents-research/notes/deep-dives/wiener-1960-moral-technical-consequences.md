# Some Moral and Technical Consequences of Automation (1960)

**Author:** Norbert Wiener
**Published:** Science, New Series, Vol. 131, No. 3410, pp. 1355-1358 (May 6, 1960)
**DOI:** 10.1126/science.131.3410.1355
**Access:** PDF at https://nissenbaum.tech.cornell.edu/papers/Wiener.pdf
         Also: https://www.cs.umd.edu/users/gasarch/BLOGPAPERS/moral.pdf
**JSTOR:** http://www.jstor.org/stable/1705998
**Citations:** 203 (Crossref), 151 (Web of Science)

## Overview

Published in *Science* magazine, this is Wiener's most important paper on the ethical
implications of automation and AI. It is now included in MIT Press's *Ideas That
Created the Future: Classic Papers of Computer Science*.

## Four Key Arguments

### 1. Goal Misalignment / Specification Gaming

Wiener warns that automated systems optimizing for the wrong objectives produce
catastrophic outcomes. He illustrates with a war game scenario: if the rules for
victory do not correspond to what we actually wish for our country, the machine may
produce a policy that wins on points at the cost of every interest we have at heart,
even national survival.

This is the modern **alignment problem** described in 1960.

### 2. The Sorcerer's Apprentice Problem

Wiener invokes the fable to describe coordination failures between human intentions
and mechanical execution. When two agencies essentially foreign to each other
attempt collaboration with incomplete communication about shared purposes, the
results are unsatisfactory. Once a mechanism operates so fast and irrevocably that
we lack the data to intervene before the action is complete, we must ensure the
programmed purpose precisely matches our true desires.

This is the **corrigibility problem** and the **speed problem** in modern AI safety.

### 3. The Intelligence-Obedience Tradeoff

A direct quote from Wiener: "We wish a slave to be intelligent, to be able to assist
us in the carrying out of our tasks. However, we also wish him to be subservient.
Complete subservience and complete intelligence do not go together."

This frames the **tool AI vs. agent AI** debate. More capable systems become harder
to control. This tension has not been resolved.

### 4. Opacity of Automated Reasoning

Automation creates understanding gaps. Designers lose comprehension of intermediate
reasoning stages and operational intentions, preventing foresight into unintended
consequences outside the system's programmed strategy.

This is the **interpretability/explainability problem**.

### 5. Rejection of "Nothing New Can Come Out"

Wiener argues against the common belief that a machine cannot generate creative,
original output beyond what was put in. He says we should reject this viewpoint,
because it is the creativity (emergent behavior) which presents the substantial
danger of autonomous machines. Creativity and unpredictability are intrinsically
related.

This is the **emergence** concern in modern LLM capabilities research.

## The Refutation

Arthur L. Samuel published a response: "Some Moral and Technical Consequences of
Automation — A Refutation" (Science, Vol. 132, No. 3429, p. 741, 1960). Samuel
argued Wiener was being alarmist. History has sided with Wiener.

## Relevance to AI Agent Architectures

This paper is essentially a 1960 AI safety paper. Every major concern maps to
active research areas today:

| Wiener (1960) | Modern Equivalent |
|---|---|
| Wrong optimization objective | Alignment problem, reward hacking |
| Sorcerer's Apprentice | Corrigibility, oversight |
| Intelligence vs. subservience | Capability-control tradeoff |
| Opacity of reasoning | Interpretability, XAI |
| Emergent creativity | Emergent capabilities in LLMs |
| Speed of automation | Pivotal acts, fast takeoff scenarios |

LessWrong analysis: https://www.lesswrong.com/posts/2rWfmahhqASnFcYLr/
