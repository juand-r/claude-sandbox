# Report: is-reality-ugly

## 1. The argument in three sentences

The previous post found a hidden regular level in the cubes (constant third differences);
one might object that the real world, unlike closed mathematics, is messy, but physics has
already found an exact, simple level beneath the surface, and the best guess is that
reality "is made of math". Our remaining uncertainty has three sources: not knowing the
fundamental laws (small, since only particle accelerators reveal it), lacking the
computing power to derive consequences (logical uncertainty, as in protein folding), and
not knowing where in the universe we are (indexical uncertainty, the little people on the
cubes, including Everett branches). Since the fundamental order is already found, messy
fields like biology will not become easy through new basic physics; uncertainty is in the
map, not the territory, and the world is "a series of cubes."

## 2. Sources checked

Files in `data/sources/4a_the-world-an-introduction/`, plus `data/originals/expecting-beauty.md`
and `data/originals/beautiful-math.md` (fetched with `src/fetch.py post uichBYWKcGAqRZZdP`
and `Rjw4qhEMvqskhL6Gm`).

- "Expecting Beauty" (2008-01-12, the "Yesterday" link). Matched: "You had to dig deeper
  to find the stable level, but it was still there - in the example I chose."; last
  paragraph: "And yet in mathematics the premises and axioms are closed systems - can we
  expect the messy real world to reveal hidden beauty?" (italics on "messy real world" in
  the original dropped in my quotation). Not in the book's manifest.
- Wikipedia, "Mathematical universe hypothesis" (`wp_Mathematical_universe_hypothesis.txt`).
  Matched: "is a speculative "theory of everything" (TOE) proposed by cosmologist Max
  Tegmark"; "The hypothesis has proven controversial."; "the physical universe is not
  merely described by mathematics, but is mathematics"; Tegmark 1998, Annals of Physics
  ("Is "the Theory of Everything" Merely the Ultimate Ensemble Theory?").
- Jumper et al., Nature 2021, PubMed 34265844 (`jumper2021_abstract.txt`). Matched:
  "demonstrating accuracy competitive with experimental structures in a majority of cases".
  Training on known structures: Wikipedia "AlphaFold": "trained the program on over 170,000
  protein structures from the Protein Data Bank"; CASP14 November 2020.
- SEP "Self-Locating Beliefs", https://plato.stanford.edu/entries/self-locating-beliefs/
  (`sep_self_locating.html`). Matched (Lewis 1979 quoted): "They inhabit a certain possible
  world, and they know exactly which world it is. Therefore they know every proposition
  that is true at their world. ... Still I can imagine them to suffer ignorance: neither
  one knows which of the two he is."
- Wikipedia, "Series of tubes": "a phrase used originally as an analogy by then-United
  States Senator Ted Stevens"; "On June 28, 2006".
- Bostrom's book: Anthropic Bias (2002). Title and year from general knowledge; the post
  names no title. Low risk.
- Our notes on "Making Beliefs Pay Rent" (Response, fourth paragraph) for the author's
  many-worlds case, and the Book IV introduction ("a number of physicists continue to reject
  it or maintain agnosticism").

## 3. Arithmetic recomputed

- Cubes 1, 8, 27, 64, 125, 216: first differences 7, 19, 37, 61, 91; second 12, 18, 24, 30;
  third 6, 6, 6. Correct.
- Four-digit cubes: 10^3 = 1000 ... 21^3 = 9261. 12^3 = 1728 is the only one starting 17
  (11^3 = 1331, 13^3 = 2197). Correct.
- 173^3: 173^2 = 29929; 29929 x 173 = 29929 x 170 + 29929 x 3 = 5,087,930 + 89,787 =
  5,177,717. So 5177717 is a cube. Correct.

## 4. Claims about other posts

- "(as I noted) is a handpicked example": confirmed in Expecting Beauty ("in the example I
  chose").
- The "perfectly regular" link points to Universal Law (overcomingbias 2007/04/universal_law);
  consistent with that post's claim.
- Many-worlds pointer: consistent with the notes on making-beliefs-pay-rent and with the
  Book IV introduction's note (my file).

## 5. Not verified

- "Some tiny little 5-nanometer molecule that folds in a microsecond": plausible for small
  fast-folding proteins; not checked; no note.
- Bostrom's book title (see above).

## 6. Judgment calls

- The "made of math" clogic: says the paragraph argues only that physics is described by
  mathematics, and that "made of math" is Tegmark's stronger, controversial hypothesis. A
  fair defender could say "made of math" is loose talk for "fully described by math". The
  post repeats it at the end ("the world is math"), so I read it as meant. The Response
  and In short line carry this; the editor may prefer it out of the In short line.
- The biology clogic ("the 'Because' does not carry it"): my counterexample is standard
  physics (thermodynamics, ideal gas law), not a speculative objection, and the note keeps
  the post's hedge ("Offered as a guess"). The post's bar, "as easy as a sequence of
  cubes", is high; a fair defender could say no higher-level biology law meets it. The
  note targets only the inference from "master order found".
- The many-worlds clogic: made briefly with a pointer (STANDARDS 2.5), and it grants that
  the conclusion holds without many-worlds. The "deterministic" point is folded into the
  cpara on the next paragraph with "see above".
- AlphaFold note: post-dated information, as allowed ("one neutral note may say so").
- Lewis credit: information; Bostrom is credited in the post.
