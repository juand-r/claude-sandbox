# Report: the-true-prisoner-s-dilemma ("The True Prisoner's Dilemma", Yudkowsky, posted 2008-09-03; book order 281)

## 1. The argument in three sentences (written before annotating)

The Prisoner's Dilemma is defined by its payoff matrix: each player prefers (D, C) to (C, C) to
(D, D) to (C, D), so defection dominates although both prefer mutual cooperation to mutual
defection. The usual illustrations (two prisoners, or strangers playing for dollars) ask the
human reader to pretend to be entirely selfish, which a person with inborn fairness and sympathy
cannot really do, so for a human the story's payoffs are not truly those of the dilemma and the
instinct is to look for mutual cooperation. A dilemma whose payoffs a human really holds needs an
opponent who cares nothing for us, such as a paperclip maximizer bargaining over a cure for
billions of people, and there (D, C) really does seem better than (C, C) while the rest of the
logic is unchanged; the post ends by asking the reader what to do then.

## 2. Sources checked

Local copies in `data/sources/5b_the-true-prisoner-s-dilemma/` (curl or API, 29 Sept 2026).

1. Post comments, LessWrong GraphQL API (`tpd_comments.json`, 118 comments).
   - Robin Hanson, 2008-09-03 23:12: "The entries in a payoff matrix are supposed to sum up
     *everything* you care about, including whatever you care about the outcomes for the other
     player. Most every game theory text and lecture I know gets this right, but even when we say
     the right thing to students over and over, they mostly still hear it the wrong way you
     initially heard it. This is just part of the facts of life of teaching game theory."
   - Yudkowsky, 2008-09-03 23:17: "...the standard illustration of the Prisoner's Dilemma, taught
     to beginning students of game theory, fails to *convey* those entries in the payoff matrix -
     as if the entries were merely *money* instead of *utilons*..." and "you can tell people all
     day long that the entries are in utilons, but until you give them a visualization where those
     really are the utilons, it's around as effective as telling juries to ignore hindsight bias."
   - Yudkowsky, 2008-09-03 22:06: "I didn't say I would defect." And 2008-09-04 02:56: "But wait
     for tomorrow's post before you accuse me of disloyalty to humanity."
2. Wikipedia, "Prisoner's dilemma" (raw, `wiki_pd.txt`), Premise section quoting Poundstone 1993,
   p. 118: "This "typical contemporary version" of the game is described in William Poundstone's
   1993 book Prisoner's Dilemma"; "They plan to sentence both to a year in prison on a lesser
   charge"; "he will go free while the partner will get three years in prison"; "both will be
   sentenced to two years in jail"; "Each prisoner is concerned only with his own welfare—with
   minimizing his own prison sentence." (My note truncates at "welfare." with the period; the
   dropped clause only specifies the welfare.) Poundstone's book itself not read.
3. SEP, "Prisoner's Dilemma" (Kuhn), `sep_pd.html`/`sep_pd.txt`. Matched: "Both care much more
   about their personal freedom than about the welfare of their accomplice"; "if the payoffs are
   not assumed to represent self-interest, a group whose members rationally pursue any goals may
   all meet less success"; section 8: "a stag hunt is a two player, two move game ... R > {T,P} >
   S"; "For this reason games with this structure are sometimes called games of "assurance" or
   "trust.""
4. Trivers 1971, Quarterly Review of Biology 46:35-57 (PDF from greatergood.berkeley.edu,
   `trivers1971.pdf/.txt`). Abstract: "Specifically, friendship, dislike, moralistic aggression,
   gratitude, sympathy, trust, suspicion, trustworthiness, aspects of guilt, and some forms of
   dishonesty and hypocrisy can be explained as important adaptations to regulate the altruistic
   system." (pdftotext scrambles the order of "trustworthiness"; the order matches the web search
   copy of the abstract.) Body text: "The relationship between two individuals repeatedly exposed to
   symmetrical reciprocal situations is exactly analogous to what game theorists call the
   Prisoner's Dilemma".
5. Fischbacher, Gächter and Fehr 2001, Economics Letters 71:397-404, abstract on IDEAS/RePEc
   (`fischbacher2001_ideas.txt`): "We find that about a third of subjects' contribution schedules
   is characterized by complete free-riding. However, a majority of 50 percent of the subjects
   displays conditional cooperation." "conditionally cooperative, i.e., to contribute more to the
   public good the more the other beneficiaries contribute."
6. Van Lange and Balliet 2015, "Interdependence Theory", APA Handbook chapter (PDF from
   amsterdamcooperationlab.com, `vanlange_balliet.pdf/.txt`): "introduces transformation of the
   given to the effective matrix, thereby formalizing interaction goals broader than immediate
   self-interest"; "Informed by research conducted during the 1960s and 1970s, they chose the
   second option"; "Messick and McClintock ... had already provided empirical evidence for some
   transformations on the basis of research using experimental games". Kelley and Thibaut (1978)
   itself not read.
