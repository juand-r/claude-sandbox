# Report: superexponential-conceptspace-and-simple-words

Book III, A Human's Guide to Words, order 178. Posted 2008-02-24 (the `Posted:` line).
Batch 3b.

## 1. The argument in three sentences

A concept is a rule that includes or excludes examples; a learner restricted to simple
concepts (here, conjunctions of attribute values) can narrow its hypotheses with a number of
examples that grows with the logarithm of its concept space, while a fully general learner,
whose space of all sets of instances grows superexponentially with the number of attributes,
cannot say anything about an example it has not seen. So learning is "nearly all inductive
bias", and this is why words have intensions: to carve reality at its joints one must draw
simple boundaries around regions of high probability density, not gerrymander the observed
cases. Given the size of concept space, singling out one concept such as "wiggin" without a
reason is audacious, which is a further reason to doubt that "you can define a word any way
you like".

## 2. Sources checked

All saved in `data/sources/b3b_superexponential-conceptspace-and-simple-words/`.

- Tom Mitchell, lecture slides for \textsc{Machine Learning} (McGraw Hill, 1997), chapter 2,
  http://www.cs.cmu.edu/afs/cs.cmu.edu/project/theo-20/www/mlbook/ch2.pdf (linked from
  http://www.cs.cmu.edu/~tom/mlbook-chapter-slides.html). Files `mitchell_ch2_slides.pdf/.txt`.
  Matched:
  - "Training Examples for EnjoySport", with columns "Sky Temp Humid Wind Water Forecst", and
    "Instances X : Possible days, each described by the attributes Sky, AirTemp, Humidity,
    Wind, Water, Forecast" (used for "EnjoySport" and the six attributes).
  - Version space for Mitchell's data: "G: { <Sunny, ?, ?, ?, ?, ?>, <?, Warm, ?, ?, ?, ?> }"
    (used for "the same two most general hypotheses").
  - "An UNBiased Learner / Idea: Choose H that expresses every teachable concept (i.e., H is
    the power set of X)" and summary point "6. Inductive leaps possible only if learner is
    biased" (quoted in the note on the post's credit to Mitchell).
  - The book's own text (section 2.7) was not available; I cite only the slides.
- Mitchell, chapter 7 slides, http://www.cs.cmu.edu/afs/cs.cmu.edu/project/theo-20/www/mlbook/ch7.pdf.
  Files `mitchell_ch7_slides.pdf/.txt`. Matched:
  - "Optimal query strategy: play 20 questions / pick instance x such that half of
    hypotheses in VS classify x positive, half classify x negative / When this is possible,
    need ⌈log2 |H|⌉ queries to learn c / when not possible, need even more" (the note quotes
    "when not possible, need even more").
  - "m ≥ 1/ε (ln|H| + ln(1/δ))" (Haussler 1988 theorem on ε-exhausting the version space).
  - "If H is as given in EnjoySport then |H| = 973" (the note's "973").
- The post as LessWrong serves it now (GraphQL `htmlBody`, file `superexp.html`): "whose size
  is 2<sup>24</sup> = 16,777,216" and "(2<sup>9</sup> = 512)". This confirms that "224" and
  "29" in our copy are lost superscripts.
- Cantor's theorem (a set has strictly more subsets than members) is standard mathematics;
  no source cited.

raz_check "quote not in post" flags, all accounted for: "EnjoySport", "Inductive leaps
possible only if learner is biased.", "when not possible, need even more." (Mitchell slides,
above); "And the way to carve reality ... unusually high" (Mutual Information post, section 4);
"can simplify the living daylights out of your calculations," and "usually isn't quite true."
(Conditional Independence post, section 4). The honest section also quotes "can simplify the
living daylights..." from the same post.

## 3. Arithmetic recomputed

Script: `data/sources/b3b_superexponential-conceptspace-and-simple-words/check_superexp.py`
(run with `.venv/bin/python`). Output, with the working:

