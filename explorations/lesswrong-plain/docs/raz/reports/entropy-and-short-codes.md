# Report: entropy-and-short-codes

## 1. The argument in three sentences

The entropy of a system, the sum of -p log2 p over its states, is the average number of
yes-or-no questions needed to learn its state, and a code that gives short words to
frequent states and long words to rare ones achieves it (1.75 questions for Y), while a
code that shortens a word without lengthening another cannot be decoded, so "short words
are a conserved resource." In an ideal code a message's length corresponds to its
probability, which is the Minimum Description Length or Minimum Message Length form of
Occam's razor, so the labels we give to concepts are not quite arbitrary, and the idea that
"you can X any way you like" obstructs learning to X wisely. Natural language shows the
pattern: basic-level categories such as "chair" are the level people talk at, and they
have shorter names than more specific or more general categories, because frequent use
goes with short words.

## 2. Sources checked

All saved in `data/sources/batch3b_entropy-and-short-codes/`.

- The post itself, from the LessWrong GraphQL API (`lw_soQX8yXLbKy7cFvy8.json`), to confirm
  the live text matches `data/originals`. No differences that matter.
- Wikipedia, "Kraft–McMillan inequality" (`wp_Kraft%E2%80%93McMillan_inequality.txt`,
  `?action=raw`): "gives a necessary and sufficient condition for the existence of a prefix
  code ... or a uniquely decodable code (in Brockway McMillan's version) for a given set of
  codeword lengths"; "If Kraft's inequality does not hold, the code is not uniquely
  decodable." Used for the note on "short words are a conserved resource."
- Wikipedia, "Shannon's source coding theorem" (`wp_Shannon%27s_source_coding_theorem.txt`):
  "the source coding theorem (Shannon 1948)"; optimal expected length satisfies
  "H(X)/log2 a ≤ E[S] < H(X)/log2 a + 1"; "it is possible to get the code rate arbitrarily
  close to the Shannon entropy". Used for the H to H + 1 bound and "Shannon's 1948 paper".
- Wikipedia, "Minimum message length" (`wp_Minimum_message_length.txt`): "It provides a
  formal information theory restatement of Occam's Razor" (link markup removed); invented by
  Wallace, "An information measure for classification" (Wallace and Boulton 1968).
  Wikipedia, "Minimum description length": "sometimes described as mathematical
  applications of Occam's razor"; Rissanen 1978. These confirm the post's MDL/MML sentence.
- Wikipedia, "Arbitrariness" (`wp_Arbitrariness.txt`): "Saussure introduced the notion of
  arbitrariness according to which there is no necessary connection between the material
  sign (or signifier) and the entity it refers to".
- Wikipedia, "Phonaesthetics" (`wp_Phonaesthetics.txt`; "Cellar door (phrase)" redirects
  there). Footnote quoting Tolkien, "English and Welsh" (1955), in Angles and Britons
  (1964), p. 36: "Most English-speaking people ... will admit that cellar door is
  'beautiful', especially if dissociated from its sense (and from its spelling)." I did not
  see Tolkien's text itself; the note says "as quoted by Wikipedia". The same article
  traces the phrase's reputation to a 1903 novel; I left that out as trivia.
- Rosch, Mervis, Gray, Johnson and Boyes-Braem (1976), "Basic objects in natural
  categories", Cognitive Psychology 8: 382-439. PDF:
  https://www.cns.nyu.edu/~msl/courses/2223/Readings/Rosch-CogPsych1976.pdf (`rosch1976.pdf`,
  `rosch1976.txt`, read with pdftotext). Matched:
  - abstract: members "(b) have motor programs which are similar to one another";
  - naming experiment: "Regardless of contrast sets, subjects overwhelmingly used the basic
    level name in this free-naming situation.";
  - frequency: "While word frequencies are not obtainable for the subordinate classes
    (because they are generally phrases, not single words), ... In nine of the 15 cases of
    superordinate-basic level comparison, the superordinate name actually had a higher word
    frequency than the basic level name";
  - I searched the text for "short", "syllable", "length": nothing on the length of basic
    names. Hence "does not test the claim about length".
- Wikipedia, "Brevity law" (`wp_Brevity_law.txt`): "the more frequently a word is used, the
  shorter that word tends to be"; "empirically verified for almost a thousand languages of
  80 different linguistic families" (Bentz and Ferrer-i-Cancho 2016). Wikipedia gives both
  1935 and 1945 for Zipf's first statement, so the note gives no year.
