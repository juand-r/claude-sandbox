# Report: but-there-s-still-a-chance-right ("But There's Still A Chance, Right?", Yudkowsky, posted 2008-01-06)

## 1. The argument in three sentences (written before annotating)

A man who doubted evolution, told that the odds against chance similarity of human and
chimpanzee DNA were 2^750,000,000 to one, replied "But there's still a chance, right?"; the
author concedes the figure was unsourced and overconfident, but finds the reply revealing.
It shows intuition treating "no chance" and "a tiny chance" as different in kind, because no
feeling is small enough to represent a tiny probability (which is also why people buy
lottery tickets), and treating any uncertain argument as one that may be ignored. But if you
may not ignore a certain disproof, you may not ignore a one-in-a-googol likelihood, or one of
0.9, just because you want to.

## 2. Sources checked (outside quotations and figures)

Saved in `data/sources/b2_lottery/`.

- Britten (2002), PNAS 99:13633-13635, PubMed abstract (PMID 12368483, `pubmed_12368483.txt`).
  Matched: "Five chimpanzee bacterial artificial chromosome (BAC) sequences ... have been
  compared with the best matching regions of the human genome sequence"; "the old saw that we
  share 98.5% of our DNA sequence with chimpanzee is probably in error. For this sample, a
  better estimate would be that 95% of the base pairs are exactly shared"; "In this sample of
  779 kb, the divergence due to base substitution is 1.4%, and there is an additional 3.4%
  difference due to the presence of indels"; "They occur equally in repeated and nonrepeated
  sequences".
- Chimpanzee Sequencing and Analysis Consortium (2005), Nature 437:69-87, full text from
  https://www.nature.com/articles/nature04072 (`nature04072.html`, `nature04072.txt`).
  Matched: "Single-nucleotide substitutions occur at a mean rate of 1.23% between copies of the
  human and chimpanzee genome, with 1.06% or less corresponding to fixed divergence between the
  species"; "Insertion and deletion (indel) events are fewer in number than single-nucleotide
  substitutions, but result in ∼1.5% of the euchromatic sequence in each species being
  lineage-specific."
- International Human Genome Sequencing Consortium (2004), Nature 431:931-945, PubMed abstract
  (PMID 15496913, `pubmed_15496913.txt`): "2.85 billion nucleotides"; "the human genome seems
  to encode only 20,000-25,000 protein-coding genes." (Used for arithmetic only; see 3 and 6.)
- Kahneman and Tversky (1979), p. 283: "π is relatively shallow in the open interval and
  changes abruptly near the end-points where π(0) = 0 and π(1) = 1." See the Lotteries report
  for the file.

## 3. Arithmetic

- 2^750,000,000 = 10^(750,000,000 x 0.30103) = about 10^225,772,497.
- Naive chance model (my own check of "probably the right meta-order of magnitude"; not in any
  note): two random sequences of N aligned bases matching at a fraction f of sites, each site
  matching with probability 1/4. log2 P = N [H(f) + f log2(1/4) + (1-f) log2(3/4)], with H the
  binary entropy. For f = 0.98: H = 0.1414, so the bracket is 0.1414 - 1.96 - 0.0083 = -1.827
  bits per site. With N = 2.85e9 (IHGSC 2004), -log2 P = 5.2e9; with N = 3e9, 5.5e9. For
  f = 0.95: 1.634 bits per site, 4.7e9 to 4.9e9. So under this model the exponent is about
  5e9, about 7 times the post's 7.5e8: the same meta-order of magnitude (log10 of the exponents
  8.9 against 9.7). The post's hedge "probably the right meta-order of magnitude" survives.
- If only coding sequence were counted (about 1.5% of 2.85e9 = 4.3e7 bases), the exponent
  would be about 1.83 x 4.3e7 = 7.8e7, one meta-order below 7.5e8. So the post's conditional
  ("in which case it's the wrong meta-order of magnitude") is correct as a conditional; the
  note says only that its antecedent does not hold.
- Possible origin of 750,000,000 (speculation, not in any note): 3e9 bases x 2 bits / 8 = 7.5e8
  bytes, the usual "750 megabytes" for the genome. The author says the source is forgotten.
- "30,000 known genes": the 2004 finished sequence gave 20,000-25,000 protein-coding genes.
  The post's figure is 20-50% high, but it sits inside a hedged conditional and does not
  affect the argument, so it is here and not in a note (STANDARDS 2.4, numbers).
- Googol = 10^100.

## 4. Claims about other posts

- "The Fallacy of Gray" (next day, 2008-01-07) uses this anecdote. Our existing note there
  (original 52, harsher standard) says: "The case does not survive a look at its source ...
  The man was answering a number the author could not source. His reply is one sentence. That
  'all probabilities, to him, were simply uncertain' is the author's reading of that sentence".
  My notes agree on the facts: the post concedes the figure is unsourced (credited here as the
  post's own concession), and the "certain vs uncertain" rule is "the author's reading of one
  reply". Book order: this post is 57, Fallacy of Gray 58, so by STANDARDS 2.5 the full point
  now sits here; the Fallacy of Gray note could become a short pointer in the whole-book pass,
  and its "does not survive" wording may be harsher than section 2 allows (the post itself
  disclosed the problem). I did not edit it.
- "Lotteries: A Waste of Hope" (the "Overcoming Bias lottery debate"): the K&T pointer in
  paragraph 8's note refers to the full note there.

## 5. Items not verified

- The conversation itself (anecdote).
- "the shared genes estimate was revised to 95%": matches Britten 2002; the note relies on it.

## 6. Judgment calls for the editor

- Four one-line paragraphs (the three dialogue lines after the first, and "But I think the
  other guy's reply is still pretty funny.") have no \cpara: 13 paragraphs, 9 \cpara notes. The
  first dialogue paragraph's note covers the whole exchange. I judged them not substantial
  (review log, batch 1, on the density of notes on dialogue lines in The Simple Truth). Add
  one-line notes if the audit count must match.
- DNA note ("The case in the conditional does not arise"). The post hedges with "may even";
  the note answers the hedge with a fact rather than calling the post wrong.
- "Both are real faults, and the post names them itself": credit, kept because leaving it out
  would make the Fallacy of Gray criticism look like something the author hid.
- The neuron note may be a nitpick. It is short; cut if needed.
- "Kahneman and Tversky described it in 1979": their subject is decision weights in choices
  between gambles, the post's is intuitive "chances". I changed the note, the Response
  and the n.b. to "described something close".
- Honest edition: 395 words, 3 n.b. notes.

## 7. Process notes (all four posts)

- Early in the session I wrote one file (`m1.txt`) and three PNGs (`lot-*.png`) into the main
  session's scratchpad before noticing the brief's rule. The PNGs are moved to
  `data/sources/b2_lottery/png/`. `m1.txt` there now has a later timestamp (22:37) than my
  write and different content, so another agent wrote it after me; I do not know whether a
  file of that name existed before my write. If the main session had an `m1.txt` of its own
  from before about 22:20 UTC, it may have been overwritten by me. Subagents share that
  scratchpad path, which makes such collisions likely.
- Notes were first inserted by `data/sources/b2_lottery/scripts/insert.py` from the lists
  `notes_*.py` into copies of the skeletons in `skel/`, then revised by exact replacements; the
  post files, not those lists, are current.
