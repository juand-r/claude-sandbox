# Report: ethical-injunctions

## 1. The argument in three sentences

An "ethical injunction" is a rule not to do something even when your own reasoning says it
is the right thing, because in that class of cases it is "far more likely that you've made a
mistake"; the author introduces it through a hoped-for AI rule (shut down if you decide to
deceive your programmers), illustrates its hardest case with the sinking of the ferry Hydro
in 1944, and argues that the injunction against self-deception has no known exception because
self-deceptions are "black swan bets" whose rare blowups can cancel all their benefits. Two
grounds support such injunctions: corrupted hardware (humans are more likely corrupted than
right when they conclude, say, that robbing banks is for the greater good) and black swans
(some kinds of action blow up for reasons outside the decider's model); the objection that
one can simply redo the calculation with these reasons included is answered by "beware of
cleverness", by the point that meta-reasoning may be corrupted too, and by the author's own
history. The author stops short of endorsing absolute injunctions, but closes by dismissing
those who argue for relaxing their ethics, who in the author's experience always move toward
lenience and show no grasp of these risks.

## 2. Sources checked

All files are in `data/sources/5c_ends-don-t-justify-means-among-humans/` (shared with my first
slug). Helper scripts `scripts/insert.py`, `scripts/notes_ei.py`; untouched skeleton
`skel_ei.tex`.

- Wikipedia, "SF Hydro" (`wp_SF_Hydro.txt`). Matched: sinking "on 20 February 1944, when
  resistance fighters sank the ferry in the deepest part of Lake Tinn"; "18 people were killed.
  Twenty-nine survived. The dead comprised 14 Norwegian crew and passengers and four German
  soldiers"; "Some of the Norwegian rescuers felt that the Germans should not be saved, but this
  attitude did not prevail and four German soldiers were saved"; saboteurs "Alf Larsen, Knut
  Lier-Hansen, Rolf Sørlie and Knut Haukelid"; "Lier-Hansen indicated that he was a worker and
  wanted to sleep on board, in the end convincing the guard." (Sources there: Payton and
  Lepperød 1995; British Embassy Oslo 2014.)
- Wikipedia, "Norwegian heavy water sabotage" (`wp_Norwegian_heavy_water_sabotage.txt`).
  Matched: "the manifest indicated that there was only 500 kg of heavy water being transported
  to Germany. The Hydro was carrying too little heavy water to supply one reactor" (citing NOVA,
  "Hitler's Sunken Secret", 2005). Note: this article says "Haukelid recruited two people",
  while the SF Hydro article names four saboteurs; the note therefore attributes the four to
  "the ferry article".
- Wikipedia, "German nuclear program during World War II"
  (`wp_German_nuclear_program_during_World_War_II.txt`). Matched: 4 June 1942 conference
  "decided on its continuation merely for the aim of energy production"; "the Germans had never
  been close to producing nuclear weapons" (scholarly consensus, citing Walker 1995).
- Wikipedia, "Haigerloch atomic pile" (`wp_Haigerloch_atomic_pile.txt`). Matched: "5 tons of
  uranium, 1.5 tons of heavy water, 10 tons of graphite and a small amount of cadmium finally
  arrived in Haigerloch at the end of February 1945"; "this last large-scale experiment".
- Soares, Fallenstein, Yudkowsky, Armstrong, "Corrigibility" (AAAI Workshops, 2015),
  https://intelligence.org/files/Corrigibility.pdf (`corrigibility.pdf`, `.txt`). Matched in the
  abstract: "While some proposals are interesting, none have yet been demonstrated to satisfy
  all of our intuitive desiderata, leaving this simple problem in corrigibility wide-open."
  The paper's problem (safe shutdown on a button press) is related to, not the same as, the
  post's rule; the note says "a related problem".
- Wikipedia, "Black swan theory" (`wp_Black_swan_theory.txt`). Matched: "an event that comes as
  a surprise, has a major effect"; "articulated by Nassim Nicholas Taleb, starting in 2001".
  *The Black Swan* (2007) date is from general knowledge of the book, consistent with the
  article's references; not separately fetched.
- SEP, "Rule Consequentialism" (`sep_consequentialism-rule.txt`). Matched: "Rule-consequentialism
  is accused of incoherence for maintaining that an act can be morally permissible or even
  required though the act fails to maximise expected good."
- Mill, *Utilitarianism*, ch. 2 (`mill_utilitarianism.txt`). Matched: "There is no ethical creed
  which does not temper the rigidity of its laws, by giving a certain latitude, under the moral
  responsibility of the agent, for accommodation to peculiarities of circumstances; and under
  every creed, at the opening thus made, self-deception and dishonest casuistry get in."
