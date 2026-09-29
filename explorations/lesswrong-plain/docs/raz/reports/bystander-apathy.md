# Report: bystander-apathy ("Bystander Apathy", Yudkowsky, posted 2009-04-13)

## 1. The argument in three sentences (written before annotating)

The post reports Latané and Darley's smoke-filled-room experiment (75% of lone subjects
report the smoke, only 38% of three-person groups, 10% of subjects with two passive
confederates) and gives the standard explanations, diffusion of responsibility and
pluralistic ignorance, with Cialdini's account of the latter and his advice to single out one
bystander. It then weighs, and rejects, an evolutionary "arms race of delay" as the cause,
suggests instead that the effect is a nonancestral problem (helping rises when people know the
victim or each other), and adds that fear of a public bid for status may play a part. Finally
it argues that the effect is not only a cold wish to avoid blame, because subjects failed to
report a threat to themselves and because telling people about the effect reduces it, which
makes this one of the few biases that teaching seems to cure.

## 2. Sources checked (outside quotations and figures)

All saved in `data/sources/6c_bystander-apathy/` unless noted.

- **Latané and Darley (1969), "Bystander 'Apathy'", American Scientist 57: 244-268** (the post's
  cited source), PDF from https://www.truthaboutnursing.org/research/orig/latane_and_darley/bystander_apathy.pdf
  (`ld1969.pdf`, `ld1969.txt`; OCR, words checked by eye). Matched:
  - Genovese opening: "Thirty-eight of her Kew Gardens neighbors came to their windows when she
    cried out in terror-none came to her assistance." (OCR renders the dash as "-"; the note
    quotes the two halves separately to avoid the dash.)
  - "'apathy,' 'indifference, ' and 'unconcern' are not entirely accurate descriptions of their reactions."
  - Audience: "Each member of a group may watch the others, but he is also aware that others are
    watching him. They are an audience to his own reactions." ... "Being exposed to the public view
    may constrain the actions and expressions of emotion of any individual as he tries to avoid
    possible ridicule and embarrassment."
  - Smoke: "Three-quarters of the 24 people run in this condition reported the smoke"; "of ten
    people run in this condition, only one reported the smoke"; "we would expect over 98% of the
    three-person groups to include at least one reporter. In fact, in only 38% of the eight groups
    in this condition did even one person report"; "If the subject had not reported the smoke
    within six minutes of the time he first noticed it, the experiment was terminated"; "By the end
    of the experimental period, vision was obscured in the room by the amount of smoke present."
    The smoke came "through a wall vent" / "a small vent in the wall", not "from under the door"
    as the post says twice. Not noted (no consequence for the argument).
  - Non-reporters: "they had decided that there was no fire at all".
  - Lady in distress: "70% of Alone subjects intervened"; "at least one person in 91 % of all
    two-person groups"; "In only 40% of the groups did even one person offer heip"; friends "in
    only 70% of the pairs did even one person intervene"; "people are less likely to fear possible
    embarrassment in front of friends than before strangers".
  - Diffusion: "Potential blame may also be diffused."
  - Seizure: "No subj ect who had not reported within three minutes after the fit ever did so.";
    friends "not noticeably different from the average speed of response in the two-person
    condition"; prior acquaintance "Subjects who had met the victim, even though only for less than
    a minute, were significantly faster to report his distress than other subjects in the
    six-person condition"; "It is not our impression that they had decided not to respond. Rather,
    they were still in a state of indecision and conflict"; "they seemed more emotionally aroused
    than did the subjects who reported the emergency."
  - Beer theft: 65% single vs 56% of pairs (not significant); not used in the notes.
- **Earlier agent's copy of Darley and Latané 1968 (seizure)**: `data/sources/b3a_evo3/darley_latane1968.txt`
  (read for context only; the note quotes the 1969 article).
- **Cialdini, Influence**: `data/sources/raz_b2b_halo/cialdini_hc_djvu.txt` (HarperCollins e-book
  of *Influence: The Psychology of Persuasion*, not the 2001 *Science and Practice* the post cites;
  the saved 2001 file is a 401 error page). Matched the whole quoted passage; two small differences:
  "We can learn, from the way the other witnesses are reacting" (commas) and "And because we all
  prefer" where the post has "Because we all prefer". The passage follows Cialdini's retelling of
  the Genovese case ("even though thirty-eight individuals had looked on"). Advice: "isolate one
  individual from the crowd: Stare, speak, and point directly at that person and no one else".
- **Manning, Levine and Collins (2007)**, Am Psychol 62(6): 555-562, PubMed abstract
  (`manning2007_pubmed.txt`): "there is no evidence for the presence of 38 witnesses, or that
  witnesses observed the murder, or that witnesses remained inactive."
