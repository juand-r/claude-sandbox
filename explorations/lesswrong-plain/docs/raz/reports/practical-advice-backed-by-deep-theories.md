# Report: practical-advice-backed-by-deep-theories ("Practical Advice Backed By Deep Theories", Yudkowsky, posted 2009-04-25)

Batch 6c, Book VI "Becoming Stronger", The Craft and the Community, book order 336.

## 1. The argument in three sentences (written before annotating)

Practical advice is more powerful when it is backed by concrete experimental results, causal
accounts that are actually true, and mathematics validly interpreted: Seth Roberts's
Shangri-La Diet spread beyond one lucky trick because Roberts could interpret his own
experience through research on set points and flavor-calorie learning, and the author's own
advice to follow the evidence became clear in practice only through probability theory. A
theory also makes advice stick, as knowing the peak-end rule and duration neglect makes a
reader feel at the dinner plate that portion size barely changes the memory of a meal. The
author wants advice on akrasia of this kind, from someone who reads the experimental
literature and can explain in its terms what worked, and ranks the three kinds of backing by
how hard they are to cite well.

## 2. Sources checked (outside quotations and figures)

All saved in `data/sources/6c_practical-advice-backed-by-deep-theories/` (with the helper
scripts `lw2.py`, `comments.py`, `body.py`, `insert.py` and the note lists `rules_pa.json`,
`rules_gf.json`).

- **Rode, Rozin and Durlach (2007)**, Appetite 49:18-29, PubMed abstract PMID 17459522
  (`pubmed_meals.txt`). Matched: "Across the three studies, there was consistent evidence for
  duration neglect (no effect of increased duration/exposure of the favorite component)";
  "In all three studies, there was no evidence for peak, primacy or recency effects"; "The
  existence of duration neglect implies that, with respect to memories of a meal, small
  portions of a highly favored dish will have roughly the same memorial effect as large
  portions"; "evaluated for similarity to effects seen in memories of pain". Abstract only;
  the full paper was not read.
- **Garbinsky, Morewedge and Shiv (2014)**, Psychological Science 25:1466-74, PubMed abstract
  PMID 24894582 (`pubmed_meals.txt`). Matched: "memory for end enjoyment, rather than
  beginning enjoyment, of a pleasant gustatory experience determines how soon people desire to
  repeat that experience"; "memory for end moments, when people are most satiated, interferes
  with memory for initial moments".
- **Ariely and Loewenstein (2000)**, JEP: General 129:508-523, the PDF the post links,
  http://web.mit.edu/ariely/www/MIT/Papers/duration1.pdf (`ariely_duration1.pdf`; the PDF is a
  scan with no text layer, so I rendered page 1 and transcribed the abstract by hand into
  `ariely_duration1.txt`). Matched: "The major finding is that response modes that reduce
  reliance on conversational norms or standard of comparison also increase the attention that
  participants pay to duration." The note paraphrases the first half of that sentence and
  quotes the second half.