- Calvin and Hobbes line: `calvin_hobbes_quotes_blogspot.txt`, from
  https://freecalvinhobbes.blogspot.com/2008/08/calvin-and-hobbes-quotes.html (a fan quotation
  list, secondary). Matched: "I don't know which is worse... that everyone has his price, or
  that the price is always so low. -- Hobbes". A web search summary (bookriot, fandom) describes
  the same strip (Calvin's price is two bucks). The strip's date and the original panels were
  not reached (michaelyingling.com search is behind a bot check). The note only identifies the
  speaker and gives the collection's wording; it does not call the post's version a misquote.

## 3. Arithmetic

None beyond reading figures (18 dead, 29 survivors, 4 Germans rescued; 500 kg against 1.5 t).

## 4. Claims about other posts

- "The Moral Void" (`data/originals/the-moral-void.md`, 2008-06-30, not in the book). Matched:
  "Would you kill babies if it was *inherently* the right thing to do?" and "If "yes", how
  inherently right would it have to be". The same post also has the Hobbes line, so its first
  appearance in the book is here.
- "Protected From Myself" (fetched to `data/originals/protected-from-myself.md` with
  `src/fetch.py post yz2btSaCLHmLWgWD5`; 2008-10-19, not in the book). Matched: "it was my
  ethical constraints, and not any conscious planning, that had put me in a recoverable
  position"; the advisers' "Let's lie!" proposals.
- "Use the Try Harder, Luke" (`data/originals/use-the-try-harder-luke.md`, book order 312).
  Matched epigraph: "When there's a will to fail, obstacles can be found." —John McCarthy.
- "When Science Can't Help" (order 250): our notes there carry the full point that cryonics'
  efficacy is unshown (absence-of-revival argument gives no positive evidence); the cryonics
  note here points back.
- "Ends Don't Justify Means (Among Humans)" (order 292): the first ground and the Mill, SEP
  and Hare credits are made there; here the Response points back.

## 5. Not verified

- The Rhodes quotation ("considered warning their benefactor but decided that might endanger
  the mission and only thanked him and shook his hand") and Rhodes's version of the guard story
  ("escaping the Gestapo"). archive.org copies of *The Making of the Atomic Bomb* are
  lending-restricted and the search-inside endpoint returned "Item not available"; Google Books
  API quota was exhausted; web search returned only mirrors of the post. The note says I could
  not check Rhodes.
- Whether the watchman who helped the saboteurs was aboard or among the dead: not found.
- Hobbes strip date (see above).

## 6. Judgment calls

- The "effectively, the end" cfact uses "Overstated". A defender could say "effectively"
  softens it, or that the author meant the end of the Norwegian supply. The sources show the
  program continued reactor work into 1945 and the cargo was small, so I kept "Overstated"
  (not a reserved word). This is a slip whose point (a hard case) survives, so it stays out of
  the "In short" line, per the brief.
- The cryonics clogic: "Stated without a hedge" is checked (no hedge in the sentence). The last
  sentence ("No evidence is given that belief in an afterlife is why preservation was not
  adopted") reads a causal claim from the context ("when they said, 'But we need religious
  beliefs to cushion the fear of death.'"); I think the context supports it, but the editor
  may prefer to cut that sentence.
- The Response's last paragraph says the closing third "adds characterization, not reasons",
  and the "In short" line says it "dismisses its opponents instead of answering them". The
  reasons are in the earlier paragraphs, and the list "They don't mention..." restates them;
  I judged that restating the reasons as things opponents fail to mention is not a new answer.
  This is the harshest judgment in the afterword.
- The guard discrepancy (Rhodes via the post vs Wikipedia/Payton and Lepperød) is in the
  paragraph note as information only; the moral example does not depend on which saboteur
  spoke, but it does bear on why the watchman helped.
- Hindsight: the corrigibility paper (2015) is a note only; I removed it from the Response.
- Credit notes (Taleb, SEP incoherence charge, Mill, McCarthy, Calvin and Hobbes) are
  information; the Response credits the post for raising the objection itself and declining
  absolute injunctions.
- Pronoun flags: "him"/"he" for the guard and Knut Lier-Hansen (historical; the post uses "him"
  for the watchman); "his" inside the Hobbes quotation. None for the author.
- Honest section is 635 words for a 2,650-word post (STANDARDS allows up to about 900 for very
  long posts); the summary is 213 words.
- Considered and left out: a note that the second ground (black swans) does not depend on a
  human bias, while "Ends Don't Justify Means" exempted a well-calibrated AI on the absence of
  that bias. It seemed speculative (a well-calibrated AI's model might include such risks).
  Also left out: the positive-illusions research against "I don't know if there was ever anyone
  for whom that was knowably a good idea" (the brief says the earlier self-deception notes are
  not for here, and the sentence is hedged and about knowable cases).
