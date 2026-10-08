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
