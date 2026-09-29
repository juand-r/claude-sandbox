# Report: conditional-independence-and-naive-bayes

Book III, A Human's Guide to Words, order 179. Posted 2008-03-01 (the `Posted:` line).
Batch 3b.

## 1. The argument in three sentences

The mutual informations among three variables cannot simply be subtracted from the sum of
their entropies, because they may carry the same information; the correct formula uses the
conditional mutual information I(X;Y|Z), and a variable Z "screens off" X from Y exactly when
learning Y no longer changes beliefs about X once Z is known. Several observable properties
that are all evidence about one another (speech, clothes, fingers, hemlock, blood) may all be
screened off by one central, possibly constructed, class variable such as "human"; pretending
that they are exactly independent given the class is Naive Bayes, which simplifies the
calculation: observations update the class, and the class predicts the rest. The blegg
"Network 2" is this structure, and with a logistic central unit and log-likelihood-ratio
weights it is exactly Naive Bayes, which the post takes as a sign that ad hoc
neural-network methods that work will turn out to have Bayesian structure.

## 2. Sources checked

Saved in `data/sources/b3b_superexponential-conceptspace-and-simple-words/` (shared with my
other slug) and `data/sources/b3b_conditional-independence-and-naive-bayes/`.

- Tom Mitchell, "Generative and Discriminative Classifiers: Naive Bayes and Logistic
  Regression", draft chapter 3 for a second edition of \textsc{Machine Learning} (copyright
  2017, draft of 1 October 2020), http://www.cs.cmu.edu/~tom/mlbook/NBayesLogReg.pdf. Files
  `NBayesLogReg.pdf/.txt`. Matched:
  - "The Naive Bayes classifier does this by making a conditional independence assumption
    that dramatically reduces the number of parameters to be estimated when modeling P(X|Y),
    from our original 2(2^n − 1) to just 2n." (pdftotext renders the exponent as "2(2n − 1)";
    the setting is n boolean attributes and boolean Y, stated at the start of section 1.)
  - "Interestingly, the parametric form of P(Y|X) used by Logistic Regression is precisely the
    form implied by the assumptions of a Gaussian Naive Bayes classifier."
  - "Although Logistic Regression is consistent with the Naive Bayes assumption that the input
    features Xi are conditionally independent given Y, it is not rigidly tied to this
    assumption as is Naive Bayes. Given data that disobeys this assumption, the conditional
    likelihood maximization algorithm for Logistic Regression will adjust its parameters to
    maximize the fit to (the conditional likelihood of) the data, even if the resulting
    parameters are inconsistent with the Naive Bayes parameter estimates."
  - The chapter is later than the post; it is used only as a textbook statement of standard
    results, not as something the post should have cited.
- Domingos and Pazzani, "On the Optimality of the Simple Bayesian Classifier under Zero-One
  Loss", Machine Learning 29 (1997). Abstract from
  https://link.springer.com/article/10.1023/A:1007413511361 (file `dp_springer.html`, the
  `dc.description` meta field): "This article shows that, although the Bayesian classifier's
  probability estimates are only optimal under quadratic loss if the independence assumption
  holds, the classifier itself can be optimal under zero-one loss (misclassification rate)
  even when this assumption is violated by a wide margin." The author's PDF
  (https://homes.cs.washington.edu/~pedrod/papers/mlj97.pdf, `domingos_pazzani_1997.pdf`)
  downloaded but its text layer is garbled, so I used the abstract only.
- The image: `/static/imported/2008/02/29/blegg2.png` redirects to
  https://raw.githubusercontent.com/tricycle/lesswrong/master/r2/r2/public/static/imported/2008/02/29/blegg2.png.
  Saved as `blegg2_0229.png`; byte-identical to `/2008/02/09/blegg2.png`, the "Network 2"
  image in Neural Categories. I viewed it: units "Color: +blue / -red", "Shape: +egg / -cube",
  "Luminance: +glow / -dark", "Texture: +furred / -smooth", "Interior: +vanadium /
  -palladium", each joined only to a central node labelled "Category: +BLEGG / -RUBE",
  caption "Network 2".
- The post's current HTML on LessWrong (GraphQL `htmlBody`, `nb.html`) was fetched only to
  look for lost superscripts (there are none in this post); I did not diff it against our
  original.

raz_check "quote not in post" flags, all accounted for: "Where there is no mutual
information, there is no Bayesian evidence, and vice versa." (Mutual Information post,
section 4); "from our original $2(2^n - 1)$ to just $2n$." and "even if the resulting
parameters are inconsistent with the Naive Bayes parameter estimates." (Mitchell, above);
"violated by a wide margin," (Domingos and Pazzani, above); "Category: +BLEGG / -RUBE." (the
image); "contributes usefully to truth-finding must have at least a little Bayesian
structure." and "the same Holy Grail" and "at least a little" (Searching for Bayes-Structure,
section 4).

