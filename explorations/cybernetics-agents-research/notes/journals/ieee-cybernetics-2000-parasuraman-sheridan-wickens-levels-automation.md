# Parasuraman, Sheridan & Wickens (2000) - A Model for Types and Levels of Human Interaction with Automation

## Citation
Parasuraman, R., Sheridan, T.B., and Wickens, C.D. (2000). "A Model for Types and Levels of Human Interaction with Automation." *IEEE Transactions on Systems, Man, and Cybernetics -- Part A: Systems and Humans*, Vol. 30, No. 3, pp. 286-297. DOI: 10.1109/3468.844354

## Journal Details
- **Journal:** IEEE Transactions on Systems, Man, and Cybernetics -- Part A: Systems and Humans
- **Volume/Issue:** 30(3), May 2000
- **Pages:** 286-297
- **Author Affiliations:** Catholic University of America (Parasuraman), MIT (Sheridan), University of Illinois (Wickens)

## Access
- IEEE Xplore: https://ieeexplore.ieee.org/document/844354
- Highly cited: one of the most influential papers in human-automation interaction
- Could not access full PDF (ResearchGate blocked)

## Key Arguments

### The Central Question
Given that automation can now be applied to virtually all aspects of human-machine systems, which system functions should be automated, and to what extent?

### Four Types of Automation (Information Processing Stages)
Automation can be applied to four broad classes of functions, mapping to stages of human information processing:

1. **Information Acquisition:** Sensing and registration of input data. Automation ranges from manual scanning to computer-highlighted displays.
2. **Information Analysis:** Cognitive processing -- working memory, inference. Automation ranges from unaided analysis to computer prediction and expert system recommendations.
3. **Decision and Action Selection:** Choosing among alternatives. Automation ranges from human selects action to computer selects action (with or without human approval).
4. **Action Implementation:** Executing the chosen action. Automation ranges from manual control to full computer control.

### Ten Levels of Automation (LOA)
For each function type, automation can range from fully manual (Level 1) to fully automatic (Level 10):

1. Computer offers no assistance; human does everything
2. Computer offers a complete set of decision alternatives
3. Computer narrows selection to a few alternatives
4. Computer suggests one alternative
5. Computer executes that suggestion if human approves
6. Computer allows human a restricted time to veto before execution
7. Computer executes automatically, then informs the human
8. Computer informs the human only if asked
9. Computer informs the human only if it decides to
10. Computer decides everything, acts autonomously, ignores the human

### Key Insight: Independence of Types and Levels
The types and levels are independent dimensions. A system might be highly automated in information acquisition but manually controlled in decision selection. This creates a matrix of possibilities rather than a single automation spectrum.

### Automation Does Not Simply Replace
A critical argument: automation does not merely supplant human activity but changes it. Automation imposes new coordination demands and can create new failure modes (automation complacency, skill degradation, mode confusion).

## Relevance to Agent Design

### The Autonomy Spectrum for AI Agents
This framework provides a principled way to think about how much autonomy to give AI agents. Current LLM agents span the full range:
- **Level 2-3:** Agent suggests options (copilot mode)
- **Level 4-5:** Agent suggests and executes with approval (tool-calling with confirmation)
- **Level 7-8:** Agent acts autonomously, reports results (autonomous agent mode)
- **Level 10:** Fully autonomous (unsupervised agent)

### The Four-Stage Model Maps to Agent Architecture
1. **Information Acquisition** -> Agent's perception/retrieval (RAG, web search, tool observation)
2. **Information Analysis** -> Agent's reasoning (chain-of-thought, inference)
3. **Decision/Action Selection** -> Agent's planning (which tool to call, what action to take)
4. **Action Implementation** -> Agent's execution (tool calls, code execution)

Different agent designs automate these stages to different degrees.

### Human-in-the-Loop Design
The framework provides vocabulary for designing human-agent interaction:
- When should the agent ask for approval? (Levels 4-5)
- When should it just inform? (Level 7)
- When should it act silently? (Level 9-10)

### The Warning About Over-Automation
Parasuraman et al.'s warning that automation changes rather than replaces human activity is directly applicable to AI agents. Over-automating can lead to:
- Users losing situational awareness
- Inability to intervene effectively when agents fail
- Skill degradation in the automated tasks
- "Automation bias" -- uncritically accepting agent outputs

## Connections to Other Work
- Extends Sheridan's earlier (1992) levels of automation framework
- Connects to Albus's hierarchical architecture (different levels of autonomy at different hierarchy levels)
- Relates to Beer's VSM: System 5 (policy) decides what to automate and what remains human
- Connects to Ashby's requisite variety: the human-automation allocation must match the variety of the environment
- Influences modern human-AI interaction design (e.g., Microsoft's "Guidelines for Human-AI Interaction")

## Key Insight for Our Research
The independence of automation types and levels means agent designers face a multi-dimensional design space, not a simple "more or less autonomous" choice. A well-designed agent might be highly autonomous in information gathering but require human approval for action execution. This maps to cybernetic principles: different feedback loops (tight/loose) at different levels of the system.
