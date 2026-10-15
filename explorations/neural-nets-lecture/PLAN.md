# Neural networks: plan for two classes

Agreed with the user on 2026-10-08. Class 1 builds the network and its forward pass and shows gradient
descent as given; class 2 explains where the gradients come from (backpropagation) and how training is
done in practice. A third lecture (architectures: CNNs, RNNs, attention) is planned later as a bonus.

Conventions carried over from the earlier decks: positives green, negatives purple, fits and models
teal, highlights amber, errors orange; every figure starts with the data; lean slides, the discussion
goes in the speaker notes; no instructions on how to use widgets. Every training run shown is
precomputed in Python (`experiments.py`), checked (`check_numbers.py`) and replayed in the deck. Only
gradient descent on the 2D cartoon surface runs in the browser, so the start point can be dragged.

Notation: score f(x) = w · x + b; labels switch from y ∈ {+1, −1} (last lecture) to one-hot vectors in
class 1, slide 4; model / loss boxes as in the logistic regression deck: ŷ = f(x | θ), min over θ of
ℒ(θ; D), D = {(xᵢ, yᵢ)}; learning rate η.

## Class 1: from one neuron to a network (`neural_nets_1.html`)

1. **Opening image.** Selfridge's Pandemonium (user's image) with the caption "Selfridge's Pandemonium
   (1959): layers of 'demons' that each shout when they detect their feature. Drawing from Lindsay &
   Norman, Human Information Processing."
2. **Title.** Neural networks. Part 1: from one neuron to a network.
3. **Recap: logistic regression.** Model box p(y = +1 | x) = σ(w · x + b); loss box
   ℒ(θ; D) = Σ log(1 + e^(−yᵢ f(xᵢ))); the single-neuron diagram from last lecture.
4. **Two classes as one-hot vectors.** y = (1, 0) or (0, 1); scores (f, 0); softmax gives
   p₁ = e^f / (e^f + e^0) = σ(f); cross-entropy −Σₖ yₖ log pₖ = −log p(true class), last lecture's log
   loss. So logistic regression is softmax with two classes.
5. **C classes: softmax and cross-entropy.** One score per class, zₖ = wₖ · x + bₖ; pₖ = e^(zₖ) / Σⱼ e^(zⱼ);
   positive, sums to 1; ℒ = −Σᵢ log p(true class of i). Worked example with three classes. Figure: N
   inputs on the left, C outputs on the right, softmax.
6. **How to train it? The loss landscape.** A 2D cartoon surface ℒ(θ₁, θ₂), labelled as a cartoon. The
   gradient ∇ℒ = (∂ℒ/∂θ₁, ∂ℒ/∂θ₂) points uphill, steepest ascent; step the other way. Two wells: two
   starts end in two different minima (live, draggable start). Logistic regression's loss is a single
   bowl; networks' losses are not.
7. **Gradient descent and the learning rate.** θ ← θ − η ∇ℒ(θ). Real example: logistic regression on
   last lecture's hours-of-study data, parameters (w, b). Precomputed runs for a small, a good and a
   too-large η, replayed as a moving dot on the contour plot, with the loss per step.
8. **The perceptron (1958).** Photo: Rosenblatt wiring the Mark I Perceptron (user confirmed it is
   Rosenblatt). Same score f(x) = w · x + b; a step instead of the sigmoid: predict sign(f); on a mistake
   w ← w + η yᵢ xᵢ, b ← b + η yᵢ, which is stochastic gradient descent on max(0, −y f(x)).
9. **XOR: no line works.** XOR data from the SVM deck; logistic regression's best fit (precomputed) is
   p ≈ 0.5 everywhere, accuracy 50%. The perceptron and logistic regression draw one line; XOR needs two.
10. **Perceptrons (1969).** Photos of Minsky and Papert, the book cover. They proved what single-layer
    perceptrons cannot compute, XOR among them. History nuance in the notes only.
11. **Add a hidden layer.** Animation: one neuron, copied into a column of hidden neurons, each
    connected to all inputs; then the output nodes and their edges appear. Each hidden neuron is a
    logistic regression on the inputs; the output layer is a softmax on the hidden neurons. Feed-forward
    and fully connected: a multilayer perceptron (MLP).
12. **Forward propagation.** h = σ(W₁x + b₁), z = W₂h + b₂, p = softmax(z), with the shapes of each
    matrix; θ = (W₁, b₁, W₂, b₂); same cross-entropy loss. Then: without σ, W₂(W₁x + b₁) + b₂ is one
    linear layer again.
