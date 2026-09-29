# Report: Final Words (batch 6b, order 316)

Posted 2009-04-27 (`data/originals/final-words.md`). Book VI, "Challenging the Difficult",
last post of the sequence; the previous post in book order is "Shut up and do the
impossible!" (2008-10-08). A story in the Beisutsukai setting.

## 1. The argument in three sentences (written before annotating)

Jeffreyssai ends his students' training with the claim that mastery cannot be taught: it
comes only from using what one was taught until it fails, and teaching matters because it
prepares a student to recover from that failure rather than give up. He warns them of three
flaws common among rationalists: looking harder for flaws in unwelcome arguments,
cleverness valued for its own sake, and underconfidence that passes for humility. Brennan,
alone afterwards, falls into the third flaw, uses a question his training gave him to find
that he has hidden from himself a desire because it seems impossible, sets out to pursue it,
and rejects the proverb that it is futile to ask how a master knows things.

## 2. Sources checked (outside quotations and facts)

Saved in `data/sources/6b_final-words/` (with `annotate.py`, the helper that inserted the notes).

| Claim in our text | Source | Exact words matched |
|---|---|---|
| "beisutsukai" = "Bayes-user" (note on Taji's paragraph; honest n.b.) | LessWrong wiki, tag "Beisutsukai", fetched by GraphQL (`tag_beisutsukai.json`) | `Derived from "beisu", a Japanese transliteration of Bayes ... plus "tsukai", Japanese "user", therefore "Bayes-user".` The same page lists five stories, Final Words last. |
| Silver shoes (note on "silver-shoes moment"; honest n.b.) | L. Frank Baum, *The Wonderful Wizard of Oz*, Project Gutenberg eBook #55 (`oz.txt`, lines 4696 to 4698) | "Your Silver Shoes will carry you over the desert," replied Glinda. "If you had known their power you could have gone back to your Aunt Em the very first day you came to this country." |
| Decision theory asks for consistency, not content (note on "decision theory did require") | Wikipedia, "Von Neumann–Morgenstern utility theorem", `?action=raw` (`vnm.txt`) | line 27: "The four axioms of VNM-rationality are ''completeness'', ''transitivity'', ''continuity'', and ''independence''."; line 35: "Transitivity assumes that preferences are consistent across any three options"; line 169: "Because the theorem assumes nothing about the nature of the possible outcomes". |

Baum's date, 1900: the Gutenberg text's introduction is signed "Chicago, April, 1900." (`oz.txt`, line 97).

## 3. Arithmetic

- "posted a week earlier": The Sin of Underconfidence `Posted: 2009-04-20`; Final Words `Posted: 2009-04-27`; 27 − 20 = 7 days.
- "the last of the book's five stories in this setting": manifest orders The Ritual 130, Initiation Ceremony 217, The Failures of Eld Science 247, Class Project 260, Final Words 316. `grep -l "Jeffreyssai\|Brennan" data/originals/*.md` (392 originals) finds, besides these five, only Bayesians vs. Barbarians (334, an essay that mentions Jeffreyssai), Einstein's Speed, My Childhood Role Model and That Alien Message (passing mentions). No later story.
- "the same day": the story opens at dawn and ends "As the sun was setting"; Brennan's lapse into the third flaw falls between.
- Paragraph count: 101 (audit); 59 \cpara, 3 \clogic, 2 \cfact. One-line narrative paragraphs ("As one, their heads turned.", "Then -", "No.") have no note.

## 4. Claims about other posts

| Our claim | File | Matched words |
|---|---|---|
| Styrlyn "one of the older-looking students" | the-failures-of-eld-science.md, line 35 | "He was one of the older-looking students, wearing a short beard speckled in grey." |
| Brennan's Mistress's name "opened doors" in Eld Science | the-failures-of-eld-science.md, line 13 | "Nor had he hesitated to use his Mistress's name to open doors." |
| Positive Bias on skill below words | positive-bias-look-into-the-dark.md, line 43 | "So much of a rationalist’s skill is below the level of words." |
| Crisis of Faith tells the reader to stage one, and to clear the mind | crisis-of-faith.md, line 79 | "you should go ahead and stage a Crisis of Faith" ... "Clear your mind of all standard arguments; try to see from scratch." |
| Jeffreyssai begins such a crisis in The Ritual | the-ritual.md, line 55 and our notes on it | "only blocking out every thought that had ever *previously* occurred to him"; our Ritual notes: "This acts out the advice of ``Crisis of Faith''". |
| Something to Protect, attitude to failure | something-to-protect.md, line 66 | "I must have had the wrong conception of rationality," and not, "Look at how rationality gave me the wrong answer!" |
| First flaw restates Knowing About Biases (a conditional) | knowing-about-biases-can-hurt-people.md | "If you’re irrational to start with, having *more* knowledge can *hurt* you." (Our notes on that post, original edition, assess its evidence; I only point there, per STANDARDS 2.5.) |
| Sin of Underconfidence names only the third sin; its list of symptoms | the-sin-of-underconfidence.md | "There are three great besetting sins of rationalists in particular, and the third of these is underconfidence." I read the whole post: the first two are not named. Also "you question yourself *but don't answer the self-questions and move on*" and "*losing your forward momentum*". |
| Sense of "impossible" | shut-up-and-do-the-impossible.md, line 23 | "the word "impossible" does not usually refer to a strict mathematical proof of impossibility in a domain that seems well-understood." (Quoted in full from "the word" to the end of the sentence.) |
| Curiosity-stopper | science-as-curiosity-stopper.md, line 31 | "consider the consequences if you permit “Someone else knows the answer” to function as a curiosity-stopper." |
| Bardic Conspiracy and drama | final-words.md itself | "tempting a Bard with drama" / "Even the Bardic Conspiracy wouldn't try for that much drama." |
| The Ritual leaves the question unnamed; Class Project stops before a result | our afterwords on those posts | consistent with their notes ("The story ends as the crisis begins"; "It does not say whose, or what"). |

Consistency with earlier Beisutsukai stories (review_log, batch 4a/4d and The Ritual): judged as fiction; neutral pointers to earlier posts; the "stops before any result" point made as in The Ritual and Class Project.

## 5. Items not verified

- Whether LessWrong's current text differs from `data/originals/final-words.md` (I used the original as fetched; the skeleton matched it).
- "Shir L'or", "Diamond Sea University", the red-tinted stream and the cave: in-world details; the notes describe them and do not interpret.
- The silver-shoes allusion is my identification (the story does not explain the phrase). Baum's silver shoes are the obvious referent, but it is an inference.

## 6. Judgment calls for the editor

1. Reserved words: none used in notes, Response or n.b.s (raz_check flagged none).
2. The one critical logic note (Jeffreyssai: "the reality will be that it was you who failed your Art"). I say that, put as fact, it assigns every failure to the student and none to the Art, and the story gives no way to tell which is at fault; read as advice, it is Something to Protect's attitude. I avoided "unfalsifiable". It is in the Response and the In short line. A fair defender could say the Art is by definition the ideal and the line is a creed, not a finding; the note gives that reading its second sentence.
3. "Foretold, not shown": the Response and last note say the failure through which mastery is said to come lies beyond the story's end. This matches how The Ritual and Class Project were handled ("stops before any result"). It is scope, and could be cut from the In short line if the editor judges it a fault of genre.
4. Note on the parenthesis about Mount Mirror: "The aside fits the book's distinction between map and territory." A mild reading; the story does not say so.
5. Note 21 reads Jeffreyssai's "I do not know" as hedging the earlier "you can only arrive at mastery". A defender could say "can only" meant "only by your own use, not by more classes"; the note says what he doubts ("a road that goes only through the monastery"), which fits both.
6. The \clogic on "you cannot provoke the moment of your crisis artificially" separates this crisis from Crisis of Faith's staged one. It is information to prevent a misreading, not a charge. Omitted from the honest section for length.
7. Gloss of "beisutsukai": the book's earlier stories never translate it and our notes on them do not either. The gloss belongs at the first occurrence (The Ritual, order 130) in the whole-book pass; here it could become a pointer.
8. Honest section is 516 words, slightly over "about 500"; the story is 2,860 words.
9. Not made, as nitpicks: Jeffreyssai calls cleverness "our chief vulnerability" though he lists it second of three; the typos "witnesssed", "noncommitally", "an sharp tinge".