## 3. Arithmetic and mathematics recomputed

Script: `data/sources/b3b_conditional-independence-and-naive-bayes/check_nb.py`. Output:

- Joint distribution: X in 1..8, Y in 1..4, same parity, uniform: 16 states.
  H(X) = 3, H(Y) = 2, H(Z) = 1, H(X,Y) = 4, H(X,Y,Z) = 4.
  I(X;Y) = I(X;Z) = I(Z;Y) = 1, I(X;Y|Z) = 0.
  Naive formula: 3 + 2 + 1 − 1 − 1 − 1 = 3 (wrong, as the post says).
  Corrected formula: 3 + 2 + 1 − 1 − 1 − 0 = 4 (right).
  H(X|Z) = 2, H(Y|Z) = 1, H(X,Y|Z) = 3, so I(X;Y|Z) = 2 + 1 − 3 = 0.
- The corrected formula in general (derivation in the note):
  H(X,Y,Z) = H(Z) + H(X|Z) + H(Y|X,Z);
  H(X|Z) = H(X) − I(X;Z);
  H(Y|X,Z) = H(Y|Z) − I(X;Y|Z) = H(Y) − I(Y;Z) − I(X;Y|Z).
  Sum: H(X) + H(Y) + H(Z) − I(X;Z) − I(Y;Z) − I(X;Y|Z). Numerically: max deviation
  1.8e-15 over 2,000 random joint distributions on 3 × 4 × 2 states. The post's
  H(S|Z) = Σ_j p(Z_j) Σ_i −p(S_i|Z_j) log2 p(S_i|Z_j) formula agrees with H(S,Z) − H(Z) on
  the same distributions.
- "if I(X;Z) = 0 and I(Y;X|Z) = 0 then I(X;Y) = 0": chain rule, I(X;Y,Z) = I(X;Z) +
  I(X;Y|Z) = 0; also I(X;Y,Z) = I(X;Y) + I(X;Z|Y) ≥ I(X;Y) ≥ 0; so I(X;Y) = 0. A numerical
  check on distributions built to satisfy the premises gave I(X;Y) ≤ 1.8e-15 (this only
  tests that family; the derivation is the proof).
- H(X|Y) = H(X,Y) − H(Y): definition/chain rule. Correct.
- Duality and the two derivations: P(x,y) ≠ P(x)P(y) ⇔ P(x|y) ≠ P(x) for P(y) > 0; the
  conditional version likewise. The post writes "=>" while claiming equivalence; each step
  reverses. Not noted (wording).
- Five parity-linked variables on 1..4: I(A;B) = 1 bit, I(A;B|C) = 0, I(A;{B,D}|C) = 0: any
  one screens off the rest, as the post says.
- Naive Bayes equals a logistic unit: for binary features with p_i = P(x_i=1|z),
  q_i = P(x_i=1|¬z), prior π,
  log-odds = log(π/(1−π)) + Σ_i log((1−p_i)/(1−q_i)) + Σ_i x_i [log(p_i/q_i) − log((1−p_i)/(1−q_i))].
  So the weight of x_i is the difference of the two log-likelihood ratios and the bias
  absorbs the x_i = 0 terms; the post's "the logarithms of the likelihood ratios, etcetera"
  covers this. Numerical check: max |posterior − σ(b + w·x)| = 2.2e-16 over 1,000 random
  cases.
- Double counting in naive Bayes (support for "can come out too extreme"): prior 0.5, one
  observation with P = 0.8 given the class and 0.2 otherwise (likelihood ratio 4). True
  posterior 0.8. If the same observation is entered as two features (perfectly dependent
  given the class), naive Bayes multiplies the ratio twice: 0.5 × 0.64 / (0.5 × 0.64 + 0.5 ×
  0.04) = 0.941.