13. **XOR by hand.** h₁ ≈ OR, h₂ ≈ AND, output ≈ "OR and not AND", with round weights and a four-row
    table students can check (sigmoid units, binary output = two-class softmax with scores (f, 0)).
14. **Training learns XOR.** Precomputed full-batch gradient descent on a small MLP (fixed start, checked
    to converge), replayed: the decision map, the loss curve and accuracy. How the gradients are found:
    next class.
15. **Takeaways.**
16. **Thanks.**

## Class 2: training a network (`neural_nets_2.html`)

1. **Title.** Neural networks. Part 2: training.
2. **Recap.** Forward propagation equations and θ ← θ − η ∇ℒ. We assumed we had ∇ℒ. Where does it come
   from?
3. **The chain rule.** A weight affects the loss through a chain of functions; multiply the derivatives
   along the chain. For a sigmoid output with cross-entropy, ∂ℒ/∂z = p − y (two-line derivation).
4. **Output-layer weights.** In a small network (two inputs, two hidden units, one output):
   ∂ℒ/∂w = (p − y) · hⱼ, with the path highlighted.
5. **One layer deeper.** ∂ℒ/∂w = (p − y) · wⱼ · hⱼ(1 − hⱼ) · xᵢ; the factor (p − y) is reused.
6. **Several paths: add them.** With several outputs a hidden weight reaches the loss along several
   paths; sum over them. In matrix form: δ₂ = p − y; δ₁ = (W₂ᵀ δ₂) ⊙ h ⊙ (1 − h); ∂ℒ/∂W₂ = δ₂ hᵀ,
   ∂ℒ/∂W₁ = δ₁ xᵀ. Backpropagation: compute δ from the output backwards, reusing each layer's δ.
7. **The recipe.** Forward pass (store h, p) → δ at the output → propagate back → all gradients → update
   every weight, using the old weights throughout.
8. **Update rule and learning rate.** θ ← θ − η ∇ℒ; too small, too large (as last class); learning-rate
   schedules that decay η.
9. **Momentum.** v ← β v + ∇ℒ, θ ← θ − η v: a running average of gradients. Figure: plain gradient
   descent zigzags on an elongated bowl, momentum does not (precomputed).
10. **Adam and other optimizers.** Momentum plus a separate step size per parameter (divide by a running
    average of squared gradients). Same figure, Adam's path. The usual default in practice.
11. **Local minima.** The two-well cartoon again: restart from several starts and keep the best;
    momentum can roll past a shallow minimum.
12. **Stochastic, mini-batch, batch.** Gradient from one record, from a few, or from all; paths on the
    same contour plot (precomputed). An epoch is one pass through the training data; updates per epoch
    for each method.
13. **When to stop.** Maximum number of epochs; convergence (gradient near 0, weights stop changing);
    loss low enough; validation loss starts rising (early stopping). Figure: training and validation
    loss per epoch from a precomputed overfitting run, early-stopping point marked; decision maps at the
    early-stopping point and at the end.
14. **Characteristics of neural networks.** Draft (the original slide was not recorded): strengths and
    weaknesses cards.
15. **The family tree.** Neural networks → perceptron (1958) → MLP + backpropagation (1986); CNN (1989);
    RNN (1990) → LSTM (1997) and GRU (2014) → encoder–decoder with attention (2014, built on GRU units)
    → Transformer (2017); MLP → Transformer (every Transformer layer contains an MLP). Next lecture.
16. **Takeaways.**
17. **Thanks.**

## Revision 1 (2026-10-12): after comparing with the course's earlier slides

The user compared our decks with the course's earlier forward-propagation and backpropagation slides
and asked for these changes (major additions are discussed afterwards):

- [x] Notation: layer index as a superscript, W⁽¹⁾, b⁽¹⁾, W⁽²⁾, b⁽²⁾, δ⁽¹⁾, δ⁽²⁾, in both decks
      (slides, figures, notes). The hidden-layer sum keeps the name aⱼ.
- [x] Class 1: three new slides before the perceptron. (1) A photo of real neurons; (2) the
      labelled neuron diagram (Blausen 0657, BruceBlaus, CC BY 3.0); (3) the neuron beside a
      simplified perceptron diagram, citing McCulloch & Pitts (1943) and Rosenblatt (1958).
- [x] Class 1: bias drawn as a node with constant input 1 (the neuron, perceptron and network figures).
- [x] Class 1: a deeper network with layer-l notation, after the single-hidden-layer forward pass.
- [x] Class 2: the small network written out as one formula, on a slide.
- [x] Class 2: a loop diagram, forward propagation → total error → gradients → update → back,
      after the recipe.
