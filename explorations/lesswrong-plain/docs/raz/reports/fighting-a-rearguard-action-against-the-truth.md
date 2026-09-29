# Report: fighting-a-rearguard-action-against-the-truth ("Fighting a Rearguard Action Against the Truth", Yudkowsky, posted 2008-09-24)

## 1. The argument in three sentences (written before annotating)

By 2001 the young Eliezer had added Friendly AI to his plans only as a contingency for "the
unlikely event that life turns out to be meaningless", which let him admit his old mistake
by small degrees instead of all at once. Because no single shock arrived, he patched the
justifications of his old strategy (rush to build AI, openness, coding as soon as money
came) instead of stopping and rethinking everything, as a broken foundational assumption
demands. The lesson is that admitting one large mistake is more efficient than admitting
many small ones, since each small admission lets the old plan repair itself.

## 2. Sources checked (outside quotations and figures)

Scratch and source files: `data/sources/batch6a_fighting-a-rearguard/` (shared by my three
posts). Helper script `annotate.py` there inserts notes into a pristine copy of the skeleton
(`skel/`); notes are in `notes_rearguard.py`.

**Yudkowsky, *Creating Friendly AI 1.0* (2001).** https://intelligence.org/files/CFAI.pdf,
saved as `CFAI.pdf` / `CFAI.txt` (pdftotext -layout). Matched:
- "Today, however, I regard objective morality as simply being one of the possibilities, with philosophically valid differential desirabilities possible even in the absence of objective morality." (lines 6797-6799; spans line breaks; "diﬀerential" uses the ff ligature in the PDF.)
- Table of contents: "6.2.1   Regulation (−)", "6.2.2   Relinquishment (−)".
- "In other words, I simply do not believe the claim that relinquishment is possible." (line 8284)
- Searched for "unlikely event", "life is meaningless", "life turns out", "contingency": the phrase "the unlikely event that life turns out to be meaningless" is not in CFAI. The note says only that I could not trace it.

**Ben Garfinkel, "On Deference and Yudkowsky's AI Risk Estimates", EA Forum, 19 June 2022.**
https://forum.effectivealtruism.org/posts/NBgpPaz5vYe3tH4ga/on-deference-and-yudkowsky-s-ai-risk-estimates
(curl; `garfinkel_deference.html/.txt`). Matched: "In 2001, and possibly later, Yudkowsky apparently believed that his small team would be able to develop a “final stage AI” that would “reach transhumanity sometime between 2005 and 2020, probably around 2008 or 2010.”" The word "2001" links to https://web.archive.org/web/20020124071714/http://www.singinst.org/intro.html. web.archive.org reset every connection in this session (proxy log: ws_closed_mid_exchange), so the archived page itself is unchecked; the note says so. I cite Garfinkel only for the quotation, not for his assessments.

**Nina Byers, "Fermi and Szilard", arXiv physics/0207094.** https://arxiv.org/html/physics/0207094
(`byers_fermi_szilard.txt`). Matched: "An early disagreement between Fermi and Szilard was over keeping their work secret. Fermi was opposed to secrecy and censorship." and "However, Szilard had prevailed on the secrecy issue in the early days and publication of results of uranium studies were postponed until after the war." Also read Wikipedia "Leo Szilard" (raw; `wp_szilard.txt`) for background (Szilard's secret Admiralty patent), not quoted.

**John Moore, *Slay and Rescue*.** The book exists (Goodreads, Google Books via search), but the quoted line could not be found in any searchable text. Not mentioned as unverified in the note, because the note makes no claim about it; the cpara only describes the line as a joke.

## 3. Arithmetic

- "sixteen days later": post 2008-09-24, "Crisis of Faith" 2008-10-10 (Posted: lines of both originals). 24 Sept + 16 = 10 Oct.
- 10% then 20%: the post's own illustration, no computation needed.

## 4. Claims about other posts

- "Leave a Line of Retreat" (data/originals/leave-a-line-of-retreat.md, Posted 2008-02-25): "leave yourself a line of retreat, so that you will have less trouble retreating"; "it helps to make a belief less uncomfortable, *before* you try to evaluate the evidence for it." Our cpara says the device "makes a frightening belief easier to examine".
- "Update Yourself Incrementally" (Posted 2007-08-14): "Just shift downward a little, and wait for more evidence." Quoted exactly.
- "The Importance of Saying 'Oops'" (Posted 2007-08-05): "I could have moved so much faster, I realized, if I had simply screamed “*OOPS!*”" and "well, it’s a long story" (the withheld case). Our notes there: "The essay's evidence for its own method is withheld" and, on its last paragraph, "The two can be reconciled, since small updates on new evidence differ from refusing to admit a known mistake, but neither post says so." My clogic points there; it does not restate the point in full (STANDARDS 2.5).
- "Crisis of Faith" (Posted 2008-10-10, order 129, Book II "How to Actually Change Your Mind", Letting Go): "Without a convulsive, wrenching effort to be rational, the kind of effort it would take to throw off a religion—then how dare you believe anything". The note quotes "a convulsive, wrenching effort to be rational, the kind of effort it would take to throw off a religion", a sub-phrase.
- "The Magnitude of His Own Folly" (Posted 2008-09-30) and "Raised in Technophilia" (2008-09-17) both use "Halt, melt, and catch fire". The first use in book order is Raised in Technophilia; I left any gloss of the computing joke to that post's annotator.

## 5. Items not verified

- The 1996-2000 strategy "formed in the total absence of 'Friendly AI' as a consideration", the 1999 "open-source AI Manhattan Project using self-modifying heuristic soup" (presumably *The Plan to Singularity* / *Coding a Transhuman AI*), and SIAI's 2001 web pages: all need web.archive.org (sysopmind.com, singinst.org), which was unreachable. yudkowsky.net/obsolete/* returned 404.
- The phrase "the unlikely event that life turns out to be meaningless": not in CFAI; may be from an SL4 post or an earlier SIAI page.
- The "technovolatile" link (acceleratingfuture.com/steven/?p=62) returns HTTP 200 with an empty page. Not mentioned in the notes (no consequence).
- John Moore quotation (see above).

## 6. Judgment calls for the editor

- No reserved words in my notes. The Response uses "candid" as credit for the memoir; I think it is warranted (the post blames its younger author throughout) but it is a praise word.
- The clogic on "Update Yourself Incrementally" is the one critical note. The post's own phrase "has been revealed as flawed" gives a fair reconciling reading, and I say so in the note; the remaining complaint is only that the post does not draw the line. The same tension was raised at The Importance of Saying "Oops", so the note is short and points there. The editor may prefer to cut it to a pure pointer.
- CFAI (2001) is a book-length Friendly AI design, which could be read as sitting uneasily with the memoir's "Friendly AI is a contingency plan". I did not make that note: CFAI's own footnote ("objective morality as simply being one of the possibilities") fits the memoir's framing, and the size of a document says nothing about how its author framed it.
- CFAI (2001) also discusses the Manhattan Project (Konopinski, Marvin and Teller on atmospheric ignition), which could be set against "Eliezer2001 hadn't read up on the Manhattan Project". I judged this a nitpick (knowing one episode is not having read up on the project) and left it out.
- Garfinkel is a critic of the author; I use him only as the carrier of a quotation from the Institute's own page, and the note says the archive was not opened.
- The cpara on the John Moore line interprets the joke ("a parent warns against what the parent once did"). It is a reading, not marked as one; the editor may prefer a plain description.
