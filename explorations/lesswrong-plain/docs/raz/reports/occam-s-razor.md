# Report: occam-s-razor

## 1. The argument in three sentences

The length of an English sentence is a poor measure of an explanation's complexity, because
words like "witch" or "anger" are labels for complex things the listener already stores, which
is why Thor seems simpler than Maxwell's equations. Solomonoff induction measures complexity by
the length of the shortest program producing the description (up to a constant for the choice
of language), gives each program prior weight 2 to the minus its length, weights by how much
probability it gives the data, and so trades one bit of program length against a factor of two
in fit; Minimum Message Length is nearly the same. On this measure "a witch did it" does not
shorten the message describing the data, so it only adds a useless prologue.