7. "Hindsight Bias" (LessWrong fkM9XsNvXdYH6PPAx, `data/originals/hindsight-bias.md`, already
   present): "57% of the experimental group concluded the flood was so likely that failure to take
   precautions was legally negligent. A third experimental group was told the outcome andalso
   explicitly instructed to avoid hindsight bias, which made no difference: 56% concluded the city
   was legally negligent." Not in the book (manifest checked).
8. "The Truly Iterated Prisoner's Dilemma" (jbgjvhszkr3KoehDh, posted 2008-09-04, fetched to
   `data/originals/`): repeats the game "exactly 100 times". Not in the book.

Tried and failed: Sally (1995) meta-analysis (paywalled; eScholarship PDF blocked by CloudFront);
Dawes and Thaler (1988, JEP, AEA site returned HTML). I dropped the cooperation-rate claim I had
planned (Sally's 47.4 per cent average, seen only in a search summary).

## 3. Arithmetic

Script `data/sources/5b_the-true-prisoner-s-dilemma/check_payoffs.py`, output in `check_payoffs.out`.
- Standard matrix (rows = player 2, columns = player 1, cells (u1, u2)): T=5, R=3, P=2, S=0 for
  both players; T>R>P>S true; D strictly dominates C for both; R>P for both; 2R=6 > T+S=5.
- Prison story, the post's rule (1 year each; testifying takes 1 off your own and adds 2 to the
  other's): (C,C)=1,1; (D,C)=0,3; (C,D)=3,0; (D,D)=2,2. Same as Poundstone. With payoff = -years,
  T>R>P>S holds. "our confederate spending three years" matches (D,C).
- True PD: humans 3>2>1>0 billion lives, paperclipper 3>2>1>0 clips; PD for both; defecting
  against a cooperator instead of cooperating: +1 billion lives, -2 paperclips (the post's
  "sacrifice a billion human lives to produce 2 paperclips").
- SEP stag hunt (4,4 / 0,3 / 3,0 / 3,3): R > T, and both (C,C) and (D,D) are equilibria.

## 4. Claims about other posts

- "Sympathetic Minds" (next in book, `data/originals/sympathetic-minds.md`): "It might have gotten
  started, maybe, with a mother's love for her children". Used in the Trivers note.
- "Anthropomorphic Optimism" (order 153), "Sorting Pebbles Into Correct Heaps" (274), "Newcomb's
  Problem and Regret of Rationality" (296): link targets, checked in the manifest. Anthropomorphic
  Optimism does not mention paperclips; my note says only that the link goes there.
- Earlier notes checked for 2.5: no earlier post in book order carries a Trivers, stag-hunt or
  Kelley-Thibaut note. Thou Art Godshatter dates Trivers (1971) in passing; Detached Lever Fallacy
  describes Tit for Tat without a source note. The Gift We Give to Tomorrow (286) is later.

## 5. Not verified

- Poundstone (1993) directly; Kelley and Thibaut (1978) directly; Messick and McClintock (1968).
- One-shot PD cooperation rates (Sally 1995; Cooper et al. 1996): not reached, not used.
- "enormous volumes of material" and "one of the great foundational issues in decision theory":
  not checked; no note.

## 6. Judgment calls

1. Overall stance: almost every note is credit or description. The one substantive criticism is
   that the claims about human instinct (cannot pretend to be selfish; what we feel in the lab) are
   offered without evidence. The hedges ("not entirely", "we may", "without a complicated
   effort") are acknowledged in the notes and Response.
2. The P13 note (Hanson's comment and the author's reply) follows the Book V lesson: the author's
   comment narrows the claim to the illustration, so I do not criticize "fake" as a claim about
   game theory.
3. The Fischbacher note uses a public-goods game, not a two-player PD; the note says so. "The
   paragraph's 'we' describes the first group" is my reading; it is not a charge that the post is
   wrong, since the post hedges with "not entirely".
4. Trivers note: "The post states the origin without a hedge" plus the pointer to Sympathetic
   Minds' "maybe" is a mild consistency observation; the editor may prefer to cut the second
   sentence.
5. Reserved words: "never" appears only in paraphrase of the post's stipulation ("never interacted
   ... never interact again") and in "would never be friends" (Sympathetic Minds). "wrong" in the
   Response is Hanson's phrase.
6. Pronouns: none for real people in our own text; "his" only inside the Poundstone quotation.
7. Honest section is 507 words, slightly over 500.
8. Honest test build (both sections in the honest preamble) has one overfull box of 1.5pt.