- Not in the notes: the naive formula can also err upward. With X, Y independent fair bits
  and Z = X xor Y, H(X,Y,Z) = 2 but the naive formula gives 3. The post's "double-counted
  ... came up with too little entropy" describes its own case only ("that may include"), and
  its corrected formula handles both, so I made no note.

## 4. Claims about other posts

- "Mutual Information, and Density in Thingspace" (`data/originals/mutual-information-and-density-in-thingspace.md`,
  Posted 2008-02-23): definition "I(X;Y) = H(X) + H(Y) - H(X,Y)"; the X/Y example ("a system
  X that can be in any of 8 states ... a system Y that can be in any of 4 states"; "let's
  suppose that X and Y are either both odd, or both even"); and "Where there is no mutual
  information, there is no Bayesian evidence, and vice versa." The other agent's note on
  that post already cites this post for "16 possible states, all equally probable"; no
  conflict.
- "Neural Categories" (`data/originals/neural-categories.md`, Posted 2008-02-10, book order
  163): the image `blegg2.png` introduced with "In this network, a wave of activation
  converges on the central node from any clamped (observed) nodes, and then surges back out
  again to any unclamped (unobserved) nodes."
- "Searching for Bayes-Structure" (`data/originals/searching-for-bayes-structure.md`, Posted
  2008-02-28, so "two days earlier" than 2008-03-01; in the collection at order 192, Mere
  Reality, Lawful Truth, per the manifest). Matched:
  - "In fact, any *part* of a cognitive process that *contributes usefully* to truth-finding
    must have at least a little Bayesian structure".
  - The thermodynamic argument: "that mind must be doing something at least *vaguely*
    Bayesian - at least one process with a sort-of Bayesian structure *somewhere* - or it
    *couldn't possibly work*" and "The mind must have *moved in harmony with the Bayes* at
    least a little".
  - The stronger claim: "It's a different quest for each facet of cognition, but the Grail
    always *turns out* to be the same. ... *Then* you always find the same Holy Grail at the
    end." Its support in that post is the narrative of repeated discovery ("Once this happens
    to you a few times, you kinda pick up the rhythm."). This is my reading of what supports
    what in that post; see judgment calls.
- "Superexponential Conceptspace, and Simple Words" (my other slug): its note on "why would
  you bother drawing boundaries?" quotes this post; consistent.

## 5. Items not verified

- Ng and Jordan (2002), cited by Mitchell's chapter; I did not read it and do not cite it.
- The link on "WRONG!" (YouTube) and on "correctly" (yudkowsky.net) were not opened; no note
  depends on them.
- The origin of "scruffy" as AI jargon (neats and scruffies) was not checked; no note depends
  on it.

## 6. Judgment calls for the editor

- The clogic on "will turn out to have Bayesian structure" (and the Response paragraph and
  n.b.): it says Searching for Bayes-Structure argues "only" for "at least a little" Bayesian
  structure, and that its stronger claim (the same Holy Grail every time) rests on the
  author's account of repeated discoveries, "not by that argument". This characterizes
  another post; a fair defender might say "as it always must be" in that post ties the
  strong claim to the argument. I read "must" there as the author's conclusion, not as a
  step the thermodynamic argument supplies. Please check.
- The cpara on "without conditional independence, the universe would have no structure"
  and the one-sentence Response mention: a passing remark; it could be cut as a nitpick
  (STANDARDS 2.4), but it is a sweeping claim stated as an example and never explained.
- The "two halves loosely joined" point (cpara on "And that's how one calculates..." and a
  Response paragraph): a structural judgment. The claim itself is checked: the words
  "conditional entropy" and the H(S|Z) formulas do not recur after that paragraph.
- The clogic on the cost of naive Bayes is framed as information ("The pretence has a known
  cost"), not as a fault; the Response says "What that costs is not said", which is a scope
  remark. The note runs three sentences, the long side of the brief's "one sentence" for
  scope points.
- "The hedge is not needed" on "(I believe)": credit, not a charge.
- Credit notes ("Correct", "checks") are frequent because the mathematics is right.
- Correction I made to my own draft: I first wrote that Searching for Bayes-Structure is "not
  in this collection"; the manifest puts it at order 192, so the note now says the collection
  places it later, in Mere Reality.
