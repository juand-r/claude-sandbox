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

## 2. Sources checked

Saved in `data/sources/b3b_typicality/`.

- The two figures, downloaded from https://www.lesswrong.com/static/imported/2008/02/09/blegg1_3.png
  and .../blegg2.png (`blegg1_3.png`, `blegg2.png`; also `blegg3.png` from 2008/02/10, used by
  "How An Algorithm Feels From Inside"). I viewed them. Network 1: Color +blue/-red, Shape
  +egg/-cube, Luminance +glow/-dark, Texture +furred/-smooth, Interior +vanadium/-palladium,
  complete graph (10 edges). Network 1b: Lifespan +mortal/-immortal, Feathers +no/-yes, Blood
  +red/-glows green, Legs +2/-17, Nails +broad/-talons. Network 2: star, centre "Category:
  +BLEGG / -RUBE".
- Hopfield (1982), PNAS 79:2554, abstract via PubMed 6953413 (`pubmed_6953413_hopfield1982.txt`):
  "Computational properties of use of biological organisms or to the construction of computers
  can emerge as collective properties of systems having a large number of simple equivalent
  components (or neurons)."; "a content-addressable memory which correctly yields an entire memory
  from any subpart of sufficient size"; "The algorithm for the time evolution of the state of the
  system is based on asynchronous parallel processing."; "Additional emergent collective
  properties include some capacity for generalization, familiarity recognition, categorization,
  error correction, and time sequence retention." The full text (PMC346238) could not be
  fetched (PNAS 403, Europe PMC 503).
- Wikipedia, "Hopfield network" (raw, `wiki_hopfield.txt`): l. 2 "each neuron is connected to
  every other neuron except itself. These connections are bidirectional and symmetric"; l. 46
  "The constraint that weights are symmetric guarantees that the energy function decreases
  monotonically while following the activation rules."; l. 65 asynchronous updating; l. 103
  "under repeated updating the network will eventually converge to a state which is a local
  minimum in the energy function" (citing Hopfield 1982); l. 124 and l. 179 Hebb's rule, 1949.
- Wikipedia, "Belief propagation" (`wiki_bp.txt`): Pearl "formulated it as an exact inference
  algorithm on trees"; "it will terminate after two full passes through the tree"; "messages are
  passed inwards ... The second step involves passing the messages back out".
- Wikipedia, "Naive Bayes classifier" (`wiki_naive_bayes.txt`): "assume that the features are
  conditionally independent, given the target class" (not quoted in the notes; the notes quote the
  author's own 1 March 2008 post instead).
- Wikipedia, "Perceptrons (book)" (`wiki_perceptrons.txt`): "The most important one is related to
  the computation of some predicates, such as the XOR function"; "Research on three-layered
  perceptrons showed how to implement such functions."
- Murphy and Ross (1994), Cognitive Psychology 27:148-193, abstract via PubMed 7956106
  (`pubmed_7956106_murphy_ross1994.txt`): "The experiments tested a Bayesian rule of prediction
  according to which (1) predictions of an object's features are based on information from
  multiple categories, and (2) features are treated as independent of one another. With one
  exception, the studies found evidence against both of these claims. Subjects did not generally
  alter their predictions as a function of information outside the most likely "target" category.
  In addition, feature relations had reliable effects on these predictions."

## 3. Arithmetic

- Connections: complete graph on N nodes has N(N-1)/2 edges; N = 5 gives 10 (matches the figure);
  star has N edges. So O(N^2) and O(N) are right.
- The reddish-purple case: with equal positive Hebbian weights w, luminance input =
  w(-2/3 + 1 + 1) = (4/3)w > 0 before interior is set, and the same for interior; both settle
  positive, as the post says. Simulated in `data/sources/b3b_typicality/scripts/sign_check.py`
  (pure Python): result [-0.67, 1, 1, 1, 1].
