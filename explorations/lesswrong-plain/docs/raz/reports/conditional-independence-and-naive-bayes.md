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
