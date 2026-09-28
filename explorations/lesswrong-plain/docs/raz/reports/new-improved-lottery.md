# Report: new-improved-lottery ("New Improved Lottery", Yudkowsky, posted 2007-04-13)

## 1. The argument in three sentences (written before annotating)

Answering a commenter who said a ticket turns zero chance into epsilon chance, the post says
the difference is only of order epsilon. If a lottery really sold epsilon hope, a better
product would be a one-dollar ticket that pays out at a random time about every five years,
with live odds on a phone screen; the satire shows how such hope would displace work and
better dreams. Governments sell weekly draws instead because they want to overcharge, so if
the lottery is a service, it is an overpriced one, charged to the poor.

## 2. Sources checked (outside quotations and figures)

Saved in `data/sources/b2_lottery/`.

- The comment quoted by the post, fetched from the LessWrong GraphQL API (comments on post
  vYsuM8cpuRgZS5rYB, view postCommentsOld; `lw_lotteries_comments.json`). The comment with
  legacyId 18216, posted 2007-04-13T16:46:40Z, author not returned by the API, reads in full:
  "There is a big difference between zero chance of becoming wealthy, and epsilon. Buying a
  ticket allows your dream of riches to bridge that gap. / I'm not a fan of lotteries, but I
  don't understand how you can apply the rubric "bias" to their value, since nobody can measure
  the value of entertainment or distant hope for another. Just measuring the expected cash value
  is ridiculously reductive. / BTW, ..." The post's link says ".../e1u"; e1u in base 36 is
  18210, not 18216, so I matched by text, not by id. The first two sentences match the post's
  quotation exactly. In the note I wrote `bias' for the comment's "bias" (nested quotes).
- A comment the same day (legacyId 18221, 2007-04-13T23:05:40Z, author not returned) already
  proposes the design: "let there be a lottery with one expected payout every five years,
  awarded at a Poisson-random time. You buy in once, and lo, at any minute you could receive a
  phone call saying you're a millionaire!" It is probably the author's (the wording matches the
  post and would explain "the aforesaid Poisson distribution"), but the API did not return an
  author, so I made no note.
- The Economist blog quotation ("daydreaming about becoming a millionaire for much less money
  than daydreaming about hollywood stars in movies"): economist.com returned 403 and a web
  search found no copy. Unchecked; no note relies on it.
- Wikipedia, "Premium Bonds", raw wikitext (`wp_Premium_Bonds.txt`). Matched: "'''Premium
  Bonds''' is a lottery bond scheme organised by the United Kingdom government since 1956";
  "The bonds are entered in a monthly prize draw and the government promises to buy them back,
  on request, for their original price"; "Numbers are entered in the draw each month, with an
  equal chance of winning, until the bond is cashed."
- Powerball and Mega Millions 2007 prices, matrices and draw days: see the Lotteries report.
  Mega Ball range in 2007 was 1 to 46 (5/56 + 1/46), so the post's "42 ... for the Mega Ball" is
  a valid number.

## 3. Arithmetic

- Ordinary lottery at the 2007 price: $1 a play, 2 draws a week (Powerball Wed/Sat; Mega
  Millions Tue/Fri). One ticket per draw of one game: 2 x 52 = $104 a year; x 5 years = $520.
  New Improved Lottery: $1 for one payout expected every 5 years. So the same span of "hope"
  costs about 520 times as much in the ordinary lottery. (If a draw's prize and number of
  players were the same, the chance per draw would be similar; the post's premise is that the
  product is the duration of hope, not the chance, so I compare durations.)
- "a hundred dollars ... a hundred times as large": 100 distinct combinations give 100 times
  the chance of one; correct.
- Waiting time: payouts at a random time with mean 5 years (radioactive decay) is a Poisson
  process with rate 0.2 per year, about 3.8e-7 per minute (1 / (5 x 525,960)); the per-minute
  chance is constant, which is what "at any minute" requires.
- "between zero ... and epsilon ... an order-of-epsilon difference": epsilon - 0 = epsilon;
  true by definition. Googolplex = 10^(10^100).
- "aforesaid Poisson distribution": "Poisson" does not occur earlier in the post (searched);
  the preceding paragraph describes a Poisson process without the word. Too small for a note.

## 4. Claims about other posts

- "Lotteries: A Waste of Hope", `data/originals/lotteries-a-waste-of-hope.md`, Posted
  2007-04-13 (same day). The notes say the satire's harm "is the claim of the previous post":
  that post's "It encourages people to invest their dreams ... into an infinitesimal
  probability. If not for the lottery, maybe they would fantasize about going to technical
  school ... hopes that would make them want to become stronger." The satire repeats "hopes of
  going to technical school". The Response says that claim was offered with "maybe" and
  "might": both words occur in that paragraph.

## 5. Items not verified

- The Economist quotation (see 2).
- "charged to the poorest members of society": not checked (Clotfelter and Cook, the standard
  source, was unreachable). No note relies on it.

## 6. Judgment calls for the editor

- Premium Bonds note. The post is satire, and a fair defender could answer "it was a joke"
  (STANDARDS 2.2.3). I kept the note because the post gives a factual reason ("Because they
  want to overcharge people") for a factual claim ("current governments ... don't offer this
  simple and obvious service"), and a government product with the post's key economic feature
  (one purchase, years of draws) has existed since 1956. The note states the differences
  (monthly draws, stake returned) so as not to overclaim. Cut it if it reads as a nitpick.
- The \$520 cpara is credit: on the post's premise the arithmetic supports "enormously
  overpriced".
- The note on paragraph 2 says the reply "assumes" that a daydream's worth should shrink with
  its probability. A fair defender might say that this is the author's considered normative
  view, argued elsewhere ("But There's Still A Chance, Right?", 2008, argues that feelings
  cannot track tiny probabilities; it does not argue that they should). I think "assumes" is
  accurate for this post.
- The comment note: the post links the comment, so "does not quote this part" is not a charge
  of hiding it; the added clause "its satire answers the price of hope, not whether its value
  can be judged by someone else" is the substantive point. It could be read as "does not
  answer"; the satire does answer a different question, so I said what it answers.
- Honest edition: 382 words, 5 n.b. notes.
