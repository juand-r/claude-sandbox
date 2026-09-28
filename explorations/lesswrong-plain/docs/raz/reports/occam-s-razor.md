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

## 2. Sources checked

All saved in `data/sources/`.

- LessWrong HTML of the post via the GraphQL API (`lw_occam.json`, `lw_occam.html`): the
  skeleton's "2N strings of length N" is printed on LessWrong as `2<sup>N</sup>`, which the
  cpara states.
- Wikipedia, "Kolmogorov complexity" (`wp_kolmogorov.txt`, `?action=raw`): "The length of the
  shortest description will depend on the choice of description language; but the effect of
  changing languages is bounded (a result called the ''invariance theorem''"; "there is a
  constant c – which depends only on the languages L1 and L2 chosen – such that ∀s. -c ≤
  K1(s) - K2(s) ≤ c"; "The minimum message length principle ... was developed by C.S. Wallace
  and D.M. Boulton in 1968."
- Wikipedia, "Solomonoff's theory of inductive inference" (`wp_solomonoff_induction.txt`):
  background; "the programming language must be chosen prior to the data".
- Leike and Hutter, "Bad Universal Priors and Notions of Optimality", arXiv:1510.04931,
  abstract (`leike_hutter_1510.04931_abs.html`): "A big open question of algorithmic
  information theory is the choice of the universal Turing machine (UTM). For Kolmogorov
  complexity and Solomonoff induction we have invariance theorems: the choice of the UTM
  changes bounds only by a constant." The note quotes the first sentence up to "machine".
- Scholarpedia, "Algorithmic probability" (`scholarpedia_algorithmic_probability.txt`):
  "M(x) := Σ_{p : U(p)=x*} 2^{-ℓ(p)}" and "the probability that the output of a monotone
  universal Turing machine U starts with x when provided with fair coin flips on the input
  tape": matches the post's description of the predictor.

## 3. Arithmetic and derivations

- HTTHHT: a fixed program gives probability 1, a fair coin (1/2)^6 = 1/64: "64 times better"
  is right.
- "HTHHTHHHTHHHHTHHHHHT" has 20 characters: "any other string of 20 coinflips" is right.
- Exchange rate: with prior 2^-L, a program storing 6 extra bits has prior 2^-(L+6) and
  likelihood 1; the fair coin has prior 2^-L and likelihood 2^-6. The posteriors are equal, so
  six stored bits exactly cancel a 64-fold gain in fit. (A self-delimiting encoding of the 6
  bits costs a little more than 6 bits, which is why "at least" is right.)
- Machine-dependence note (shown derivation). Let U be a universal prefix machine and T a
  program for U that simulates Thor. Define V by V(0) = U(T) and V(1p) = U(p). The domain
  {0} ∪ {1p : p in dom U} is prefix-free, V simulates U with one extra bit, so V is
  universal. On V the Thor hypothesis has length 1 and every other program length |p| + 1.
  The invariance constants are 1 in one direction and about |T| in the other, so the theorem
  holds while the ranking of Thor against Maxwell reverses. The note claims only that the
  invariance result does not settle the ranking.

## 4. Claims about other posts

- "Einstein's Arrogance" (Posted 2007-09-25; this post 2007-09-26): "the previous day's post".
- No claim about other posts' notes. The neighbour "How Much Evidence Does It Take?" makes a
  related criticism (a unit the essay never shows how to apply); this post's Response makes
  its own version (an uncomputable measure with no estimate) without repeating that one.

## 5. Items not verified

- The Heinlein line, "The lady down the street is a witch; she did it." Two web searches found
  only copies of this post. I made no note, since the argument does not depend on who said it.
- I considered a note that the deterministic and probabilistic versions of Solomonoff's prior
  agree up to a constant (Levin). I dropped it: for a mixture over computable measures (which
  is what "programs that assign probabilities" suggests) I could not confirm the exact
  equivalence from a source read this session.

## 6. Judgment calls for the editor

1. The only critical note is the machine-dependence logic note ("True, but ..."). It depends
   on the derivation above. A fair defender may say Solomonoff predictions converge whatever
   the machine, so the constant washes out with data. That is true for prediction in the
   limit; the post's claim here is a prior ranking of two hypotheses, which the constant can
   reverse. The note does not say the post is wrong, only that the formalism alone does not
   settle the ranking.
2. Credit in notes: "The argument is correct" (exchange rate) and "the answer holds" (witch).
   STANDARDS 2.1 allows brief credit where omission would mislead; the Response also opens
   with credit. The editor may prefer to trim one of these.
3. The uncomputability point (cpara on the Solomonoff paragraph, and the Response): the post
   itself says the method is uncomputable; the criticism is only that it gives no estimate
   for a real case beyond Maxwell versus Thor. I added that exception after a
   fair-defender reading.
4. No reserved words used.
