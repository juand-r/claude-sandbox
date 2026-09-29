# Report: My Bayesian Enlightenment (order 310)

Agent: batch 6a. Slug: `my-bayesian-enlightenment`. Posted 2008-10-05.

## 1. The argument in three sentences

The author separates two early steps, being "born" a Bayesian (an anecdote about a
two-children puzzle in which the author's answer of 1/2 was called the Bayesian one) and
discovering heuristics and biases, from the "Bayesian enlightenment" proper. That came from
Jaynes's Probability Theory: The Logic of Science, which presented probability as unique
laws; together with the realization of past folly, it led the author to hold Friendly AI
designs to the standard of doing "only that which you must do, and which you cannot do in any
other way," to discard the old theories, and to study probability and decision theory.
Later the author found (through Pearl) that precision saves time and is the price of
thinking about a problem at all, and concludes that saying "Oops" is something to look
forward to.

## 2. Sources checked

Saved in `data/sources/6a_the-magnitude-of-his-own-folly/` unless noted.

- Wikipedia, "Boy or girl paradox" (raw, `wiki_Boy_or_Girl_paradox.txt`). Matched: "Gardner
  initially gave the answers 1/2 and 1/3, respectively, but later acknowledged that the second
  question was ambiguous. Its answer could be 1/2, depending on the procedure by which the
  information "at least one of them is a boy" was obtained." (fractions are {{sfrac}} templates
  in the source); the two procedures "From all families with two children, at least one of
  whom is a boy, a family is chosen at random. This would yield the answer of 1/3." and "From
  all families with two children, one child is selected at random, and the sex of that child is
  specified to be a boy. This would yield an answer of 1/2."; "It must be further assumed that
  Mr. Smith would always report this fact if it were true" (Wikipedia's sentence, following a
  quotation from Bar-Hillel and Falk 1982; my note attributes the words to Wikipedia
  "following Bar-Hillel and Falk"). Gardner's column: May 1959, "Mr. Smith" is the article's
  name for the second question.
- Jaynes, Probability Theory: The Logic of Science, draft ch. 1-3 with preface
  (`data/sources/jaynes_book_ch1-3.txt`, saved by an earlier agent; "Copyright c 1995 by
  Edwin T. Jaynes"). Matched: "invoke the aforementioned intuitive ad hoc devices to do,
  arbitrarily and imperfectly, what the rules of probability theory would have done for them
  uniquely and optimally. It is just this strict adherence that enables us to avoid the
  artificial paradoxes and contradictions of orthodox statistics"; chapter 3: "The denominator
  (1 − 1/6) in (3–57) has now been calculated in three different ways, with the same result. If
  the three results were not the same, we would have found an inconsistency in our rules".
- Wikipedia, "Edwin Thompson Jaynes" (raw, `wiki_Edwin_Thompson_Jaynes.txt`): died April 30,
  1998; the book "was published posthumously in 2003 (from an incomplete manuscript that was
  edited by Larry Bretthorst)".
- Wikipedia, "Neyman–Pearson lemma" (raw, `wiki_Neyman_Pearson.txt`): "describes the existence
  and uniqueness of the likelihood ratio as a uniformly most powerful test in certain
  contexts. It was introduced by Jerzy Neyman and Egon Pearson in a paper in 1933."
- Goodreads quotation 39654 (`goodreads_39654.html`), with the page's own warning "Quotes are
  added by the Goodreads community and are not verified by Goodreads.": "Do nothing because it
  is righteous or praiseworthy or noble to do so; do nothing because it seems good to do so; do
  only that which you must do and which you cannot do in any other way." ― Ursula K. LeGuin,
  The Farthest Shore. Wikiquote's Le Guin page (`wikiquote_LeGuin.txt`, Farthest Shore section)
  does not have the line. I could not check the novel (archive.org not tried; web.archive.org
  blocked). The note says so.
- yudkowsky.net/obsolete/singularity (`yudnet_singularity.txt`): "A good deal of the material I
  have ever produced – specifically, everything dated 2002 or earlier – I now consider
  completely obsolete." (en dashes in the source; the note uses \ldots for the omitted words.)

## 3. Arithmetic recomputed

