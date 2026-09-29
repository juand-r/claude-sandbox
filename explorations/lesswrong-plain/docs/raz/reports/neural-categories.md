# Report: neural-categories

## 1. The argument in three sentences

A naive neural network for the blegg task (Network 1) connects every observable feature to
every other, learns by Hebb's rule, and settles into a "blegg" attractor that predicts
unobserved features, but it can oscillate, double-counts evidence and needs O(N^2)
connections. A network with one central category unit (Network 2) computes in one inward and
outward pass and needs O(N) connections, at the cost of not representing some within-category
correlations; the author judges it "a fair guess" that the brain is closer to Network 2. A
brain built that way would find it hard to notice a correlation confined to a subgroup, and
would tend to classify things once and for all and then infer everything from the category.
