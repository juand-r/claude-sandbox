# Can a small transformer report its own embedding weights?

## The question

A small transformer is trained to answer one kind of question: "what is
coordinate i of the embedding vector of token t?". The correct answer is one of
the model's own weights.

After training, we change a token's embedding vector and ask the same questions
again. If the answers change along with the embedding vector, the model is
computing them from the current embedding vector (reading). If the answers do
not change, they cannot come from the current embedding vector, so they must be
encoded in the model's other weights (memorizing). The measures below put
numbers on where a model lies between the two.

This follows the neural-network quine (`../neural-network-quine/`). Its best
network output its own weights with R² 0.9975, yet for a typical hidden-layer
weight, a change of 0.1 moved the network's output for that weight by only
about 0.001 (300 sampled weights; median size of the derivative 0.010;
`../neural-network-quine/results/diag_own_influence_lmnormReset_L2fn_seed0_b.txt`).
The embedding table is a better place to look for reading. Before the first
layer, the model's internal state at the token's position is exactly that
token's embedding vector, so these weights are available to the model as an
input.

## Terms

Every term used in the rest of this report is defined here.

The model's inputs and outputs:

- Token: one of 64 symbols, numbered 0 to 63, that the model is asked about.
- Embedding table: the model's table of 64 embedding vectors, one per token.
  Its entries are weights of the model. Written E.
- Embedding vector of token t: the vector in ℝ³² that the embedding table holds
  for token t. Written E[t]. Its coordinates are numbered 0 to 31; coordinate
  i is written E[t, i].
- Coordinate token: one of 32 extra symbols, meaning "coordinate 0" to
  "coordinate 31". They have their own embedding table, which is not asked
  about.
- Question: a pair (token t, coordinate i), given to the model as a sequence of
  two symbols: t at the first position, coordinate token i at the second.
- Answer: the single number the model outputs for a question.
- Correct answer: E[t, i], the current value of coordinate i of the embedding
  vector of t.
- Length of a vector: its Euclidean norm.

Inside the model:

- Internal state at a position: the vector in ℝ³² that the model holds at that
  position of the input sequence. Before the first layer it is the embedding
  vector of the symbol there; each layer adds to it.
- Attention is causal: the second position can draw on both positions, the
  first position only on itself. So the internal state at the first position
  depends only on E[t].

Which inputs are used where:

- Training tokens: 48 of the 64 tokens. During training the model is asked all
  32 questions about each of them, 48 × 32 = 1,536 questions in all.
- Held-out tokens: the other 16 tokens. The model is never asked about them
  during training.
- Random vectors: 1,024 vectors in ℝ³², each coordinate drawn from a standard
  normal distribution, the distribution of the initial embedding vectors. They
  were never in the embedding table. A random vector x is put at the first
  position in place of an embedding vector; question i about it asks for x_i,
  and the correct answer is x_i. Random vectors are used only for R².

Measures:

- R²: 1 − (sum of squared differences between the answers and the correct
  answers) / (sum of squared differences between the correct answers and their
  mean), where the mean is a single number, taken over all questions in the set
  being measured. R² = 1 means every answer is correct; R² = 0 means the answers
  are no better than answering that mean every time; R² is negative when they
  are worse.
- Follow: increase coordinate i of E[t] by a tiny amount ε. The answer to
  question (t, i) then changes by f·ε, where f is some number. Follow is the
  average of f over the 32 coordinates and over the tokens of the set being
  measured (training tokens or held-out tokens). It is computed exactly, from
  derivatives: f for coordinate i is the i-th diagonal entry of the 32 × 32
  matrix J of derivatives of the 32 answers about t with respect to the 32
  coordinates of E[t].
- Other movement: adding a small vector δ to E[t] changes the 32 answers about
  t by J·δ. A reader would change them by exactly δ. Other movement is the
  length of (J·δ − follow·δ) divided by the length of δ, as a root mean square
  over random directions of δ, averaged over tokens. It is computed exactly from
  J.
- Finite-change follow: the same idea as follow, measured with actual changes
  instead of derivatives. Add to E[t] a vector δ in a random direction, whose
  length is 1%, 10% or 100% of the length of E[t]; the 32 answers about t change
  by some vector Δ; the finite-change follow is Δ·δ / |δ|². Four such δ per
  token and length. For very small δ its average equals follow.
- Jump: a change δ after which the answers moved more than three times as far
  as the embedding vector did (|Δ| > 3|δ|). The memorizer jumps when a change
  makes a different stored vector the nearest one; jumps can distort an average
  of finite-change follow, so they are counted.