- Well-posed version (you ask "Is at least one a boy?"): P(yes | BB) = P(yes | BG) = P(yes | GB)
  = 1, P(yes | GG) = 0; P(BB | yes) = (1/4)/(3/4) = 1/3. Correct.
- Post's version, with P(says "boy" | one of each) = 1/2: P(BB and says boy) = 1/4 x 1 = 1/4;
  P(one of each and says boy) = 1/2 x 1/2 = 1/4; P(GG and says boy) = 0. P(BB | says boy) =
  (1/4)/(1/4 + 1/4) = 1/2. Correct.
- The frequentist count in my note: among many families, a fraction 1/4 are BB and all their
  parents say "boy"; 1/2 are mixed and half of those parents say "boy" (1/4 of all families);
  so half of the families whose parent says "boy" are BB: 1/2. Same number, by counting.

## 4. Claims about other posts

- Probability is in the Mind (order 197, `annotated/posts/probability-is-in-the-mind.tex`):
  states the ask-the-question version with answer 1/3; its note says "If the mother had
  instead chosen what to mention, naming a boy or a girl at random when she has one of each,
  the same words would give 1/2", and its Response says the puzzles "show that you must
  condition on exactly what you learned" and do not decide between the views. My note points
  there and agrees.
- Beautiful Probability (order 188): the tools/laws contrast ("Old School statisticians thought
  in terms of tools ... we think in terms of laws"); our notes there discuss Cox's theorem
  ("It has been debated to what degree the theorem excludes alternative models"), the sense of
  "better"/optimal, and the frequentist rationale. My notes point there instead of repeating.
- The Level Above Mine (order 307, posted 2008-09-26): title as quoted.
- The Magnitude of His Own Folly (order 308): stop follows from seeing what the 1997 design
  would do ("It wasn't until my insight into optimization let me look back and see Eliezer1997
  in plain light"). This post: "I'm not sure if I read E. T. Jaynes's ... before or after the
  day when I realized the magnitude of my own folly". My note says the accounts need not
  conflict.
- Trying to Try (2008-10-01) and Use the Try Harder, Luke (2008-10-02, order 312): the
  "five minutes" note in Use the Try Harder, Luke (original edition) says the claim is
  "supported by nothing but a film scene, spoken by a fictional version of a real man". My
  note says "a made-up outtake of a film scene", which matches that post ("I present to you a
  little-known outtake"; the annotated note calls it "an invented outtake").

## 5. Not verified

- The Le Guin attribution (novel not checked; Goodreads is user-added).
- The Emil Gilliam comment behind the strikethrough (overcomingbias comment link not fetched;
  the note only describes what the published text shows).
- The online availability dates of Jaynes's drafts: I only know the draft used here carries a
  1995 copyright, and the note says only that.
- Which 1973 Tversky and Kahneman paper the author received (post does not say; no note).

## 6. Judgment calls

- L27 (the main note), Response paragraph 2, honest n.b.: that the anecdote does not show a
  difference between the schools. The post reports the claim ("someone said to me"), so I
  framed it as "The post takes its label from the other person's claim". A fair defender could
  say the post never asserts that frequentists answer 1/3; but it adopts the label on that
  basis and calls frequentist statements "mad blasphemy" (a joke, not noted).
- L51: the frequentist comparison. "Repeat Jaynes's picture" is my characterization; the
  support is the quoted preface. The Neyman–Pearson lemma is offered as information about
  frequentist method, not as a refutation of "no two of them agreed" (different frequentist
  procedures can give different answers; the note does not deny it).
- L81 clogic: "A cause stated as fact, with no evidence" for "because human beings are lazy".
  This is a claim about other people's motives in the post, not a motive reading by us.
- Not noted (nitpick): the quoted 1/2 reasoning calls P(she says "boy" | one of each) a
  "prior probability"; in Bayes's rule it is a likelihood. It has no effect on the answer.
- Reserved words: "wrong" and "invented" were flagged in drafts and removed. Pronoun flags left
  are for Martin Gardner (a historical figure) and for "His" in the other post's title.
- Length: honest section 511 words (limit "about 500"); summary 187 words, a little above 150,
  because the post has three strands.
