# Report: 0-and-1-are-not-probabilities

## 1. The argument in three sentences

Probabilities can be rewritten as odds or log odds without loss, and Cox's theorem says
all reasonable ways of representing uncertainty are equivalent; on the log-odds scale
probability 1 is positive infinity and 0 is negative infinity, and the distance between
two degrees of belief is the evidence needed to move between them. So reaching certainty
would take infinitely strong evidence, and theorems of probability break down at 0 and 1
(for example, updating on an observation of probability 0). The post therefore proposes,
by analogy with keeping infinity out of the real numbers, that 0 and 1 be excluded from
the probabilities, admits that theorems relying on probabilities summing to 1 would need
rederiving, and hopes for a way to do so without a "magic symbol" for certainty.

## 2. Sources checked

- Jaynes, Probability Theory: The Logic of Science, chapters 1 to 3,
  http://bayes.wustl.edu/etj/prob/book.pdf (`data/sources/jaynes_book_ch1-3.pdf`, `.txt`),
  chapter 2, "The Quantitative Rules" (Cox's derivation). Matched: "Certainty is represented by
  w(A|C) = 1. (2–32)"; "there will be no loss of generality if we now adopt the choice
  0 ≤ w(x) ≤ 1 as a convention"; and "If it is increasing, it must range from zero for
  impossibility up to one for certainty." Also, relevant to the post's practical point and not
  used in a note: the robot's predictions "can approach, but (except in degenerate cases) not
  actually reach, the certainty of logical deduction" (chapter 3).
- Wikipedia, "Cox's theorem" (raw, `data/sources/wiki_Cox_s_theorem.txt`): "Certain truth is
  represented by Pr(A|B)=1, and certain falsehood by Pr(A|B)=0." It also reports Halpern's
  counterexample (Halpern 1999, JAIR 10: 67–85) to the theorem as originally stated; the post's
  "plus various extensions and refinements thereof" covers this, so no note.
- Wikipedia, "Probability axioms" (raw, `data/sources/wiki_Probability_axioms.txt`): "Second
  axiom ... This is the assumption of unit measure ... P(\Omega) = 1"; "one deduces that
  P(\emptyset) = 0"; "P(A) + P(A^c) = P(A\cup A^c)= P(\Omega) = 1".
- Wikipedia, "Probability density function" (raw, `data/sources/wiki_Probability_density_function.txt`):
  "The (absolute) probability for a continuous random variable to take on any particular value is zero."
- Wikipedia, "Almost surely" (raw, `data/sources/wiki_Almost_surely.txt`): "the set of outcomes
  on which the event does not occur has probability 0, even though the set might not be empty";
  dart example: "a point on a diagonal is no less possible than any other point". Basis for
  "probability 0 does not mean impossible" and "probability 1 does not mean certain".
- Wikipedia, "Borel–Kolmogorov paradox" (raw, `data/sources/wiki_Borel_Kolmogorov_paradox.txt`):
  "a paradox relating to conditional probability with respect to an event of probability zero";
  two coordinate choices give different conditional distributions on the same great circle.
- Wikipedia, "Extended real number line" (raw, `data/sources/wiki_Extended_real_number_line.txt`):
  "\overline\R is not even a semigroup, let alone a group, a ring or a field". Confirms the
  post's "do not obey the field axioms"; no note needed.

## 3. Arithmetic

- Die: prior odds 1:5; likelihood ratio 0.2/0.1 = 2; posterior 2:5 = 0.4; P = 0.4/1.4 = 2/7 =
  0.2857, "~29%". Correct.
- Odds of each face: (1/6)/(5/6) = 0.2. Odds of 1–4: (4/6)/(2/6) = 2, not 0.8. The post's
  point holds.
- 0.0001 → odds 1/9999 → 10 log10 = −39.9996 dB ("around −40"). LR 100 → 20 dB. −20 dB → odds
  0.01 (exactly 100/9999 = 0.010001) → P = 0.0099 ("~0.01").
- 0.502 → 1.00803 → 0.0347 dB ("0.03"); 0.503 → 1.01207 → 0.0521 dB ("0.05");
  0.9999 → 9,999 → 39.9996 dB ("40"); 0.99999 → 99,999 → 49.99996 dB ("50"). All correct.
- 0.99999 − 0.9999 = 0.00009; 0.503 − 0.502 = 0.001. Correct.
- Log-odds addition: O_post = O_prior × LR, so log O_post = log O_prior + log LR; the gap
  between two log odds is the log likelihood ratio needed. Correct.
- Countability: if uncountably many disjoint events had positive probability, then for some
  n infinitely many would have probability > 1/n, and n + 1 of them would sum to more than 1.
  So at most countably many (at most n with probability > 1/n for each n). Standard; my
  derivation, shown in the clogic note.

## 4. Claims about other posts

- "Infinite Certainty" (previous day): its note on 3↑↑↑3 points forward to this post. Its
  logical-omniscience note is related but distinct (credence in logical truths vs. the axioms
  of probability); I did not repeat it here.
- "An Intuitive Explanation of Bayes's Theorem" and "How Much Evidence Does It Take?" (our notes):
  the decibel scale is credited to Jaynes there, and the log-scale evidence idea to Turing and
  Good in the notes on "How Much Evidence". This post credits Jaynes, so I made no crediting note.

## 5. Not verified

- Jaynes's chapter 4 (decibels) is not in the fetched PDF; the post's attribution to Jaynes
  agrees with our notes on "An Intuitive Explanation of Bayes's Theorem".

## 6. Judgment calls for the editor

- This post carries the strongest technical notes of the batch. Each rests on a cited source
  or a shown derivation: Kolmogorov's normalization axiom (Wikipedia), the continuous case
  (Wikipedia, and the countability derivation), and Jaynes's own statement that certainty is
  represented by 1. I avoided "wrong", "false" and "contradicts". The strongest phrasing is in
  the Response ("conflicts with the foundations it would revise") and the "In short" line ("a
  title claim that the axioms of probability rule out"). The evidence: the post proposes that
  1 and 0 are "not in the probabilities", while P(Ω) = 1 is an axiom. A fair defender might say
  the post meant only degrees of belief a human should hold; the post's own framing ("I would
  like to be a probability theorist", "we would need to rederive theorems") is about the theory,
  so I kept it. The editor may soften "rule out".
- The circularity/appearance note ("An argument from appearance ...") uses the post's own
  hedge ("doesn't look like"). I did not call it circular.
- The clogic note on continuous distributions starts "Taken literally", since the post does
  not discuss continuous cases.
- Reserved-word flag: "never reaches infinity" describes the post's own analogy. Kept.
- BUILD PROBLEM (needs the editor): `annotated/preview.sh posts 0-and-1-are-not-probabilities`
  fails with "Unicode character ∕ (U+2215) not set up for use with LaTeX". The character is in
  the post text ("P = (O∕(1 + O))") and must stay. \DeclareUnicodeCharacter is preamble-only, and
  check_verbatim rejects anything added outside notes, so I could not fix it in my files. Fix:
  add `\DeclareUnicodeCharacter{2215}{/}` to `annotated/preamble.tex` (for example after the
  line for 2212). I tested this on a copy of the preamble and the post plus afterword build
  without errors. I did not edit the preamble (brief: do not edit other files).
