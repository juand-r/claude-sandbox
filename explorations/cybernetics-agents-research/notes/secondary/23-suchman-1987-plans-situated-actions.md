# Plans and Situated Actions: The Problem of Human-Machine Communication

## Citation
Suchman, L. A. (1987). *Plans and Situated Actions: The Problem of Human-Machine Communication.* Cambridge University Press. 2nd edition: Suchman, L. A. (2007). *Human-Machine Reconfigurations: Plans and Situated Actions.* Cambridge University Press.

## Summary

A foundational critique of AI's planning paradigm, written from the perspective of ethnomethodology and workplace studies at Xerox PARC. Suchman argues that the dominant model in cognitive science and AI — that human action is governed by plans — fundamentally misrepresents how people actually act. Plans are not programs that control behavior; they are retrospective rationalizations or prospective resources that people draw on flexibly and contextually during situated activity.

## Key Arguments

1. **Two views of purposeful action.** Cognitive science and AI adopt the "planning model": action is the execution of pre-formed plans. Suchman draws on ethnomethodology, phenomenology, and anthropology to propose the alternative: action is fundamentally **situated** — constituted in real-time by the actor's ongoing relationship to the specific, concrete circumstances of the moment.

2. **Plans are weak resources, not strong directives.** People do make plans, but plans are vague, incomplete, and work only because actors continually improvise, interpreting and reinterpreting the plan in light of unfolding circumstances. A plan is like a sketch, not a blueprint. It tells you roughly where you're going, but the actual path is determined moment-by-moment.

3. **The user-photocopier study.** Suchman's empirical centerpiece: video analysis of novice users trying to operate a "smart" photocopier with an expert help system. The machine assumed a planning model — it predicted what the user would do based on an internal model of the task and provided help accordingly. Users did not follow the predicted path; they improvised, got confused, and the machine's "help" often made things worse. The system could not understand context, and its plan-based model of the user was systematically wrong.

4. **Mutual intelligibility.** The planning model claims that communication succeeds because agents can recognize each other's plans. Suchman argues the reverse: communication succeeds because of shared context, embodied cues, and ongoing interactive repair — resources that plan-based systems cannot access.

5. **The indexicality of action.** Actions derive their meaning from the specific context in which they occur. The same physical action (pressing a button) can mean different things in different contexts. Plans, being context-free abstractions, cannot capture this indexicality.

6. **Against AI's model of the user.** AI systems that model users as plan-executing agents will systematically fail because users do not act that way. Effective human-machine interaction requires systems that can cope with improvised, situated, context-dependent action — not just plan recognition.

## Connection to Cybernetics

- **Open-loop vs. closed-loop control.** The planning model is essentially open-loop: specify the action sequence in advance, then execute it. Suchman's situated action is closed-loop: act, observe the consequences, adjust. This is the cybernetic pattern.
- **The interactive repair process** — actors continually monitoring and adjusting their behavior based on feedback from the environment and other actors — is a multi-layered feedback system.
- **Second-order cybernetics.** Suchman's emphasis on the observer's role in constituting the meaning of action parallels second-order cybernetics' insistence that observation is participation. The meaning of an action is not in the action itself but in how it is observed and interpreted.
- **Ashby's black box.** Suchman's critique of the "user model" parallels the cybernetic insight that you cannot build a complete internal model of a complex system (the user). You can only regulate your relationship to it through feedback.

## Relevance to Agent Design

1. **LLM agents as plan-executing systems.** Modern LLM agents that generate multi-step plans and execute them are implementing exactly the paradigm Suchman critiqued. Her prediction: they will fail when faced with the situatedness, indexicality, and improvisation of real tasks. This is exactly what happens.

2. **The user-model problem.** LLM agents that try to model user intent (through system prompts, conversation history, user profiles) face Suchman's critique: user intent is not a fixed mental state that can be modeled; it is constituted in the ongoing interaction and shifts moment-by-moment.

3. **Interactive repair for agents.** Suchman's analysis suggests that the most important capability for an agent is not planning but **interactive repair** — the ability to detect when things have gone wrong and adjust course through interaction with the user and environment. This supports conversational agent designs that check in with users rather than executing autonomously.

4. **Situated tool use.** Suchman's framework suggests that tool use by agents should be situated — determined by the specific context of the current task — rather than planned in advance. The agent should decide which tool to use based on what just happened, not based on a pre-formed plan.

5. **Against comprehensive user modeling.** Suchman would be skeptical of attempts to build detailed user models or personas for LLM agents. Instead, she would advocate for systems that can cope with ambiguity, ask clarifying questions, and adapt to the user's actual behavior rather than predicted behavior.

6. **Ethnomethodological evaluation.** Suchman's approach suggests that agent evaluation should include ethnomethodological analysis — detailed study of how real users actually interact with agents, not just benchmark scores. The gap between planned and situated use of AI agents is likely large and systematically overlooked.

## Historical Note

Though published in 1987 (thus technically outside the 1990s decade), Suchman's work was enormously influential throughout the 1990s and is cited by nearly every work in the situated cognition and behavior-based AI traditions. The 2nd edition (2007) updated the arguments for the era of ubiquitous computing. Its inclusion here is warranted by its foundational role in the intellectual movement that produced the other 1990s works in this series.
