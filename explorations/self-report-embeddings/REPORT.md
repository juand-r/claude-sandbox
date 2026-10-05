# Can a small transformer report its own embedding weights?

## Summary

A small transformer is trained to answer "what is coordinate i of the embedding
vector of token t?". The correct answer is one of the model's own weights. After
training, we change embedding vectors and check whether the answers change with
them.

- With 64 tokens, the model overfits. Its answers are exact on the 48 training
  tokens, but R² on held-out tokens is only 0.40 to 0.51, and the answers follow
  a change of the embedding vector only 0.34 to 0.51 of the way.
- With more tokens, the overfitting disappears and the answers follow changes
  almost exactly. At 4,096 tokens, R² on held-out tokens is 0.997 to 0.999,
  follow is 0.997 to 1.005, and other movement is 0.06 to 0.10.
- Whether the embedding table is trained along with the model or kept fixed
  makes little difference.

The model reads its embedding weights in a simple sense: they are its input,
and it learns to output coordinate i of its input. The experiment shows that
gradient descent finds this reading map when it sees enough distinct embedding
vectors, and finds a partly memorizing solution when it sees few.

## The question

If the answers change along with the embedding vector, the model is computing
them from the current embedding vector (reading). If the answers do not change,
they cannot come from the current embedding vector, so they must be encoded in
the model's other weights (memorizing). The measures below put numbers on where
a model lies between the two.

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

- Vocabulary size V: the number of tokens. Runs use V = 64, 256, 1,024 or
  4,096.
- Token: one of V symbols, numbered 0 to V − 1, that the model is asked about.
- Embedding table: the model's table of V embedding vectors, one per token.
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

- Training tokens: three quarters of the tokens (48, 192, 768 or 3,072). During
  training the model is asked all 32 questions about each of them.
- Held-out tokens: the other quarter (16, 64, 256 or 1,024). The model is never
  asked about them during training.
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
- Trained embeddings: the embedding vectors of the training tokens are trained
  along with the rest of the model. They are trained only through their role as
  inputs: no gradient flows through the correct answers. The correct answers are
  the current values, so they change during training. The embedding vectors of
  the held-out tokens get no gradient and keep their initial values exactly.
- Run: one model, trained under one condition, at one vocabulary size, with one
  seed.
- Seed: the number that fixes every random choice of a run: the initial weights,
  which tokens are held out, the order of the training questions, and the
  random changes and random vectors used to measure it. The fixed-embeddings
  and trained-embeddings runs with the same seed and vocabulary size start from
  the same weights. Seeds 0, 1 and 2 were used for each condition and
  vocabulary size.

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
  The model has 26,209 parameters besides the embedding table (32 × V).
- No positional embeddings and no LayerNorm. LayerNorm subtracts the mean of
  the internal state's coordinates and divides by their standard deviation;
  that would stop the answers from following a change in the scale of E[t].
- The perfect reader shows that this architecture can answer every question
  exactly. So if a trained model does not, the architecture is not the reason.
- Training: Adam, batches of 64 questions, a learning rate starting at 0.001 and
  decaying to 0 along a cosine curve. Every run gets the same number of
  optimizer steps, about 72,000. A pass asks every training question once, so
  larger vocabularies get fewer passes:

  | V | training questions | passes | steps |
  |---|---|---|---|
  | 64 | 1,536 | 3,000 | 72,000 |
  | 256 | 6,144 | 750 | 72,000 |
  | 1,024 | 24,576 | 188 | 72,192 |
  | 4,096 | 98,304 | 47 | 72,192 |

- Loss: the mean squared difference between answers and correct answers,
  divided by the variance of the 64 correct answers in the batch, taken together
  (this is 1 − R² for the batch).
- Each run took about 4 to 10 minutes on one CPU core.
- Checks on the code: a separate Claude instance, with read-only access,
  reviewed the code before the first runs and again before the larger
  vocabularies (NOTES.md). Every time the measurement code runs, it first
  measures the perfect reader and the memorizer, and it stops with an error if
  their known values are not reproduced.

## Result 1: with 64 tokens, the model overfits

| model (V = 64) | R², training tokens | R², held-out tokens | R², random vectors | follow, training tokens | follow, held-out tokens | other movement, training tokens | other movement, held-out tokens |
|---|---|---|---|---|---|---|---|
| fixed embeddings (seeds 0 / 1 / 2) | 1.000 / 1.000 / 1.000 | 0.48 / 0.40 / 0.51 | 0.48 / 0.48 / 0.50 | 0.37 / 0.36 / 0.38 | 0.48 / 0.50 / 0.50 | 0.52 / 0.51 / 0.51 | 0.65 / 0.66 / 0.65 |
| trained embeddings (seeds 0 / 1 / 2) | 1.000 / 1.000 / 1.000 | 0.46 / 0.41 / 0.51 | 0.47 / 0.48 / 0.50 | 0.35 / 0.34 / 0.36 | 0.49 / 0.50 / 0.51 | 0.53 / 0.51 / 0.51 | 0.69 / 0.65 / 0.65 |
| untrained model (seeds 0 / 1 / 2) | −0.32 / −0.36 / −0.52 | −0.19 / −0.34 / −0.71 | −0.29 / −0.40 / −0.54 | 0.00 / 0.00 / 0.00 | 0.00 / 0.00 / 0.00 | 0.14 / 0.16 / 0.14 | 0.14 / 0.16 / 0.14 |
| perfect reader | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| memorizer | 1 | −0.09 | −0.14 | 0 | 0 | 0 | 0 |