- Piantadosi, Tily and Gibson (2011), "Word lengths are optimized for efficient
  communication", PNAS 108: 3526-3529. Crossref abstract (`piantadosi2011_crossref.json`):
  "we show across 10 languages that average information content is a much better predictor
  of word length than frequency."

## 3. Arithmetic (script: `check_numbers.py`, output reproduced)

- H(X), 8 equally likely states: 3.0 bits. Code 100 is X4 (yes, no, no). Correct.
- H(Y) for 1/2, 1/4, 1/8, 1/8: 1.75. Average code length with 1, 01, 001, 000:
  0.5 + 0.5 + 0.375 + 0.375 = 1.75. Correct.
- log2(1/8) = -3; -(1/8)(-3) = 0.375. Correct.
- Kraft sum of the post's code: 1/2 + 1/4 + 1/8 + 1/8 = 1. With 10 for Y4:
  1/2 + 1/4 + 1/8 + 1/4 = 9/8 > 1, so no uniquely decodable code has these lengths.
- With 10 for Y4: Y4 Y2 = "10"+"01" = 1001, Y1 Y3 = "1"+"001" = 1001. Correct.
- Ideal lengths -log2 p: 1, 2, 3, 3 (the post's code is exactly ideal, since all
  probabilities are powers of 1/2).
- Non-dyadic example for the note: three equally likely states, H = log2 3 = 1.585;
  Huffman code 0, 10, 11 averages (1 + 2 + 2)/3 = 1.667.
- Syllables: re-clin-er 3, chair 1, fur-ni-ture 3. The post's "fewer syllables" holds.
- No correction to any figure in the post.

## 4. Claims about other posts

- "Occam's Razor" (`data/originals/occam-s-razor.md`): "“Witch,” itself, is a label for
  some extraordinary assertions—just because we all know what it means doesn't mean the
  concept is simple." Also its MML paragraph ("The Minimum Message Length formalism is
  nearly equivalent to Solomonoff induction"), for "The author described it". Our notes on
  that post (order earlier in the book) discuss Solomonoff and MML and the choice of
  machine; I did not repeat any of that here.
- "37 Ways That Words Can Be Wrong" (`data/originals/37-ways-that-words-can-be-wrong.md`),
  item 31, which cites this post: "You use a short word for something that you won't need
  to describe often ... This can result in inefficient thinking, or even misapplications of
  Occam's Razor, if your mind thinks that short sentences sound "simpler"."
- The Response says "The author kept them apart in 'Occam's Razor' ... and again in '37
  Ways'". Occam's Razor (2007) is earlier; 37 Ways (6 March 2008) is later. Both are
  described with the matched words above.
- The link on "carving reality at its joints" points to "Where to Draw the Boundary?"
  (order 175), which I read; the cpara says only that the argument for definitions was
  made in the preceding posts.

## 5. Not verified

- The Hofstadter attribution ("there's a reason why the English language uses 'the' to
  mean 'the' ..."). One web search found nothing. The note only says "attributed to"; it is
  a joke and nothing depends on it.
- Tolkien's lecture text itself (only Wikipedia's quotation of it).
- Whether "recliner" and "furniture" are less frequent than "chair" in a corpus. Not needed:
  no note relies on it.

## 6. Judgment calls

1. The cpara on "And so even the labels..." (two probabilities: frequency of use against
   probability of a hypothesis), repeated in the Response and the "In short" line and in one
   honest n.b. This is the one critical point of the post. A fair defender could say the
   previous paragraph already says "things that you'll need to say frequently", so the post
   is clear that word length follows use. My reply: the paragraph between them ties the
   same "its probability" to MDL as Occam's razor, and the author's own later list (37 Ways,
   item 31) names exactly this confusion and cites this post. If the editor thinks this is
   too fine for the "In short" line, the line could end at "better supported than its one
   example shows".
2. The clogic "Not arbitrary in length" (Saussure). It is information more than a fault:
   the post says "not quite arbitrary" and means length, which is correct. I kept it because
   the post also calls the sensible-sounding claim an obstacle, and a reader may think
   linguists' arbitrariness is refuted. Could be cut if judged a nitpick.
3. The clogic "Loosely worded" (length follows log of probability). Mild; kept because it is
   the post's key technical sentence and the exact relation is what the next post uses.
4. The cfact on Rosch's word-frequency finding. It complicates, and does not refute, the
   post's "Frequent use goes along with short words" as applied to basic-level names. I
   used "less direct", not a reserved word.
5. No reserved words (STANDARDS 2.3) are used. No motive readings.
6. Honest section is 517 words by the checker's count, a little over "about 500".
