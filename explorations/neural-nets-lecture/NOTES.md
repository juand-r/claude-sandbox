# Notes

## Request

The user teaches neural networks over two classes, after the logistic regression deck. They gave
the topics and order (see `PLAN.md`) and decided:

- class 1 covers forward propagation; gradient descent comes before backpropagation;
- write logistic regression as softmax with one-hot labels; skip the σ(z₁ − z₂) identity;
- the photo on the perceptron slide is Rosenblatt (the user confirmed it);
- compute every experiment first, save it and replay it, so the result in class is known in advance.
  Only gradient descent on the 2D cartoon surface runs live, so the start can be dragged;
- a third lecture on architectures will be planned later, as bonus topics.

## Status

- [x] `PLAN.md`, slide by slide, for both classes.
- [x] `experiments.py`: all runs, written to `build/data.json`.
- [x] `check_numbers.py`: every quoted number, the gradients and the replays, recomputed independently.
- [x] Class 1 deck, 16 slides. Tested: every step, dragging, replays, presenter view, dark mode,
      phone width, formula wrapping.
- [x] Class 2 deck, 17 slides. Same tests.

## Decisions

- Data. The hours-of-study data from the logistic regression deck is reused for every
  gradient-descent picture, because it has two parameters (w, b) and so the loss can be drawn.
  Standardized hours give a round bowl, used in class 1 and for the batch-size slide. Raw hours give a
  long, narrow valley (curvature ratio about 350), used for momentum and Adam.
- The loss plotted is the average over the training points, not the sum on the slides. The minimum is
  in the same place; the speaker notes say so.
- Learning rates were picked by hand so each run shows its point: class 1 η = 0.1, 1, 20; raw
  valley η = 0.2 (plain), 0.05 with β = 0.9 (momentum), 0.15 (Adam). The class 2 notes say the
  optimizer comparison is a picture, not a benchmark.
- XOR uses the data of the SVM deck (24 points, 6 per corner), with inputs scaled to about [−1, 1]. A
  2-3-2 network with η = 2: seed 1 converges, seed 0 stalls at loss 0.35 with 14 of 24 right. The
  stalled run is a flat region rather than a strict minimum (the Hessian's smallest eigenvalue is
  about −10⁻⁶ and the loss keeps creeping down), so the slide says "stalls", not "local minimum".
- Early stopping uses noisy two-moons data: 30 training points, 400 validation points, 40 hidden
  units, Adam with η = 0.02, 3,000 epochs. Lowest validation loss at epoch 443.
- The characteristics slide (class 2, slide 14) is a draft: the user's original slide was not recorded.
- Class 2 uses vⱼ for the output weights of the small network, to keep them apart from the hidden
  weights wⱼᵢ; the matrix form then uses W₁ and W₂ as in class 1.

## Corrections found by checking

- Class 1 notes first said XOR training does little for the first hundred steps. The run reaches
  100% accuracy by step 60; the notes now say the loss barely moves for about thirty steps.
- Class 1 notes first gave e² + e + e⁻¹ ≈ 10.47; it is 10.48.
- Class 2 notes first said Adam reaches the minimum in about 100 steps; it is about 80.
- The η = 20 note now describes what the run does: the loss jumps between about 0.5 and 1.2.

## Sources

- Pandemonium: O. Selfridge, "Pandemonium: a paradigm for learning", 1959. The drawing is credited on
  the slide to Lindsay & Norman, Human Information Processing (the illustrator is not named).
- Perceptron: F. Rosenblatt, 1958. Minsky & Papert, Perceptrons, MIT Press, 1969.
- Backpropagation: Rumelhart, Hinton & Williams, 1986.
- Universal approximation: G. Cybenko, Mathematics of Control, Signals and Systems 2 (1989) 303–314;
  K. Hornik, M. Stinchcombe & H. White, Neural Networks 2 (1989) 359–366. Checked by web search.
- Momentum: B. T. Polyak, 1964 (heavy-ball method). Adam: D. Kingma & J. Ba, arXiv:1412.6980 (2014),
  defaults β₁ = 0.9, β₂ = 0.999, ε = 10⁻⁸. Checked by web search.
- Family tree dates: CNN (LeCun et al., 1989), RNN (Elman, 1990), LSTM (Hochreiter & Schmidhuber,
  1997), GRU (Cho et al., 2014), attention (Bahdanau, Cho & Bengio, 2014; its encoder–decoder uses
  GRU-style units, appendix A.1.1), Transformer (Vaswani et al., 2017).

## Math typesetting (2026-10-09)

The user said the formulas did not show up well. The cause, checked: the formulas used JetBrains Mono
from Google Fonts, whose served subsets lack 12 of the 85 characters the formulas use (the Unicode
subscripts ₁ ₂ ᵢ ⱼ ₖ ᵀ and ℒ ∂ ∇ ← √ ⊙). The browser drew those from whatever system font it found, so one
formula mixed several fonts and sizes, and the one-character subscripts are small by design. The user
chose real math typesetting.

- Class 1 formulas are now LaTeX, typeset by KaTeX 0.16.28 at build time (`build/tex.js`). KaTeX's
  woff2 fonts are embedded (about 0.4 MB of base64), so nothing loads from the network.
