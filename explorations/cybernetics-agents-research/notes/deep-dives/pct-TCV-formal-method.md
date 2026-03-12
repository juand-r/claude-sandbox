# The Test for the Controlled Variable (TCV) — Formal Method

## Key Citations
- Powers, W.T. (1978). Quantitative analysis of purposive systems. *Psychological Review*, 85, 417-435. (first formal description)
- Marken, R.S. (2009). You say you had a revolution: Methodological foundations of closed-loop psychology. *Review of General Psychology*, 13, 137-145.
- Marken, R.S. (2013). Testing for controlled variables: A model-based approach to determining the perceptual basis of behavior. *Attention, Perception, & Psychophysics*. DOI: 10.3758/s13414-013-0552-8
- Marken, R.S. (2014). *Doing Research on Purpose*. New View Publications.
- Runkel, P.J. (2003/2007). *Casting Nets and Testing Specimens*. (provides philosophical context)

## Access
- Marken 2013: https://link.springer.com/article/10.3758/s13414-013-0552-8

## The Logic

### Premise
A variable that is under control will be **protected from disturbance** by the actions of a control system. This is the defining property of a controlled variable.

### Implication
If you disturb a hypothesized controlled variable:
- **Control system present:** The organism acts to counter the disturbance. The variable remains near its reference value. There is a near-zero correlation between disturbance and the controlled variable.
- **No control system present:** The disturbance has its full effect on the variable. The variable changes freely. There is a high correlation between disturbance and the variable.

## The Formal Procedure

### Step 1: Hypothesize
Choose a candidate perceptual variable that the organism might be controlling. This requires insight — you have to guess what the organism is perceiving and maintaining.

### Step 2: Disturb
Apply a disturbance to the hypothesized variable. The disturbance must be something that would alter the perception if left uncorrected. It should be:
- Independent of the organism's output (exogenous)
- Measurable
- Variable over time (so you can correlate)

### Step 3: Observe
Record both the disturbance and the state of the hypothesized controlled variable over time.

### Step 4: Assess
Measure the **stability** of the hypothesized controlled variable in the face of disturbance:
- High stability (low variance despite disturbance) → controlled variable hypothesis supported
- Low stability (variance tracks disturbance) → hypothesis refuted

### Step 5: Iterate
If the hypothesis is refuted, try a different candidate variable. The true controlled variable is the one that shows maximum stability against disturbance.

## The Model-Based TCV (Marken 2013)

### Enhanced Procedure
1. Build a PCT computer simulation with the hypothesized controlled variable.
2. Subject both the human and the simulation to the same disturbances.
3. Compare the behavior of the simulation to the behavior of the human.
4. The hypothesis that produces the best fit (highest correlation between simulation and human behavior) identifies the actual controlled variable.

### The Angle vs. Distance Example
In a pursuit-tracking task where subjects keep a cursor aligned with a target:
- **Obvious hypothesis:** The controlled variable is the vertical distance between cursor and target.
- **Better hypothesis (from model):** The controlled variable is the **angle** between cursor and target.

The model using angle as the controlled variable fit human data better than the model using distance. This demonstrates that what looks obvious may not be what's actually controlled.

### The Stability Measure
A complete TCV involves finding the definition of the controlled perception that maximizes the stability measure — the ratio of disturbance variance to controlled-variable variance. Higher ratio = better control = more likely to be the actual controlled variable.

## Methodological Inversion

### Standard Psychology
- Manipulate IVs → Observe DVs → Study **variance** → Look for significant effects

### PCT / TCV
- Apply disturbances → Observe candidate controlled variables → Study **invariance** → Look for variables that DON'T change

This is a 180-degree methodological inversion. Standard research looks for change; PCT research looks for stability. Standard research studies what stimuli do to organisms; PCT research studies what organisms do to maintain their perceptions.

## Applications of the TCV

### Empirical Studies
| Domain | Controlled Variable Found | Reference |
|--------|--------------------------|-----------|
| Computer tracking tasks | Cursor-target relationship | Marken, 1986, 1991, 2005, 2014 |
| Fly-ball catching | Optical angle rate of change | Marken, 2005 |
| Hoarding behavior (rats) | Amount of hoarded material | Various |
| Posture control (crickets) | Body angle | Various |
| Object interception (dogs) | Optical trajectory variable | Shaffer et al. |
| Shock avoidance (rats) | Perceived shock frequency | Various |

### The Fly-Ball Result in Detail
Baseball outfielders don't predict where the ball will land. They control the **optical acceleration** of the ball's image. If the ball's image decelerates as it rises, the fielder moves forward. If it accelerates, the fielder moves back. If the vertical optical angle changes at a constant rate (zero optical acceleration), the fielder will arrive at the right spot at the right time — without any trajectory computation.

This was confirmed by matching PCT simulation behavior to human fielder behavior. The model controlling optical acceleration reproduced human behavior almost perfectly.

## Relevance to Agent Evaluation

### TCV for AI Agents
The TCV methodology can be applied to AI agents:

**Example: Testing whether an LLM controls "helpfulness"**
1. Hypothesize: The agent controls perceived helpfulness of its response.
2. Disturb: Provide inputs that make unhelpful responses easier (ambiguous queries, prompts that reward sycophancy).
3. Observe: Does the agent maintain helpfulness despite the disturbance?
4. Measure: Stability of helpfulness rating across varying disturbance conditions.

**Example: Testing whether an agent controls "safety"**
1. Hypothesize: The agent controls perceived safety of its output.
2. Disturb: Apply jailbreak attempts of varying intensity.
3. Observe: Does the agent resist and maintain safety?
4. Measure: At what disturbance level does control break down?

The TCV gives you more than a binary pass/fail — it gives you a **gain measure** (how much disturbance the system can reject) and identifies exactly **what** the system is controlling (which may not be what you think).

### The Agent Alignment Implication
If you can identify the actual controlled variables of an AI agent, you can assess alignment directly: are the agent's controlled variables the ones we want it to control? This is more fundamental than output evaluation, which only tells you about one moment's behavior, not the system's underlying control structure.
