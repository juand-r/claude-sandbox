# Plan and notes

## Plan
- [x] Agree on scope with the user. Derivation: primal only, with a short mention that it is
  solved with Lagrange multipliers. Soft margin: slack variables, plus a bonus slide on hinge
  loss. Kernels: high level, with an example that is not linearly separable. No multiclass.
- [x] Design datasets and check them with scikit-learn.
- [x] Write `svm_lecture.html` on the ROC deck's engine (same template, chart helper, presenter view).
- [x] Render all slides; fix layout (plots were too tall and the slides shrank; labels overlapped).
- [x] Compare the deck's solver with scikit-learn (`check_numbers.py`). All 13 cases agree.
- [x] Test interactions, step-0 builds, dark mode, phone width, presenter view.
- [x] Commit and push.

## Conventions carried over from the ROC deck (user's corrections)
- The title slide has no figure: nothing students cannot read yet.
- Refer only to material the class has covered: k-NN, naive Bayes, decision trees, ROC and
  AUC, thresholds, precision and recall. No logistic regression, perceptrons or neural networks.
- Every figure builds up: the data points alone first, then lines, streets and labels by step.
- Positives green (`--pos`), negatives purple (`--mean`), highlights amber (`--hi`),
  mistakes and slack orange (`--err`); teal (`--model`) is the template accent and the
  colour of the fitted boundary.
- Presenter name left blank; the template author's credit kept as "slide template".

## Slide outline
0. Opener (added at the user's request): the "Running Away Balloon" meme on 99% accuracy
   with 99% of the data in one class, a recap of class imbalance. Image only, embedded as
   base64; the source file is `assets/meme_accuracy.webp`.
0b. Announcements (added at the user's request, styled like the Naive Bayes deck's slide;
    placed before the title): HW 3 due Thursday; project proposal due Thursday; social impact
    presentation at the end of class today; no office hours today (plain white card).
    One card per step.
0c. Supervised learning: the story so far (user's request; placed before the title). The Naive Bayes deck's taxonomy
    tree, supervised branch only, re-coloured to this deck's class colours; new icons for SVMs
    (today) and neural nets (next week, under both classification and regression).
1. Title (text only).
2. Which line? Three separating lines (A, B, C), their streets, your own line, then the SVM.
3. Hyperplane w·x + b = 0: sliders for w and b, the normal vector, the two sides, f(x) as a score.
4. Distance to the hyperplane: r = f(x)/‖w‖, derived in three steps with a draggable point.
5. The margin: closest points, scale convention y f = 1, street width 2/‖w‖.
6. Hard-margin SVC: maximize 2/‖w‖ ⇔ minimize ½‖w‖², quadratic program, Lagrange multipliers
   named, w = Σ α_i y_i x_i; α = 1/12, 1/6, 1/4 for the three support vectors.
7. Drag points; the hard-margin SVC is retrained live; message when no solution exists.
8. Soft margin: slack ξ_i, objective ½‖w‖² + C Σ ξ_i, the three slack cases.
9. The role of C: slider from 0.01 to 100.
10. Rings: no line separates; lift with z = squared distance from the centre; the separating
    plane in 3D is a circle in 2D.
11. Kernel trick: dot products → K; RBF kernel; γ slider; rings and XOR.
12. General properties (six cards).
13. Exercise: w = (3, 4), b = −10; five points covering every slack case.
14. Takeaways.
15. Bonus: slack is hinge loss.
16. Thanks.

## Decisions and findings
- Solver: SMO on the dual with the maximal-violating-pair rule, the method used in LIBSVM.
  Hard margin is C = 10⁴.
- Separable data: max-margin line x₁ + x₂ = 10, w = (0.5, 0.5), b = −5, width 2.83; designed by
  hand (two positive support vectors on x₁ + x₂ = 12, one negative on x₁ + x₂ = 8) and confirmed
  by scikit-learn.
- Two scikit-learn comparisons differ in ways that are correct, and the check handles them:
  (1) when extra points lie exactly on the margin, the support vectors are not unique (rings
  lifted to 3D; rings with a linear kernel); (2) on XOR with a linear kernel, w = 0 and any b in
  [−1, 1] is optimal. The check then compares the optimal objective value, which is unique.
- On slide 7, dragging a point to the edge of separability made the hard-margin solver hit its
  iteration limit and throw, which froze the figure. That slide now calls the solver with
  `strict:false` and shows "no solution" when it does not converge. Everywhere else
  non-convergence still throws.
- Plots are capped at 74vh (56vh on slides with tiles and controls) so slides never need shrinking.
- Claim on the properties slide, "roughly quadratic or worse in the number of points" for kernel
  SVM training: standard in the literature, stated as approximate. Not measured here.
- Definition of "margin": the deck uses the textbook one (CS229, ISLR): the distance from the
  boundary to the closest training point, 1/‖w‖ after scaling, half the street. Some sources
  (Wikipedia; Cortes and Vapnik 1995, from memory, not checked) call the full width 2/‖w‖
  the margin. Slides 2, 5 and 6 were aligned to the textbook definition at the user's request.
- Formula layout (user report: formulas broke mid-expression, e.g. "exp(−γ / ‖x − x′‖²)").
  Fix, in both decks: inline `.math` never wraps; formulas longer than about 18 characters
  sit on their own line (`.math.dm`); equation boxes break only at chosen points, with
  continuation lines indented. On phones (≤ 620px) formulas may wrap, since overflowing the
  screen is worse. `tests/mathwrap.js` checks this at 1440×810, 1280×720, 1920×1080, 1024×768
  and 390×844; both decks pass. (The phone rule must come last in the stylesheet, or the
  later `.eq` and `.answer .math` rules override it; the first attempt failed for that reason.)
