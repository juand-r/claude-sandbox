# Report: dreams-of-ai-design ("Dreams of AI Design", Yudkowsky, posted 2008-08-27; book order 268)

## 1. The argument in three sentences (written before annotating)

AI is fundamentally about reducing the mental to the non-mental, and living inside a mind does
not teach this, because the brain's work is hidden and we predict mental words such as
"contemplative" only by empathy, running our own brain as a black box. Fake reductions
(Aristotle's cooling blood, "lots of neurons" plus "emergence", boxes with labels and arrows)
leave that black box closed; real reductions (Bayes's theorem after Jaynes, Pearl's conditional
independence, the minimax search tree) let you say what a system does without pointing at a
human. So designs built on commonsense knowledge, parallelism or brain-likeness are dreams, a
proposal that an AI will work "just like humans" should be refused until it explains what the
AI does and why, and teaching fundamental AI work means teaching reductionism, Taboo and the
avoidance of anthropomorphism.

## 2. Sources checked

Local copies in `data/sources/5a_detached-lever-fallacy/` (shared scratch folder for both my
slugs; scripts `insert.py`, `notes_dreams.py`).

1. Dennett, dictionary entry "homunculus" (Tufts Digital Library,
   https://dl.tufts.edu/downloads/rr1729066?filename=b27746887.pdf, `dennett_homunculus.txt`):
   "If one can get a team or committee of relatively ignorant. narrow-minded, blind homunculi to
   produce the intelligent behavior of the whole, this is progress" (Dennett, Brainstorms, 1978)
   (the full stop after "ignorant" is OCR for a comma). Brainstorms itself was not read.
2. Aristotle, Physics II.8, trans. Hardie and Gaye, https://classics.mit.edu/Aristotle/physics.2.ii.html
   (`aristotle_physics2.txt`): "It is absurd to suppose that purpose is not present because we do
   not observe the agent deliberating. Art does not deliberate. If the ship-building art were in
   the wood, it would produce the same results by nature."
3. Aristotle, Parts of Animals II, trans. Ogle (`data/sources/b3a_power/aristotle_parts_animals_2.txt`,
   saved by an earlier batch): Part 7, "Of all animals, man has the largest brain in proportion to
   his size"; "It is then as a counterpoise to his excessive heat that in man's brain there is this
   superabundant fluidity and coldness"; Part 2, "of sanguineous animals, those are the most
   intelligent whose blood is thin and cold." (Part numbers located by script.)
4. Pearl (1988), pp. 7-9, as quoted by J. G. Wolff, arXiv cs/0307010 (`wolff_cs0307010.txt`,
   lines 2196-2209): "If you hear a radio announcement that there was an earthquake nearby, and if
   the last false alarm you recall was triggered by an earthquake, then your certainty of a burglary
   will diminish." and "explaining away". Pearl's book itself was not reachable (the earlier
   `data/sources/pearl1988_djvu.txt` is a 401 error page).
5. The formula: LessWrong HTML via GraphQL (`dreams_html.json`) has MathJax `mjx-denominator`
   spans, confirming the fractions. The odds form P(H|E)/P(notH|E) = P(E|H)/P(E|notH) x
   P(H)/P(notH) follows from Bayes's theorem by dividing the expressions for P(H|E) and P(notH|E);
   P(E) cancels.
6. Wikipedia "Connectionism" (raw): reference "Rumelhart, D.E., J.L. McClelland and the PDP
   Research Group (1986). Parallel Distributed Processing ... Volume 1". (The article's body says
   "a 1987 book"; I used the reference list's 1986, which is the publication year of both volumes.)
7. Wikipedia "AlexNet" (raw, `wiki_AlexNet.txt`): "Developed in 2012"; "The network achieved a
   top-5 error rate of 15.3% to win the contest, more than 10.8% points better than the runner-up";
   "split into two copies, each run on one GPU"; "influenced a large number of subsequent work in
   deep learning".
8. McDermott (1976), `mcdermott1976_raw.txt`: section heading "Wishful Mnemonics".
9. Mentifex: https://mind.sourceforge.net/diagrams.html (`mentifex_diagrams.html`): title "Diagrams
   of a Theory of Cognitivity"; the ASCII diagram contains "The Senses", "The Muscles",
   "Cerebellum", "(Motor Habituation)", "Concept ... Fibers". Identification of Mentifex as Arthur
   T. Murray and of AI4U as Murray's book: https://www.nothingisreal.com/mentifex_faq.html
   ("The Arthur T. Murray/Mentifex FAQ"; mentions "the AI4U Theory of Mind", "Mind.Forth") and
   the comment by "Mentifex" on this post ("as described in the AI4U textbook", "Mind.Forth").
10. LessWrong comments (`comments_dreams.md`): RobinHanson 2008-08-27: "But whole brain emulation
    hardly relys on vague analogies to human brains - it would be directly making use of their
    abilities." Eliezer Yudkowsky 2008-08-27: "Robin, whole brain emulation might be physically
    possible, but I wouldn't advise putting venture capital into a project to build a flying
    machine by emulating a bird."

## 3. Arithmetic

- The odds form of Bayes's theorem (item 5 above): correct.
- AlexNet margin: "more than 10.8% points" per Wikipedia; the note says "more than ten points".

## 4. Claims about other posts

- "Detached Lever Fallacy" (previous post in the book, 2008-07-31): linked on "detached levers".
- "Humans in Funny Suits" (order 146): its note calls empathic inference simulation theory, one
  side of a debate; my note points there instead of repeating the source.
- "The Futility of Emergence" (order 39): its In short says "with no user of the word quoted"; my
  note points back and adds only that the sentence attacked is written for the opponent.
- "The Power of Intelligence" (order 132): its note says the Aristotle aside is accurate, citing
  "tempers the heat and seething of the heart"; my cfact says "Roughly so" and adds the passages on
  brain size and cold blood.
- "Angry Atoms" (order 219): its note credits Shannon (1950) with minimax search.
- "Artificial Addition" (order 149): its note names Cyc.
- "Truly Part of You" (order 48): McDermott.

## 5. Not verified

- Dennett's Brainstorms and Pearl's book: quoted through secondary sources, as the notes say.
- "creative destruction" and "intuitive rather than rational reasoning": I could not identify the
  positions meant, so the note names only the two that match known programmes.
- Whether "demonstrably" refers to some evidence the author had in mind: none is given in the post.

## 6. Judgment calls

1. The AlexNet cfact is hindsight. It is information, and it says explicitly that the post's
   sentence is not refuted, since the post mocks nets justified by likeness to the brain. The
   Response mentions it in one paragraph and keeps it out of the In short line. The honest n.b.
   says the same. The editor may prefer to cut it as outside the text; "Artificial Addition"'s
   honest section already carries a similar hindsight note about language models.
2. Aristotle. I first wrote in the Response that the post's reading was "not one Aristotle
   overlooked". That fails the fair-defender test: the post's hedged guess is about what
   Aristotle's brain did, and Aristotle's denial that nature deliberates does not settle it. The
   Response now calls it context, not correction, and the note ends with the post's hedge.
3. Hanson's whole-brain-emulation objection is used as a contemporary counterexample to the funding
   rule. The author's reply is quoted. The In short line reports it as an objection ("as a
   contemporary objected"), not as settled. The author accepted the consequence (would not fund
   emulation), so the editor may judge this a disagreement rather than a flaw.
4. "Demonstrably" note: it says no demonstration is given, which is true of the post; it does not
   say the claim is false.
5. Dennett is given as credit (an earlier statement of the thesis), not as a charge of
   uncredited borrowing; the post does not claim the thesis is new.
6. Reserved word flagged: "refuted" in the Response, used as "is not refuted".
7. Pronouns: Aristotle keeps "he/his" (historical figure); Murray's program is "the program".
8. Overfull box of 0.42pt in one margin note (under the 1pt threshold).
