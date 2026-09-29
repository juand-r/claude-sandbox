# Report: ends-don-t-justify-means-among-humans

## 1. The argument in three sentences

Building on the previous day's post ("Why Does Power Corrupt?", not in the book), the author
says humans may have evolved to believe that seizing power is for the good of the tribe while
the power in fact serves themselves, so a human's sense that a power grab is altruistic "may
not be be much evidence" that it is, and the sensible human response is a rule that forbids
the act even when it seems, or even is, beneficial ("the ends don't justify the means"). The
author rejects as "a dodge" the reply that humans can never know the stipulated facts of a
trolley-style thought experiment, yet holds that humans should keep deontological prohibitions
while a well-calibrated Friendly AI, which lacks the evolved tendency to be corrupted by power,
might rightly push one person to save five. The rule is therefore not "inherently" right but
"reflective consequentialism": consequentialist reasoning one level up, for beings who know
their moment-to-moment judgments run on untrusted hardware.

## 2. Sources checked

All files are in `data/sources/5c_ends-don-t-justify-means-among-humans/` (Wikipedia pages as
`?action=raw` wikitext, SEP as HTML plus tag-stripped `.txt`). The helper scripts that inserted
the notes (`scripts/insert.py`, `scripts/notes_ends.py`) and the untouched skeleton
(`skel_ends.tex`) are there too.

- J. S. Mill, *Utilitarianism* (1861), Project Gutenberg #11224 (`mill_utilitarianism.txt`),
  ch. 2. Matched: "We are told that an utilitarian will be apt to make his own particular case
  an exception to moral rules, and, when under temptation, will see an utility in the breach of
  a rule, greater than he will see in its observance." "Stock arguments" appears in the sentence
  before ("The remainder of the stock arguments against utilitarianism"), which supports
  "standard objection".
- SEP, "Consequentialism" (Sinnott-Armstrong; substantive revision Wed Oct 4, 2023),
  https://plato.stanford.edu/entries/consequentialism/ (`sep_consequentialism.txt`). Matched:
  "Utilitarians regularly argue that most people in most circumstances ought not to try to
  calculate utilities, because they are too likely to make serious miscalculations that will
  lead them to perform actions that reduce utility." And: "Some utilitarians (Sidgwick 1907,
  489–90) suggest that a utilitarian decision procedure may be adopted as an esoteric morality
  by an elite group that is better at calculating utilities". The quoted words in the note are
  SEP's, and the note says so.
