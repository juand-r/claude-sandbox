# Report: asch-s-conformity-experiment

## 1. The argument in three sentences

In Asch's line-judgment experiments many subjects gave an obviously wrong answer that agreed
with a unanimous group of confederates. Because other people's beliefs are evidence (Aumann's
agreement theorem), going along with the majority is not automatically irrational. But the
detailed results (conformity stops rising after three confederates, collapses with one
dissenter, returns when the dissenter defects, differs by sex and ingroup, falls with blatant
stimuli and private answers) fit neither rational updating nor a conscious strategy of fitting
in, so the conformity is best read as nervousness about being the odd one out.

## 2. Sources checked

All saved in `data/sources/raz_b2b_asch/`.

- Asch 1955, "Opinions and Social Pressure", *Scientific American* 193(5), full text as
  mirrored at https://www.panarchy.org/asch/social.pressure.1955.html
  (`asch1955_panarchy.html`, `.txt`). Exact words matched:
  - "swung to acceptance of the misleading majority's wrong judgments in 36.8 per cent of the selections"
  - "about one quarter of the subjects were completely independent and never agreed with the erroneous judgments of the majority" (not quoted by me; agrees with lonely-dissent notes)
  - "Others who acted independently came to believe that the majority was correct in its answers, but they continued their dissent on the simple ground that it was their obligation to call the play as they saw it."
  - "Many of the individuals who went along suspected that the majority were \"sheep\"..." (read, not used)
  - "All the yielding subjects underestimated the frequency with which they conformed."
  - "But further increases in the size of the majority apparently did not increase the weight of the pressure substantially."
  - "Its pressure on the dissenting individual was reduced to one fourth"
  - "the subjects repudiated the suggestion that the partner decided them to be independent"
  - moderate dissenter: "the effect of the majority on the subject decreases by approximately one third"
  - extremist dissenter: "their errors dropped to only 9 per cent"
  - desertion: "Their submission to the majority was just about as frequent as when the minority subject was opposed by a unanimous majority throughout."; "the strong specific effect of \"desertion\""; "the partner's effect outlasted his presence. The errors increased after his departure, but less markedly than after a partner switched to the majority."
  - "depends to a considerable degree on how wrong the majority is"
  - The post's block quotation: "That we have found the tendency to conformity in our society so strong that reasonably intelligent and well-meaning young people are willing to call white black is a matter of concern. It raises questions about our ways of education and about the values that guide our conduct." (post's ellipsis drops the middle clause; meaning unchanged).
  The mirror is not the magazine itself, but Bond and Smith (below) quote the same passage as "(Asch, 1955, p. 34)", which confirms both text and source.
- Asch 1956, *Psychological Monographs* 70(9), PDF from
  https://eclass.uowm.gr/modules/document/file.php/NURED262/%CE%A0%CE%A1%CE%A9%CE%A4%CE%9F%CE%A4%CE%A5%CE%A0%CE%91%20%CE%91%CE%A1%CE%98%CE%A1%CE%91/Asch%20studies%20in%20independence%20and%20conformity%201956%20PM.pdf
  (`asch1956.pdf`, `asch1956.txt`, OCR text layer). Matched:
  - Table 3 (all experimental, N = 123), errors 0..12: 29, 8, 10, 17, 6, 7, 7, 4, 13, 6, 6, 4, 6; mean 4.41; mean per cent 36.8.
  - "The critical subject was nearly always seated before the last member of the majority."
  - "While the majority effect was considerable, it was by no means complete, or even the strongest force at work."
  - Summary items 14(c)-(e): "A very few yielding subjects appeared unaware of the effect of the majority upon them"; "A substantial proportion of subjects yielded once their confidence was shaken."; "being dominated by an imperious desire not to appear different". (OCR renders "rightness" as "Tightness"; I did not quote that word.)
  - grep for "matter of concern" and "white black" in the monograph: no hits (basis for "in which I did not find them"; OCR could in principle have garbled it).
- Bond and Smith 1996, abstract via OpenAlex (`openalex_bond_smith.json`): "133 studies drawn from 17 countries"; "An analysis of U.S. studies found that conformity has declined since the 1950s." The OpenAlex record also carries the paper's opening, which quotes Asch 1955 p. 34. Full text not reachable (radford.edu TLS failure; web.archive.org reset).
- Bond 2005, "Group Size and Conformity", *Group Processes & Intergroup Relations* 8(4), postprint https://d-nb.info/1186499532/34 (`bond2005_group_size.pdf`, `.txt`). Matched:
  - moderators Bond and Smith (1996) "found were significantly related to conformity effect size: (a) the percentage of female respondents, (b) the date ..., (c) the consistency of the majority ..., (d) whether the majority were an out-group for the respondent, and (e) stimulus ambiguity"
  - "Mean effect sizes for majority sizes of 3, 4, 5, 6 and 7 are very similar, and give some support to Asch's (1951) contention that a majority of 3 is sufficient."; slope "b = 0.057, is modest"; relationship "significant, but is weak nevertheless".
