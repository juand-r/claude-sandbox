# Report: truly-part-of-you

## 1. The argument in three sentences

A belief you were only told, like "light is waves", is like a suggestively named token in
an old AI program (McDermott's critique): it connects to nothing, and you could not recover
it if it were deleted, except by asking again. The test is to ask "How would I regenerate
this knowledge if it were deleted from my mind?", with deeper deletions giving stricter
tests (re-proving the Pythagorean theorem, reinventing proof). Knowledge whose source you
hold can be adapted and extended (the shepherd's pebbles), so you should strive to be the
source of every thought worth thinking.

## 0. Skeleton note (tooling problem)

`src/new_post.py truly-part-of-you` failed: `src/md2tex.py` raises `IndexError` in
`Inline.restore`. Cause: footnote 2's link text contains Markdown-escaped underscores
(`out\_ of\_ the\_ matrix`); the outer `Inline` protects them as placeholders, then the link
text is converted by a fresh nested `Inline()` whose own store is empty, so it cannot restore
the outer placeholders. I did not edit `md2tex.py` (brief: do not edit other files). I built
the skeleton with a one-off script that runs `md2tex.convert` with all `Inline` objects
sharing one store (`data/sources/agent_b1_ewi_scs_tpy/mk_truly.py`). `check_verbatim.py`
printed OK (1197 words). The link prints its URL with the underscores as in the original.
The editor may want to fix `md2tex.py` the same way (share the store with the nested
converter).

## 2. Sources checked

- McDermott, "Artificial Intelligence Meets Natural Stupidity," SIGART Newsletter 57 (April
  1976), PDF from `http://www.cs.yorku.ca/~jarek/courses/ai/F11/naturalstupidity.pdf`, saved
  as `data/sources/mcdermott1976.pdf` and `mcdermott1976.txt` (pdftotext -layout; OCR has
  noise). Matched:
  - "A good test for the disciplined programmer is to try using gensyms in key places and
    see if he still admires his system. For example, if STATE-OF-MIND is renamed G1073; we
    might have: [diagram] which looks much more dubious." (page marked 5.)
  - "Communication between computer programs is under completely, different constraints.
    ... Instead, the whole problem is getting the hearer to notice what it has been told.
    (Not "understand", but "notice". To appeal to understanding at this low level will doom
    us to tail-chasing failure.) The new structure handed to the receiver should give it
    "permission" to make progress on its problem." The comma after "completely" looks like
    OCR noise; I quote it without the comma. The preceding paragraph is about human speakers
    ("The problem of a language speaker is to get the directed attention of an unprepared
    hearer ...").
  - "Wishful Mnemonics ... A major source of simple-mindedness in AI programs is the use of
    mnemonics like "UNDERSTAND" or "GOAL" to refer to programs and data structures." The
    STATE-OF-MIND / HAPPINESS network is on the same page.
- The post's figure (Cloudinary PNG, downloaded and viewed; saved as
  `data/sources/agent_b1_ewi_scs_tpy/truly_part_of_you_figure.png`): STATE-OF-MIND above
  HAPPINESS, joined by an arrow labelled IS-A.
- Rorty, "Out of the Matrix," Boston Globe, 5 October 2003, the URL in the post's footnote,
  fetched with curl; saved as `data/sources/rorty_globe_2003.html` and `.txt`. Matched:
  - "Take beavers, for example. If you believe that beavers live in deserts, are pure white
    in color, and weigh 300 pounds when adult, then you do not have any beliefs, true or
    false, about beavers. For you are using the word "beaver" in a way that has no connection
    with its ordinary use. What the rest of us mean by the word "beaver" is a function of our
    commonly held beliefs about beavers."
  - "One way to sum up this anti-Cartesian line of thought is to say that words acquire their
    meanings by being used in roughly similar ways by most speakers, not by being paired off
    with particular experiences or objects."
  - Rorty also quotes Wittgenstein, with "nothing else turns with it" (the post has "moves").
- Wittgenstein, Philosophical Investigations §271 (Anscombe translation), page at
  `https://topologicalmedialab.net/xinwei/classes/readings/Wittgenstein/pi_94-138_239-309.html`,
  saved as `data/sources/wittgenstein_pi_239-309.html` and `.txt`. Matched: "271. "Imagine a
  person whose memory could not retain what the word 'pain' meant -- so that he constantly
  called different things by that name -- but nevertheless used the word in a way fitting in
  with the usual symptoms and presuppositions of pain" -- in short he uses it as we all do.
  Here I should like to say: a wheel that can be turned though nothing else moves with it, is
  not part of the mechanism." The post's wording matches this translation.

## 3. Arithmetic

- 3-4 right triangle: hypotenuse sqrt(9 + 16) = 5 (no note relies on it).
- "Six weeks earlier": Cached Thoughts `Posted: 2007-10-11`, this post `Posted: 2007-11-21`:
  41 days, about six weeks.
- Artificial Addition `Posted: 2007-11-20`: the day before.

## 4. Claims about other posts

- `data/originals/cached-thoughts.md` (2007-10-11): "In modern civilization particularly, no
  one can think fast enough to think their own thoughts." and "No one can think fast enough to
  recapitulate the wisdom of a hunter-gatherer tribe in one lifetime, starting from scratch."
- `data/originals/artificial-addition.md` (2007-11-20): "pocket calculators work by storing a
  giant lookup table of arithmetical facts, entered manually by a team of expert Artificial
  Arithmeticians".
- `data/originals/the-simple-truth.md` (`Posted: 2008-01-01`, manifest order 49, the next
  essay): the shepherd drops "a pebble into a bucket" as each sheep leaves and takes one out
  as each returns; "the bucket already contained pebbles when I started; this, it turned out,
  was a bad idea." I said only that the shepherd comes from that essay and gave its LessWrong
  date. I did not check whether it was published elsewhere before this post.
- Consistency with `cached-thoughts` (our notes): its cpara on "In modern civilization
  particularly..." already makes the point that relying on others' conclusions is how
  knowledge works and that the post never says which to trust. My last cpara makes the
  corresponding point for this post (no rule for which thoughts to regenerate) briefly. Book
  order: this post is order 48, Cached Thoughts order 96, so by STANDARDS 2.5 the full
  version of this recurring criticism may belong here, not there. I made it briefly here, as
  the caller asked, and did not touch cached-thoughts. Editor to decide.

## 5. Items not verified

- Whether the beaver example is Davidson's own or Rorty's illustration. Davidson's "A
  Coherence Theory of Truth and Knowledge" (1983) was not fetched. The footnote cpara says I
  could not check it.
- "For what physicists mean by 'wave' is not 'little squiggly thing' but a purely
  mathematical concept": arguably overstated (a physical wave is a mathematical object with an
  observable interpretation), but I could not make this checkable in a short note and dropped
  it.
- The claim that telling an AI facts it cannot learn is "the terrible danger": context is
  symbolic AI; no note.

## 6. Judgment calls for the editor

1. McDermott cpara ("The McDermott sentence is about something else"): the matched context is
   above. A fair defender could say the principle carries over from programs to people.
   The note does not say it cannot; it says the post applies the sentence to the case the
   paper set apart. I did not use "misquotes" or "out of context".
2. Davidson cpara and Wittgenstein clogic: two notes on the same paragraph, with related
   points (the sources locate meaning in shared use, not in the believer's experience). I kept
   them separate because they concern two sources. The post's own claim is put as a question
   ("do you have enough experience to connect that belief to anything at all?"); the Response
   says "put as a question".
3. Reserved word "false" appears three times, always describing the content of the beaver
   beliefs in the example (they are false), not as a verdict on the post. "invented" appears
   once, paraphrasing the post's "reinvent".
4. Pythagorean cpara: "The fallback is much weaker than the question." The post itself
   concedes "harder to boast, without putting it to the test"; my note keeps that hedge and
   says only how much weaker the fallback is.
5. "The post describes no case in which the test was run and found a belief wanting." I read
   the whole post for one: the light-is-waves listener, the Pythagorean case and the proof
   question are hypotheticals or guesses.
6. Pronouns: "his head" refers to Wittgenstein's imagined man (the passage uses "he");
   McDermott is referred to by name or as "the paper".