- Checked with Chrome's own font report: every visible math glyph comes from a KaTeX font.
- Figure labels (2026-10-09, at the user's request): `mtxt()` in `build/common.js` draws SVG labels in
  the KaTeX fonts. Single letters are italic variables, words and digits upright, ℒ is the script L,
  and subscripts (Unicode, or `_N`) are smaller and lowered. The chart axes (ticks and axis names)
  are redrawn the same way. Chrome's font report shows only KaTeX fonts in formulas and labels.
- Class 2 converted the same way. On phones the forward-propagation box is set slightly smaller so
  it does not scroll.
- Still plain text: the speaker notes (presenter view only) and the numeric read-out tiles.

## Revision 1 (2026-10-12): changes after comparing with the course's earlier slides

- Layer index is a superscript: W⁽¹⁾, b⁽¹⁾, W⁽²⁾, b⁽²⁾, δ⁽¹⁾, δ⁽²⁾ (slides, figures, notes). The label
  helper `mtxt()` gained superscripts, written `W^(1)`; all five copies of it were updated together.
- New class 1 slides: "Networks of neurons", "A neuron", "A very simplified neuron", "Deeper networks".
- Images. `assets/neurons_photo.webp` was extracted from the user's earlier course slides
  ("11 - NeuralNets - ForwardProp", slide 8); its original source is not known, so it carries no
  credit line. `assets/neuron_blausen.webp` is "Blausen 0657 MultipolarNeuron" by BruceBlaus,
  Wikimedia Commons, CC BY 3.0 (licence and author read from the Commons file page). It is the same
  image as in the user's slides (mean pixel difference 0.3 of 255 after resizing); the Commons
  original was used because it has a higher resolution. Credit line on the slide.
- Citations, checked against the publishers' records (Springer, PubMed):
  W. S. McCulloch and W. Pitts, "A logical calculus of the ideas immanent in nervous activity",
  Bulletin of Mathematical Biophysics 5 (1943), 115–133, doi:10.1007/BF02478259.
  F. Rosenblatt, "The perceptron: a probabilistic model for information storage and organization in
  the brain", Psychological Review 65(6) (1958), 386–408, doi:10.1037/h0042519.
- Deeper networks uses h⁽ˡ⁾ for layer outputs (see PLAN.md for why not a⁽ˡ⁾).
- Patience. Computing the stopping epoch showed that the validation loss dips to 0.35 at epoch 25,
  rises, and only beats that at epoch 327. So a patience of 300 or less stops early (patience 300:
  epoch 325, keeping the epoch-25 weights), while patience 400 stops at epoch 843 and keeps epoch 443
  (validation loss 0.33). The slide uses 400 and the notes tell the dip story; check_numbers.py
  verifies both.
- New class 2 slides: "The network is one formula", "The training loop".
- Characteristics gained "irrelevant inputs can be ignored: training can drive their weights to zero"
  and "training is time-consuming".

## Revision 2 (2026-10-13): class 1 reordered

The user asked for structure and the forward pass first, then the loss and optimization. The new
order (24 slides) is in `PLAN.md`. What changed besides the order:

- New slides: "Losses for a classifier" (the four cases of y and f(x), then the 0–1, hinge and log
  losses against y f(x)), "Confident and wrong costs a lot" (−log p(true class) against
  p(true class), with the 0–1 loss dotted), "Softmax with two classes is the sigmoid", "How do we
  choose the weights?", "Cross-entropy", "Multilayer perceptrons" (Model and Loss boxes and a general
  diagram).
- Removed: "A neuron". Its explanation of the parts of a neuron moved to the notes of "A very
  simplified neuron", and the image credit moved with the image.
- "Add a hidden layer" is now "Combining multiple neurons", with one sigmoid output and the log loss.
  Softmax, forward propagation and deeper networks now show three classes (the 2-3-3 network on
  the forward-propagation slide has 21 weights and biases).
- The XOR slide shows the data only. The hand-set XOR slide draws the 2-2-1 network with its weights.
- The perceptron moved to a bonus slide after "Thank you".
- Training slide. The plan said "one sigmoid output, log loss". The replayed run was trained with two
  softmax outputs, and gradient descent follows a different path on that parametrization, so the
  slide says two softmax outputs and cross-entropy. That also keeps class 2 correct, which calls it
  "the same 2-3-2 network as last class" with 17 weights and biases.
- New numbers checked in `check_numbers.py`: −log 0.99 = 0.01, −log 0.5 = 0.69, −log 0.01 = 4.61;
  log 2 = 0.69; −log σ(y f) = log(1 + e^(−y f)); cross-entropy 0.35, 1.35, 3.35 for true class 1, 2, 3
  (the class 3 value was quoted as 3.3 before); 21 parameters.

## Activation functions (2026-10-13)

Agreed with the user: introduce φ where the forward-propagation slide argues that a nonlinearity is
needed, since any nonlinear function prevents the collapse into one linear map.

- Forward propagation: the step is now "Why a nonlinearity?" and ends with "Any nonlinear function φ
  works; the sigmoid is one choice." Its equations keep σ.
- New slide after it, "Activation functions": sigmoid, tanh and ReLU on the same axes, and the
  output layer stays softmax (or σ for two classes).
- From "Deeper networks" on, hidden layers are written with φ (Deeper networks, Multilayer
  perceptrons, Takeaways). "Combining multiple neurons", the hand-set XOR network and the training
  run keep σ, because they are sigmoid networks.
- φ is typeset as \varphi, so that the formulas match the figure labels (Unicode φ in KaTeX_Math
  is the curly form; KaTeX's \phi is the straight form ϕ).
- Class 2 backpropagation still derives the sigmoid case. Added: on "One layer deeper" and in the
  recipe, a line saying h(1 − h) is σ′(a) and becomes φ′(a) for another activation; the notes of
  "Several paths" say the same, and the notes of "One layer deeper" give the ReLU factor.
- Checked in check_numbers.py: tanh(a) = 2σ(2a) − 1, the sigmoid's slope is at most 1/4 (at a = 0),
  tanh's slope at 0 is 1.
