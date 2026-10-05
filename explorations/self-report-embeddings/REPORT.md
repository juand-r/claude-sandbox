# Can a small transformer report its own embedding weights?

## The question

A small transformer is trained to answer one kind of question: "what is
coordinate i of your embedding of token t?". Its answer should equal E[t, i],
an entry of its own embedding table. After training, we change one row of the
table and ask again. If the answers change with the row, the model is reading
its weights. If they stay put, it has memorized the answers.

This follows the neural-network quine (`../neural-network-quine/`), where a
network matched its own weights with R² 0.9975, but changing a weight by 0.1
moved the network's guess for that weight by only about 0.001. The embedding
table is a natural place to try again: when the model reads token t, its
internal state starts as exactly the row E[t], so the weights are in front of
the model, as an input.

## Setup

- 64 content tokens with 32-dimensional embedding rows; 16 of them are held out
  (never asked about in training), 48 are used for training.
- Input: two tokens, [t, "coordinate i"]. Output: one number.
- Model: 2 transformer layers, width 32, 4 attention heads, MLP width 128 with
  ReLU. No positional embeddings and no LayerNorm, so that position 0 holds
  exactly E[t] and nothing rescales it.
- A perfect reader exists in this exact architecture: I built one by hand
  (`canaries.py`), and it answers every question exactly, for any row with
  entries below 15 in size. So a trained model that does not read cannot blame
  the architecture.
- Training: all 48 × 32 = 1,536 questions about the training tokens, 3,000
  epochs of Adam with a cosine learning-rate decay. Loss: squared error divided
  by the variance of the targets in the batch (1 − R² of the batch).
- Two conditions, 3 seeds each:
  - fixed: the embedding table stays at its random initial values (entries
    drawn from a standard normal distribution);
  - trained: the table is trained together with the rest of the model, and the
    targets are its current values.

Each training run takes about 4 minutes on one CPU core. All code was reviewed
by an independent subagent before the runs (NOTES.md), and the measurement code
reproduces known results on two hand-built models (a perfect reader and a
memorizer) every time it runs.

## Terms used in the tables

- R², training tokens: how well the answers match the current embedding values,
  over all 1,536 training questions. 1 is perfect; 0 is no better than
  answering the average value.
- R², held-out tokens: the same for the 16 tokens never asked about.
- R², new rows: the same for 1,024 random rows that were never in the table.
- Follow: the model's sensitivity to a small change of a row. For token t, take
  the 32 × 32 matrix of derivatives of the 32 answers about t with respect to
  the 32 entries of E[t]. A perfect reader has the identity matrix. "Follow" is
  the average of its diagonal: if a row is nudged by a small random δ, the
  answers move on average by "follow" times δ. 1 means the answers move with the
  change; 0 means they ignore it.
- Other movement: how much the answers move in directions other than δ, in
  units of |δ|. 0 for a perfect reader.

## Result 1: both conditions memorize the training tokens perfectly

| condition | seed 0 | seed 1 | seed 2 |
|---|---|---|---|
| fixed | 1.000 | 1.000 | 1.000 |
| trained | 1.000 | 1.000 | 1.000 |

(R² on training tokens; rounded to three decimals, all are 1.000.)

## Result 2: the models read their embedding, but only partly

| | R², held-out tokens | R², new rows | follow, training tokens | follow, held-out tokens | other movement, held-out tokens |
|---|---|---|---|---|---|
| fixed (seeds 0 / 1 / 2) | 0.48 / 0.40 / 0.51 | 0.48 / 0.48 / 0.50 | 0.37 / 0.36 / 0.38 | 0.48 / 0.50 / 0.50 | 0.65 / 0.66 / 0.65 |
| trained (seeds 0 / 1 / 2) | 0.46 / 0.41 / 0.51 | 0.47 / 0.48 / 0.50 | 0.35 / 0.34 / 0.36 | 0.49 / 0.50 / 0.51 | 0.69 / 0.65 / 0.66 |
| untrained (seeds 0 / 1 / 2) | −0.19 / −0.34 / −0.71 | −0.29 / −0.40 / −0.54 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.14 / 0.16 / 0.14 |
| perfect reader (hand-built) | 1 | 1 | 1 | 1 | 0 |
| memorizer (hand-built) | −0.09 | −0.14 | 0 | 0 | 0 |

Observation. On rows the model never saw, it gets about half the variance
right (R² 0.40 to 0.51). When a row is nudged, the answers move between a third
and a half of the way with it (follow 0.34 to 0.51). They also move about as
much again in other directions (other movement 0.65). An untrained model has
follow 0.00. So training produced real, partial reading: the answers do depend
on the row, in the right direction, but not one-for-one.

Finite changes agree with the derivative-based numbers. For random changes of
1%, 10% and 100% of a row's size, the median follow ratio on training tokens
was 0.35 to 0.41 in every run, with no jumps (no change where the answers moved
more than three times as far as the row). The full numbers are in
`results/follow_test.json`.

Observation. On the training tokens, follow is lower (about 0.36) than on the
held-out tokens (about 0.50). In a short trial run (30 epochs, seed 0, before
the answers were exact) both were about 0.41-0.43. So fitting the training
answers exactly lowered the model's sensitivity to changes at exactly those
rows.

Interpretation. The model learned a mixture of reading and memorizing. Near the
48 rows it was trained on, it bends its answers to fit them exactly, and that
bending makes the answers less sensitive to the row there. This is an
inference from the two numbers above, not a direct test.

## Result 3: training the embedding makes no difference

The fixed and trained conditions agree to within the spread between seeds on
every measurement. In the trained condition the table hardly moved: its size
(root mean square of the entries of the training rows) grew from 1.02, 1.04
and 1.01 at initialization to 1.07, 1.08 and 1.07 (seeds 0, 1, 2). So the
trained condition behaved like the fixed one with a slightly different table.

## Why not a perfect reader?

The training set shows the model only 48 distinct rows. A reader that is linear
in the row, a(x) = A x + b, would be pinned down exactly by 48 rows in 32
dimensions (48 is more than the 33 unknowns per answer), and it would be the
perfect reader. But the transformer is not linear in its input. With 128 ReLU
units and attention, it can fit 48 points in many ways, and gradient descent
found one that is only partly the reading map. This is a statement about what
the data allow; I have not tested which property of the network or the training
drives it.

## What this does and does not show

- It shows that a transformer trained to report its own embedding entries
  learns answers that depend on the actual entries: change a row, and the
  answers change in the same direction, about half as much. That is the
  "scale", not the "jar label", but a weak scale.
- It does not show perfect self-reading. The model is far from the hand-built
  reader that the architecture allows.
- One architecture, one size, 64 tokens, 3 seeds per condition. Held-out tokens
  are just new inputs for this model; in the fixed condition they come from the
  same distribution as the "new rows", and the two R² columns agree.

## Possible next steps (not started; for discussion)

1. More content tokens. With 64 tokens the model sees 48 rows. With 1,000 or
   10,000 it cannot fit each one separately, and should be pushed toward reading.
   This tests the interpretation above directly.
2. A smaller MLP, or no MLP in the second layer: less room to memorize.
3. Answers written as text tokens, and then a pretrained model (PLAN.md).