- Sign of the colour-luminance weight (the `\clogic` on "negative connection"). With the figure's
  coding, red = -1 and dark = -1, so red -> dark needs a positive weight: (-1)(+w) = -w.
  Simulation (same script), patterns: 10 bleggs, 10 rubes, 5 red furred egg-shaped vanadium
  objects that do not glow; Hebbian weights give colour-luminance +25, and the red furred object
  settles to glowing (+1) because shape, texture and interior (15 each) outweigh it. With a
  strong NEGATIVE weight (-75) it still glows; with a strong POSITIVE weight (+100) it settles to
  [-1, 1, -1, 1, 1], dark, egg, furred, vanadium, which is what the post wants.
- Dates: this post 2008-02-10; "How An Algorithm Feels From Inside" 2008-02-11 ("the next day");
  "Conditional Independence, and Naive Bayes" 2008-03-01 (20 days, "about three weeks later").

## 4. Claims about other posts

- "Conditional Independence, and Naive Bayes" (`data/originals/conditional-independence-and-naive-bayes.md`
  l. 124): "if you use the right kind of neural network units, this "neural network" ends up
  *exactly, mathematically* equivalent to Naive Bayes." (italics dropped in the quote). The same
  post shows the Network 2 figure.
- "Cached Thoughts" (`cached-thoughts.md` l. 9): "most neurons fire 10–20 times per second, or
  200Hz tops."
- "Fake Causality" (`fake-causality.md` l. 31): "One of the primary inspirations for Bayesian
  networks was noticing the problem of double-counting evidence if inference resonates between an
  effect and a cause." (the cpara's "describes Bayesian networks as a response to this problem").
- "Cultish Countercultishness" (`cultish-countercultishness.md` l. 19): "The human mind, as it
  thinks about categories, seems to prefer essences to attractors."
- "How An Algorithm Feels From Inside": our notes there (order 164) say of Network 2 "The reasons
  given are engineering virtues ("fast, cheap, scalable"). No neuroscience is cited." and the
  afterword "No study of categorization, human or animal, is cited." My notes agree.

## 5. Items not verified

- Hopfield (1982) full text: abstract only; the convergence statement is from Wikipedia citing
  the paper. The note says "(Wikipedia, ``Hopfield network,'' citing Hopfield 1982)".
- Murphy and Ross: abstract only. The note's gloss "within categories" on "features are treated
  as independent of one another" is my reading of the Bayesian rule tested (Anderson's model,
  where features are independent given the category); the abstract does not say "within
  categories".
- Hebb 1949 as "one of the first rules ever proposed": accepted; Wikipedia gives Hebb 1949.
- "differential equations for gradient descent": the derivation is of derivatives
  (backpropagation), not differential equations; a loose phrase, not noted.

## 6. Judgment calls for the editor

1. Consistency with order 164 (STANDARDS 2.5). The point that the Network 2 guess has no
   evidence about brains is made here in full, at its first occurrence (the "Make no mistake"
   cpara and the Response). The 164 notes and afterword make it in full too. The editor may want
   164's version shortened to a pointer back to this post. Also, 164's post text repeats
   "potentially oscillating/chaotic behavior" as a disadvantage of Network 1; my Hopfield
   convergence note here would apply there, and a pointer could be added.
2. Sign `\clogic` uses "wrong way round", qualified by "Read as the sign of a weight". A fair
   defender could say "negative connection" meant "a connection that makes red predict dark". The
   qualifier allows this. The point is kept out of the "In short" line (slip whose point survives).
3. Convergence `\clogic`: the post says "Recurrent networks don't always settle right away", which
   is true in general; the note grants this and restricts itself to the design described
   (symmetric Hebbian weights, asynchronous updates, which the post names, though in mockery).
   The note does not claim that settling is fast.
4. Hopfield and Naive Bayes/belief-propagation notes are information and credit, not charges.
   The Response's "A reader of this post would not learn that either design has a literature" is
   the only judgment drawn from them; cut if the editor treats non-naming as a nitpick.
5. Murphy and Ross is used twice, for two findings of the same abstract: once against Network 2's
   independence assumption, once in support of "classify once and for all". The two notes point to
   each other.
6. Considered and dropped: the Aristotle attribution of "All men are mortal" (the author marks it
   "Aristotle(?)" in "The Parable of Hemlock", order 156, which is the place for any note); the
   typo "Positive activation flows luminance from shape"; "differential equations".
