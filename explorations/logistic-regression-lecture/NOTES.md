# Plan and notes

## Request
The nonlinear regression deck does not fill the 90-minute class (the in-class notebook will probably
not be done). The user asked for a separate deck to use in the same class, to prepare for their neural
networks lecture the following week:
- start from the SVM written with hinge loss, then use another loss;
- binary only (the user was unsure; binary keeps the comparison with the SVM clean);
- structure only: students have not seen gradient descent, which comes next lecture;
- the user corrected one claim in the draft outline: an SVM gives a score that can be thresholded,
  not just a side. The deck says both models give a thresholdable score; logistic regression's score
  is a probability.

## Plan
- [x] Check scikit-learn's objective and a Newton's-method fit on draft data.
- [x] Write the slides and figures (`build/`), assemble the deck.
- [x] Verify fits and every number (`check_numbers.py`).
- [x] Screenshot every step; dark mode, phone width, presenter view, formula wrapping.

## Slide outline
1. Title: Logistic regression.
1a. What are we minimizing? (added at the user's request) Linear regression: squared errors; PCA:
    reconstruction error; SVM: ½‖w‖² + C Σ ξᵢ. The quantity is the loss.
    Each loss is written ℒ = …; two boxes follow: Model, ŷᵢ = f(xᵢ | θ) (the user's notation), and Loss,
    min over θ of ℒ(θ). The notes answer "what is the model in each case?" (linear regression w · x + b;
    PCA's reconstruction μ + V Vᵀ(x − μ); SVM sign(w · x + b)).
1b. Minimize the training error? (added at the user's request) The binary actual/predicted table with
    ✓/✗; for a threshold t, f(xᵢ) > t for yᵢ = +1 and < t for yᵢ = −1; the count of mistakes is the
    0–1 loss; with t = 0 both read yᵢ f(xᵢ) > 0. The speaker notes answer "why not minimize the 0–1
    loss directly?": no direction (flat, then jumps), NP-hard in general as the number of features grows
    (Ben-David, Eiron & Long 2003), no preference among equally good lines; hence hinge or log loss.
2. The SVM as a loss: score f(x) = w · x + b; hinge loss; soft-margin SVM as ½‖w‖² + C Σ hinge;
   points past the margin pay nothing. Figure: 0–1 and hinge loss against y·f(x).
3. Log loss: log(1 + e^(−y f(x))) beside the hinge; logistic regression as ½‖w‖² + C Σ log loss.
4. The sigmoid: σ(z); p(y = +1 | x) = σ(w · x + b); p(true class) = σ(y f); log loss = −log p(true class).
4a. Sigmoid and log loss (added at the user's request): 1 − σ(f) = σ(−f), so the true class gets σ(y f);
    −log σ(y f) = log(1 + e^(−y f)); the sigmoid's inverse is the log-odds, z = log(p/(1 − p)), so the score
    is the log-odds. (The user asked to show the two are "inverses"; they are not. The inverse pair is the
    sigmoid and the log-odds, and the log loss is −log of the sigmoid.)
5. A fitted model: hours of study → pass (simulated, 20 students); fitted curve; p = 0.5 at 5.4 h;
   threshold slider with TPR and FPR, linking to the ROC lecture.
6. Still a hyperplane: the SVM deck's soft-margin data; probability shading and the p = 0.5
   line (the p = 0.1 and 0.9 lines were removed at the user's request: they looked like margins); the soft-margin SVM's line (C = 1) overlaid; Platt scaling in the notes.
7. One neuron: inputs → weights → Σ + b → σ → p; then a small network; "next week: networks and how
   to find the weights".
8. Takeaways. 9. Thanks.

## Decisions
- Objective: ½‖w‖² + C Σ log(1 + e^(−yᵢ f(xᵢ))), intercept not penalized, which is what scikit-learn's
  LogisticRegression minimizes (checked: the deck's Newton fit matches it to 1e-6). This makes the
  parallel with the soft-margin SVM exact. The 1D example is fitted without the ½‖w‖² term (C = ∞).
- The deck fits the models with Newton's method in JavaScript but never shows or names it; the slides
  say the fit is next week's topic.
- The SVM solver is copied from the SVM deck, where it is tested against scikit-learn; here it is
  tested again on the one dataset used.
- Colours: positives green, negatives purple; 0–1 loss orange, hinge teal (as in the SVM deck), log
  loss amber; logistic boundary teal, SVM line dashed ink.
- Probability shading uses cells that do not overlap; overlapping translucent cells showed a grid.

## Open
- The nonlinear regression deck's map slide shows logistic regression as "not covered"; it will be
  covered in the same class. Not changed (not asked).
- The nonlinear regression deck ends with the notebook and thanks slides; if this deck follows in the
  same class, the user may want to drop or move them.
- Notation pass (user's request): the loss box reads min over θ of ℒ(θ; D), D the training data
  (not ℒ(θ | D), which reads as a likelihood). Objectives on the SVM and log-loss slides are written
  ℒ = … like the loss slide's cards. The SVM slide names the model: f(x) = w · x + b with θ = (w, b).
  p(y = +1 | x) = σ(f(x)). Predict positive when p > t (strict, as on the training-error slide; the
  slider tiles and check_numbers.py follow). The 0–1 loss counts y f(x) ≤ 0 as a mistake, in the
  formula and in the plot. The algebra slide states that f stands for f(x) = w · x + b.
  One overload remains: on the loss slide f(xᵢ | θ) is the prediction ŷᵢ; for classifiers f is the
  score and the prediction is its sign (or its comparison with t).
- 2D slide, step 4 (user's request): the text stays and the figure is replaced by the same model in
  3D, height = p(green), so the surface visibly stays between 0 and 1. Green points at height 1,
  purple at 0, the p = 0.5 line in teal; the SVM line and its legend entry are hidden in this view.
  Drag turns it (code adapted from the SVM deck's 3D lift slide). The starting view looks roughly
  along the boundary, so the sigmoid profile shows.

## Math typesetting (2026-10-09)

At the user's request, the same fix as in `../neural-nets-lecture/` (see its NOTES.md for the cause:
the old math font lacked the subscripts and several symbols, so browsers mixed in fallback fonts).

- Formulas are LaTeX in `build/slides.html`, typeset by KaTeX 0.16.28 at build time (`build/tex.js`,
  copied from the neural nets deck so this folder stays self-contained). KaTeX's fonts are embedded.
- Figure labels and chart axes use the KaTeX fonts too (`mtxt()` in `build/code.js`). The "5.4 h"
  threshold label keeps "h" upright, since it is a unit.
- The 0–1 loss indicator 𝟙[·] is now a bold 1, 𝟏[·]: KaTeX's fonts have no blackboard-bold 1.
- Phones: the two long loss formulas (hinge and log loss slides) have a second, narrower
  line-breaking shown only below 620 px, because typeset math cannot reflow.
- The build files are now the source of the deck. Before this change the build reproduced the
  published deck byte for byte, so nothing was lost.
- Checked: Chrome's font report shows only KaTeX fonts in formulas and labels; check_numbers.py
  passes on fresh deck output; formula wrapping passes at five screen sizes.

## Student notes (2026-10-09)

The user reported that some students, less strong in math, were confused by the logistic regression
slides, and asked for LaTeX notes that go through the material in detail, spelling out how the two
threshold conditions become one formula with the indicator function.

- `notes/logistic_regression_notes.tex` (11 pages) follows the slide order: training as model plus
  loss; the 0–1 loss built in small steps (threshold 0, multiply by the label, a four-case table, the
  indicator function, a five-point worked example); the hinge and the log loss on the same five
  points; the sigmoid; σ(y f) as the probability of the true class; the log loss as −log p(true
  class); the log-odds; predictions and thresholds on the hours-of-study fit; a summary; an appendix of
  exp/log rules.
- Every number is computed by `notes/check_notes.py`. The hours-of-study fit comes from
  `tests/deck_outputs.json` (the deck's own fit, checked against scikit-learn by check_numbers.py).
- The Ben-David, Eiron and Long (2003) reference details (JCSS 66(3), 496–514) were checked by web search.
- TeX Live was installed in the session container with apt to compile it.