Reading and memorizing, in terms of these measures:

- Reading: follow 1 and other movement 0 (the answers change exactly as the
  embedding vector does).
- Memorizing: follow 0 and other movement 0 (the answers do not change).

Experimental conditions:

- Fixed embeddings: the embedding table keeps its random initial values; only
  the rest of the model is trained.
- Trained embeddings: the embedding vectors of the 48 training tokens are
  trained along with the rest of the model. They are trained only through their
  role as inputs: no gradient flows through the correct answers. The correct
  answers are the current values, so they change during training. The
  embedding vectors of the held-out tokens get no gradient and keep their
  initial values exactly.
- Run: one model, trained under one condition with one seed.
- Seed: the number that fixes every random choice of a run: the initial weights,
  which 16 tokens are held out, the order of the training questions, and the
  random changes and random vectors used to measure it. The fixed-embeddings
  and trained-embeddings runs with the same seed start from the same weights.
  Seeds 0, 1 and 2 were used for each condition.

Reference models, whose values of every measure are known in advance:

- Perfect reader: a model with the same architecture as the trained ones,
  with weights set by hand so that every answer is exactly the correct answer,
  for any vector at the first position whose coordinates are all smaller than
  15 in absolute value (`canaries.py`). Follow 1, other movement 0, R² 1 on every
  set.
- Memorizer: a hand-written program, not a neural network. It stores the
  embedding vectors of the training tokens and, given any vector, answers with
  the coordinates of the stored vector nearest to it. Follow 0, other movement 0,
  R² 1 on the training tokens.

Baseline:

- Untrained model: a run's model before any training (the same initial weights).

## Setup

- Model: a transformer with 2 layers, width 32 (each internal state is a vector
  in ℝ³², the same as an embedding vector), 4 attention heads, and a
  feed-forward block of 128 ReLU units in each layer. The answer is a linear
  function of the internal state at the second position after the last layer.
- No positional embeddings and no LayerNorm. LayerNorm subtracts the mean of
  the internal state's coordinates and divides by their standard deviation;
  that would stop the answers from following a change in the scale of E[t].
- The perfect reader shows that this architecture can answer every question
  exactly. So if a trained model does not, the architecture is not the reason.
- Training: 3,000 passes over the 1,536 training questions (each pass asks every
  training question once, in random batches of 64), with the Adam optimizer, a
  learning rate starting at 0.001 and decaying to 0 along a cosine curve. Loss:
  the mean squared difference between answers and correct answers, divided by
  the variance of the 64 correct answers in the batch, taken together (this is
  1 − R² for the batch).
- Each run took about 4 minutes on one CPU core.
- Checks on the code: a separate Claude instance, with read-only access,
  reviewed the code before the runs (NOTES.md). Every time the measurement code
  runs, it first measures the perfect reader and the memorizer, and it stops
  with an error if their known values are not reproduced.

## Result 1: on the training tokens, the answers are essentially exact

R² on the training tokens is 1.000 (to three decimals) in all six runs: fixed
and trained embeddings, seeds 0, 1 and 2. This alone does not tell reading from
memorizing; the memorizer also has R² 1 on the training tokens.

## Result 2: follow is about 0.36 on training tokens and 0.5 on held-out tokens

| model | R², held-out tokens | R², random vectors | follow, training tokens | follow, held-out tokens | other movement, training tokens | other movement, held-out tokens |
|---|---|---|---|---|---|---|
| fixed embeddings (seeds 0 / 1 / 2) | 0.48 / 0.40 / 0.51 | 0.48 / 0.48 / 0.50 | 0.37 / 0.36 / 0.38 | 0.48 / 0.50 / 0.50 | 0.52 / 0.51 / 0.51 | 0.65 / 0.66 / 0.65 |
| trained embeddings (seeds 0 / 1 / 2) | 0.46 / 0.41 / 0.51 | 0.47 / 0.48 / 0.50 | 0.35 / 0.34 / 0.36 | 0.49 / 0.50 / 0.51 | 0.53 / 0.51 / 0.51 | 0.69 / 0.65 / 0.65 |
| untrained model (seeds 0 / 1 / 2) | −0.19 / −0.34 / −0.71 | −0.29 / −0.40 / −0.54 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.14 / 0.16 / 0.14 | 0.14 / 0.16 / 0.14 |
| perfect reader | 1 | 1 | 1 | 1 | 0 | 0 |
| memorizer | −0.09 | −0.14 | 0 | 0 | 0 | 0 |

(The perfect reader and the memorizer were measured with the embedding table
and held-out tokens of seed 0.)

