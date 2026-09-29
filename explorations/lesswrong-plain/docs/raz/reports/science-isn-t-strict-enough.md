# Report: Science Isn't Strict Enough (book order 251, batch 4d)

## 1. The argument in three sentences

The traditional ideal of Science asks only that you make your hypothesis testable, test it and accept
the result; it leaves the choice of which hypothesis to test to the individual, and so gave the
author's younger self a gold star for a theory that was never going to be right. Probability theory,
by contrast, gives one exact rational estimate for any state of evidence (the mammography example,
7.5%), with no room for whim either in the evidence or in the priors, so it can say in advance that
you picked the wrong hypothesis. This stricter standard is much harder to use than Science, but a
person who does not want to waste years must use it privately, as Nick Tarleton put it: the problem
is a private epistemic standard as lax as the social one.

## 2. Sources checked

All saved in `data/sources/4d_science-isn-t-strict-enough/`.

| Claim | Source | Exact words matched |
|---|---|---|
| Tarleton comment (post's quote, and the note's second quote) | LessWrong GraphQL, comments on post PGfJdgemDJSwWBZSX, comment ZdRB8WbvXqcctoFtg by Nick_Tarleton, 2008-05-16 (`sise_comments.json`) | "Surely this is a good thing, else fear of being thought stupid would overly discourage people from raising novel hypotheses. The problem is encouraging a *private*, *epistemic* standard as lax as the social one." |
| poke's objection (note on the scope paragraph, honest n.b.) | same file, comment FCzfuiKAmvEGwMCHZ by poke, 2008-05-16 | "what you're actually discussing is a second-hand imprecise (idealized) *description* of science. This sort of \"science as hypothesis-testing\" is a philosophical model." ; "But it's not used (or aimed for) *within* science" |
| Popper ranks by content, prefers improbable theories | SEP, "Karl Popper", https://plato.stanford.edu/entries/popper/ (`sep_popper.txt`) | "Popper rejects this. Science values theories with a high informative content ... For that reason, the more improbable a theory is the better it is scientifically, because the probability and informative content of a theory vary inversely" |
| Subjective vs objective Bayesians | SEP, "Bayesian Epistemology" (`data/sources/sep_bayesian_epistemology.txt`, saved by an earlier agent) | "Subjective Bayesianism is the view that every prior is permitted unless it fails to be coherent (de Finetti 1970 [1974]; Savage 1972; ...)"; "the party of subjective Bayesians, who hold that every prior is permitted unless it fails to be coherent"; "Objective Bayesians contend that, in addition to coherence, there is another epistemic virtue or ideal that needs to be codified into a norm for prior credences ... (Jeffreys 1939; Carnap 1945; Jaynes 1957, 1968; ...)" |

## 3. Arithmetic

Mammography: 0.01 x 0.8 = 0.008 true positives; 0.99 x 0.10 = 0.099 false positives;
0.008 / (0.008 + 0.099) = 0.008 / 0.107 = 0.07477 = 7.48%, which rounds to 7.5%. The post's
"not 7.4% or 7.6%" is correct at one decimal place.

## 4. Claims about other posts

- Twelve Virtues quotation: `data/originals/twelve-virtues-of-rationality.md` (Posted 2006-01-01), third
  virtue paragraph; the four quoted sentences match word for word.
- "The Importance of Saying Oops" (2007-08-05): "I switched to Bayescraft (Laplace / Jaynes / Tversky /
  Kahneman)". Used for the note on the paragraph naming Kahneman, Tversky and Jaynes.
- "When Science Can't Help" (2008-05-15, the day before): our notes there carry the Reichenbach point
  (context of discovery and justification); this post's note points there.
- "My Wild and Reckless Youth": our note there carries the SEP subjective/objective point in full; this
  post points there (STANDARDS 2.5).
- "Beautiful Probability": original line 41 "we think in terms of *laws.*" and line 71 "Think laws, not
  tools." Our Response there: "states claims of coherence and optimality more broadly than the results
  behind them"; the note here says the same in those terms.

## 5. Not verified

- Popper's own text (Logic of Scientific Discovery, Conjectures and Refutations) not read; the claim
  rests on the SEP summary, which the note names.
- The "ideal as traditionally preached" is the author's construct; I did not try to survey textbooks.

## 6. Judgment calls

- Popper note (inline \clogic on "in advance of the experiment"): I say the tradition "does contain a
  criterion applied before the test". The post's "official verdict" could be read as "a verdict of the
  institution", which a philosopher's criterion is not. I kept the note because the post's "Science" is
  the preached ideal, and Popper's falsificationism is its best-known form ("Changing the Definition of Science", two days
  later, quotes New Scientist on "Popper's notion"). Worded as a criterion, not a verdict.
- Note on the "cognitive engine" paragraph: says the argument addresses accuracy while the subjective
  school's claim is about what is permitted. This is my reading of the argument's structure, supported
  by the SEP wording ("permitted"); the editor may judge it too close to an argument of my own.
- Note on the scope paragraph: "The post quotes no text that states the ideal" (checked: the only
  quotations are the author's Twelve Virtues and Tarleton's comment). Response repeats it once.
- Reserved-word flags: "false" appears only in "false positives"/"false-positive rate". Motive flag
  ("inference") is "Bayesian inference". Pronouns: the Response's "He" for Popper was
  restructured to "Popper"; "his comment" for Tarleton became "the comment".
- Earlier-edition notes on When Science Can't Help and No Safe Defense are harsher in tone than these;
  I kept facts consistent (the Eliezer18 story, Reichenbach) and did not repeat their points.