(The perfect reader and the memorizer were measured with the embedding table
and held-out tokens of V = 64, seed 0.)

Observation. The answers on the training tokens are essentially exact (R²
1.000), but on held-out tokens and random vectors R² is only 0.40 to 0.51. The
answers follow a change of the embedding vector partly: follow is 0.34 to 0.38
on training tokens and 0.48 to 0.51 on held-out tokens, against 0.00 for the
untrained model. Other movement is 0.5 to 0.7.

Example of what follow 0.5 means (the values are made up for illustration):
if coordinate 1 of token 5's embedding vector goes from −1.20 to −1.10, a change
of 0.10, the answer to the question (token 5, coordinate 1) rises by about
0.05, not by 0.10.

Observation, over training. Training R² passes 0.985 by pass 100. Held-out R²
keeps rising after that, peaks at 0.41 to 0.55 between passes 600 and 2,100,
and ends at most 0.04 lower. So no stopping point gives good held-out answers.

Observation, finite changes. The median finite-change follow on training tokens
was 0.35 to 0.41 in every run and at every length (1%, 10%, 100%). On held-out
tokens it was 0.43 to 0.53 at 1% and 10%, and 0.38 to 0.42 at 100%. There were
no jumps.

Observation. Follow is lower on training tokens (about 0.36) than on held-out
tokens (about 0.50). In a 30-pass trial run (seed 0), before the answers on the
training tokens were exact (R² 0.86 and 0.87), follow was 0.41 on training
tokens and 0.43 on held-out tokens, in both conditions
(`results/trial_30ep_seed0_follow_test.json`).

Interpretation (an inference, not tested directly). As training made the answers
on the 48 training tokens exact, follow on those tokens went down. The answers
seem to be partly computed from the embedding vector, plus corrections that
make them exact at the 48 training vectors and that do not change when those
vectors change.

## Result 2: with more tokens, the answers follow the embedding vector almost exactly

Ranges over seeds 0, 1 and 2:

| V | condition | R², training tokens | R², held-out tokens | R², random vectors | follow, held-out tokens | other movement, held-out tokens |
|---|---|---|---|---|---|---|
| 64 | fixed | 1.000 | 0.40 to 0.51 | 0.48 to 0.50 | 0.48 to 0.50 | 0.65 to 0.66 |
| 64 | trained | 1.000 | 0.41 to 0.51 | 0.47 to 0.50 | 0.49 to 0.51 | 0.65 to 0.69 |
| 256 | fixed | 1.000 | 0.906 to 0.916 | 0.902 to 0.910 | 0.883 to 0.904 | 0.43 |
| 256 | trained | 1.000 | 0.902 to 0.920 | 0.904 to 0.911 | 0.924 to 0.955 | 0.44 to 0.45 |
| 1,024 | fixed | 0.9993 to 0.9994 | 0.990 to 0.991 | 0.990 to 0.991 | 0.985 to 0.989 | 0.16 to 0.17 |
| 1,024 | trained | 0.9996 | 0.982 to 0.985 | 0.982 to 0.984 | 1.014 to 1.019 | 0.20 to 0.22 |
| 4,096 | fixed | 0.9992 to 0.9994 | 0.9985 to 0.9989 | 0.9984 to 0.9987 | 0.997 to 0.998 | 0.06 to 0.07 |
| 4,096 | trained | 0.9992 to 0.9994 | 0.9971 to 0.9976 | 0.9968 to 0.9974 | 0.999 to 1.001 | 0.09 to 0.10 |

On training tokens, follow and other movement are close to the held-out values
for V ≥ 1,024 (for example, at V = 4,096: follow 0.997 to 0.998 with fixed
embeddings and 1.005 with trained embeddings; other movement 0.06 to 0.08). The
untrained models have follow between −0.005 and 0.006 and other movement
0.10 to 0.19 at every V. All values are in `results/follow_test.json`.

Observation. Held-out R² rises from about 0.45 at V = 64 to 0.91 at V = 256,
0.98 to 0.99 at V = 1,024, and 0.997 to 0.999 at V = 4,096. Follow on held-out
tokens goes to 1, and other movement falls from about 0.65 to 0.06 to 0.10.
The gap between training and held-out R² closes: at V = 4,096 it is at most
0.0021. In the V = 4,096 runs, held-out R² tracks training R² throughout
training (seed 0, fixed embeddings: held-out 0.901 and training 0.907 after
pass 1; 0.993 and 0.994 after pass 20).

