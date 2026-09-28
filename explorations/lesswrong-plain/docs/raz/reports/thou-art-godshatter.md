# Report: thou-art-godshatter

## 1. The argument in three sentences

Natural selection favours only inclusive genetic fitness, yet humans do not want fitness as
such, and an agent that did (a consequentialist born with the concept of fitness and a
library of explicit strategies) is possible in principle. Evolution did not build one because
it cannot redesign a whole system at once: brains first evolved reinforcement learning on
short-range rewards (fat, sugar, sex) that correlated with reproduction, and when general
reasoning appeared it was put to work getting those existing rewards. So human values are a
"thousand shards of desire" splintered from evolution's one goal, and the author judges this a
good thing, since the alternative is a future of pure replicators.

## 2. Sources checked

Saved in `data/sources/batch3a/`.

- Britten (2002), PNAS 99: 13633-5, abstract from PubMed (PMID 12368483), file
  `pubmed_britten2002.txt`: "a better estimate would be that 95% of the base pairs are exactly
  shared between chimpanzee and human DNA ... there is an additional 3.4% difference due to
  the presence of indels." The post's "Chimpanzees share 95% of your genes" matches this figure
  for DNA sequence; "genes" is loose (it is base pairs). Below the number threshold, and the
  argument does not depend on it, so the note only names the source.
- Wikipedia, "Reciprocal altruism" (raw, `wp_Reciprocal_altruism.txt`): "Trivers ... year = 1971
  | title = The evolution of reciprocal altruism". Wikipedia, "Handicap principle"
  (`wp_Handicap_principle.txt`): "a hypothesis proposed by the Israeli biologist Amotz Zahavi in
  1975".
- Wikipedia, "Retina" (raw, `wp_Retina.txt`), section "Inverted versus non-inverted retina":
  "can generally come about as a consequence of two alternate processes - an advantageous
  "good" compromise between competing functional limitations, or as a historical maladaptive
  relic of the convoluted path of organ evolution and transformation." Also: "Although the
  inverted retina of vertebrates appears counter-intuitive, it is necessary for the proper
  functioning of the retina."
- Wikipedia, "The Mote in God's Eye" (raw): "Moties (other than the short-lived, sterile
  Mediators) must become pregnant periodically or die. This inevitably results in
  overpopulation ... and civilization-ending wars." Novel 1974.
- Godshatter as Vinge's word: Wikipedia's "A Fire Upon the Deep" does not use the word. Found
  in a review, https://strangematterscifi.substack.com/p/review-a-fire-upon-the-deep-by-vernor
  (`strangematter_fire.html`): "When the Straumli Blight murders Old One, it crams as much of
  its knowledge into Pham's tiny mind than he can handle. At once empowered and debilitated by
  his "godshatter,"". Novel date 1992 from Wikipedia (`wp_A_Fire_Upon_the_Deep.txt`). I have
  not seen the novel's text; the note says "as one review describes it".

## 3. Arithmetic

- "less than two centuries since ... natural selection": Darwin and Wallace 1858, post 2007,
  149 years. No note.
- Chimpanzee: 95% (Britten) vs the post's 95%: same number.
- Sibling relatedness 1/2: standard coefficient for full siblings; the post's gloss ("any
  variations ... 50% likely to be shared") is the identity-by-descent reading. No note.

## 4. Claims about other posts

- "as was discussed yesterday": `data/originals/protein-reinforcement-and-dna-consequentialism.md`
  (fetched this session with `src/fetch.py post gTNB9CQd5hnbkMxAG`). Not in the manifest. Its
  postedAt is 2007-11-13T01:34:25Z; Godshatter's is 2007-11-13T19:38:56Z, so both have the same
  Posted date and "yesterday" is off by the database's reckoning (likely a time-zone matter, or
  the original Overcoming Bias dates). Nitpick; no note. The note says "(November 2007)".
- "Evolutionary Psychology" (order 141, `data/originals/evolutionary-psychology.md`) uses the
  ironic "Evolution-of-Birds Fairy" and "Evolution-of-Humans Fairy". Matched.
- "An Alien God" (order 133): "The human retina is constructed backward ... Hence the blind
  spot. To a human engineer, this looks simply stupid". The retina example is made in full
  there first. See judgment call 3.
- "Evolutions Are Stupid (But Work Anyway)" (order 135): title only.
- "Adaptation-Executers, not Fitness-Maximizers" (order 140): its epigraph quotes Tooby and
  Cosmides, "Individual organisms are best thought of as adaptation-executers rather than as
  fitness-maximizers." Used in the Response as credit.
- "The Logical Fallacy of Generalization from Fictional Evidence" (order 100): the post's link
  on "depicts" points to it (URL lw/k9/the_logical_fallacy_of_generalization_from).

## 5. Items not verified

- The Mote in God's Eye: only Wikipedia's summary. Whether the novel frames the Moties'
  breeding as evolution making them fitness maximizers is not checked; the note says so.
- Vinge's coinage: from a review, not the novel.
- "Only in the last century ... have evolutionary biologists really begun to understand"
  reciprocal altruism and costly signalling: dates checked on Wikipedia only.
- Hamilton (1964) as the origin of "inclusive fitness", which would confirm "Before the 20th
  century": not checked; no note relies on it.

## 6. Judgment calls for the editor

1. Reserved words: none used.
2. The cpara on "When hominid brains ..." says the explanation "is an inference from what
   selection could easily find, stated as history without a hedge" and that the post gives no
   evidence beyond it. A fair defender may say that any evolutionary explanation of this kind
   is an inference. The note does not call it wrong; the Response says it "may well be right".
   Consider softening if it reads as faulting the post for not doing palaeontology.
3. Retina: the example is made in full in "An Alien God" (order 133, another agent). My note
   points there and adds the dispute from Wikipedia. If the An Alien God note makes the dispute
   point in full, this note should shrink to a pointer (STANDARDS 2.5).
4. The "So what?" note calls it "a position" with "no argument for it here". A fair defender
   might say the Genetic Fallacy point was made earlier in the book; that post is about beliefs,
   not values, so I did not point to it.
5. The Vinge title note is information, not a fault. It could be cut as a naming nitpick; I
   kept it because the word is the title and the post never explains it.
6. I considered and dropped: a note on "within each species ... purely obsessed with inclusive
   genetic fitness" (meiotic drive is an exception, and "Evolving to Extinction", order 137,
   discusses such cases) as too technical for the argument; Robert Frank's commitment argument
   that non-calculating emotions can beat pure calculation, as my own speculative objection
   against the "in principle" claim; Dawkins/Pinker precedents for "rebelling against the
   genes", not checked verbatim and not needed.
