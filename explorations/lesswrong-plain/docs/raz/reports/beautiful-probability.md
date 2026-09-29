# Report: Beautiful Probability (order 188)

Agent: batch 4a. Slug: `beautiful-probability`. Posted 2008-01-14.

## 1. The argument in three sentences

Jaynes's example of two researchers who stop with the same data (100 patients, 70 cures) under
different stopping rules shows, the post says, that frequentist methods can give different
conclusions from the same data, whereas the Bayesian likelihood, and so the posterior, cannot
depend on the researcher's private intentions. Bayesians expect probability theory to be
consistent, unique math (Jaynes, Cox's theorem), so a method that is not Bayesian must fail a
coherence test and can be Dutch-booked, and every approximation succeeds or fails to the extent
it approximates the Bayesian calculation. The difference is one of mindset: frequentists think in
tools, Bayesians in laws, like the second law of thermodynamics and the Carnot engine, which
govern real engines that cannot reach the ideal.

## 2. Sources checked

All saved under `data/sources/4a_beautiful-probability/` unless noted.

- Jaynes, "Probability Theory as Logic" (1990), https://bayes.wustl.edu/etj/articles/prob.as.logic.pdf
  (`jaynes1990_prob_as_logic.pdf`, text `jaynes1990.txt`). The post's quotation matches the
  paragraph beginning "Two medical researchers use the same treatment independently" word for
  word except: "stop after treating n = 100 patients" (post: "N=100 patients"), "decided that he
  would not stop" (post drops "that"), "n = 100; r = 70" (post: "n = 100 [patients], r = 70
  [cures]"). Not worth a note. Matched: "the private thoughts that went through the
  experimenter's mind"; "it is for all practical purposes impossible to sample deliberately to a
  foregone conclusion that is appreciably false" (Jaynes citing Savage 1962).
- Jaynes, *Probability Theory: The Logic of Science*, ch. 1-3 and preface
  (`data/sources/jaynes_book_ch1-3.txt`, saved by an earlier agent). Matched desideratum (IIIa):
  "If a conclusion can be reasoned out in more than one way, then every possible way must lead to
  the same result." Preface: "those rules admit only finite sets and infinite sets that arise as
  well-defined and well-behaved limits of finite sets."
- Wikipedia, "Likelihood principle" (raw wikitext, `wiki_Likelihood_principle.txt`). Matched: "This
  principle is controversial because it is inconsistent with the mainstream frequentist approach
  to inference."; "lies not in the actual data collected, nor in the conduct of the experimenter,
  but in the  two different designs of the experiment" (double space in source); Birnbaum 1962
  "argued that the likelihood principle follows from two more primitive and seemingly reasonable
  principles"; "upon further consideration Birnbaum rejected both his conditionality principle and
  the likelihood principle"; disputed by Akaike, Evans, Mayo (2010, 2014); Dawid "arguing
  Birnbaum's argument cannot be so readily dismissed"; Gandenberger "A new proof". Also Birnbaum's
  "confidence concept" quotation (used only for my understanding of the frequentist rationale).
- Wikipedia, "Interim analysis" (`wiki_Interim_analysis.txt`): "when repeated significance testing
  on accumulating data is done, some adjustment of the usual hypothesis testing procedure must be
  made to maintain an overall significance level" (citing Armitage, McPherson and Rowe 1969).
  Wikipedia "Sequential analysis" (`wiki_Sequential_analysis.txt`): stagewise ordering of p-values
  "first proposed by Armitage"; type I error rises with repeated looks.
- MacKay, *Information Theory, Inference, and Learning Algorithms*, ch. 37
  (`data/sources/mackay_itila.txt`, earlier agent). Matched: "seems to me a compelling argument for
  having nothing to do with p-values at all."
- Wikipedia, "Cox's theorem" (`data/sources/wiki_Cox_s_theorem.txt`, earlier agent). Matched: "It
  has been debated to what degree the theorem excludes alternative models for reasoning about
  uncertainty." Also Halpern (1999) on Cox's original postulates (not used in a note).
- SEP, "Dutch Book Arguments", https://plato.stanford.edu/entries/dutch-book/ (`sep_dutch_book.html`,
  `.txt`). Matched: "The conclusion of the basic DBA is that the degrees of belief, or credences,
  that an agent attaches to the members of a set \(X\) of propositions, or sometimes statements or
  sentences, should satisfy the axioms of probability."
