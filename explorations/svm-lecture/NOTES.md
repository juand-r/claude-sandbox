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
1b. Decision Boundaries (user's request): the user's two figures, images only. The tree figure
    is tinted by `tint_tree_regions.py`: yellow where circles are the majority (R1, R3, R5),
    blue where triangles are (R2, R4, R6). Counts read off the figure: R3 holds one circle and
    no triangles; R1 has one triangle among many circles.
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
- Definition of "margin" (final, at the user's request): the deck follows the course's lecture 11.
  The margin is the empty region between the margin lines w·x + b = ±1, and its width is
  ρ = 2/‖w‖. (Textbooks such as CS229 and ISLR instead call the half-width 1/‖w‖ the margin.)
  Distances are unsigned, |w·x + b|/‖w‖, as in lecture 11.
- Terminology changes requested by the user: no "street" anywhere (now "margin", "margin lines");
  "quadratic program" is now "constrained convex quadratic minimization problem".
- Added from lecture 11: the link to linear regression (w as the slopes, b the intercept);
  ‖w‖ defined as √(w₁² + w₂² + …); numeric features (one-hot encoding) and the slow or
  non-finishing solver on unscaled data; tuning C and the kernel by grid search in nested
  cross-validation; a hedged "many features" card.
- Formula layout (user report: formulas broke mid-expression, e.g. "exp(−γ / ‖x − x′‖²)").
  Fix, in both decks: inline `.math` never wraps; formulas longer than about 18 characters
  sit on their own line (`.math.dm`); equation boxes break only at chosen points, with
  continuation lines indented. On phones (≤ 620px) formulas may wrap, since overflowing the
  screen is worse. `tests/mathwrap.js` checks this at 1440×810, 1280×720, 1920×1080, 1024×768
  and 390×844; both decks pass. (The phone rule must come last in the stylesheet, or the
  later `.eq` and `.answer .math` rules override it; the first attempt failed for that reason.)
- Lagrange multipliers (user's decision): the deck names the method but shows no α and no
  w = Σ αᵢyᵢxᵢ, since that would be taken on faith. The hard-margin figure rings the support
  vectors (at the step that names them) without α labels. The kernel slide says the solver
  only needs pairwise similarities (dot products), and a new point is scored by a
  similarity-weighted vote of the support vectors. check_numbers.py still verifies the α
  values internally.

## Math typesetting (2026-10-09)

At the user's request, the same math fonts as the logistic regression and neural nets decks (see
`../neural-nets-lecture/NOTES.md` for why: the old math font lacked the subscripts and several
symbols, so browsers mixed in fallback fonts).

- This deck has no build step (the HTML file is the source), so KaTeX typesets the formulas when the
  page opens, not at build time. The LaTeX stays readable in the HTML. KaTeX's library and fonts are
  embedded (about 0.65 MB), so nothing loads from the network.
- The formulas were converted from Unicode to LaTeX with a small script, and every conversion was
  reviewed by eye. Slider labels, tile labels and table headers with math are converted too; the
  numeric read-outs stay in the monospace font.
- Figure labels and chart axes use the KaTeX fonts (`mtxt()`), with italic variables and real
  subscripts.
- Checked: no page errors; Chrome's font report shows only KaTeX fonts in formulas and figure labels;
  formula wrapping passes at five screen sizes; check_numbers.py passes on fresh deck output.
- On phones, two long objectives (soft margin, hinge form) have a second, narrower line-breaking.
- The KaTeX block sits inside `<main>`, outside the marker cuts the logistic regression and neural nets
  builds take from this file. After the change those three decks still rebuild byte for byte.
