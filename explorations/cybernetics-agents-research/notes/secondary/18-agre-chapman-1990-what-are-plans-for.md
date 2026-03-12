# What Are Plans For?

## Citation
Agre, P. E. & Chapman, D. (1990). "What Are Plans For?" In P. Maes (Ed.), *Designing Autonomous Agents: Theory and Practice from Biology to Engineering and Back* (pp. 17-34). MIT Press. Originally: A.I. Memo 1050a, MIT AI Lab, 1989. Also in *Robotics and Autonomous Systems*, 6, 17-34.

## Summary

A philosophical and technical critique of the "plan-as-program" view dominant in classical AI planning. Agre and Chapman distinguish two views of plans: (1) **plan-as-program** — a plan is an effective procedure that, when executed, produces the desired behavior; (2) **plan-as-communication** — a plan is like a natural-language instruction that must be interpreted in context, with gaps filled by situated improvisation. They argue for the second view and began building computational models based on it.

## Key Arguments

1. **Plans do not fully determine behavior.** Classical AI planning (STRIPS, etc.) treats plans as complete specifications: execute the plan steps and the goal is achieved. Agre and Chapman argue this is unrealistic. Real plans are partial, indexical, and require ongoing interpretation in context. "What plans are like depends on how they're used."

2. **Situated action, not plan execution.** Drawing on Suchman (1987), they argue that real-world activity is fundamentally improvised. Plans are resources for action, not programs that control it. An agent uses a plan the way a cook uses a recipe — as a rough guide, not as a program to execute literally.

3. **Deictic representations.** Instead of maintaining a complete world model with object identities, agents should use "deictic" (action-oriented, role-based) representations. For instance, "the-thing-I'm-reaching-for" rather than "object-37-at-coordinates-(x,y,z)." This reduces representational burden and keeps the agent coupled to its current situation.

4. **Critique of STRIPS-style planning.** STRIPS assumes: (a) complete world state is known, (b) actions have deterministic effects, (c) nothing changes while you plan. All three assumptions fail in real environments. Plans that depend on these assumptions are brittle.

5. **Plans emerge from activity.** Plans are not constructed before action and then executed. They are retrospective rationalizations or prospective sketches that become concrete only in the course of activity. This inverts the classical sequence: activity first, plans second.

## Connection to Cybernetics

- **Plans as open-loop control.** Classical AI planning is essentially open-loop control: specify the sequence of actions in advance and execute them without feedback. Agre and Chapman's critique is fundamentally cybernetic: effective control requires closed-loop feedback, not pre-specified action sequences.
- **Situated action = closed-loop control.** Their alternative — situated, improvisational action guided by environmental feedback — is the cybernetic pattern.
- **Deictic representations** reduce the variety the agent must manage internally, consistent with the Law of Requisite Variety applied parsimoniously.
- **Regulation, not execution.** Cybernetics frames the agent's task as regulation (maintaining desired relationships with the environment) rather than execution (performing a pre-specified sequence). Agre and Chapman's framework is regulatory.

## Relevance to Agent Design

1. **LLM agents as plan generators.** Modern LLM agents generate multi-step plans and then execute them. This is exactly the "plan-as-program" model that Agre and Chapman critiqued. Their prediction: these plans will break on contact with reality. This is exactly what happens — LLM agents that generate complete plans before acting are brittle.

2. **ReAct as plan-as-communication.** The ReAct framework (Thought → Action → Observation, repeated) is closer to Agre and Chapman's plan-as-communication model: the agent generates a partial plan (one step), executes it, observes the result, and then generates the next step. The "plan" emerges from the activity.

3. **The case for incremental planning.** Agre and Chapman's work provides theoretical justification for iterative, one-step-at-a-time agent architectures over batch-plan-then-execute architectures. This has been empirically confirmed: ReAct-style agents outperform single-shot planners on complex tasks.

4. **Deictic representations for tool use.** Rather than maintaining a complete model of available tools and their capabilities, agents could use deictic references: "the-tool-I-used-last-time-for-this-kind-of-task" or "the-database-with-the-information-I-need-now." This is more robust than maintaining exhaustive tool catalogs.

5. **Plans as communication between agents.** In multi-agent systems, Agre and Chapman's framework suggests that plans exchanged between agents should be treated as natural-language communications (to be interpreted in context), not as programs (to be executed literally). This has implications for how agents coordinate.