- [x] Class 2: patience (stop after a set number of epochs without improvement) on "When to stop".
- [x] Class 2: characteristics gain "training is time-consuming" and "irrelevant inputs can get
      zero weights".

Done as follows (details in NOTES.md):
- Class 1 order now: … gradient descent → Networks of neurons (photo) → A neuron (diagram) → A very
  simplified neuron (diagram beside a perceptron, both citations) → The perceptron (1958) → …
  → Forward propagation → Deeper networks → XOR by hand → …
- Deeper networks writes layer outputs as h⁽ˡ⁾, h⁽⁰⁾ = x, not a⁽ˡ⁾, because class 2 uses aⱼ for the
  sum before the sigmoid.
- Bias nodes ("1", dashed) are drawn in the class 1 recap neuron, the perceptron, the forward
  propagation network and the deeper network. The class 2 diagrams are unchanged.
- Class 2 order now: Recap → The network is one formula → The chain rule → … → The recipe → The
  training loop → The learning rate → … When to stop gains a patience step (patience 400).

## Revision 2 (2026-10-13): new order for class 1

Agreed with the user: structure and the forward pass first, then the loss and optimization.

1. Pandemonium · 2. Title
3. Losses for a classifier (from the logistic deck): the 0–1 loss broken into cases; plot of 0–1,
   hinge and log loss against y f(x)
4. Recap: logistic regression, Model box defines f(x) = w · x + b and p = σ(f(x))
5. −log p(true class) against p(true class), with the 0–1 loss dotted
6. A very simplified neuron (Blausen credit moves here) · 7. Networks of neurons
8. Combining multiple neurons: hidden layer, one sigmoid output, log loss
9. Softmax: three classes · 10. Two classes: softmax = sigmoid
11. Forward propagation (3 outputs) · 12. Deeper networks (3 outputs)
13. Why hidden layers? Logistic regression can't learn XOR (points only)
14. Perceptrons (1969), new wording · 15. XOR with two hidden units, with the network drawn
16. How do we choose the weights? (transition) · 17. Cross-entropy
18. Multilayer perceptrons: Model and Loss boxes, general diagram
19. The loss landscape · 20. Gradient descent · 21. Training learns XOR
22. Takeaways · 23. Thank you · 24. Bonus: the perceptron
Removed: "A neuron". Decisions: keep Gradient descent (class 2 refers to it); eyebrow "Why hidden
layers?" since XOR needs one hidden layer, not depth; the second softmax slide becomes "Cross-entropy".

Status (2026-10-13): implemented. Built, every step screenshotted, interaction, phone, dark-mode and
formula-wrapping tests pass, check_numbers.py passes. One deviation: the training slide says two
softmax outputs (see NOTES.md, Revision 2).

## Revision 3 (2026-10-14): class 2 backpropagation as one worked example

Asked by the user, after comparing with last year's backprop slides: the 1-D chain slide was confusing
because the chain is really part of the larger network. Work through one example on the full network,
with numbers. Agreed order:

1. xkcd · 2. Title · 3. Recap: shown all at once (no steps)
4. The network is one formula (kept); its loss is now squared error, ℒ = ½(p − y)², to match the example
5. **A worked example** (new): the 2-2-1 network with the weights on the connections, one point
   x = (2, 1), y = 1; forward pass with numbers (h, z, p, ℒ)
6. **An output weight, v₁**: the path v₁ → z → p → ℒ highlighted on the full network; the chain rule;
   the three factors with numbers, one per step; ∂ℒ/∂z kept for reuse
7. **A hidden weight, w₁₁**: the longer path x₁ → h₁ → z → p → ℒ; reuse ∂ℒ/∂z
8. **Update** (new): η = 1, the two new weights
9. **Same example, cross-entropy** (new): only ∂ℒ/∂p changes; p(1 − p) cancels and ∂ℒ/∂z = p − y;
   the gradients compared
10. Several paths: add them (kept) · 11. The recipe (kept) · then the training loop and the rest
Removed: the chain rule slide (1-D chain) and the Adam slide.

Numbers (x = (2, 1), y = 1): w₁₁ = −0.5, w₁₂ = 1, b₁ = 1; w₂₁ = 0.5, w₂₂ = −1, b₂ = −0.5; v₁ = 2, v₂ = 0.5,
c = −1. They were chosen by a search so that a student working with three decimals gets the same
three-decimal answers as the exact computation at every step; check_numbers.py verifies this.