- SEP, "Rule Consequentialism" (Hooker; substantive revision Sun Jan 15, 2023),
  https://plato.stanford.edu/entries/consequentialism-rule/ (`sep_consequentialism-rule.txt`).
  Matched: "consequentialists nearly never defend this act-consequentialist decision procedure
  as a general and typical way of making moral decisions (Mill 1861: ch 2; Sidgwick 1907: ...;
  Hare 1981; Parfit 1984: ...; Railton 1984: ...". Also "the agent might make mistakes in the
  calculations. (This is especially likely when the agent's natural biases intrude ...)".
- Wikipedia, "Two-level utilitarianism" (`wp_Two-level_utilitarianism.txt`). Matched: "The
  theory was initially developed by R. M. Hare"; "The former he called the 'archangel' and the
  latter the 'prole'" (citing Hare 1981, pp. 44-46); "The archangel has superhuman powers of
  thought, superhuman knowledge and no weaknesses"; "Such a person would not need a set of
  intuitive moral rules"; "One objection is that two-level utilitarianism undermines an agent's
  commitment to act in accordance with his or her moral principles" (McNaughton 1988, p. 180);
  "It is impossible, he claims, to compartmentalise one's thinking"; "Hare's response to this
  type of criticism is that he does his own moral thinking in this way". Hare's and McNaughton's
  books were not read; the notes say "as summarized in Wikipedia".
- Wikipedia, "Trolley problem" (`wp_Trolley_problem.txt`). Matched: "raised in 1967 ... by the
  English philosopher Philippa Foot"; "Later dubbed 'the trolley problem' by Judith Jarvis
  Thomson in a 1976 article that catalyzed a large literature"; "scenarios in which the
  sacrificed person is instead pushed onto the tracks as a way to stop the trolley".
- Wikipedia, "Blackstone's ratio" (`wp_Blackstone%27s_ratio.txt`). Matched: "It is better that
  ten guilty persons escape than that one innocent suffer", from the *Commentaries* "in the
  1760s". Blackstone's own text was not opened.

## 3. Arithmetic

None.

## 4. Claims about other posts

- "Why Does Power Corrupt?" (fetched to `data/originals/why-does-power-corrupt.md` with
  `src/fetch.py post v8rghtzWCziYuMdJ5`; not in the book). LessWrong API `postedAt`:
  2008-10-14T00:23:23Z; this post 2008-10-14T21:00:00Z, so "yesterday" is consistent (US time)
  and both files say 14 October 2008. Matched: "Call it a just-so story if you must"; "A much
  more important objection is the need to redescribe this scenario in terms of power structures
  that actually exist in hunter-gatherer bands, which, as I understand it, have egalitarian
  pressures (among adult males)"; "The original Communist Revolutionaries, I would guess
  probably a majority of them, really were in it to help the workers"; "George Washington
  refused the temptation of the crown".
- "Ethical Injunctions" (next in book order, 293): its "But surely... redo the calculation"
  paragraph is the version of the two-level objection the last note points to.
- "When Science Can't Help" and others: not relied on here.

## 5. Not verified

- The Corwin epigraph and the "variously attributed" line: not checked; no note depends on them.
- Hare's *Moral Thinking* and McNaughton's *Moral Vision*: read only through Wikipedia's summary.
  Whether Hare himself used the archangel against trolley-type cases specifically is not claimed.
- Sidgwick's *Methods of Ethics* pp. 489-90: only SEP's summary.

## 6. Judgment calls

- The P18 clogic (and the Response's third paragraph, and one n.b.) says the post's own view
  reaches the reply's verdicts on the same ground, and that what it rejects "as far as the text
  shows" is the refusal to consider the case. A defender could say the difference is that the
  author answers for humans (keep the prohibition) while the reply declines to. I think the
  note is compatible with that reading, since that is the "refusal" it names, but the editor
  should check it.
- The P19 clogic compares the unhedged "specific biological adaptation, supported by specific
  cognitive circuits" with the post's own "may have evolved" and the previous day's "just-so
  story". It is the only criticism in the "In short" line. The hedge in paragraph 1 is ten
  paragraphs earlier and about the revolution story; I judged it the same thought (the same
  adaptation), so the hedge-dropping reading is fair. The author could reply that the phrase
  "clear evolutionary reason" is shorthand for the previous post's argument.
- The P14 note on "some historical statistics" is mild ("The post gives none"); it is hedged
  with "seem" in the post, and the note does not call the claim false.
- Credit notes (Mill, trolley problem, Hare, Blackstone, Sidgwick, SEP) are information and
  support the post. The Response gives the credit in one paragraph and says the view is sound.
- Main published objection: McNaughton's, via Wikipedia, placed at the last paragraph with a
  pointer to "Ethical Injunctions". I chose it over the SEP "incoherence" and "rule-worship"
  objections because the post's view is two-level (act-consequentialist criterion, rules as the
  human decision procedure), not rule-consequentialist as a criterion of rightness. The SEP
  incoherence formulation is used in the "Ethical Injunctions" notes instead, at the paragraph
  where that post raises the objection itself.
- Pronoun flags: Mill's own "his"/"he" inside his quotation; "he"/"himself" for R. M. Hare
  (well-documented historical figure). No pronoun for the post's author.
- "Reversed rule" replaced "the opposite rule" (reserved-word list), though it only described
  the post's own hypothetical.
- Other agents are annotating neighbouring posts (291, "The 'Intuitions' Behind
  'Utilitarianism'", and later ones). If they also credit Hare or Mill, STANDARDS 2.5 may call
  for one full statement with pointers; I could not coordinate.