- Wikipedia, "Admissible decision rule" (`wiki_Admissible_decision_rule.txt`). Matched: "According to
  the complete class theorems, under mild conditions every admissible rule is a (generalized) Bayes
  rule (with respect to some prior ...)"; Bayes rule = minimizer of the Bayes risk (expectation of
  the risk over the prior). Also saved `wiki_Bayes_estimator.txt`.
- Wikipedia, "Lasso (statistics)" (`wiki_Lasso_statistics.txt`): "Just as ridge regression can be
  interpreted as linear regression for which the coefficients have been assigned normal prior
  distributions, lasso can be interpreted as linear regression for which the coefficients have
  Laplace prior distributions." Also `wiki_Ridge_regression.txt`, `wiki_Ordinary_least_squares.txt`
  ("ridge regression and lasso regression can both be viewed as special cases of Bayesian linear
  regression").
- `data/originals/is-reality-ugly.md`: "even when you know all the relevant laws of physics, you may
  not have enough computing power to extrapolate them." Posted 2008-01-12 (two days before).

## 3. Arithmetic recomputed

Script: `data/sources/4a_beautiful-probability/stopping_rule.py` (pure Python, exact binomial
sums via lgamma); output saved as `stopping_rule_output.txt`. Runtime about 2.5 minutes.

1. Fixed n: P(X >= 70 | n = 100, p = 0.6) = 0.0248. One-sided, significant at 5% (and just
   under 2.5%). Normal approximation: (0.70 - 0.60)/sqrt(0.24/100) = 2.04 SD.
2. Second researcher, formalized as "after each patient, one-sided exact binomial test of p = 0.6;
   stop the first time p-value < alpha".
   - alpha = 0.05: boundary c[99] = 68, c[100] = 69, so 70/100 cannot be a first crossing (the
     rule would have stopped earlier). Jaynes's story is not consistent with this version.
   - alpha = 0.025: c[99] = 70, c[100] = 70, so a path ...(99, 69) -> (100, 70) is a first
     crossing. This is the version used in the notes.
3. Probability of having stopped (dynamic programming over paths not yet stopped; states with
   probability < 1e-18 pruned):

   | true p | by n = 100 | by 1,000 | by 10,000 |
   |---|---|---|---|
   | 0.6, alpha 0.025 | 0.108 | 0.204 | 0.293 |
   | 0.5, alpha 0.025 | 0.010 | 0.010 | 0.010 |
   | 0.6, alpha 0.05 | 0.202 | 0.340 | 0.457 |
   | 0.5, alpha 0.05 | 0.031 | 0.031 | 0.031 |

   Stopping at n = 100 with alpha = 0.025 means r = 70 exactly (at n = 99, r <= 69), so the
   stagewise-ordered p-value (stop earlier, or at the same stage with a larger count) equals
   P(stopped by 100 | p = 0.6) = 0.108. Not significant at 5%. This supports the post's "It's
   quite possible that the first experiment will be 'statistically significant', the second not."
4. Likelihoods. Binomial design: C(100,70) p^70 (1-p)^30. Sequential design: K p^70 (1-p)^30 where
   K is the number of admissible paths. Ratio p1 vs p2 is (p1/p2)^70 ((1-p1)/(1-p2))^30 in both:
   0.7 vs 0.6 gives 8.7; 0.7 vs 0.5 gives 3745.
5. Posterior with uniform prior: Beta(71, 31). P(p > 0.6) = P(Binomial(101, 0.6) <= 70) = 0.979.
   Posterior mean 71/102 = 0.696.
6. Cubes 1, 8, 27, 64, 125, 216, 343: first differences 7, 19, 37, 61, 91, 127; second 12, 18, 24,
   30, 36; third 6, 6, 6, 6. Arithmetic (2*5)+(7+3) = 20 and 2*(4+6) = 20.
7. "At a given true value another rule can do better than the Bayes rule": the constant rule
   delta(x) = theta0 has zero loss when theta = theta0, while a Bayes rule with a prior that is not
   a point mass at theta0 has positive risk there. So no rule minimizes risk at every theta
   (outside trivial problems).
8. Least squares as a Bayesian point estimate: with Gaussian noise the log-likelihood is minus the
   sum of squared residuals over 2 sigma^2 plus a constant; with a flat prior the log-posterior is
   the same up to a constant, so the posterior mode is the least-squares estimate.

## 4. Claims about other posts

- "Is Reality Ugly?" (`data/originals/is-reality-ugly.md`, posted 2008-01-12): quoted above.
- The Second Law post is not referred to here. The Toolbox-thinking note (not in the book) made
  a similar optimality point ("Only when the expectation is taken under the same prior and
  likelihoods that the update uses"); my note agrees with it. Since Toolbox is not in the book,
  this is the first occurrence in book order and carries the point in full.
- Earlier notes on Cox's theorem (0-and-1-are-not-probabilities, order 62) are about where
  certainty sits on the scale; no overlap with my note.

## 5. Not verified

- Savage (1962) itself: only as cited by Jaynes 1990.
- Mayo (2014), Dawid (2014), Gandenberger (2014), Birnbaum (1962, 1970): only through Wikipedia's
  article on the likelihood principle (a secondary source, cited as such in the note).
- Carnot's theorem stated from standard knowledge, no source fetched (the post's statement is the
  textbook one).
- "ZF provides a model for probability theory": hedged in the post ("I'm pretty sure"), no note.
  Measure theory is normally done in ZFC; countable additivity of Lebesgue measure needs some
  choice. Not worth a note.
- The parenthesis "(Presumably the two control groups also had equal results.)" is the post's
  addition; Jaynes's example has no control group. Harmless; no note.

## 6. Judgment calls for the editor

- The formalization of "definitely greater than 60%" is mine (exact one-sided test at 2.5% after
  every patient). Other formalizations change the numbers (at 5% per look, 70/100 cannot even be the
  first stopping point). The notes say "Suppose ..." to mark this, and the Response says "a natural
  version". Figures should be read as illustrative of the frequentist worry, not as Jaynes's.
- Neutral treatment: I gave the frequentist reason (error rates of procedures) and the Bayesian
  answer (Savage; 1% at a true rate of 50%) in adjacent notes, and the Response names the
  disagreement as one about which question matters. The note on "at least one ... must discard
  relevant information" says the claim follows only if the likelihood principle is granted. I did
  not say the post is wrong; "wrong calculation" in that note echoes the post's own words.
- Dutch-book note: says "not shown", not "does not apply". Frequentist confidence statements can
  be made incoherent if read as betting odds (Buehler 1959, Cornfield 1969, from memory, not
  checked), so a stronger claim would not be safe.
- "No statistician is quoted": checked the whole post; the only non-Bayesian voices are the
  post's own invented replies.
- Optimality note ("better"): decision-theoretic framing from Wikipedia plus my derivation 7.
- The quote check flags only outside sources (listed in section 2); all post quotations match.
- Pronouns: Jaynes and Birnbaum restructured to avoid "his" even though both are historical
  figures.
- The insert helper (`insert_notes.py`, `notes_bp.py`) was used for the first draft only; later
  edits were made in the post file, which is authoritative.
- raz_check flags read: "wrong" (echoes the post's "do the wrong calculation"), "contradiction"
  (the post's own word), "never" in the Summary (the post's claim about real engines), "false"
  (Jaynes's and Savage's "appreciably false"), "inference" (inside the Wikipedia quotation). None is
  a verdict of ours.
