# Report: humans-in-funny-suits

## 1. The argument in three sentences

Science fiction's aliens are usually humans in costume, and the deeper failure is that they
think like humans, because we model other minds by "empathic inference", running a copy of
their state on our own brain, which works only because humans share one psychology. Minds
with other emotions, no sense of humor, or no emotions at all (natural selection is the real
example) cannot be grasped this way, and anthropomorphism is too deep to drop by an act of
will. The inability to imagine the alien is the inability to see one's own humanity as a
special case.

## 2. Sources checked

Saved in `data/sources/batch3a/`.

- The image: downloaded from the post's URL (`biggorn.jpg`) and viewed: Kirk in a yellow shirt,
  tangled in rope, and a green reptilian alien. Wikipedia, "Arena (Star Trek: The Original
  Series)" (`wp_Arena_TOS.txt`): airdate 1967-01-19; "Kirk gets caught in a rope trap set by
  the Gorn"; "The Gorn was portrayed by stuntmen Bobby Clark and Gary Combs and by extra Bill
  Blackburn in close-ups."
- Russell (1994), Psychological Bulletin 115: 102-41, abstract from PubMed (PMID 8202574,
  `pubmed_russell1994_barrett2019.txt`): "When they are combined, these method factors may help
  to shape the results. Facial expressions and emotion labels are probably associated, but the
  association may vary with culture". Comments by Ekman and Izard are listed on the record.
- Barrett, Adolphs, Marsella, Martinez and Pollak (2019), Psychological Science in the Public
  Interest 20: 1-68, abstract (PMID 31313636): "how people communicate anger, disgust, fear,
  happiness, sadness, and surprise varies substantially across cultures, situations, and even
  across people within a single situation." Also, for balance: "people do sometimes smile when
  happy ... more than what would be expected by chance."
- Stanford Encyclopedia of Philosophy, "Folk Psychology as Mental Simulation" (first published
  1997, revised 2017), https://plato.stanford.edu/entries/folkpsych-simulation/
  (`sep_folkpsych_simulation.txt`): "ST challenges the Theory-Theory of mindreading (TT), the
  view that a tacit psychological theory underlies the ability to represent and reason about
  others' mental states." Also: "In its modern guise, ST was established in 1986".
- Wikipedia, "The Omega Glory" (`wp_The_Omega_Glory.txt`): airdate 1968-03-01; "Spock then
  conjectures that the history of Omega IV had closely paralleled that of Earth"; "The second
  document proves to be a version of the American Constitution" (link text; the link target is
  the Preamble).
- Orson Scott Card remark: web search found nothing; the note says I could not find it.

## 3. Arithmetic

None.

## 4. Claims about other posts

- "The Psychological Unity of Humankind" (fetched, `src/fetch.py post Cyj6wQLW6SeF6aGLy`,
  Posted 2008-06-24; not in the manifest). The facial-expression sentences are copied from it
  word for word; its argument is "In a sexually reproducing species, complex adaptations are
  necessarily universal."
- "Mind Projection Fallacy" (order 196, Posted 2008-03-11): "Probably the artist did not even
  think to ask whether an alien *perceives* human females as attractive." The note quotes
  without the emphasis (no italics in our text).
- "Thou Art Godshatter" (this batch): "because evolution is stupid in an absolute sense".
- "Belief in Intelligence" (this batch): ""Intelligence" is too narrow a term to describe these
  remarkable situations in full generality. I would say rather "optimization process"." and the
  friend's competence as "an extremely abstract property".
- "The Tragedy of Group Selectionism" (order 138): "Before 1966, it was not unusual to see
  serious biologists advocating evolutionary hypotheses that we would now regard as magical
  thinking." Pointer only.
- Metaethics links: "Changing Your Metaethics" (order 277) and "The Gift We Give to Tomorrow"
  (order 286) are later in the book; "Interpersonal Morality" is not in the book.

## 5. Items not verified

- "'Humans in funny suits' is a well-known term in literary science-fiction fandom" and "It is
  proverbial in literary science fiction that the true test of an author is their ability to
  write Real Aliens": not checked; no note (the argument does not depend on them).
- "folded-up hydrocarbon chains internally bound by van der Waals forces (aka proteins)":
  proteins are polyamide chains of amino acids (containing N, O, S), not hydrocarbons, and
  folding depends on the hydrophobic effect, hydrogen bonds and other interactions as well as
  van der Waals forces. A joke-register gloss with no consequence for the argument; report only
  (STANDARDS 2.4(2)).
- Card attribution (hedged in the post).

## 6. Judgment calls for the editor

1. Verbatim check: `check_verbatim.py` prints DIFF (insert '-'). This is a checker false
   positive, not an edit. The original Markdown has a line beginning "- not as a norm ..."
   (a line break inside a sentence), which the checker strips as a bullet marker. The LessWrong
   htmlBody (fetched via GraphQL) has "<em>special case</em>\n- not as a norm", which renders as
   "special case - not as a norm", so the skeleton, which keeps the dash, is right.
   `notes_backup.py export` reports 0 characters changed against the skeleton. I did not edit
   the checker or the skeleton. raz_check exits 1 for this reason only.
2. Reserved words: none.
3. Simulation theory (two notes: one that the view is one side of a debate, one that the
   argument skips an abstract model and that "Belief in Intelligence" uses one). A fair defender
   could say the post only needs simulation to be how we model minds "in detail". The post says
   "The only reason you can try at all to grasp" another brain is simulation, so I kept the
   notes. The Belief in Intelligence comparison crosses book order in reverse of writing order
   (that post is later, October 2008); the note says "the previous post in the book", which is
   true.
4. Natural selection as an example of a mind without emotions. The fair defender: "I said
   optimization process, and the objection's premise was building complex machines". The note
   says what the example does show. I think the point stands because the post's own objection
   is worded "any intelligent mind".
5. The humor paragraph note says the first objection "gets no answer here". The later
   "don't bother explaining" paragraph is about emotions in general and is also a dismissal, so I
   did not treat it as the answer.
6. The torn-dress note (hedge in "Mind Projection Fallacy" dropped here). Small; could be cut if
   the editor thinks it a nitpick. I considered adding that pulp covers were drawn to sell to
   human buyers (so not an error about aliens at all) and dropped it: unsourced.
7. The facial-expressions note is the first occurrence in book order of this claim (the
   Psychological Unity post is not in the book), so it is made in full here.
8. Honest section is 516 words, slightly over the 500 guideline.