Observation. For held-out tokens and random vectors, R² is between 0.40 and
0.51. Follow is 0.34 to 0.38 on training tokens and 0.48 to 0.51 on held-out
tokens; for the untrained model it is 0.00. Other movement is about 0.51 on
training tokens and 0.65 on held-out tokens.

Example of what follow 0.5 means (the values are made up for illustration):
if coordinate 1 of token 5's embedding vector goes from −1.20 to −1.10, a change
of 0.10, the answer to the question (token 5, coordinate 1) rises by about
0.05, not by 0.10.

Interpretation. The trained models are between memorizing and reading. Their
answers depend on the current embedding vector, in the right direction, but
with follow between 0.34 and 0.51 instead of 1, and with other movement of 0.5
to 0.7 instead of 0.

Finite changes. The median finite-change follow over the 192 changes of each
run and length (48 training tokens × 4) was 0.35 to 0.41 for training tokens,
in every run and at every length. For held-out tokens (64 changes per run and
length) it was 0.43 to 0.53 at lengths of 1% and 10%, close to follow, and
0.38 to 0.42 at 100%, lower than follow. There were no jumps in any run, set or
length. So follow describes changes of up to 10% of an embedding vector's
length well; for changes as large as the vector itself, the answers on
held-out tokens follow somewhat less. All values are in
`results/follow_test.json`.

Observation. Follow is lower on training tokens (about 0.36) than on held-out
tokens (about 0.50). In a 30-pass trial run (seed 0), before the answers on the
training tokens were exact (R² 0.86 and 0.87), follow was 0.41 on training tokens and
0.43 on held-out tokens, in both conditions
(`results/trial_30ep_seed0_follow_test.json`).

Interpretation (an inference from these numbers, not tested directly). As
training made the answers on the 48 training tokens exact, follow on those
tokens went down. One explanation consistent with this: the model's answers
are partly computed from the embedding vector, plus corrections that make them
exact at the 48 training tokens' embedding vectors and that do not change when
those vectors change.

## Result 3: training the embedding table makes no difference to the measures

Fixed and trained embeddings agree on every measure to within the differences
between seeds (table above).

This is not because the trained embedding vectors stayed put. Each training
token's embedding vector moved during training by a median of 19%, 20% and 21%
of its initial length (seeds 0, 1, 2; the largest moves were 52%, 39% and 44%).
Their directions changed less: the cosine between final and initial vector was
at least 0.925 for every training token. The held-out tokens' embedding
vectors did not change at all.

## Why are the answers not exact on held-out tokens?

During training the model is asked about only 48 different embedding vectors.
Consider a model whose 32 answers about a vector x are a linear function of x:
answers = A x + b, with A a 32 × 32 matrix and b ∈ ℝ³². For the answer to
question i there are 33 unknowns (the i-th row of the matrix A and the i-th
coordinate of b), and the 48 training tokens give 48 equations. With more
equations than unknowns and random embedding vectors, there is exactly one
solution, and it is the perfect reader: A = identity, b = 0.

The transformer is not a linear function of its input. With 128 ReLU units per
layer and attention, it has many ways to make the answers exact on 48 vectors,
and training found one with follow about 0.5. This explains why the training
data do not force follow 1. It does not say which property of the network or
of the training produced this particular solution; I have not tested that.

## What this does and does not show

- It shows that a transformer trained to report the coordinates of its own
  embedding vectors gives answers that depend on their current values: change
  an embedding vector, and the answers change in the same direction, with
  follow about 0.36 on training tokens and 0.5 on held-out tokens.
- It does not show exact reading. The trained models are far from the perfect
  reader, which this architecture can represent.
- The scope is one model size (2 layers, width 32), 64 tokens and 3 seeds per
  condition.
- For this model, held-out tokens' embedding vectors are simply inputs it was
  never asked about in training. In both conditions they keep their initial
  values, so they come from the same distribution as the random vectors, and
  the two R² columns agree, as they should.

## Possible next steps (not started; for discussion)

1. More tokens. With 64 tokens the model is asked about 48 embedding vectors in
   training. With 1,000 or 10,000 tokens, the network would no longer have
   enough parameters to make the answers exact at each training token by
   corrections specific to that token. If the interpretation in Result 2 is
   right, follow should then rise toward 1.
2. A smaller feed-forward block, or none in the second layer: fewer parameters
   for such corrections, with the same 64 tokens.
3. Answers as text: the model writes the number as a sequence of digit tokens,
   as a language model would, instead of outputting one number. Then the same
   test on a pretrained language model fine-tuned to report its own embedding
   coordinates (PLAN.md).
