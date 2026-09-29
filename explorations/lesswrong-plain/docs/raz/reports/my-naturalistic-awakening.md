# Report: my-naturalistic-awakening ("My Naturalistic Awakening", Yudkowsky, posted 2008-09-25)

## 1. The argument in three sentences (written before annotating)

The author dates the break with the earlier folly to grasping, in full generality, the
notion of an optimization process: something that squeezes the future into a narrow region
of the possible. Having seen natural selection and human intelligence only as a dichotomy,
the author generalized once a third case appeared, a non-cognitive plot device in an
unfinished story, and this naturalistic view went beyond defining intelligence as
"achieving goals", which keeps mentalistic language. Seeing an optimizer as a physical
process that steers the future toward whatever its utility function says made the author
see that the 1997 design would have wiped out humanity, and conclude "I've been stupid."

## 2. Sources checked (outside quotations and figures)

Files in `data/sources/batch6a_fighting-a-rearguard/`; notes in `notes_awakening.py`.

**Yudkowsky, "Levels of Organization in General Intelligence"**, MIRI reprint
https://intelligence.org/files/LOGI.pdf (`LOGI.pdf/.txt`). Citation block matched: "Yudkowsky, Eliezer. 2007. “Levels of Organization in General Intelligence.” In Artificial General Intelligence, edited by Ben Goertzel and Cassio Pennachin, 389–501. Cognitive Technologies. Berlin: Springer." The reprint says "This version contains minor changes."
- Footnote 34 (LOGI.txt lines 3638-3642): "Viewing evolution itself through the lens provided by DGI is just barely possible. There are so many diﬀerences as to render the comparison one of “loose analogy” rather than “special case.” This is as expected; evolution is not intelligent, although it may sometimes appear so." We quote the first two sentences.
- Line 120-121: "Evolution is a useful inspiration but a dangerous template."
- Because the reprint "contains minor changes", these words may differ slightly from the 2002 draft; the note calls it "the paper".

**SL4 archive, April 2002 index** http://sl4.org/archive/0204/index.html (plain http worked; https failed; `sl4/idx_0204.html`): "PAPER: Levels of Organization in General Intelligence  Eliezer S. Yudkowsky (Sun Apr 07 2002 - 15:14:18 MDT)". I also searched the indexes for 0201-0303 for Emil Gilliam's posts: none is a reply about LOGI or the human line, and no subject contains "alien" from him. So the Gilliam exchange could not be traced (it may have been private or in a thread under another subject). Not mentioned in the notes. "My Bayesian Enlightenment" confirms Gilliam as a correspondent of the period (he bought the author a book).

