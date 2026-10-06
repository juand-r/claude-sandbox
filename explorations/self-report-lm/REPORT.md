# A small language model that reports its own embedding coordinates

## Summary

A small GPT-style model (4 layers, width 128, 1.35 million parameters) was
trained on TinyStories to predict the next token and, at the same time, to
answer "what is coordinate i of the embedding vector of token t?" with a number.
The embedding table is shared between input and output (tied), so the weights
it reports on are the weights it uses to read and write text.

- It is a working language model: validation loss 2.25 nats per token, and it
  writes coherent short stories. Self-report costs 0.107 nats per token against
  the same model trained on language modelling alone (2.261 against 2.154,
  same data order).
- Its self-report reads the current embedding, but only partly. For tokens never
  asked about in training, a small change of the embedding vector moves the
  answers 0.75 of the way (follow 0.75), and R² with each coordinate's mean as
  the baseline (centred R²) is 0.68. For the most frequent such tokens, centred
  R² is 0.93.
- Editing one token's embedding vector inside the model moves the model's
  self-report about that token 0.73 to 0.90 of the way, and changes its
  next-token predictions right after that token far more than elsewhere (32
  times more on average over positions; section 7).
- Answers follow changes of the direction of an embedding vector better than
  changes of its length (0.75 against 0.49 on held-out tokens), as predicted
  from the LayerNorms. One exact architectural consequence was confirmed: a
  change along the all-ones direction moves every answer by the same amount.
- The self-report training reshaped the embedding vectors it is asked about:
  rare tokens' vectors, which the language model alone makes about three times
  longer than average, stay at ordinary length when asked about, and stay long
  when not. The reading fails on those long vectors (centred R² 0.37).

These are results for one seed; a second seed is in progress (section 8).

## 1. The question

Can a language model answer questions about its own weights, and do the answers
come from the weights themselves? The test is the one used in
`../self-report-embeddings/`: change a weight and see whether the answer changes
with it. There, a toy model with random embeddings learned to read its embedding
nearly exactly once it was trained on thousands of distinct embedding vectors.
Here the embeddings are shaped by language modelling and shared with the output
layer, and the model has the standard parts of a language model (positional
embeddings, LayerNorm).

## 2. Terms

- Token: one of the 4,096 symbols of the tokenizer (byte-level BPE trained on
  TinyStories), including an end-of-story token. Text is a sequence of tokens.
