# Report: the-hidden-complexity-of-wishes ("The Hidden Complexity of Wishes", Yudkowsky, posted 2007-11-24; preface added May 2024)

## 1. The argument in three sentences (written before annotating)

A device that makes any specified outcome happen (the Outcome Pump) will satisfy a wish such
as "get my mother out of the burning building" by paths no human helper would consider, such as
exploding the building, because humans never generate plans they rank very low. Patching the
wish case by case turns it into an endless lookup table, since what you really want involves
your whole structure of values (life, health, state of mind, the dog, and so on), which is finite
but large. So there is no safe wish smaller than an entire human morality: a genie is safe only
if it shares your values, and then wishing is superfluous.

## 2. Sources checked

Local copies in `data/sources/b3a_wishes/`.

1. Wade, M. J. (1976), "Group selections among laboratory populations of Tribolium", PNAS
   73(12):4604-4607. Abstract only, from PubMed efetch
   (https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=1070012&rettype=abstract&retmode=text;
   `wade1976_abstract.txt`). Matched: "Group selection for both increased and decreased adult
   population size was carried out among laboratory populations of Tribolium castaneum";
   "\"Assay\" experiments indicated that selective changes in fecundity, developmental time, body
   weight, and cannibalism rates were responsible in part for the observed treatment differences
   in adult population size." The full text (PMC431563) was behind a captcha or returned HTML
   from every route I tried (PMC, Europe PMC render, NCBI CDN, PNAS).
2. Allee, Emerson, Park, Park and Schmidt (1949), Principles of Animal Ecology, full text from
   archive.org (https://archive.org/download/principlesofanim00alle/principlesofanim00alle_djvu.txt;
   `allee1949_djvu.txt`, lines 48430-48460). Matched: "An experimental demonstration of canni-
   balism in relation to densitv is afforded by studies of the flour beetle Tribolium confu-
   sum. Chapman (1928) pointed out that adult beetles eat their own eggs— a coac- tion of some
   importance in regulating the upper limits of population growth of the colony." The running
   head "POPULATION FACTORS AND SELECTED POPULATION PROBLEMS 371" follows a few lines later, so
   the quoted words are on p. 370. The same passage: "later observations by Stanley (1942) and
   Boyce (1946) suggest that females may be more cannibalistic than males" (cannibalism by
   females, not of females; not used).
3. Wiener (1960), quoted via Wikipedia "AI alignment", raw wikitext
   (https://en.wikipedia.org/w/index.php?title=AI_alignment&action=raw; `wiki_ai_alignment.txt`,
   line 32): "If we use, to achieve our purposes, a mechanical agency with whose operation we
   cannot interfere effectively [...] we had better be quite sure that the purpose put into the
   machine is the purpose which we really desire." Cited as Science 131:1355-1358, 6 May 1960.
   The primary source was not read (paywalled); the note says "as quoted in Wikipedia".
4. Taylor, J., "Quantilizers: A Safer Alternative to Maximizers for Limited Optimization"
   (https://intelligence.org/files/QuantilizersSaferAlternative.pdf; `taylor_quantilizers.pdf`,
   `t2.txt`). Matched: "Given that utility maximization can have many unintended side effects,
   Armstrong, Sandberg, and Bostrom [12] and others have suggested designing systems that
   perform some sort of \"limited optimization,\""; "Expected utility quantilization is not a
   silver bullet." Date: MIRI announced it at https://intelligence.org/2015/11/29/new-paper-quantilizers/
   (URL date; found by search); presented at the AAAI 2016 workshop. The note says 2015.
5. Post's own quotation "as high as possible": "This way you can get an outcome that tends to be
   as high as possible in the future function".
6. Open-Source Wish Project epigraph: links go to web.archive.org, which is blocked from this
   environment. Not checked; the note says so.

## 3. Arithmetic

- Coin: survival weight of an outcome is P(outcome) x (1 - reset probability). Heads: 0.5 x 0.01
  = 0.005; tails: 0.5 x 0.99 = 0.495. Ratio tails:heads = 99:1, as the post says.
- Money: reset 99.999999% for $10 leaves 1e-8; 99.99999% for $100 leaves 1e-7; ten times the
  weight for the larger amount, consistent with "diminished as the amount of money increased".
- Preface date: post 24 November 2007, preface May 2024: 16 years 5-6 months, "sixteen and a
  half years".

## 4. Claims about other posts

- "The Tragedy of Group Selectionism" (data/originals/the-tragedy-of-group-selectionism.md,
  posted 2007-11-07): contains "No; the adults adapted to cannibalize eggs and larvae, especially
  female larvae." and names "Vero Wynne-Edwards, Warder Allee, and J. L. Brereton".
- "Artificial Addition", posted 2007-11-20 (manifest); the note only describes its topic.
- "Anthropomorphic Optimism" (2008-08-04) tells the group-selection story again; checked.
- "Lost Purposes" (next day) links this post as "wish to the genie of an imagined AI"; not used
  in a note (the preface's "literally" makes it no contradiction).

## 5. Not verified

- The Wade paper's full text, hence the source of "especially of immature females" (also in The
  Tragedy of Group Selectionism, order 138, not yet annotated).
- The Open-Source Wish Project wording (archived pages unreachable).
- Wiener's primary text (via Wikipedia only).
- "Terry Schiavo" is spelled "Terri" in the usual sources; a spelling slip, not noted (STANDARDS 2.4).
- The stray "<" line after the preface is in LessWrong's text; given no note.

## 6. Judgment calls

1. Group selection: the full treatment belongs at "The Tragedy of Group Selectionism" (order 138),
   the first occurrence in book order, which no one has annotated yet. I made the two points (Wade's
   abstract; Allee's textbook) in full here, the first of my posts, and point back from
   "Anthropomorphic Optimism". When 138 is done, the editor may want to move the full notes there
   and leave pointers here.
2. Allee note: "sits uneasily with" (not "contradicts"). The textbook shows Allee's school knew
   egg cannibalism as density regulation; it does not show that they considered it as a product
   of group selection, and the note says so. Allee was first of five authors; the Tribolium
   section is probably Park's (not checked); the note says "with Allee as first author".
3. The thesis note ("argument covers maximizing genies; the claim covers all of them") uses a
   later MIRI proposal only to show the case the post leaves out, not as a refutation; Taylor
   herself says it is "not a silver bullet". A fair defender might say the window-fall patch
   already shows a non-maximizing failure. The window case is still a patched maximizer of
   distance, so I kept the note.
4. Wiener credit: prior work that supports the post, given as credit (Book II lesson), with
   the post's addition stated.
5. Reserved words: none used as verdicts. "never" was removed from two paraphrases.
