# Report: the-intuitions-behind-utilitarianism ("The \"Intuitions\" Behind \"Utilitarianism\"", Yudkowsky, posted 2008-01-28; book order 291)

## 1. The argument in three sentences (written before annotating)

Answering Paul Gowder's charge that the author's choice of torture over dust specks rests on
utilitarian intuitions that were never argued for, the post grants that all moral reasoning
starts from intuitions, but holds that some survive reflection and some do not, and that
refusing to build on the reflective ones leads to circular preferences. The intuitions
against adding up (people giving more to one child than to eight, scope insensitivity, the
Allais preferences, sacred values) are best explained as the brain's failure to multiply, and
the rhetoric of unconditional rules as a social signal, so they reveal no deep truth about
non-additive or two-tier values; a lexically lower tier would never affect any decision.
Hence, while the value of a single event may be complex, where lives and probabilities are
concerned one should "shut up and multiply", which is why the author is a utilitarian.

## 2. Sources checked

Local copies in `data/sources/5c_feeling-moral/` (curl, 29 Sept 2026).

1. Paul Gowder, "Knowing your argumentative limitations, OR 'one [rationalist's] modus ponens is
   another's modus tollens.'", Overcoming Bias, datePublished 2008-01-27
   (https://www.overcomingbias.com/p/knowing-your-arhtml, `gowder_ob.html`). Matched: "At most, at
   most! , Eliezer's arguments establish an inconsistency between two propositions."; "your
   intuitions about putting dust specks in people's eyes, sacred values, etc., to the extent they
   recommend inflicting a small harm on lots of people rather than a lot of harm on one person,
   when that the aggregate pain from the first is higher than the aggregate pain from the second,
   are true."; "They're on equal footing — you have no more reason to believe your utilitarian
   intuitions than you have to believe your dust speck intuitions!" The page's description:
   "Response to: Circular Altruism". The post's summary of Gowder is fair.
2. Paul Slovic, "Numbed by Numbers", Foreign Policy, 13 March 2007
   (https://foreignpolicy.com/2007/03/13/numbed-by-numbers/, `foreignpolicy_numbed.txt`). The
   post's block quotation matches word for word ("Other recent research shows similar results. Two
   Israeli psychologists ... Contributions to individual group members far outweighed the
   contributions to the entire group."). The post's link (story_id=3751) returns 403.
3. Kogut and Ritov, "The 'Identified Victim' Effect: An Identified Group, or Just a Single
   Individual?", J. Behav. Dec. Making 18 (2005) 157-167
   (https://pluto.huji.ac.il/~msiritov/KogutRitovIdentified.pdf, `kogut_ritov_2005a.txt`).
   Abstract: "the identified single victim elicited considerably more contributions than the
   non-identified single victim, while the identification of the individual group members had
   essentially no effect on willingness to contribute"; "the main difference being the inclusion
   of a picture in the 'identified' versions"; "Hence, the emotional reaction to the victims
   appears to be a major source of the effect." Study 1: "Singularity did not have a significant
   main effect on WTC." My note quotes the abstract up to "no effect" (the quotation ends before
   "on willingness to contribute"; meaning unchanged).
4. Kogut and Ritov, "The singularity effect of identified victims in separate and joint
   evaluations", OBHDP 97 (2005) 106-116 (https://pluto.huji.ac.il/~msiritov/KogutRitovSingularity.pdf,
   `kogut_ritov_2005b.txt`). Abstract: "for identified victims, contributions for a single victim
   exceed contributions for a group when these are judged separately, but preference reverses
   when one has to choose between contributing to the single individual and contributing to the
   group." Results: "Forty-three out of 62 subjects in the joint evaluation condition chose to
   donate money to the identified group, as opposed to 19 who preferred to donate to the
   identified individual". (In the other joint condition, free to give to both, "contributions
   were quite evenly divided"; my note speaks only of the choice condition.)
5. SEP, "Contractualism" (Ashford and Mulgan), https://plato.stanford.edu/entries/contractualism/
   (`sep_contractualism.txt`). Matched: "this restriction to single individuals' reasons bars the
   interpersonal aggregation of complaints; it does not allow a number of lesser complaints to
   outweigh one person's weightier complaint"; The Rocks, "Many contractualists, however, wish to
   capture the intuition that you ought to save the five"; "A further difficult kind of case for
   contractualism is where the burdens ... are unequal ... one person suffers agony for a hundred
   years; while in the second a million people suffer agony for a hundred years minus a day";
   Parfit 2011 vol. 2 pp. 196-7 as quoted there: "We might even believe that we ought to save Blue
   from her 100 days of pain rather than saving any number of such other people from their much
   smaller burden of 10 days of pain"; risk section: "Indeed, contractualism must prohibit all
   socially useful activities that carry any risk of harm", followed by discussion of solutions
   and "see Frick 2015, Fried 2012a, Horton 2017, Kumar 2015".
6. SEP, "Reflective Equilibrium" (`sep_re.txt`): "Reflective equilibrium is the dominant method in
   moral and political philosophy"; "especially as it has been developed by Rawls and Norman
   Daniels".
7. Huemer, "Lexical Priority and the Problem of Risk", Pacific Philosophical Quarterly 91 (2010)
   332-51, author's copy https://spot.colorado.edu/~huemer/papers/absolutism.pdf
   (`huemer_absolutism.txt`). Abstract: "lexical-priority theories are in danger of becoming
   irrelevant to decision-making, becoming absurdly demanding, or generating paradoxical cases in
   which each of a pair of actions is permissible yet the pair is impermissible."
8. Wikipedia, "Runaround (story)" (raw, `wiki_runaround.txt`): "oscillate around the point where
   the two compulsions are of equal strength" (Second Law vs strengthened Third Law). My note says
   "circles" and quotes the phrase "the point where the two compulsions are of equal strength".
9. Tetlock 2003 abstract (see the Feeling Moral report): "They treat the mere thought of trading
   off sacred values against secular ones (such as money) as transparently outrageous". My note
   rephrases the verb ("people treat ``the mere thought ... as transparently outrageous''").
10. Peter Norvig's remark on Asimov: one web search found nothing. Not traced; the note says so.

## 3. Arithmetic

Script `data/sources/5c_feeling-moral/arith.py`:
- 1,329,342,410 + 7 = 1,329,342,417 (the three totals are consistent: one more child, then
  seven more).
- 5 x 5,000 = 25,000 < 50,000.
- 0.0000000001% = 1e-12 as a probability (the sneeze remark; no note).

## 4. Claims about other posts

- "Scope Insensitivity" (`data/originals/scope-insensitivity.md`): "residents of four western US
  states would pay only 28% more to protect all 57 wilderness areas in those states". This post
  says "57 wilderness areas in Ontario"; Ontario was the lakes study. A slip with no consequence
  for the argument (STANDARDS 2.4, names), so no note; reported here.
- "Circular Altruism" (`data/originals/circular-altruism.md`): the chain and "If you find your
  preferences are circular here". "Feeling Moral" (`data/originals/feeling-moral.md`) omits it
  (read both).
- "The Allais Paradox" (`data/originals/the-allais-paradox.md`): "You become a *money pump.*";
  "Zut Allais!" (`zut-allais.md`): "preference reversals, dynamic inconsistency, money pumps".
  The post's link goes to "Allais Malaise", not in the book; my note points to the two book posts.
- "Ends Don't Justify Means (Among Humans)" (`data/originals/ends-don-t-justify-means-among-humans.md`,
  posted 2008-10-14, book order 292): "I endorse "the end doesn't justify the means" as a principle
  to guide humans running on corrupted hardware". Quoted in two parts in my note.
- "Mind Projection Fallacy": manifest order 196, Mere Reality, posted 2008-03-11. Metaethics posts
  in Value Theory: orders 270 ("Where Recursive Justification Hits Bottom", 2008-07-08), 277-279
  (July and August 2008).
- Gowder's dust-speck number: the post says "a googolplex dust specks"; the original question
  used 3^^^3 and "Circular Altruism" used a googolplex. No note.
- STANDARDS 2.5: no earlier note in book order on Scanlon, Parfit, Huemer, Kogut and Ritov,
  reflective equilibrium or lexical priority (grep of annotated/, honest/, reports).

## 5. Not verified

- Norvig's Asimov remark (not found).
- Scanlon's own text (What We Owe to Each Other) and Parfit's On What Matters: quoted only as
  the SEP entry quotes and describes them.
- The replies to the risk objection (Frick 2015, Horton 2017): only listed by the SEP; I say
  only that the entry "discusses replies".
- Whether Asimov's Laws are ever strictly ordered in other stories: not checked; the note is
  limited to "Runaround" as Wikipedia summarizes it.

## 6. Judgment calls

1. The main critical point (clogic on "That's aggregation." and the Response): the arguments from
   counting lives do not reach the dust-speck case, because contractualists who deny aggregation
   of small harms still save five over one. This depends on the SEP's account. The note ends by
   saying which argument in the post is aimed at the disputed case, so it is not a "never
   answers" charge.
2. The lexical-tier argument is given credit ("A real objection"), with Huemer (2010, after the
   post) as later development, not prior work. The SEP's risk problem for contractualism is
   presented as the same objection pressed against the other side, with replies mentioned.
3. The "other side's hard case" (Parfit's agony case) is included as information supporting the
   post's circular-preference claim, so the notes do not take a side.
4. "None is shown here" (paragraph on paradoxes and circular preferences): the post says "if you
   try to violate ... you run into ..." without an example in this post. The Response states this
   neutrally, with the book's omission of the chain.
5. The Gowder cpara says the post's summary is fair and that Gowder gave no definition; the
   latter matches the post's own complaint, and my note adds what Gowder's description implies.
6. Reflective equilibrium: credit ("close to"), not a charge that the idea is unoriginal.
7. Reserved-word flags: "the opposite" and "false" occur only in paraphrases of the post; "never"
   no longer appears in my text.