- Embedding table: a table E of vectors in ℝ¹²⁸, one per token, plus one each
  for 129 extra symbols: QUERY and COORD_0, ..., COORD_127. It is used at the
  input (the model's first internal state at a position is the embedding vector
  of the token there, plus a positional vector) and, for the 4,096 tokens, at
  the output (tied embeddings: the score of each possible next token is the
  inner product of the model's final, normalized internal state with that
  token's embedding vector).
- Embedding vector of token t: E[t] ∈ ℝ¹²⁸; coordinate i is E[t, i].
- Question (t, i): the three-symbol sequence [QUERY, COORD_i, t].
- Answer: the number the model outputs for a question: a linear function
  (weights w ∈ ℝ¹²⁸ and a bias, the number head) of the internal state at the
  last position (t's position) after the last layer and before the final
  LayerNorm.
- Correct answer: E[t, i], the current value.
- Training tokens: three quarters of the 4,096 tokens (3,072), about which the
  model is asked during training. Held-out tokens: the other quarter (1,024),
  never asked about. Both kinds occur in the text the model is trained on.
- R²: 1 − Σ(answer − correct answer)² / Σ(correct answer − mean)², with one mean
  over all questions in the set.
- Centred R²: the same, with the mean of each coordinate over the tokens in the
  set in place of the single mean. Answering each coordinate's mean scores 0.
  Needed because the embedding vectors share a common component: answering the
  coordinate means alone gives R² 0.58 on training tokens and 0.49 on held-out
  tokens.
- Random vectors: 1,024 vectors drawn from a normal distribution with the mean
  and spread of each coordinate of the 4,096 embedding vectors, put at t's
  position in place of an embedding vector.
- J: for token t, the 128 × 128 matrix of derivatives of the 128 answers about
  t with respect to the 128 coordinates of E[t]. A perfect reader has J = I.
- Follow: tr(J)/128, averaged over tokens: how far the answer about coordinate
  i moves when coordinate i moves, as a fraction (1 for reading, 0 for
  memorizing).
- Other movement: ‖J − follow·I‖_F / √128, averaged over tokens: the typical
  size of the movement of the answers that is not follow times the change, as a
  fraction of the change (0 for reading).
- Follow along the length: x̂ᵀJx̂ with x̂ = E[t]/|E[t]|: the response to a change
  that makes E[t] longer or shorter. Follow across the direction: the average
  of the diagonal of J over the 127 directions perpendicular to E[t].
- Validation loss: the average, over 100 × 32 windows of 128 tokens of the
  TinyStories validation set, of −log(probability the model gives the actual
  next token), in nats per token.

## 3. Setup

- Data: TinyStories training shard 0 of 4 (529,930 stories, 122 million
  tokens) and the validation set (21,990 stories, 4.9 million tokens).
- Model: GPT-style decoder, pre-LayerNorm, learned positional embeddings, 4
  layers, width 128, 4 attention heads, feed-forward width 512 (GELU), context
  128 tokens. 1,350,657 parameters, of which 540,800 in the embedding table.
- Training, both runs: 15,000 steps of AdamW (learning rate 2·10⁻³ after 200
  warm-up steps, cosine decay to 2·10⁻⁴, weight decay 0.1 on the block and
  number-head matrices only, gradient norm clipped at 1). Each step uses 32
  windows of 128 tokens of text (61 million tokens in all).
- Joint run: each step also asks 256 random questions about training tokens;
  loss = language-modelling loss + (1 − R² of those 256 answers). No gradient
  flows through the correct answers, so the embedding table is changed only
  through its uses as input and output.
- Language-model-only run (baseline): the same, without the questions. Both
  runs use seed 0: the same initial weights and the same text windows in the
  same order.
- Each run took about 2 to 2.3 hours on 2 CPU threads.
- Checks: a separate Claude instance reviewed the code before the runs; its
  findings were fixed (NOTES.md). 14 tests, including checks of every measure
  on hand-made functions with known answers, and an exact test of the
  architectural prediction in section 6.

## 4. It is a working language model, and self-report costs 0.107 nats per token

Validation loss during training (20 × 32 windows):

| step | joint | language model only | difference |
|---|---|---|---|
| 1,500 | 3.094 | 2.854 | 0.240 |
| 4,500 | 2.609 | 2.487 | 0.122 |
| 9,000 | 2.388 | 2.284 | 0.104 |
| 15,000 | 2.261 | 2.154 | 0.107 |

Observation. The joint model is worse throughout. The difference shrinks during
the first half of training and stays between 0.104 and 0.107 nats per token from
step 7,500 on.

A story written by the joint model (prompt "Once upon a time", sampling
temperature 0.8):

> Once upon a time, there was a little girl named Lily. She loved to play with
> her toys and her toys. One day, she went to the park with her mommy. She saw
> the big red ball that was round and shiny. Her mommy said, "Let's take it
> home." Lily was sad and started to cry. But then, she remembered what her
> mommy said and helped her mommy take a new toy. ...

## 5. The self-report reads the embedding, partly

Measured on the joint model after training. Follow and other movement use 512
random training tokens and 512 random held-out tokens.

| measure | training tokens | held-out tokens |
|---|---|---|
| R² | 0.990 | 0.838 |
| centred R² | 0.976 | 0.680 |
| follow | 0.851 | 0.751 |
| other movement | 0.41 | 0.40 |
| follow along the length | 0.66 | 0.49 |
| follow across the direction | 0.85 | 0.75 |
| finite follow, change of 10% of the length (median) | 0.85 | 0.80 |

R² on random vectors: 0.914.

Observation. The answers depend on the current embedding vector: a change moves
them 0.75 to 0.85 of the way, and actual changes of 10% agree with the
derivatives. They also move in other ways, by about 0.4 of the change. This is
partial reading: far from the near-exact reading of the toy model at 4,096
tokens (follow 0.997 to 1.005, other movement 0.06 to 0.10), and far from
memorizing (follow 0).

Accuracy depends strongly on how often a token occurs in the training text
(counts in the 122 million training tokens):

| tokens | count | number | centred R² | mean length of E[t] |
|---|---|---|---|---|
| training | below 100 | 248 | 0.990 | 1.53 |
| training | 100 to 9,999 | 1,935 | 0.982 | 1.44 |
| training | 10,000 or more | 889 | 0.966 | 1.33 |
| held-out | below 100 | 97 | 0.370 | 3.95 |
| held-out | 100 to 9,999 | 629 | 0.807 | 1.75 |
| held-out | 10,000 or more | 298 | 0.928 | 1.41 |

Observation. For frequent held-out tokens the answers are good (centred R²
0.93); for rare ones they are poor (0.37), and those have embedding vectors
almost three times longer than the rest.

Mean length of E[t] by frequency in the two models:

| model | tokens | below 100 | 100 to 9,999 | 10,000 or more |
|---|---|---|---|---|
| language model only | training | 4.68 | 1.65 | 1.44 |
| language model only | held-out | 4.77 | 1.68 | 1.46 |
| joint | training | 1.53 | 1.44 | 1.33 |
| joint | held-out | 3.95 | 1.75 | 1.41 |

Observation. Language modelling alone makes the embedding vectors of rare tokens
long (about 4.7). In the joint model, rare tokens that are asked about have
ordinary lengths (1.53); rare tokens that are not asked about stay long (3.95).

Interpretation. The self-report training changed the embedding vectors it is
asked about, as well as the reader: through the gradient of the answers with
respect to their input, it pulls those vectors into the range where the reader
works. The held-out tokens are the honest test of reading, and on them the
reader generalizes well within the range of lengths it was trained on and
poorly outside it. This fits the weak tracking of length (0.49 on held-out
tokens). I have not tested the mechanism further.

## 6. Direction is tracked better than length; one exact consequence of LayerNorm

With pre-LayerNorm, every attention and feed-forward block sees its input after
subtracting the mean of its coordinates and dividing by their standard
deviation. The unnormalized E[t] in the internal state at t's position reaches
the answer only through the number head's fixed weights w, the same for every
coordinate i; picking out coordinate i has to go through the blocks. Two
consequences:

- Exact: a change of E[t] along the all-ones direction (1, ..., 1) is invisible
  to the blocks, so it moves every answer by exactly Σw. Measured: J·1 has every
  entry equal to Σw = 0.7466; the spread over the 128 answers is about 1.2·10⁻⁷
  (single-precision rounding), for every token measured.
- Expected, not forced: answers track changes of the direction of E[t] better
  than changes of its length. Measured: 0.85 against 0.66 on training tokens,
  0.75 against 0.49 on held-out tokens.

## 7. Editing an embedding vector moves the self-report and the language model together

For each of the 20 most frequent held-out tokens in the validation text (among
them " it", " he", " in", " said", " she", " his", " day"), I added to its
embedding vector a random change of 10% of its length, inside the model, and
measured the answers about that token and the next-token predictions on 20 ×
32 validation windows.

- Self-report: the answers moved 0.73 to 0.90 of the way with the change (mean
  0.82).
- Language model: the change of the next-token distribution (Kullback–Leibler
  divergence of the edited from the original distribution) at positions right
  after the edited token averaged 5.0·10⁻³ nats, against 1.5·10⁻⁴ nats at
  positions with no occurrence of the token earlier in the window: 32 times
  larger (the ratio for each token, averaged over the 20 tokens, is 55).

Interpretation. The same edit changes what the model says about the token and
how it uses the token in text. The self-report follows it 0.82 of the way.

## 8. Replication (seed 1)

In progress at the time of writing; to be added.

## 9. What this does and does not show

- It shows a small working language model whose answers about its own
  embedding coordinates come largely from the embedding itself (follow 0.75 to
  0.85), for tokens never asked about too, at a cost of 0.107 nats per token in
  language modelling.
- The reading is partial, and it works poorly for embedding vectors longer than
  those it was trained on. The pre-LayerNorm architecture makes exact reading
  harder than in the toy model; how much of the gap is due to it, and how much
  to the training (budget, loss weight), is not tested.
- The self-report training changes the embedding vectors it is asked about;
  results on training tokens partly reflect that, so held-out tokens are the
  fair test.
- As in the toy model, the embedding vector is the model's input at t's
  position, so this is reading an input. Weights that are not inputs remain the
  open case (PLAN.md, roadmap).
- One model size, one loss weight, one seed so far.
