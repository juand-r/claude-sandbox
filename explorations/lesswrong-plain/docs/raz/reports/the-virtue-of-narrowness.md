# Report: the-virtue-of-narrowness

## 1. The argument in three sentences

People who know a field draw fine distinctions within it, but outside their fields they often
stretch words as wide as they will go, because broad words and general theories sound loftier.
The post argues, by a parable of pebbles called diamonds and by examples ("evolution",
"Everything is connected", Newton), that useful categories and hypotheses must exclude
something: a graph with every edge says no more than a graph with none. Sneering at narrowness
recalls Plato's contempt for learning by looking; rationalists and poets alike need narrow
words, and over-broad words give something neither true nor poetic.

## 2. Sources checked

All saved in `data/sources/raz_b2b_narrow/` unless noted.

- Epigraph: `data/originals/twelve-virtues-of-rationality.md` line 32 (tenth virtue,
  precision): "What is true of one apple may not be true of another apple; thus more can be
  said about a single apple than about all the apples in the world." Exact match.
- "Stellar evolution": Wikipedia, https://en.wikipedia.org/w/index.php?title=Stellar_evolution&action=raw
  (`wiki_Stellar_evolution.txt`): "'''Stellar evolution''' is the process by which a [[star]]
  changes over the course of time." (Secondary source; the term is standard in astronomy.)
- Merriam-Webster, "evolution" (`data/sources/mw_evolution.txt`, fetched by an earlier agent):
  sense 2a "a process of change in a certain direction : unfolding". Matched verbatim.
- Online Etymology Dictionary, https://www.etymonline.com/word/evolution
  (`etym_evolution.txt`): "evolution (n.) 1620s, "an opening of what was rolled up," ... Modern
  use in biology, of species, first attested 1832 in works of Scottish geologist Charles
  Lyell." The note says "dates the word in English to the 1620s and its use for the development
  of species to 1832." (Earlier draft cited MW's "1616", which MW gives for sense 6, military
  movements; replaced by etymonline.)
- Plato, Republic VII 529a-c:
  - Jowett, Project Gutenberg #1497 (`data/sources/b2_lottery/plato_republic_jowett_pg1497.txt`,
    lines 19586-19614): "And I dare say that if a person were to throw his head back and study
    the fretted ceiling ...". Different wording from the post.
  - Shorey (Loeb), Perseus, https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.01.0168%3Abook%3D7%3Asection%3D529b
    (`shorey_529.html`): "for apparently if anyone with back-thrown head should learn something
    by staring at decorations on a ceiling ...". Different wording. Shorey's footnote 1: "The
    humorous exaggeration of the language reflects Plato's exasperation at the sentimentalists
    who prefer star-gazing to mathematical science." Quoted in the note (words matched).
  - The post's translation could not be identified (web searches for "staring at the varied
    patterns on a ceiling" and "floating on his back on land or on sea" found nothing). The
    sense matches both translations. Context (Glaucon's praise of astronomy, Socrates' reply)
    from Jowett lines 19586-19614.
  - Neither translation mentions labor or slaves (checked the passage).
- Popper pointer: our notes on `your-strength-as-a-rationalist` (book order 27; the earliest
  post in book order where our notes say "The principle is Karl Popper's, uncredited").

## 3. Arithmetic

None beyond the graph claim. Check: the complete graph K_n is the complement of the empty
graph on n vertices; complementation is a bijection on labelled graphs, so the two carry the
same information. The post's claim is correct; the note says so.

## 4. Claims about other posts

- "Twelve Virtues of Rationality" (Posted: 2006-01-01), tenth virtue, precision: quoted above.
- "Your Strength as a Rationalist" (2007-08-11), our note: "The principle is Karl Popper's,
  uncredited." My note points there (STANDARDS 2.5, recurring criticism made once). This post
  (2007-08-07) predates it by date but comes later in book order (98 vs 27).
- I checked `data/originals/entangled-truths-contagious-lies.md` for a possible clash with
  "Everything is connected": that post (2008) distinguishes noticeable entanglements ("the
  list of *noticeable* entanglements is much shorter, and it gives you something like a
  network"), which agrees with this post. No note.

## 5. Items not verified

- The translator of the Plato passage (see above).
- Who actually uses "evolution" to cover stars, life and technology as one process. The post
  names no one; I did not look for a target (Kurzweil's "six epochs" might be one), since the
  note only says the post names no one.

## 6. Judgment calls for the editor

1. Parable note (P3) and Response: "the parable decides the question in advance ... wrong by
   construction". "Wrong" refers to the parable's characters, not to the author. Fair
   defender: "a parable illustrates, it does not argue." My reply: the post offers no other
   test of which category is right, so the stipulation is where the argument would have to be.
2. Newton note: "its achievement was a new connection", set against the post's "subtracting
   edges" two paragraphs earlier. Fair defender: "Newton also excluded money and blood, which is
   my point." The note grants this ("It excludes money and blood, as the post says") and
   claims only that the example shows joining matters as well as excluding.
3. Evolution note: "The post names no one who reasons from the shared word". Fair defender 4
   (essays need not name targets) is a risk. I kept it because the example's force depends on
   someone reasoning that way, and the second half (standard usage, older general sense) is
   sourced.
4. Last-paragraph note: "isn't true" versus the graph argument's "totally useless". This reads
   the post's closing flourish literally; fair defender 3 (figure of speech) is possible. I
   kept it as the closing sentence states it as a claim.
5. Considered and dropped: (a) "panther" is itself a broad word (leopard, cougar, jaguar;
   genus Panthera includes lions): nitpick, 2.4(2). (b) Newton did write on money as Master
   of the Mint: takes the example too literally. (c) Scholarly work on technological evolution
   (e.g. Basalla 1988): not fetched, and not needed.
6. Pronoun flag: "His complaint" refers to Socrates (historical figure), kept.

## Checks

- check_verbatim: OK. raz_check: run, every flag read (see section 6). audit: OK.
- `annotated/preview.sh posts the-virtue-of-narrowness` builds (build-preview/the-virtue-of-narrowness.pdf).
- `annotated/notes/the-virtue-of-narrowness.json` not exported (brief did not ask; editor may run notes_backup.py export).