- Aumann 1976, "Agreeing to Disagree", abstract via OpenAlex (`openalex_aumann.json`): "THEOREM. If two people have the same priors, and their posteriors for an event $A$ are common knowledge, then these posteriors are equal." (Project Euclid PDF returned HTML, not the paper.)
- Deutsch and Gerard 1955: title via OpenAlex (`openalex_deutsch_gerard.json`), truncated abstract "These include a face-to-face situation, an anonymous situation, and a group situation". Deutsch's Citation Classic commentary (1980), https://garfield.library.upenn.edu/classics1980/A1980KF12300001.pdf (`garfield_deutsch_gerard.txt`): "We labeled the type of social influence most associated with groups as 'normative social influence' and distinguished this from 'informational social influence'"; "The distinction between 'normative' and 'informational' social influence caught on and has been widely employed". I did not read their results, so no note says what they found in the anonymous condition.
- Wikipedia, "Asch conformity experiments", raw (`wiki_asch.txt`): "Social psychologists later interpreted these findings to have reflected both normative and informational social influence."

## 3. Arithmetic

- At least one error: 123 - 29 = 94; 94/123 = 76.4% ("three-quarters" OK).
- More than half the time = 7 to 12 errors of 12: 4+13+6+6+4+6 = 39; 39/123 = 31.7% ("a third" OK). (6 or more: 46 = 37.4%.)
- Per answer: 36.8% conforming, so 63.2% correct ("nearly two answers in three").
- Truthful partner: one fourth of 36.8% is about 9.2%; extremist dissenter 9%. The post's "5–10%" fits the answer rates; it calls them "of subjects".
- Aumann 1976 vs Asch 1951-56: 20 to 25 years ("more than twenty years" OK).
- Svenson-type driver figure ("90% of drivers") not checked; it is an aside and no note relies on it.

## 4. Claims about other posts

- "The next day's post, 'On Expressing Your Concerns'": posted 2007-12-27, this post 2007-12-26. Its sentence: "we both agree that Aumann's Agreement Theorem extends to imply that common knowledge of a factual disagreement shows *someone* must be irrational."
- Consistency with `lonely-dissent` notes: they give "36.8 per cent of the selections", "about four times as often as with an ally", and "about one quarter never agreed". My figures agree (36.8%; one fourth; 29/123 errorless). STANDARDS 2.5: this post is earlier in book order (116 vs 118), so the full statement of the "independence left out" point belongs here; lonely-dissent also states it in full. The editor may want lonely-dissent's version reduced to a pointer, or accept both since the two posts misuse the figures differently (this one reports true figures and omits the per-answer rate; lonely-dissent says the first dissent is "a lot harder" and omits that most answers were dissent).

## 5. Not verified

- "Around one-half the women conform more than half the time, versus a third of the men": no source found; the note says so. Direction supported by Bond and Smith via Bond 2005.
- "a handicapped subject alongside other handicapped subjects": not found; the note says so.
- Whether Bond and Smith 1996 itself reports the majority-size plateau: full text unavailable. The note avoids saying it does not; it says the plateau is Asch's finding and reports Bond 2005's reanalysis of the same studies.
- The diagram image (readthesequences.com) not viewed; described from the text.

## 6. Judgment calls

- The per-answer note (paragraph 4) credits both figures as correct and faults only the omission of the per-answer rate and Asch's emphasis. A defender could say the post answered its own question ("how many people"); the note says so.
- Interviews note (paragraph 5): "gives belief more room than 'some' suggests" rests on Asch's "a substantial proportion ... yielded once their confidence was shaken" plus "the presumed rightness of the majority". Asch gives no proportions, so this is a judgment, mildly worded.
- Aumann common-prior clogic: technical claim; supported by Aumann's own abstract. It is flagged as mattering mainly in the next post.
- Blatant-diagram clogic ("this item fits it"): my inference that lower conformity with clear stimuli is predicted by the evidence reading. I think this is standard (Wikipedia: "conformity increased when the line comparison task became more difficult, suggesting that uncertainty amplified informational influence").
- Deutsch and Gerard note: "old idea uncredited". The post does not claim novelty; the note only says it does not mention the distinction.
- Reserved words: "wrong" appears only in "wrong answer" (literal description of the experiment).
- Pronouns: "he/his" for Asch (historical figure) and for Asch's partner (Asch's own usage). None for Yudkowsky.
- Footnote 1 citation (1956 monograph for a 1955 quotation): kept in the margin only, per the editor's earlier ruling that citation slips stay out of the verdict.
