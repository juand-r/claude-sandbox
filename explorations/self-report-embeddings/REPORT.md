# Can a small transformer report its own embedding weights?

## The question

A small transformer is trained to answer one kind of question: "what is
coordinate i of the embedding vector of token t?". The correct answer is a
number stored inside the model itself, one of its own weights.

After training, we change a token's embedding vector and ask the same
questions again. There are two possibilities.

- If the answers change along with the embedding vector, the model computes
  its answers from the current embedding vector. We call this reading.
- If the answers stay the same, the model has stored its answers somewhere
  else, and they no longer match the changed weights. We call this memorizing.

This follows the neural-network quine (`../neural-network-quine/`). There a
network output its own weights with R² 0.9975, but changing one weight by 0.1
moved the network's output for that weight by only about 0.001: it was
memorizing. The embedding table is a better place to look for reading. When the
model processes token t, the first thing in its internal state is exactly the
embedding vector of t, so these weights are available to the model as an
input.

## Terms

Every term used in the rest of this report is defined here.

The model's inputs and outputs:

- Token: one of 64 symbols, numbered 0 to 63, that the model is asked about.
- Embedding table: the model's table of 64 embedding vectors, one per token.
  Its entries are weights of the model. Written E.
- Embedding vector of token t: the 32-dimensional vector that the embedding
  table holds for token t. Written E[t]. Its coordinates are numbered 0 to
  31; coordinate i is written E[t, i].
- Coordinate token: one of 32 extra symbols, meaning "coordinate 0" to
  "coordinate 31". They have their own separate embedding table, which is
  not asked about.
- Question: a pair (token t, coordinate i), given to the model as the two-symbol
  input [t, coordinate token i].
- Answer: the single number the model outputs for a question.
- Correct answer: E[t, i], the current value of coordinate i of the embedding
  vector of t.

Which tokens are used where:

- Training tokens: 48 of the 64 tokens. The model is trained on all 32
  questions about each, 48 × 32 = 1,536 questions in all.
- Held-out tokens: the other 16 tokens. The model is never asked about them
  during training.
- Random vectors: 1,024 vectors in ℝ³² drawn at random from the same
  distribution as the initial embedding vectors (a standard normal for each
  coordinate). They were never in the embedding table. We give one to the model
  in place of a token's embedding vector and ask the 32 questions about it.

Measures:

- R²: 1 − (sum of squared differences between answers and correct answers) /
  (sum of squared differences between the correct answers and their mean). R² = 1
  means every answer is correct. R² = 0 means the answers are no better than
  answering the mean every time. It is negative when the answers are worse than
  that.
- Follow: how much the answers move when an embedding vector is changed slightly,
  as a fraction of the change. Exactly: increase coordinate i of E[t] by a tiny
  amount ε. The answer to question (t, i) then increases by f·ε for some
  fraction f. Follow is the average of f over the 32 coordinates and over the
  tokens in question. Follow is 1 for reading and 0 for memorizing. (Computed
  exactly as the average of the diagonal of the 32 × 32 matrix of derivatives of
  the 32 answers about t with respect to the 32 coordinates of E[t].)
- Other movement: changing the embedding vector of t by a small random amount
  also moves the answers in ways that have nothing to do with the change. Other
  movement is the size of that unrelated movement, as a fraction of the size
  of the change. It is 0 for reading. (Computed exactly from the same matrix of
  derivatives, after subtracting follow times the identity matrix: the
  root-mean-square of the unrelated movement over random directions of the
  change.)

Experimental conditions:

- Fixed embeddings: the embedding table keeps its random initial values; only
  the rest of the model is trained.
- Trained embeddings: the embedding table is trained along with the rest of the
  model. The correct answers are then the table's current values, which change
  during training.
- Seed: the number that fixes the random choices of a run (the initial
  weights, which 16 tokens are held out, the order of training questions).
  Each condition was run with seeds 0, 1 and 2.

Reference models (built or chosen to give known values of every measure):

- Perfect reader: a model with the same architecture as the trained ones, with
  weights set by hand so that the answer is exactly the correct answer for any
  embedding vector whose coordinates are all smaller than 15 in absolute value
  (`canaries.py`). Follow 1, other movement 0, R² 1 everywhere.
- Memorizer: a hand-written program, not a neural network. It stores the
  embedding vectors of the training tokens and, given any vector, answers with
  the coordinates of the stored vector closest to it. Follow 0.
- Untrained model: the trained model's architecture and initial weights, before
  any training.

## Setup

- Model: a transformer with 2 layers, width 32, 4 attention heads, and a
  feed-forward block of 128 units with the ReLU activation in each layer. The
  answer is a linear function of the model's internal state at the second input
  position (the coordinate token).
- No positional embeddings and no LayerNorm. Without them, the model's internal
  state at the first input position is exactly the embedding vector E[t] before
  the first layer, and nothing rescales it. (LayerNorm divides the internal
  state by its size, which would stop the answer from following a change in the
  size of E[t].)
- The perfect reader shows that this architecture can read exactly. So if a
  trained model does not read, the architecture is not the reason.
- Training: 3,000 passes over the 1,536 training questions, in random batches
  of 64, with the Adam optimizer and a learning rate that decays to 0 along a
  cosine curve. Loss: the squared difference between answers and correct
  answers, divided by the variance of the correct answers in the batch (this
  equals 1 − R² for the batch).