- **Hagger et al. (2016)**, Perspectives on Psychological Science 11:546-73, PubMed abstract
  PMID 27474142 (`pubmed_steel_hagger.txt`). Matched: "Although a meta-analysis of
  ego-depletion experiments found a medium-sized effect"; "Multiple laboratories (k = 23, total
  N = 2,141)"; "(d = 0.04, 95% CI [-0.07, 0.15]".
- **Steel (2007)**, Psychological Bulletin 133:65-94, PubMed abstract PMID 17201571
  (`pubmed_steel_hagger.txt`). Matched: "based on 691 correlations"; "These effects prove
  consistent with temporal motivation theory, an integrative hybrid of expectancy theory and
  hyperbolic discounting." (The note quotes from "consistent with".)
- **Muehlhauser, "How to Beat Procrastination"**, LessWrong, posted 2011-02-05, user
  lukeprog, https://www.lesswrong.com/posts/RWo4LwFzpHNQCTcYt/how-to-beat-procrastination
  (`lw_how_to_beat_procrastination.md`, via the GraphQL API). Matched: "Most of the advice
  below is taken from the best book on procrastination available, Piers Steel's The
  Procrastination Equation"; reference list includes "Steel (2007). The nature of
  procrastination." The name Luke Muehlhauser for lukeprog is common knowledge; not separately
  sourced.
- **ClinicalTrials.gov NCT00726271** (`ct_NCT00726271.json`, API v2). Matched: briefTitle
  "Pilot Study of Dietary Modification of Appetite Set Point in Obesity"; overallStatus
  "TERMINATED"; whyStopped "Record owner left institution"; startDate 2008-06; hasResults
  False; the summary names "the Shangri-La Diet" and Seth Roberts.
- **"The Most Important Thing You Learned"** (LessWrong, 2009-02-27,
  https://www.lesswrong.com/posts/bsdxuNdSGbfEKZREP), 99 comments via GraphQL
  (`most_important_comments.json`). Comments matching /bottom.line/: AnnaSalamon ("A
  near-tie. Either: (1) The Bottom Line, or ..."), Z_M_Davis ("This is to nominate 'The Bottom
  Line'"), Cameron_Taylor (a list ending "The bottom line."). Matching /engines of
  cognition|second.law|thermodynamic/: infotropism, Emile, SilasBarta. Hence "three name each".
- **Seth Roberts's Paris story**: Wikipedia raw "The_Shangri-La_Diet" (`wp_The_Shangri-La_Diet.txt`):
  "In 2000, Roberts visited Paris ... it was due to experiencing unfamiliar flavors of soft
  drinks that were not available to him in the USA." Psychology Today (2017), "How a
  Psychologist Lost Weight Drinking Soda" (`psychtoday_soda.txt`): "the thing he remembered
  most were the sodas, which came in many flavors unavailable in the US." Used only for the
  report (see section 6), and for the neutral wording "unfamiliar-tasting drinks" in the notes.

## 3. Arithmetic

- "Fifteen days earlier": The Unfinished Mystery of the Shangri-La Diet, Posted 2009-04-10;
  Beware of Other-Optimizing, Posted 2009-04-10; this post, Posted 2009-04-25. 25 - 10 = 15.
- "published two years before the post": Rode et al., Appetite July 2007 (epub April 2007);
  post April 2009.
- Thread counts: 3 and 3 of 99 comments, by regex (section 2).
- No number in the post is recomputed; the post's only number is the p-value rule of thumb.

## 4. Claims about other posts

- "The Unfinished Mystery of the Shangri-La Diet" (`data/originals/the-unfinished-mystery-of-the-shangri-la-diet.md`):
  "*this theory has never been analyzed by controlled experiment, which drives me up the
  frickin' WALL.*"; "[Many people](http://boards.sethroberts.net/), including some trustworthy
  [econblogger types](...), have reported losing 1-2 pounds/week". Also used for "an elegant
  combination of pieces individually backed by previous experiments" (considered, not used;
  see section 6).
- "Beware of Other-Optimizing" (`data/originals/beware-of-other-optimizing.md`, book order 335):
  "I don't possess the deep keys that would tell me *when* and *why* and for *who* a technique
  works or doesn't work."
- "The Bottom Line" (`data/originals/the-bottom-line.md`): the post's paraphrase ("once a
  conclusion is written in your mind, it is already true or already false ... no amount of
  later argument can change that") matches "The arguments you write afterward, above the
  bottom line, will not change anything either way." No note; our model notes on that post
  concern the evidential value of the listed clues, a different point.
- "The Second Law of Thermodynamics, and Engines of Cognition": "Engines of cognition are not
  so different from heat engines". The post's "minds as mapping engines that require evidence
  as fuel" is a fair summary. No note.
- "Illusion of Transparency" cites Keysar's experiments; "Expecting Short Inferential
  Distances" gives the evolutionary account. The post's parenthesis ("a cognitive science
  experiment and some evolutionary psychology") fits. No note.

## 5. Items not verified

- Roberts's own first-hand account of the Paris trip (his book, his 2004 paper in Behavioral
  and Brain Sciences) was not read; the "soft drinks" versus "fruit juices" point rests on
  Wikipedia and Psychology Today.
- The full texts of Rode et al. (2007), Garbinsky et al. (2014), Steel (2007) and Hagger et al.
  (2016); abstracts only.
- The earlier ego-depletion meta-analysis (Hagger et al. 2010) is cited only through the 2016
  abstract's "a meta-analysis of ego-depletion experiments found a medium-sized effect".
- Whether any controlled trial of the Shangri-La Diet was published after 2008: my searches
  found only the terminated pilot. The note says only that the pilot was terminated with no
  results posted.

## 6. Judgment calls for the editor

- The main critical point (notes on paragraph 4 and the last paragraph, Response, In short,
  two n.b.s): the thesis is supported by illustrations, and the lead example's benefits are
  self-reported and, by the author's own account fifteen days earlier, untested. The post
  itself grants that the diet "is visibly incomplete". I judged the point fair because the
  post states the diet's benefit as the effect of the theory ("the reason why as many people
  have benefited as they have ... is that Roberts knew the experimental science"). If the
  editor reads the post's claim as about the diet's spread rather than its effect, the
  Response's lead-example paragraph should be softened.
- The dessert note: "(You also know to save the dessert for last.)" is a light aside. I kept a
  note because it is the post's own example of advice derived from a theory and can be
  checked, and I added the 2014 end-effect finding so the note does not overstate. If the
  editor judges it a joke taken literally (THIRD_PASS rule 1), cut the note and the dessert
  clause of the Response, In short line and n.b.; the portion-size credit then stands alone.
- The Response's sentence "Findings about memories of pain, carried over to meals, held for
  duration and not for the end" is my summary of the Rode abstract ("evaluated for similarity
  to effects seen in memories of pain"). Check that it is not read as a claim about the
  peak-end literature in general.
- Information notes (Steel 2007, ego depletion 2016) are marked as information and kept out
  of the In short line. Steel is given as evidence that such advice could be written, not as
  a fault; the post hedges its survey of advisers with "for the most part".
- Considered and dropped: (a) "fruit juices" against the sources' "soft drinks"/"sodas" (a
  slip with no consequence for the argument; report only). (b) That Roberts's combined theory
  was his own synthesis, not a theory "used by a majority within a given science", sits
  uneasily with the post's ladder; dropped because the post rests the case on "deep factors
  that actually did exist" (set points, flavor-calorie learning), which are established, and
  the ladder is advice for readers who do not know whom to trust. (c) A note that the
  counterfactual's "temporary" effect is predicted from Roberts's own theory (cut as an
  objection any illustration would face). (d) "the breakdown of the self" versus Ainslie's book
  title Breakdown of Will (nitpick). (e) A tension with "Knowing About Biases Can Hurt People"
  (the original-edition Lens note makes that point; not repeated here).
- Reserved words: "never" appears only inside the author's quotation ("has never been
  analyzed"). No other reserved word is used.
- Pronouns: "he/his" appear only for Seth Roberts, whom the post calls "he".
