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
6. Still a hyperplane: the SVM deck's soft-margin data; probability shading, p = 0.1 / 0.5 / 0.9
   lines; the soft-margin SVM's line (C = 1) overlaid; Platt scaling in the notes.
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