- Days: 3 × 2 × 2 × 2 = 24. Concepts in the format: each attribute is "?" or one value,
  4 × 3 × 3 × 3 = 108, plus the empty concept = 109. All 109 have different extensions.
  All subsets of days: 2^24 = 16,777,216. All as the post says.
- Version space for the three examples: enumerated all 109 concepts; 6 fit:
  {?,Warm,?,?}, {?,Warm,High,?}, {Sunny,?,?,?}, {Sunny,?,High,?}, {Sunny,Warm,?,?},
  {Sunny,Warm,High,?}. Most general: {?,Warm,?,?} and {Sunny,?,?,?}; most specific:
  {Sunny,Warm,High,?}. As the post says. {?,Warm,High,?} fits. "Sunny or warm" fits the data
  and is not representable.
- Fully general learner: for an unseen day d, the set of labelings consistent with the data
  is closed under flipping d's label, so exactly half accept d. (Shown, not simulated.)
- Five attributes: 3 × 2^4 = 48 days; 4 × 3^4 + 1 = 325 concepts. log2 325 = 8.34, so
  ⌈·⌉ = 9 and 2^9 = 512. Each day is accepted by exactly 2^5 = 32 of the 325 concepts
  (each attribute: "?" or the day's own value), so the first split is 32 / 293, not half.
- Simulation (target concept uniform over all 325, including the empty concept):
  - random days drawn uniformly with replacement until one concept is left:
    mean 60.2, median 46, 90th percentile 126 (20,000 runs, seed 0);
  - learner chooses, at each step, the day whose split of the remaining concepts is closest
    to half (greedy, not guaranteed optimal): mean 14.64, min 6, max 48, over all 325 targets.
  - The information bound: an average below log2 325 = 8.34 is impossible for any
    strategy with yes/no answers. So the true optimum lies between 8.34 and 14.64 on average;
    the note says only "choosing each day to split ... as evenly as possible took 15 days on
    average", which is what I computed.
- Forty yes-or-no attributes: 2^40 = 1,099,511,627,776 (past a trillion, short scale).
  3^40 + 1 = 12,157,665,459,056,928,802; log2 = 63.40, so 64. 40 bits = 5 bytes.
  2^(2^40) has 2^40 × log10 2 = 1.0995e12 × 0.30103 = 3.31e11 decimal digits ("about 331
  billion").
- PAC bound (not in the post, cited for support): with ε = 0.1, δ = 0.05, n = 40,
  (1/ε)(n ln 3 + ln 20) = 10 × (43.94 + 3.00) = 469 examples.
- "Nearly all inductive bias": in the four-attribute example the format rules out
  16,777,216 − 109 = 16,777,107 concepts; the three examples then rule out 109 − 6 = 103.
  In bits: log2(2^24/109) = 17.23 against log2(109/6) = 4.18. Not in the notes: counted as
  raw numbers the comparison depends on order (the three examples alone would rule out
  2^24 − 2^21 = 14,680,064 of all concepts, seven eighths), so the claim is cleanest in bits.
  I judged this a nitpick of wording and kept it here only.
- Mitchell's 973: 1 + 4 × 3^5 = 973 (Sky has 3 values plus "?", five two-valued attributes
  with 3 options each, plus the empty concept), the same counting rule as the post's 109.

Number threshold (STANDARDS 2.4): the post's "might only take 9 examples" and "64 examples"
are stated under an explicit assumption ("Let's say that each Day we see is, usually,
classified positive by around half..."). The assumption fails at the start in the post's
own concept space, and the realistic figure (about 15 even with chosen examples) is more
than a fifth above 9. It does not change the argument, which needs only logarithmic growth,
and the note says so. I gave it one note because a reader could take nine random days to
be enough.

## 4. Claims about other posts

- "Mutual Information, and Density in Thingspace" (`data/originals/mutual-information-and-density-in-thingspace.md`,
  Posted 2008-02-23, one day before; "yesterday's post" is right). Last sentence: "And the way
  to carve reality at its joints, is to draw your boundaries around concentrations of
  unusually high probability density in [Thingspace](...)." The post's quotation drops "And",
  "your" and "in Thingspace", as its "(slightly edited)" says. Our note on that post already
  points forward to this one and to the "chicken-and-eggish" concession; no conflict.
- "Conditional Independence, and Naive Bayes" (`data/originals/conditional-independence-and-naive-bayes.md`,
  Posted 2008-03-01, a week after 2008-02-24): "This is called the "Naive Bayes" method,
  because it usually isn't quite true, but *pretending* that it's true can simplify the
  living daylights out of your calculations." Used in the clogic note on "why would you
  bother drawing boundaries?", in the Response and in an n.b. I annotated that post too; the
  notes agree.
- "Where to Draw the Boundary?" (`data/originals/where-to-draw-the-boundary.md`, line 50):
  "You could say, "Aesthetic emotion is *not* what these things have in common; what they
  have in common is an intent to inspire *any* complex emotion for the sake of inspiring
  it."" Supports "offered as a reader's possible reply".
- "The Cluster Structure of Thingspace" (`data/originals/the-cluster-structure-of-thingspace.md`,
  line 21): "dimensions would include the mass, the volume, and the density." Matches the
  post's own description; no note needed beyond the first cpara.
- "Einstein's Arrogance" (linked by the post): our note there (annotated/posts/einstein-s-arrogance.tex,
  line 15) carries the full Peirce point ("Think of what trillions of trillions of hypotheses
  might be made..."). Per STANDARDS 2.5 I only point to it.
- "Extensions and Intensions" (`data/originals/extensions-and-intensions.md`): read to check
  what "intension" means there ("The actual intension of my "tiger" concept would be the
  neural pattern ..."). No note relies on it.

## 5. Items not verified

- Mitchell's book text itself (only the lecture slides). The slides are Mitchell's own and
  carry the same example and results, so I cite them as slides.
- "There is a rather large literature" on concept learning: a commonplace, not checked.
- The post's "Thingspace ... may be too poorly defined to have ... a size" and "nothing above
  the level of molecules repeats itself exactly": figures of speech or concessions, not noted.

## 6. Judgment calls for the editor

- The clogic note on nine examples (see the threshold discussion in section 3). The simulation
  choices (uniform target over 325 concepts including the empty one; greedy query choice,
  which is not optimal) are mine. If the editor prefers, the note can drop the simulation and
  keep only the one-in-ten fact and Mitchell's proviso.
- The clogic note on "wiggin" (and the matching Response paragraph and n.b.): a fair defender
  could say the superexponential count is what explains why minds restrict themselves to
  simple concepts, so it bears on the example indirectly. The note claims only that the count
  is not what makes the choice audacious, and that the detective's point holds in the small
  space. The In short line says the example's audacity "does not come from the
  superexponential count" (I first wrote "does not bear on", and weakened it).
- The clogic note answering "why would you bother drawing boundaries?" with the author's own
  post a week later. It uses a later post to answer a rhetorical question; I judged it fair
  because the question is offered as support for "the probability distribution comes from
  drawing the boundaries".
- The cpara on "In fact, the above statement ... chicken-and-eggish": "moves to its next point
  without resolving it." I searched the rest of the post; the next paragraph is the "yet
  another reason" paragraph and nothing returns to the circularity.
- Credit notes: many cpara notes say "Correct" or "Checks". That is the honest result for a
  technical post whose numbers are right; the audit's praise-word flags, if any, come from
  these.
- Summary is 206 words (above the usual 150) because the post has two parts.
- Pronoun: "him" refers to Socrates (a character in the post); the author gets none.
- Process slip: at the start I wrote two scratch files into the session scratchpad path given
  in my environment, which turned out to be the main session's scratchpad. I deleted only the
  files I had created (models2.txt, sx-*.png) and moved all later work to
  `data/sources/b3b_*`.