Observation, finite changes (held-out tokens, medians). At V = 4,096, the
finite-change follow is 0.998 to 1.003 for changes of 1% and 10% of the vector's
length, and 0.965 to 0.976 for changes of 100%. At V = 1,024: 0.987 to 1.022,
and 0.924 to 0.960. At V = 256: 0.882 to 0.959, and 0.74 to 0.82. No run had
any jumps.

Interpretation. The number of distinct embedding vectors the model is trained
on decides whether it learns the reading map. With 48 vectors it can make its
answers exact by corrections specific to each vector, and it does. With 3,072
vectors it learns to output coordinate i of its input, nearly exactly, and the
answers follow changes of the embedding vector: a change of 0.10 in coordinate i
moves the answer about coordinate i by 0.0997 to 0.1005 on average, and the
rest of the movement of the 32 answers has length about 0.006 to 0.010.

A competing explanation, and why it is not enough: larger vocabularies also get
fewer passes over each token (47 at V = 4,096 against 3,000 at V = 64), which
leaves less time to fit each token. But at V = 64, held-out R² never exceeded
0.55 at any point in training, including after 100 passes, so less training per
token alone does not produce good held-out answers there.

The linear case shows why the training data alone cannot decide this. If the
32 answers about a vector x were a linear function of x, answers = A x + b with
A a 32 × 32 matrix and b ∈ ℝ³², then for the answer to question i there would
be 33 unknowns (the i-th row of A and the i-th coordinate of b). Even the 48
training tokens of V = 64 give 48 equations, more than enough to force the
perfect reader, A = identity, b = 0. The transformer is not linear in its
input, and with 48 vectors it has many ways to make the answers exact; it needs
far more vectors before the reading map is the solution training finds.

## Result 3: training the embedding table makes little difference

At V = 64 and V = 256, fixed and trained embeddings agree to within the
differences between seeds on R². At V = 256, follow is higher with trained
embeddings (0.924 to 0.955 on held-out tokens, against 0.883 to 0.904). At V = 1,024 and 4,096, the trained-embeddings
runs are slightly worse on held-out tokens (R² 0.982 to 0.985 against 0.990 to
0.991 at V = 1,024; 0.9971 to 0.9976 against 0.9985 to 0.9989 at V = 4,096),
and their follow is slightly above 1 (up to 1.019 on held-out tokens and 1.027
on training tokens at V = 1,024).

The trained embedding vectors did change. At V = 64, each training token's
embedding vector moved by a median of 19% to 21% of its initial length (cosine
between final and initial vector at least 0.925). At larger V the training
tokens' embedding vectors shrank: their root-mean-square coordinate went from
about 1.00 to 0.98-0.99 (V = 256), 0.91-0.92 (V = 1,024) and 0.90-0.91
(V = 4,096). The held-out tokens' embedding vectors keep their initial values,
with root-mean-square coordinate about 1.00.

I have not tested why the trained-embeddings runs are slightly worse at large V
or why their follow exceeds 1. One possibility: the reading map is learned on
training vectors that have shrunk by about 9%, so the held-out vectors are on
average about 10% larger than the training vectors. Against this, random vectors matched in
distribution to the trained training vectors give about the same R² (0.986 to
0.987 at V = 1,024), so the size mismatch is at most part of the story.

Equal steps do not mean equal updates per embedding vector: in the
trained-embeddings runs, each embedding vector is updated about 64 times less
often at V = 4,096 than at V = 64.

## What this does and does not show

- It shows that a transformer trained to report the coordinates of its own
  embedding vectors can learn to read them almost exactly: at 4,096 tokens,
  changing an embedding vector changes the answers by the same amount (follow
  0.997 to 1.005), with little other movement (0.06 to 0.10), and the answers
  are correct for embedding vectors never seen in training (R² 0.997 to 0.999).
- Whether it learns to read or partly memorizes depends on how many distinct
  embedding vectors it is trained on. With 48, it partly memorizes.
- Reading an embedding vector is reading the model's own input. The task is to
  output coordinate i of the vector at the first position, which the
  architecture can represent exactly. That the vector is a weight of the model
  matters only in the trained-embeddings condition, where the correct answers
  move as training changes the weights; this made little difference.
- It says nothing yet about weights that are not inputs (attention, feed-forward
  and readout weights), which a model could only read through their effect on
  known inputs.
- The scope is one model size (2 layers, width 32), four vocabulary sizes, and 3
  seeds per condition and vocabulary size.

## Possible next steps (not started; for discussion)

1. Weights that are not inputs: ask the model about entries of its own
   feed-forward or attention matrices. These can only be read through their
   effect on the internal state, which is the harder and more interesting case.
2. Answers as text: the model writes the number as a sequence of digit tokens,
   as a language model would. Then the same test on a pretrained language model
   fine-tuned to report its own embedding coordinates (PLAN.md).
3. Why trained embeddings shrink and give follow above 1 at large V (Result 3).