- Each run took about 4 minutes on one CPU core.
- Checks on the code: an independent subagent reviewed it before the runs
  (NOTES.md). Every time the measurement code runs, it first measures the perfect
  reader and the memorizer, and it stops with an error if their known values are
  not reproduced.

## Result 1: on the training tokens, every answer is correct

R² on the training tokens is 1.000 (to three decimals) in all six runs: fixed
and trained embeddings, seeds 0, 1 and 2.

This alone does not distinguish reading from memorizing: the memorizer also
gets R² 1 on the training tokens.

## Result 2: the models read their embedding vectors, but only partly

| model | R², held-out tokens | R², random vectors | follow, training tokens | follow, held-out tokens | other movement, held-out tokens |
|---|---|---|---|---|---|
| fixed embeddings (seeds 0 / 1 / 2) | 0.48 / 0.40 / 0.51 | 0.48 / 0.48 / 0.50 | 0.37 / 0.36 / 0.38 | 0.48 / 0.50 / 0.50 | 0.65 / 0.66 / 0.65 |
| trained embeddings (seeds 0 / 1 / 2) | 0.46 / 0.41 / 0.51 | 0.47 / 0.48 / 0.50 | 0.35 / 0.34 / 0.36 | 0.49 / 0.50 / 0.51 | 0.69 / 0.65 / 0.66 |
| untrained model (seeds 0 / 1 / 2) | −0.19 / −0.34 / −0.71 | −0.29 / −0.40 / −0.54 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.14 / 0.16 / 0.14 |
| perfect reader | 1 | 1 | 1 | 1 | 0 |
| memorizer | −0.09 | −0.14 | 0 | 0 | 0 |

(The perfect reader's and memorizer's values were measured with the embedding
table and held-out tokens of seed 0.)

Observation. For embedding vectors the model was never trained on (held-out
tokens and random vectors), R² is between 0.40 and 0.51. When an embedding
vector is changed slightly, the answers move in the same direction by 0.34 to
0.51 of the change. They also move in unrelated ways, by about 0.65 of the
change. The untrained model has follow 0.00.

Example of what follow 0.5 means (the values are made up for illustration):
if coordinate 1 of token 5's embedding vector goes from −1.20 to −1.10 (a
change of 0.10), the answer to "coordinate 1 of token 5" rises by about 0.05,
not by 0.10.

Interpretation. Training produced real but partial reading. The answers depend
on the current embedding vector, in the right direction, but they move only
about half as much as the vector does.

Check with actual changes instead of derivatives. I also changed each embedding
vector by a random amount whose size was 1%, 10% or 100% of the vector's
length, and measured how far the answers moved along the change, as a fraction
of the change. For the training tokens, the middle value (median) of this
fraction over all changes was between 0.35 and 0.41 in every run and at every
size. In no case did the answers move more than three times as far as the
change. So the derivative-based numbers describe what happens under real
changes too. All numbers are in `results/follow_test.json`.

Observation. Follow is lower for the training tokens (about 0.36) than for the
held-out tokens (about 0.50). In a short trial run (30 passes over the training
questions, seed 0, before the training answers were all correct), follow was
0.41 for training tokens and 0.43 for held-out tokens.

Interpretation (an inference from these numbers, not tested directly). Getting
the training answers exactly right reduced the model's sensitivity to changes of
exactly those embedding vectors. The model seems to combine partial reading
with adjustments that fit the 48 training tokens one by one.

## Result 3: training the embedding table makes no difference

Fixed and trained embeddings agree, on every measure, to within the differences
between seeds. In the trained-embeddings runs, the embedding table changed
little. The root-mean-square value of the training tokens' coordinates went
from 1.02, 1.04 and 1.01 at the start to 1.07, 1.08 and 1.07 at the end (seeds
0, 1, 2). So these runs behaved like fixed-embedding runs with a slightly
different table.

## Why not a perfect reader?

During training the model sees only 48 different embedding vectors. Consider a
model whose 32 answers about a vector x are a linear function of x: answers =
A x + b, with A a 32 × 32 matrix and b ∈ ℝ³². For each of the 32
answers there are 33 unknowns (one row of A, plus one number of b), and the 48
training tokens give 48 equations. With more equations than unknowns, and
random embedding vectors, there is exactly one solution, and it is the perfect
reader (A = identity, b = 0).

The transformer is not a linear function of its input. With 128 ReLU units per
layer and attention, it has many ways to give the correct answers on 48
vectors, and training found one that reads only partly. This explains why the
data do not force reading. It does not say which property of the network or
of the training produced this particular solution; I have not tested that.

## What this does and does not show

- It shows that a transformer trained to report its own embedding coordinates
  gives answers that depend on the current values: change an embedding vector,
  and the answers change in the same direction, by about half as much.
- It does not show exact self-reading. The trained models are far from the
  perfect reader, which this architecture can represent.
- The scope is one architecture, one size, 64 tokens and 3 seeds per condition.
- For this model, held-out tokens are simply embedding vectors it has not been
  trained on. With fixed embeddings they come from the same distribution as the
  random vectors, and the two R² columns agree, as they should.

## Possible next steps (not started; for discussion)

1. More tokens. With 64 tokens the model is trained on 48 embedding vectors.
   With 1,000 or 10,000 tokens it could no longer fit each training token
   separately. If the interpretation above is right, it would then read more
   exactly.
2. A smaller feed-forward block, or none in the second layer, leaving less
   room to fit each training token separately.
3. Answers written out as text tokens, and then a pretrained language model
   (PLAN.md).
