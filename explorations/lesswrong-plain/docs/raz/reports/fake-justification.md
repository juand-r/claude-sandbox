# Report: fake-justification ("Fake Justification", Yudkowsky, posted 2007-11-01)

## 1. The argument in three sentences (written before annotating)

People who reached a conclusion for one reason (reverence for the Bible, "Ooh, shiny") often defend it afterwards with a respectable criterion (literary merit, stimulating the economy), but such a justification is a false history of the conclusion unless it was a real search that could have changed it. People overestimate how likely they are to change their minds, so these after-the-fact checks are usually token inspections. It would be a suspicious coincidence if the answer produced by an unrelated, indefensible process were also the best answer under the new criterion: "It's improbable that you used mistaken reasoning, yet made no mistakes."

## 2. Sources checked (outside quotations and figures)

Saved in `data/sources/raz_batch2_b/`.

- **Sam Harris, "Is Religion Built Upon Lies?"** (exchange with Andrew Sullivan). The footnote's URL (`samharris.org/site/full_text/debate-with-andrew-sullivan-part-two`) returns 404. The exchange is at https://www.samharris.org/blog/sam-harris-vs-andrew-sullivan (fetched with curl; `harris_sullivan.html`, `harris_sullivan.txt`). Page header: "Debates Is Religion Built Upon Lies? April 28, 2007 From: Sam Harris To: Andrew Sullivan 01/16/07". Matched verbatim: "You and I both know that it would take us five minutes to produce a book that offers a more coherent and compassionate morality than the Bible does." (Harris continues: "Did I say five minutes? Five seconds—just tear out Leviticus, ...".) I did not establish which letter of the exchange the sentence is in, so the note does not say.
- **OLPC XO price** (report only, no note): Wikipedia "OLPC XO" raw (`wiki_olpc_xo.txt`): "Pricing was set to start at US$188 in 2006". The post's 5,000 laptops for $1 million implies $200 each, consistent.
- **Merriam-Webster on "rationalize"**: not re-fetched; the note only points to the notes on "Rationalization", which quote it.

## 3. Arithmetic

- $1,000,000 / 5,000 = $200 per laptop (see above).
- Griffin and Tversky, as quoted in "We Change Our Minds Less Often Than We Think": "only 1 of the 24 respondents chose the option to which he or she initially assigned a lower probability, yielding an overall accuracy rate of 96%". 23/24 = 95.8%, so "23 of the 24" is right.

## 4. Claims about other posts

- "The Bottom Line" (`data/originals/the-bottom-line.md`): "Your effectiveness as a rationalist is determined by whichever algorithm actually writes the bottom line of your thoughts." Our note quotes "whichever algorithm actually writes the bottom line" (flagged by raz_check as not in this post; it is from that post).
- "We Change Our Minds Less Often Than We Think" (`data/originals/we-change-our-minds-less-often-than-we-think.md`, Posted: 2007-10-03): the Griffin and Tversky quotation above ("The average confidence in the predicted choice was a modest 66%, but only 1 of the 24 respondents chose the option to which he or she initially assigned a lower probability"). 2007-10-03 to 2007-11-01 is 29 days, "four weeks".
- "The Third Alternative" (`data/originals/the-third-alternative.md`, Posted: 2007-05-06) and "Motivated Stopping and Motivated Continuation" (Posted: 2007-10-28, four days before 2007-11-01): the post says "I've touched before on the failure to look for third alternatives. But this is not really motivated stopping." It does not name the posts; the note says "Refers back, without naming them".
- "Rationalization": our notes there quote Merriam-Webster's subsense "to attribute (one's actions) to rational and creditable motives without analysis of true and especially unconscious motives". Our note here says only that a fake justification "is what the dictionary calls rationalizing", pointing there. This agrees with the Response of "Is That Your True Rejection?" ("what psychologists since Ernest Jones in 1908 have called rationalization").

## 5. Not verified

- Nothing the notes rely on. The Griffin and Tversky figures are taken as quoted in the author's own post; I did not read the 1992 paper.

## 6. Judgment calls for the editor

- The note on "Easy enough if you're not a Christian" says the neutrality requirement "is applied to one side only" and that the post's own rankings (Tolkien, Harry Potter) "come with no reading shown". This applies the post's rule to the author. A fair defender could say the rankings are rhetorical flourishes, not a justification; I think the point stands because the post does make them as claims ("vastly superior", "superior ... as moral philosophy").
- The cpara on "Many Christians who've stopped really believing" calls it a claim about what those Christians believe, with no evidence. Not a motive reading of the author; a note that the post reads others' inner states.
- The cpara on "No search ever occurred" uses the post's own next paragraph to say the question is one of fact about each person. I believe the two paragraphs are read correctly (the post's "genuinely has that power" clause).
- Credit given: the coincidence argument is "sound as stated"; the laptop case "shows how to test for it". The "test" phrasing is my summary of the laptop example (the post does find a better option, 5,000 OLPC laptops), not a claim the post makes in words.
- Reserved words: none remain in our text for this post ("invented" was changed to "a hypothetical one").
- Build: the post text contains U+2661 (♡), which the shared preamble does not declare, and the preview failed. I could not edit `preamble.tex` (not my file), and `\DeclareUnicodeCharacter` is preamble-only. I appended to the `\post{...}` line of `annotated/posts/fake-justification.tex` (a line the verbatim checker strips): `\expandafter\gdef\csname u8:\detokenize{♡}\endcsname{\ensuremath{\heartsuit}}`. It builds and renders the heart. The editor may prefer to add `\DeclareUnicodeCharacter{2661}{\ensuremath{\heartsuit}}` to `annotated/preamble.tex` and remove my line. `notes_backup.py export` may also need to handle that line (I did not run the export for any of my slugs).
