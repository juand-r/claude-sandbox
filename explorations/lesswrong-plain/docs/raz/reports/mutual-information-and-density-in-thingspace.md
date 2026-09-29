# Report: mutual-information-and-density-in-thingspace

## 1. The argument in three sentences

The mutual information of two variables, I(X;Y) = H(X) + H(Y) - H(X,Y), is how much less
uncertain the joint system is than the two parts taken separately; it is zero exactly when
the joint distribution factors into the product of the marginals, which is exactly when
learning one variable tells you nothing about the other, so mutual information and Bayesian
evidence go together. In an efficient code the word for a conjunction of properties is
shorter than the words for its parts only if the conjunction occurs more often than the
marginal probabilities predict, which is the same condition under which some of the
properties can be inferred from the others. So a word such as "wiggin" is worth having only
if its defining properties go together, or predict further properties, more often than
chance; otherwise it is "a lie," or at least an error, and the way to carve reality at its
joints is to draw boundaries around concentrations of unusually high probability density in
Thingspace.

## 2. Sources checked

All saved in `data/sources/batch3b_entropy-and-short-codes/` (shared folder for my two slugs).

- The post's live HTML from the LessWrong GraphQL API (`lw_yLcuygFfMfrfK8KjF.json`).
  Confirms: "2<sup>3</sup> = 8 and 2<sup>2</sup> = 4" (the superscripts are lost in
  `data/originals`, hence the note "printed as 2 to the power 3"); the entropy sum is printed
  "3/16 log<sub>2</sub>(3/16) + ... + 5/64 log<sub>2</sub>(5/64)" with no minus sign; the
  first table's fourth column really reads "Z<sub>1</sub>Y<sub>3</sub>" and
  "Z<sub>2</sub>Y<sub>3</sub>" (a typo for Y4; see section 3).
- Wikipedia, "Mutual information" (`wp_Mutual_information.txt`): "I(X;Y) is equal to zero
  precisely when the joint distribution coincides with the product of the marginals, i.e.
  when X and Y are independent"; "mutual information is nonnegative ... and symmetric (i.e.
  I(X;Y) = I(Y;X))". Supports "Correct in both directions", "The general result ... is
  standard", and "The symmetry is standard".
- Rosch et al. (1976), Cognitive Psychology 8 (`rosch1976.txt`; URL in the entropy report):
  "The world is structured because real-world attributes do not occur independently of each
  other. Creatures with feathers are more likely also to have wings than creatures with
  fur". Quoted in the cpara on "Having a word for a thing", the Response and one n.b., as
  prior work that supports the post.

## 3. Arithmetic (script: `check_numbers.py`, output reproduced)

- Parity example: with X uniform on 8, Y uniform on 4, both odd or both even, and the 16
  allowed pairs equally likely: marginals uniform (1/8, 1/4); H(X) = 3, H(Y) = 2,
  H(X,Y) = log2 16 = 4, I = 3 + 2 - 4 = 1 bit. X5 leaves Y in {1, 3}; Y4 leaves X in
  {2, 4, 6, 8}. All correct.
- Independent table: products 3/8 x (1/2, 1/4, 1/8, 1/8) = 3/16, 3/32, 3/64, 3/64 and
  5/8 x ... = 5/16, 5/32, 5/64, 5/64. Sum 1. P(Z1Y2) = 3/32. P(Y1) = 3/16 + 5/16 = 1/2.
  All correct.
- H(Y) = 1.75, H(Z) = -(3/8 log2 3/8 + 5/8 log2 5/8) = 0.954434; sum 2.704434. Entropy of
  the independent joint table = 2.704434. Equal, as the post says.
- The printed sum without the minus sign evaluates to -2.704434. Correction: the displayed
  expression should be preceded by a minus sign (entropy = -[3/16 log2(3/16) + ... +
  5/64 log2(5/64)] = 2.704 bits). Effect on the argument: none; the post's claim about the
  total is right, and the previous post gives the formula with the sign. It gets a short
  cfact because the post invites the reader to do this calculation and the reader who
  follows the printed expression gets a negative entropy. By the STANDARDS 2.4 threshold
  this is borderline (the figure is not off by a fifth; the sign is flipped); judgment
  call 2 below.
- Table typo: the fourth column of the independent table is labelled Z1Y3 / Z2Y3; it should
  be Z1Y4 / Z2Y4. The numbers (3/64, 5/64) are right. No effect on the argument; report only
  (STANDARDS 2.4(2)).