**Legg and Hutter, "A Collection of Definitions of Intelligence"**, IDSIA-07-07, arXiv 0706.3639 (`legg_hutter_defs.pdf/.txt`). The post links a 2010 archive of vetta.org (unreachable); I used the 2007 published version. Counts: section 2 (collective) numbered 1-18, section 3 (psychologists) 1-35, section 4 (AI researchers) 1-18: 71 in all (numbered items; my grep for opening quotes found 65 because some items wrap before the quote mark, so I counted the numbering). AI-researcher definitions using "goal(s)", "goal-achieving" or "problems": Albus, Fogel, Goertzel, Gudwin, Horst, Kurzweil, Legg-Hutter, McCarthy, Minsky, Poole = 10 of 18 (Newell-Simon's "ends" not counted). Lenat and Feigenbaum, item 7, matched: "Intelligence is the power to rapidly find an adequate solution in what appears a priori (to observers) to be an immense search space."

**Rosenblueth, Wiener and Bigelow, "Behavior, Purpose and Teleology", *Philosophy of Science* 10 (1943) 18-24.** Scanned PDF at https://courses.media.mit.edu/2004spring/mas966/rosenblueth_1943.pdf (`rwb.pdf`); no text layer and no OCR tool, so I rendered p. 18 to an image and read it; transcription in `rwb_p18_transcribed.txt`. Matched: "The term purposeful is meant to denote that the act or behavior may be interpreted as directed to the attainment of a goal—i.e., to a final condition in which the behaving object reaches a definite correlation in time or in space with respect to another object or event." The note replaces "—i.e.," by \ldots (the checker forbids em dashes in our text). Citation confirmed by Crossref (DOI 10.1086/286788).

**Campbell (1960).** PubMed record PMID 13690223 (`pubmed_campbell.txt`): "Blind variation and selective retention in creative thought as in other knowledge processes." Psychol Rev 1960;67:380-400. (Crossref gives "retentions"; I follow PubMed.) I did not read the paper. The note's description ("treats thought as another case of the process natural selection runs") rests on the title and on Simonton's review abstract (Phys Life Rev 2010, PMID 20416854, same file): "Campbell (1960) proposed that creative thought should be conceived as a blind-variation and selective-retention process (BVSR)." 

**Creating Friendly AI (2001)** (`CFAI.txt`), lines 3632-3666. Matched: "Scenario: The Riemann Hypothesis Catastrophe. You ask an AI to solve the Riemann Hypothesis. As a subgoal of solving the problem, the AI turns all the matter in the solar system into computronium, exterminating humanity along the way." and "The other way to get a Riemann Hypothesis Catastrophe is to make solving the Riemann Hypothesis a direct supergoal of the AI—perhaps the only supergoal of the AI. This would require sheer gibbering stupidity, blank incomprehension of the Singularity, and total uncaring recklessness." We quote up to "of the AI," and "would require sheer gibbering stupidity".

**Second Law / Bennett:** no new source; the note relies on the SEP quotation already in our notes on "The Second Law of Thermodynamics, and Engines of Cognition" ("the cost lies in resetting the demon's memory").

## 3. Arithmetic

- 71 = 18 + 35 + 18 (see above). 10 of 18 AI-researcher definitions.
- "six damned years": 1997 to late 2002 is five to six years; the post itself says it is unsure of years, and "The Magnitude of His Own Folly" also says "for the last six years". No note on this.
- "five days later": 2008-09-25 to 2008-09-30. "nine days"/"sixteen days" belong to the other reports.
- LOGI pages 389-501 as given in the citation.

## 4. Claims about other posts

- "Twelve Virtues of Rationality" (Posted 2006-01-01), line 14: "The third virtue is lightness. ... Beware lest you fight a rearguard retreat against the evidence, grudgingly conceding each foot of ground only when forced, feeling cheated. Surrender to the truth as quickly as you can. Do this the instant you realize what you are resisting, the instant you can see from which quarter the winds of evidence are blowing against you." The post's version has a semicolon for the last comma; not noted (no consequence).
- "The Magnitude of His Own Folly" (Posted 2008-09-30): "at the point where, in late 2002, I looked back to Eliezer1997's AI proposals and realized what they really would have done" and "It wasn't until my [insight into optimization](/lw/u9/my_naturalistic_awakening/) let me look back and see Eliezer1997 in plain light". The link target is this post, so "this insight" is right.
- "Optimization and the Intelligence Explosion" (order 147, Book III): "your power as a mind is your ability to hit small targets in a large search space".
- "The Importance of Saying 'Oops'": "As opposed to, “I’ve been stupid.”" (said of Enron's executives).
- "No Universally Compelling Arguments": our notes there state the orthogonality thesis via Bostrom (2012). My note only points there.

## 5. Items not verified

- The Emil Gilliam exchange and the "Completely Alien Mind Design" reply (see above).
- The 1997 goal-system design and what it "would have" done ("generic tools"): the 1997-1999 texts (Coding a Transhuman AI, the Meaning of Life FAQ) need web.archive.org, which was unreachable. The cpara says so.
- "I've already been corrected once in my recollections": not checkable.
- The unfinished science-fiction story: not public, as the post says.

## 6. Judgment calls for the editor

- Reserved words: none in the notes or afterword after revision ("That does not refute" was reworded).
- The CFAI Riemann Hypothesis note is the most delicate. The memoir says Eliezer2001 "didn't think he *knew*" whether a paperclip-like superintelligence was possible. The 2001 text names such a case as a way to get a catastrophe. I present it as information and say the old text "cannot settle" what its author knew (memoir rule: no demand for evidence of inner states). The Response and "In short" say the picture of 2001 "should be read beside" that text. If the editor thinks even that implies a charge, the In short line could drop the clause.
- The Rosenblueth-Wiener-Bigelow note says the post's contrast is between a mentalistic and a physical reading of "goal". This is a mild logical point against "A goal is a mentalistic object", which the post states flatly (the next sentence, "When a human imagines a goal", is about how people imagine it). I think the point is fair and sourced; it is framed as prior work close to the post's own view.
- Campbell 1960 is cited from its PubMed record and Simonton's abstract; I did not read the paper itself.
- The Response says the post "takes a side against" Campbell's line of thought. The post does not name Campbell; it states its own view ("drives me up the wall"). I avoided "does not engage" or "does not name" per the brief.
- Lenat and Feigenbaum: prior work close to the post's view, presented as information, not as a claim that the post's idea is unoriginal. The post's own claim is hedged ("less obvious reply than it seems").
