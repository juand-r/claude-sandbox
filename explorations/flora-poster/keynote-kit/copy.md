# Poster text, by element

## 01 title-block

ARXIV 2607.02668
Improving LLMs via Validator-to-Generator Alignment
Juan Diego Rodriguez1, Jocelyn Zhang1, Katrin Erk2, Greg Durrett3
1UT Austin 2UMass Amherst 3New York University

## 02 s1-heading

1
Generators and validators disagree

## 03 s1-text

Ask an LLM for an example of a noble gas and it rarely says “Rn”. Ask it whether Rn is a noble gas and it says yes. The generator mixes up two things: whether an answer is correct, and how often people say it.

## 04 s1-noble-gas-diagram

Generator
“Give an example of a noble gas.”
Hydrogen > Rn: inconsistent
Helium
Neon
Radon
Hydrogen
Rn
Validator
“Is hydrogen a noble gas?” → No
“Is Rn a noble gas?” → Yes
Frequency-corrected
Rn > Hydrogen: consistent
Helium
Neon
Radon
Hydrogen
Rn
Illustration, after Figure 1 of the paper. Striped bar: the wrong answer.

## 05 s2-heading

2
What should agree with what

## 06 s2-text

Model the LLM as an agent that is unsure which answers are correct. Then, for an answer y to a prompt x, the validator’s log-odds equal a frequency-corrected generator score:

## 07 s2-equation

log
pV
1 − pV
validator log-odds
=
log
p
G
generator, asked for a correct answer
−
log
p
G′
generator, asked for a wrong answer: how common y is
+
log
r
assumed ≈ 0

## 08 s2-note

So the raw generator score need not match the validator. The corrected score should.

## 09 s3-heading

3
FLORA: train for agreement

## 10 s3-text

Frequency-corrected Learning of Ordered Rank Alignment turns this relation into a fine-tuning loss.

## 11 s3-flora-diagram

Corrected generator score
s = log pG(y | x) − log pG′(y | x)
Validator log-odds
from “Is y correct?”
Pairwise ranking loss
Take two answers to the same prompt. The validator says which is better. Train the corrected generator score to rank them the same way.

## 12 s3-note

FLORA-Neg gets pG′ from a wrong-answer prompt. FLORA-PMI uses the unconditional log p(y) and needs no extra prompt. Likelihood terms on labeled examples keep both modes accurate.

## 13 main-idea

Correct for how often an answer is said, and an LLM’s generator lines up with its own validator.

## 14 main-subtext

We derive the correction from a model of a rational agent, then train on it. FLORA raises generator–validator correlation by up to 0.27 and generator AUROC by up to 7.3 points over the strongest alternative, without hurting validator AUROC.

## 15 figure-caption

One IFEval prompt, Gemma-2-9b-it. Each point is a candidate answer (green: correct, red: incorrect). The vertical axis is the model’s own validator.

## 16 figure-scatter



## 17 figure-panel-labels

Raw score. No relation to the validator (ρ = −0.24).
Corrected, no training. Most of the agreement appears (ρ = 0.64).
After FLORA. Tighter still (ρ = 0.75).

## 18 qr-paper

Paper
arxiv.org/abs/2607.02668

## 19 qr-code

Code and data
github.com/juand-r/flora

## 20 s4-heading

4
Results

## 21 s4-definitions

Three tasks: instruction following (IFEval), Python coding (HumanEval), category membership (Hyponymy). Generator AUROC: how well the corrected generator score separates correct from incorrect answers. ρ: Pearson correlation between generator score and validator log-odds. Both per prompt, then averaged.

## 22 results-title

Better generators, closer agreement

## 23 results-legend

Untrained
Best prior method
FLORA

## 24 results-chart

Generator AUROC | 60 | 70 | 80 | 90 | 100 | 85.1 | 74.9 | 79.6 | 75.4 | 94.2 | 86.9 | 88.9 | 94.1 | 92.5 | 91.6 | 88.2 | 88.2 | G–V correlation ρ ×100 | 20 | 40 | 60 | 80 | 62.8 | 29.9 | 44.7 | 32.8 | 76.3 | 49.0 | 68.5 | 69.5 | 73.8 | 75.2 | 69.4 | 70.4 | IFEval | Gemma-2-9b-it | IFEval | Qwen-3.5-9B | HumanEval | Gemma-4-31b-it | HumanEval | Qwen-3.5-9B | Hyponymy | Gemma-2-9b-it | Hyponymy | Qwen-3.5-9B

## 25 results-takeaway

FLORA is best or tied on generator AUROC in 5 of 6 settings, and best on ρ in 3 of 6 (within 1.4 points elsewhere). Its one clear loss is HumanEval with Qwen, where SFT reaches 94.1 AUROC to FLORA’s 88.9.

## 26 results-footnote

Each dot is the best variant per setting and metric: FLORA-PMI or FLORA-Neg for FLORA; SFT, Consistency FT or RankAlign for prior methods. “Strongest alternative” in the center panel also includes the untrained model.

## 27 ablation-title

The correction matters during training

## 28 ablation-note

FLORA with and without frequency correction in its training loss. Both use the same correction at test time.

## 29 ablation-table

Task	Gen. AUROC	ρ ×100
IFEval Gemma-2-9b-it	78.5 → 85.1	61.1 → 62.8
HumanEval Gemma-4-31b-it	87.9 → 94.2	60.2 → 76.3
Hyponymy Gemma-2-9b-it	90.9 → 92.5	73.1 → 73.8

## 30 ablation-footnote

Without → with the correction in training.

## 31 validator-title

The validator does not pay for it

## 32 validator-note

Change in validator accuracy after FLORA training, in points. Each bar spans the two FLORA variants.

## 33 validator-chart

−5 | 0 | +5 | +10 | +15 | +20 | +3.9 to +7.8 | IFEval Gemma-2-9b-it | +1.0 to +2.8 | IFEval Qwen-3.5-9B | +14.4 to +16.9 | HumanEval Gemma-4-31b-it | +11.1 to +13.0 | HumanEval Qwen-3.5-9B | −2.5 to −2.2 | Hyponymy Gemma-2-9b-it | −1.1 to −0.6 | Hyponymy Qwen-3.5-9B

## 34 validator-takeaway

Validator accuracy rises on IFEval and HumanEval and dips by at most 2.5 points on Hyponymy. Validator AUROC never drops by more than 0.4 points.

## 35 limits-title

Limits

## 36 limits-text

The theory needs log r ≈ 0, which cannot be measured. We rank fixed sets of candidate answers and do not test greedy outputs. Correctness is treated as binary.
