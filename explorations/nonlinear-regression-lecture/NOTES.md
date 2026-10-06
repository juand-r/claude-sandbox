# Plan and notes

## Plan
- [x] Read lecture 14 (10 slide images and the transcript, 7,750 words).
- [x] Outline the deck: announcements, the map, title, then the three methods in the lecture's order.
- [x] Make datasets (`make_data.py`) and check the regression-tree example with scikit-learn first.
- [x] Build the deck on the SVM deck's engine (`build/assemble.py`).
- [x] Verify the deck's tree, kNN and SVR code against scikit-learn, and every number in the slides
  and notes (`check_numbers.py`).
- [x] Screenshot every step of every slide; fix layout and build-up problems (list below).
- [x] Dark mode, phone width, presenter view, formula wrapping.
- [x] Redesign "the story so far" as a table, as the user asked (details below).

## Requests that shaped the deck
- Same style as the SVM deck. Title "Nonlinear Regression".
- Announcements: homework and project proposal due "midnight tonight"; no office-hours card. The
  social-impact card is kept as it was in the SVM deck ("Today, end of class.").
- Cover everything in the lecture, without the banter; lean slides, since the questions to the class
  are said out loud; no instructions on how to use the widgets.
- "The story so far" (user's design): a table instead of a tree. Classification on the left,
  regression on the right; each classifier beside its regression version. Rows: logistic regression
  (faint, not covered) | linear regression; decision trees | regression trees; nearest neighbors |
  kNN regression; SVMs | support vector regression; Naive Bayes | a faint dash. The three regression
  versions fill in one per click, in lecture order. Polynomial regression and neural networks are
  left out. Icons are static: the classification ones from the Naive Bayes deck; logistic regression,
  regression trees, kNN regression and SVR are new, in the same style.
- Naive Bayes row: a regression version exists (Frank, Trigg, Holmes & Witten, "Naive Bayes for
  regression", Machine Learning 41, 2000) but is rarely used and, by that paper's own results,
  performs poorly; Gaussian naive Bayes takes continuous features but still predicts a class. The
  cell is a faint dash with a footnote marker; the footnote says "Naive Bayes regression exists
  (does not work well, not commonly used)" and gives the reference (the user's wording and citation).

## Slide outline
1. Announcements (3 cards).
2. Supervised learning: the story so far (table: each classifier beside its regression version).
3. Title: Nonlinear Regression.
4. Not every pattern is a line: dosage data, the least-squares line, then a regression tree.
5. A regression tree: the tree (splits at 14.5, 29, 23.5 mg) beside its step-function fit; one leaf
   highlighted with its four points and their average, 55.25.
6. Choosing a split: a threshold slider with the side means and residuals; the SSE of every
   candidate threshold (two local minima, at 14.5 and 29); best 14.5, SSE 19,523.
7. Grow, then stop: slider for the minimum number of points needed to split. 2: training SSE 0
   (overfit); 7 (do not split 6 or fewer, the lecture's example): 4 leaves; 19: one leaf (underfit).
8. Many features: a table like the lecture's (dosage, age, weight, sex); best threshold per feature; binary and multi-valued
   categoricals (one-hot, one value against the rest).
9. kNN regression: bone density against age; the 9 neighbours of age 40; the curve; k = 1, k = 40.
10. kNN with two features: prediction maps for k = 1 and k = 9.
11. Support vector regression: the ε-tube, the labels w · x + b ± ε, vertical slack; ε slider.
12. The SVR problem: the optimization problem; C slider (0.1 default, 10 large, 0.01 small).
13. Nonlinear SVR: dosage data, linear versus RBF, γ slider (0.02, then 0.2). C = 1000, ε = 5.
14. Takeaways: the three methods and their hyperparameters.
15. In-class notebook (Canvas → Assignments; pairs can turn it in together).
16. Thanks.

## Decisions
- Datasets. DOSE is hand-made to resemble the lecture's StatQuest example and chosen so the tree
  with "do not split 6 or fewer points" has the lecture's three splits in the lecture's order. Its
  leaf values are 4.17, 100, 55.25 and 3.0 (the lecture's were 4.2, 100, 52.8 and 2.5). The other
  three datasets are simulated with a fixed seed and labelled "Simulated data" on the slides.
- The lecture used a separate bone-density dataset for kNN; this deck simulates one with the same
  shape (rises to a peak near 30, then falls). The lecture's 2D figure was a pair of 3D surfaces; the
  deck shows the same two predictions (k = 1, k = 9) as colour maps.
- Colours: data points ink; fits and tubes teal (`--model`); thresholds and the highlighted leaf
  amber (`--hi`); residuals and slack orange (`--err`); the least-squares line purple (`--mean`).
- Tree convention: a node "dosage < t" sends yes to the left. Thresholds are midpoints between
  neighbouring values, as in scikit-learn.
- SVR solver: the ε-SVR dual in LIBSVM's form (2n variables), solved by the same SMO code as the SVM
  deck. A point within 0.001 (in units of y) of the tube's edge counts as on the edge, because free
  support vectors sit there only up to the solver's tolerance.
- On the linear data, C = 1 and C = 100 give the same line, so the C slide uses 0.1 as the default,
  10 as "large" and 0.01 as "small" (slopes 1.57, 2.12, 0.31).
- Two-feature kNN maps and the regression-tree diagram are excluded from the draw-in animation
  (thousands of cells; the tree has its own step reveals).

## Where the slides differ from the lecture transcript
These are said out loud in the lecture; the slides and notes avoid repeating them.
- scikit-learn's default for the minimum number of samples to split is 2, not 20
  (`min_samples_split=2`; `min_samples_leaf=1`). The slides do not quote a default.
- ε is measured vertically, along the y-axis, because it is an error in y. The transcript says
  "perpendicular to our y-axis" once, then (for slack) "parallel to the y-axis".
- SVR does not maximize the number of points inside the tube. It penalizes the total vertical
  distance outside the tube (C Σ (ξ + ξ*)), plus ½‖w‖². The slides say this.
- "Bone marrow density" in the transcript is bone (mineral) density; the slides say "bone density".
- Left out: the opening remarks about the weekend's events, the memes on the first slide of the
  original deck (ensembles and random forests, and "Scientists be like" on the title slide).

## Problems found in screenshots and fixed
- Regression-tree slide too small and its outer leaves clipped: moved to one column with the plot
  and tree side by side below the bullets.
- 2D kNN maps were not square, so the colour cells were taller than wide; fixed the chart size.
- kNN and "grow, then stop" showed tiles and a fit before anything was introduced; now points first.
- The split slide became too tall without height caps and the whole slide shrank; caps restored.
- The features table overflowed at phone width; it now scrolls inside its box.