Follow-up (2026-10-14), asked by the user: "Several paths" used δ and the matrix form, which last year's
slides do not (they show the highlighted paths only). Now two slides with numbers: "Two outputs" (same
first layer; v₂₁ = 1, v₂₂ = 0.5, c₂ = −1; softmax, cross-entropy, y = (1, 0); p = (0.675, 0.325)) and
"Add the paths" (−0.256 through z₁, +0.128 through z₂, sum −0.128). The recipe and the takeaways are in
words and partial derivatives; no δ, no matrix form on the slides (the recipe's notes keep one line).

Follow-up 2 (2026-10-14), asked by the user: the squared-error example looked like regression (squared
error) but had a sigmoid output p and a label y = 1. Now it is regression first, then the same problem as
a class, then cross-entropy:
- Regression (slides "The network is one formula" to "Update the weights"): linear output ŷ = z, target
  y = 2, ℒ = ½(ŷ − y)²; ŷ = 0.651, ℒ = 0.910; ∂ℒ/∂v₁ = −0.986, ∂ℒ/∂w₁₁ = −1.061; η = 0.1 gives
  v₁ = 2.099, w₁₁ = −0.394.
- "Now predict a class" (new): sigmoid output p = 0.657, label y = 1, squared error kept; the one new
  factor is p(1 − p) = 0.225 in place of ∂ŷ/∂z = 1; table regression vs class.
- "Now with cross-entropy": as before (class, squared error vs class, cross-entropy).
The sigmoid's slope h₁(1 − h₁) is shown with four decimals, 0.1966: with 0.197 the regression gradient
for w₁₁ comes out −1.063 by hand against −1.061 exactly. All later slides give the same numbers with
0.1966.

Follow-up 3 (2026-10-14), asked by the user ("we are only showing examples of the chain rule"):
- "The chain rule" (one path, x → u → y; y = (3x + 1)² at x = 1 gives 24) and "When the chain branches"
  (u₁ = x², u₂ = 3x, y = u₁u₂ at x = 2 gives 24 + 12 = 36), right after "The network is one formula".
- "The general rule", after "Add the paths": aⱼ = Σᵢ wⱼᵢoᵢ + bⱼ, oⱼ = φ(aⱼ); ∂ℒ/∂wⱼᵢ = (∂ℒ/∂aⱼ)oᵢ;
  ∂ℒ/∂aⱼ = φ′(aⱼ) Σₖ wₖⱼ ∂ℒ/∂aₖ; the output's error from the loss; checked on the example (−0.128).
- The recipe now refers to these rules instead of repeating the formulas.

Follow-up 4 (2026-10-14), asked by the user: notation. For layer l, z⁽ˡ⁾ is the pre-activation (weighted
sum) and a⁽ˡ⁾ = φ(z⁽ˡ⁾) the activation; a⁽⁰⁾ = x; layer superscripts everywhere. Hidden h → a⁽¹⁾, hidden
pre-activation a → z⁽¹⁾, output z → z⁽²⁾, output weights v → w⁽²⁾, biases b → b⁽¹⁾, c → b⁽²⁾. Stated on
"The network is one function" (now with a diagram naming every symbol). Slides renamed: "Regression
example", "Classification example". The recap slide and class 1 keep h (the user's choice). "When the
chain branches" keeps dy/dx (y depends only on x there). Figure labels now stack a superscript over a
subscript (w₁₁⁽¹⁾), as KaTeX does (mtxt in common.js).

Follow-up 5 (2026-10-15), asked by the user: "Classification example" and "Now with cross-entropy" are one
slide. The classifier uses log loss from the start (as for logistic regression): p = 0.657, ℒ = 0.420,
∂ℒ/∂z⁽²⁾ = p − y = −0.343, gradients −0.251 and −0.270. Squared error on p is only in the speaker notes.
The table is gone, so the network sits exactly where it does on slide 9 (and appears at once).

Follow-up 6 (2026-10-15), asked by the user: the recap slide (slide 2) gets a last step where the network
is live. Each of the 12 weights is a vertical bar on its edge, dragged between −3 and 3; edges turn teal
(positive) or orange (negative) and thicken with the weight. The inputs change by ▲/▼ buttons (step 0.5,
−2 to 2), on the user's request that they not look like the weight sliders. Biases are 0 and not drawn.
p₁ and p₂ are bars from 0 to 1. Start values are fixed (W1, W2, x in code_2.js); leaving the slide resets
them. Checked in check_numbers.py and tests/recap2.js (also driven from the presenter window).
