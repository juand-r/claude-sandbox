# Report: lotteries-a-waste-of-hope ("Lotteries: A Waste of Hope", Yudkowsky, posted 2007-04-13)

## 1. The argument in three sentences (written before annotating)

Defenders call a lottery ticket a rational purchase of a day's fantasy, but the fantasy is
of wealth with near-zero probability that the buyer can do nothing to bring about. It
therefore wastes hope: without the lottery, people might dream about things they could do
(school, a business, a promotion) and find a way to do them. People buy tickets because the
brain cannot scale a feeling down by a factor of 10^-8 and does not let the expected-utility
calculation override instinct; defending the bias instead of rejecting it is the error.

## 2. Sources checked (outside quotations and figures)

Saved in `data/sources/b2_lottery/`.

- Kahneman and Tversky (1979), "Prospect Theory", Econometrica 47:263-291, PDF from
  https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Behavioral_Decision_Theory/Kahneman_Tversky_1979_Prospect_theory.pdf
  (`kt1979.pdf`, `kt1979.txt`). Matched, p. 282: "The sharp drops or apparent
  discontinuities of π at the endpoints are consistent with the notion that there is a limit
  to how small a decision weight can be attached to an event, if it is given any weight at
  all." pp. 282-283: "Because people are limited in their ability to comprehend and evaluate
  extreme probabilities, highly unlikely events are either ignored or overweighted". p. 286:
  "In prospect theory, the overweighting of small probabilities favors both gambling and
  insurance". p. 283 (used in the Chance post): "π is relatively shallow in the open interval
  and changes abruptly near the end-points". (pdftotext renders π as "7T"/"Ir"; checked by
  context.)
- Oettingen and Mayer (2002), JPSP 83:1198-1212, PubMed abstract (PMID 12416922,
  `pubmed_12416922.txt`). Matched: "Positive expectations (judging a desired future as likely)
  predicted high effort and successful performance, but the reverse was true for positive
  fantasies (experiencing one's thoughts and mental images about a desired future
  positively). Participants were graduates looking for a job (Study 1), ..." Abstract only.
- Po Bronson, "How Not to Talk to Your Kids", New York, 9 February 2007
  (https://nymag.com/news/features/27840/, `bronson.html`, `bronson.txt`). Matched: "Of those
  praised for their effort, 90 percent chose the harder set of puzzles. Of those praised for
  their intelligence, a majority chose the easy test."
- Wikipedia "Powerball" and "Mega Millions", raw wikitext (`wp_Powerball.txt`,
  `wp_Mega_Millions.txt`). Powerball matrix table: "August 28, 2005 | 55 | 42 |
  1:146,107,961"; next change "January 7, 2009 | 59 | 39". Mega Millions: "The final 5/56 +
  1/46 Mega Millions drawing was held on October 18, 2013" (format from June 22, 2005).
  Price: Powerball "On January 15, 2012, the price of each basic Powerball play doubled to $2";
  Mega Millions "despite remaining a $1-per-play game" (2012). Draw days in 2007: "Powerball
  drawings were aired ... on Wednesday and Saturday ... with the Mega Millions drawings being
  aired Tue and Fri evenings".
- "Debiasing as Non-Self-Destruction" (the post's footnote 2), fetched with
  `src/fetch.py post XZWMeeqKmfMSPTLha` to `data/originals/debiasing-as-non-self-destruction.md`
  (not in the collection), Posted: 2007-04-07. Matched: "The great victories of debiasing are
  *exactly* the lottery tickets we didn't buy".

## 3. Arithmetic

- The post's factor 0.00000001 = 10^-8 = 1 in 100,000,000.
- Powerball, 5 of 55 plus 1 of 42 (Aug 2005 to Jan 2009): C(55,5) = 3,478,761; x 42 =
  146,107,962 combinations; P(jackpot) = 6.84e-9. Ratio 10^-8 / 6.84e-9 = 1.46.
- Mega Millions, 5 of 56 plus 1 of 46 (June 2005 to Oct 2013): C(56,5) = 3,819,816; x 46 =
  175,711,536; P = 5.69e-9. Ratio 1.76.
- So the post's factor is within a factor of two of both jackpot probabilities (and is larger
  than both, i.e. slightly generous to the ticket). No note on the discrepancy; the cpara
  states the real figures as confirming the order.
- No expected-value figure is given in the post. I did not compute a ticket's expected cash
  value because I could not reach a primary source for 2007 payout rates (Clotfelter and Cook
  1990, JEP, behind a Cloudflare challenge at pubs.aeaweb.org). The note on the expected-utility
  sentence therefore makes a logical point only (the anticipation term is what is in dispute).

## 4. Claims about other posts

- "Debiasing as Non-Self-Destruction" (footnote 2): see section 2.
- "Want to become stronger" alludes to "Tsuyoku Naritai" (2007-03-27); no note.
- The Chance post (2008-01-06) points back to "the Overcoming Bias lottery debate" and uses
  the same explanation; its K&T note points back to this post's note, where the full source is.

## 5. Items not verified

- The Economist-style defense and the commenters referred to in the first paragraph: only the
  one comment quoted in "New Improved Lottery" was checked (see that report).
- Oettingen and Mayer: abstract only. The note relies only on the abstract's summary sentence
  and its list of participants. Whether Study 1's job fantasies were about promotions or new
  jobs I do not know; the note says "a pleasant daydream about a promotion is not clearly" the
  productive alternative, which extends the finding by analogy. The editor may prefer "a
  pleasant daydream about a better job".
- "the people who play are the ones who can least afford to lose": framed by the post as "the
  classic criticism", not asserted; not checked.

## 6. Judgment calls for the editor

- Oettingen note. "does not support it" and "the reverse was true" (quoted) are the strongest
  words in the notes. The post's claim is hedged ("maybe", "might"), and the note does not say
  the post is false, only that the nearest research does not support the hedged suggestion.
  A fair defender could say: the post contrasts achievable dreams with lottery dreams, and
  Oettingen's work on "mental contrasting" (not read here) says fantasies help when joined to
  realistic expectations. I did not read that work, so I did not mention it.
- K&T note. It is credit plus "stated as fact, with no source". The post does not claim
  novelty, so I did not call it uncredited.
- Expected-utility note. A fair defender could say "financial instincts" means expected money,
  and the anticipation is a separate question. The note quotes nothing it does not use and says
  the calculation "would have to put a value on that anticipation", which holds for expected
  utility as the post names it.
- Step 3 note. The post does not name the defenders at step 3; the placement is by juxtaposition
  ("Coming right after the question about the lottery's defenders"). This is close to an
  inference; I stated the textual basis in the note.
- Dweck footnote note. "The post uses it for the value of effort" describes where the footnote
  is attached. It could be cut as a nitpick; I kept it because the reader otherwise cannot tell
  what the cited article is about.
- Honest edition: 424 words, 5 n.b. notes.