- Dependent table: sum 1; P(Z1) = (12+8+1+3)/64 = 24/64 = 3/8; P(Z2) = 40/64 = 5/8;
  P(Y1..Y4) = 32/64, 16/64, 8/64, 8/64 = 1/2, 1/4, 1/8, 1/8. P(Z1)P(Y2) = 3/32 = 6/64 < 8/64.
  P(Z1 | Y2) = (8/64)/(1/4) = 1/2 > 3/8. All correct.
- The unchecked claim: H(Y,Z) for the dependent table = 2.664467 < 2.704434, so
  I(Y;Z) = 0.039967 bits. Also H(Y) - H(Y|Z) = H(Z) - H(Z|Y) = 0.039967 (symmetry).
  The post's claim is correct.
- Pointwise values (log2 of joint over product), used in the note on "In efficient codes":
  Z1Y2 +0.415, Z1Y3 -1.585, Z2Y2 -0.322, Z2Y3 +0.485, the other four cells 0. Code lengths:
  -log2 P(Z1) = log2(8/3) = 1.415, -log2 P(Y2) = 2, sum 3.415; -log2 P(Z1Y2) = log2 8 = 3.
  The expected saving of the joint code over the separate codes is
  H(Y) + H(Z) - H(Y,Z) = I = 0.040 bits.
- "by Bayes's Rule": the three displayed lines use the definition of conditional
  probability (divide by P(Zj)), not Bayes's theorem proper. The derivation is valid. I did
  not make this a note (a label, no effect on the argument); the cpara says only that the
  derivation "divides both sides by P(Zj) and is correct".

## 4. Claims about other posts

- "Conditional Independence, and Naive Bayes" (`data/originals/conditional-independence-and-naive-bayes.md`,
  posted 2008-03-01): "So for the joint distribution (X,Y) there are only 16 possible states,
  all equally probable, for a joint entropy of 4 bits." Quoted in the cpara on "In
  particular" as "16 possible states, all equally probable."
- "Superexponential Conceptspace, and Simple Words"
  (`data/originals/superexponential-conceptspace-and-simple-words.md`, posted 2008-02-24,
  the next post in the book): "I deliberately left out a key qualification in that
  (slightly edited) statement, because I couldn't explain it until today"; "The way to carve
  reality at its joints, is to draw *simple* boundaries around concentrations of unusually
  high probability density in Thingspace"; "the above statement about 'how to carve reality
  at its joints' is a bit chicken-and-eggish: You can't assess the *density* of actual
  observations, until you've already done at least a little carving."
- "Empty Labels" (`data/originals/empty-labels.md`) contains the syllogism "All [mortal,
  ~feathers, bipedal] are mortal." as quoted.
- "Sneaking in Connotations" (`data/originals/sneaking-in-connotations.md`): "So suppose we
  decided to invent a new word, "wiggin", and *defined* this word to mean people with green
  eyes and black hair". Hence "the word coined in".
- "yesterday": both posts have Posted 2008-02-23 in `data/originals` (API: 03:16 UTC and
  19:14 UTC), so "yesterday" is the author's local date. None of my text computes a date
  from it; I write "the previous post".

## 5. Not verified

Nothing in the notes rests on an unchecked source. The raven "exercise" answer in the
digression cpara is my own one-line statement of a standard fact (I(X;Y) = I(Y;X) while
P(black | raven) and P(raven | black) differ).

## 6. Judgment calls

1. The Response is mostly credit. After checking, I found no substantive fault in the
   post's mathematics or its argument. I considered a note that the post shifts from "things
   that you'll need to say frequently" (previous post) to how often things are "found"
   together in the world, so that a word could pay for itself because a task singles out a
   combination, even with independent properties. I dropped it: the post's condition 2
   (wiggins "share other properties") covers that case, since being singled out by the task
   is itself such a property, and the objection would be my own speculative argument.
2. The cfact on the missing minus sign is kept as a note (see section 3) and appears in the
   Response's second paragraph, but not in the "In short" line (Book III lesson on slips).
3. The table typo (Y3 twice) and the "Bayes's Rule" label are report-only.
4. The cpara on the pointwise savings ("In efficient codes ...") and the matching Response
   paragraph say "something the post does not say": the saving on over-represented pairs is
   paid for by longer codes on under-represented ones. It is information, not a charge; the
   post's sentence says only "can be shorter", which is correct.
5. Rosch 1976 is given as prior work supporting the post, not as an uncredited source; the
   post makes no claim of novelty.
6. The "lie" paragraph: I describe the charge and note it rests on the hedged Gricean
   paragraph ("One may even consider") and is softened in the next paragraph. No criticism.
7. No reserved words. The raz_check "motive?" flags are the word "inference" in its
   statistical sense.