- **NYT 2016 (Moseley obituary, McFadden, 4 April 2016)**: the Times page returned a stub (paywall);
  quoted from Wikipedia "Murder of Kitty Genovese" raw (`wiki_genovese.txt`): "The article grossly
  exaggerated the number of witnesses and what they had perceived." The note says "as quoted by
  Wikipedia".
- **Fischer et al. (2011)**, Psychol Bull 137(4): 517-537, PubMed abstract (`fischer2011_pubmed.txt`):
  "overall effect size of g = -0.35"; "reduce the bystander effect, such as when the bystanders were
  exclusively male, when they were naive rather than passive confederates or only virtually present
  persons, and when the bystanders were not strangers."
- **Philpot et al. (2020)**, Am Psychol 75(1): 66-75, PubMed abstract (`philpot2020_pubmed.txt`):
  "in 9 of 10 public conflicts, at least 1 bystander, but typically several, will do something to
  help"; "increased bystander presence is related to a greater likelihood that someone will intervene."
- **Beaman, Barnes, Klentz and McQuirk (1978)**, PSPB 4(3): 406-411, abstract via Crossref
  (`beaman_crossref.json`): "A group of undergraduates previously informed as to how
  social-psychological factors operate to inhibit helping behavior was more likely to help a victim
  at a later date than was an uninformed group." Secondary summaries give 25% vs 42.5% or 43% or 45%;
  not checked, not used.
- **Hanson, "Choke To Submit?"** (overcomingbias, 5 April 2009) (`hanson_choke.html`, `hanson_choke.txt`):
  "But this is all just a guess".
- **Evolving to Extinction**: `data/originals/evolving-to-extinction.md` (Posted 2007-11-16): "a
  genetic arms race might occur to be the *last* one to step forward."
- **Knowing About Biases Can Hurt People**: `data/originals/knowing-about-biases-can-hurt-people.md`:
  "If you’re irrational to start with, having *more* knowledge can *hurt* you."

## 3. Arithmetic

- Expected share of three-person groups with at least one reporter if independent: 1 - 0.25^3 =
  0.984, "over 98%": correct. 38% of 8 groups = 3 groups (37.5%). 75% of 24 = 18. 10% = 1 of 10.
- Lady in distress, pairs: 1 - 0.3^2 = 0.91: matches the article's 91%.
- Dates: Evolving to Extinction 2007-11-16, this post 2009-04-13 (about 17 months; the afterword
  says "in 2007", not "two years").

## 4. Claims about other posts

- Evolving to Extinction (order 137): quoted above. Our notes there call it "I speculate" and
  report the seizure figures; the new note agrees and does not repeat the seizure numbers.
- Knowing About Biases Can Hurt People (order 74): quoted above; used as a pointer, not a charge.
- Collective Apathy and the Internet (next post): its first note points back here for the
  Philpot study (STANDARDS 2.5: made in full here).

## 5. Items not verified

- The NYT 2016 wording (paywall); taken from Wikipedia's quotation, and the note says so.
- Beaman et al. (1978) beyond the abstract; the size of the effect ("strongly reduce") is unchecked.
- Cialdini's 2001 edition itself; checked against a later edition.
- Latané and Darley's 1970 book (*The Unresponsive Bystander*), where the three-process model is
  usually cited from; not read. The notes rely only on the 1969 article.

## 6. Judgment calls for the editor

- The Genovese note: the post does not mention the case (the brief said it "relies on" it). I
  attached the note to the citation, because the cited article opens with the story, and said
  plainly that the post and the experiments do not depend on it. The Response gives it one
  paragraph as information for the reader.
- Philpot et al. (2020) is hindsight (eleven years after the post). It sits in a note and in the
  Response, with the date stated; the In short line says only that the collective claim "rests on
  small laboratory studies". If the editor thinks that phrase still carries the hindsight, it could
  become "an accurate report ... with hedged guesses that the cited article had in several cases
  already made."
- The shyness note says the post's guess "has support in its own source". This is credit, but it
  also shows the author's "I can't actually recall seeing shyness discussed" was mistaken about a
  source the post cites. The post hedged it ("probably just my poor memory"), so I did not call it
  an error.
- The afterword uses "never" once, reporting the article: "subjects who had not responded within
  three minutes never did" (source: "No subject who had not reported within three minutes after
  the fit ever did so"). It meets the word.
- Pronouns: he/his/him/she/her occur only inside quotations from Latané and Darley. Cialdini gets
  no pronoun; Genovese's pronoun appears only in a quotation.
- Considered and dropped: "smoke from under the door" versus the article's wall vent (nitpick);
  the one-minute acquaintance as a challenge to the "band member" parenthesis (it is consistent with
  the post, so it stays as information).
