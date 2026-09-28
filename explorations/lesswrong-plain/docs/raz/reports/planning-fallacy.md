# Report: planning-fallacy ("Planning Fallacy", Yudkowsky, posted 2007-09-17)

## 1. The argument in three sentences (written before annotating)

Big construction projects run late and over budget, and while that may be partly
selection and incentives, experiments with individual students show the same bias:
people's time forecasts, even ones they call 99% certain, are too optimistic, because
their "realistic" scenario is the same as their best case. The cure is the "outside
view": ignore the special features of this project and ask how long broadly similar
projects took, or ask an experienced outsider. The answer will sound too long, and it is
true.

## 2. Sources checked (outside quotations and figures)

All fetched in this session. PDFs were read as text with `pdftotext -layout`.

**Buehler, Griffin and Ross (1994), JPSP 67:366-381** (the post's footnote 2).
URL: https://web.mit.edu/curhan/www/docs/Articles/biases/67_J_Personality_and_Social_Psychology_366,_1994.pdf
Matched words:
- Sydney figures: "According to original estimates in 1957, the opera house would be completed early in 1963 for $7 million. A scaled-down version of the opera house finally opened in 1973 at a cost of $102 million (Hall, 1980)."
- Name of the effect: "has been termed the planning fallacy (Kahneman & Tversky, 1979)." (spans a line break in the PDF)
- Megaprojects: "Proponents of these schemes may deliberately provide overly optimistic assessments of cost and time to win political approval for the projects." (read, not quoted in our text)
- Abstract, think-aloud: "Think-aloud procedures revealed that Ss focused primarily on future scenarios when predicting their completion times." We quote only "focused primarily on future scenarios".
- Study 1 (honors theses, worst case): "fewer than half of the respondents (48.7%) finished by the time they had predicted assuming that "everything went as poorly as it possibly could." Although the difference was not significant, respondents tended to underestimate their actual completion times even when they made pessimistic predictions (M = 48.6 days vs. 55.5 days)". Table 1 note: "Means are based on 33 subjects."
- Study 4 (recall): "However, leading people to remember past experiences did not, in itself, reduce the optimistic bias. The bias was attenuated only when subjects were induced both to consider their past experiences and to relate the experiences to the task at hand." Abstract: "In Study 4, the optimistic bias was eliminated for Ss instructed to connect relevant past experiences with their predictions."
- Study 4 (accuracy): "Predictions were no more accurate in the recall-relevant condition than in the other conditions."
- Study 5 (observers): "Although the observers' predictions were more conservative, they were no more accurate than the actors' predictions. The two groups of subjects tended to err in opposite directions." Observers were "123 undergraduate psychology students", i.e. not experienced outsiders.

**US General Accounting Office, "Denver International Airport", AIMD-95-230 (September 1995).**
URL: https://www.govinfo.gov/content/pkg/GAOREPORTS-AIMD-95-230/pdf/GAOREPORTS-AIMD-95-230.pdf
Matched: "Actual construction costs to the date DIA opened totaled $3.004 billion, close to $1 billion over the original estimate. Most of the cost increases were due to changes in the scope of the airport, such as the addition of an automated baggage system and widening and lengthening concourses. In addition to the $1 billion growth in construction costs, a 16-month delay in opening DIA due to automated baggage system complications increased capitalized construction interest by about $300 million." Also "the $4.8 billion Denver International Airport".

**Newby-Clark et al. (2000), J Exp Psych: Applied 6:171-182** (the post's footnote 5). Abstract only, from PubMed (PMID 11014050), via
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=11014050&rettype=abstract&retmode=text
Matched: "Task completion plans normally resemble best-case scenarios and yield overly optimistic predictions of completion times." and "Pessimistic scenarios did not affect predictions or accuracy and were consistently rated less plausible than optimistic scenarios (Experiments 1-3)." The full text was not reachable (Zenodo returned 403; ResearchGate and APA blocked), so the post's "indistinguishable results" claim is unchecked, and the note says so.

**Roy, Christenfeld and McKenzie (2005), Psychological Bulletin 131:738-756** (a review; secondary for the Christmas study).
URL: https://pages.ucsd.edu/~mckenzie/Royetal2005PsychBull.pdf
Matched: "All participants, regardless of whether they made detailed plans, underestimated when they would be finished, 4 days later than planned for Christmas shopping and 1.7 days later than planned for their school assignment, with underestimation greatest for participants who formed detailed future plans." Roy attributes the study to Buehler & Griffin (2003, OBHDP), not to the 2002 chapter the post cites; presumably the chapter reports the same study.

**Wikipedia, "Eurofighter Typhoon"** (secondary), raw wikitext
https://en.wikipedia.org/w/index.php?title=Eurofighter_Typhoon&action=raw
Matched: "In 1985, the estimated cost of 250 UK aircraft was £7 billion. By 1997 the estimated cost was £17 billion; by 2003, £20 billion, and the in-service date (2003, defined as the date of delivery of the first aircraft to the RAF) was 54 months late." Its cited source (House of Commons Public Accounts Committee, https://publications.parliament.uk/pa/cm200304/cmselect/cmpubacc/383/38305.htm) returned a Cloudflare challenge / 403. The note says it could not be reached.

**Wikipedia, "Planning fallacy"** (read for orientation, not quoted). It gives the Eurofighter as "six years longer than expected, with an overrun cost of €8 billion" citing Sanna et al. 2005, which differs again from both the post and the Eurofighter article. I did not use it.

## 3. Arithmetic

- Denver (GAO): 3.004 - 2.08 = 0.924, "close to $1 billion" of construction overrun; plus about 0.3 of interest, so about $1.2 billion against the post's "$2 billion". The post's footnote gives "$3.1 billion" as another figure. Baselines differ; the note says so and does not call the post's figure wrong.
- Sydney: 102 / 7 = 14.6 times the estimate; 1973 - 1963 = 10 years late.
- Eurofighter (Wikipedia, UK share): 20 / 7 = 2.9; post: 19 / 7 = 2.7. The ratio is similar; the currency and scope differ.
- 99% level: 45% finished, so 55% missed a date they called 99% certain.
- Worst case (1994, Study 1): 100 - 48.7 = 51.3% finished after their worst-case date; mean gap 55.5 - 48.6 = 6.9 days, not significant. So "usually ... somewhat worse" fits narrowly; our note says "fits the sentence narrowly".
- Christmas (post's numbers): detailed-plan group missed by more than 7 - 3 = 4 days; control group by 4 - 3 = 1 day. Roy's Table 1 gives the study's overall means as 22.9 days actual vs 20.4 estimated, a 2.5-day underestimate, which equals the mean of 4 and 1 if the groups were equal in size. That is consistent with the post but is not a verification.
- Japanese students: 10 - 1 = 9 days optimistic.

## 4. Claims about other posts

None in the notes. (The post links no other posts.)

## 5. Items not verified, and what would be needed

- The 13% / 19% / 45% figures (cited to the 1995 European Review of Social Psychology chapter). Every web copy I found repeats the post. Needs the 1995 chapter (DOI 10.1080/14792779343000112).
- The Buehler et al. quotation about the 99% level (cited to the 2002 chapter in Gilovich, Griffin and Kahneman). Cambridge Core and ResearchGate blocked; a Princeton-hosted document that search results associated with the chapter (markus.scholar.princeton.edu/document/124) returned a Cloudflare challenge, so I do not know what it is. Needs the chapter.
- The Christmas-shopping numbers (more than a week, four days, three days) and the Japanese-students study (the latter listed on Buehler's lab page as "Culture and optimism: The planning fallacy in Japan and North America. Unpublished manuscript."). Needs the 2002 chapter.
- Newby-Clark's "indistinguishable" best-guess vs best-case result: needs the full paper.
- The Eurofighter primary source (House of Commons PAC report 2003-04, HC 383).
- Whether experienced outsiders (as opposed to Study 5's student observers) are more accurate. Other literature (Kahneman and Lovallo 1993; Flyvbjerg on reference-class forecasting) may support the post here. I did not check it, so the note is scoped to "the post's sources, as far as I could check them".

## 6. Judgment calls for the editor

- Paragraph 4 note: "That concession takes the first three paragraphs out of the evidence." The post never says the megaprojects are evidence for the bias ("But there's also a corresponding cognitive bias"), so the note does not accuse it of that. It says only that they cannot serve as evidence. The honest edition originally said they are "probably not examples of the bias". I changed that to "very probably have other causes too, and cannot show the bias", because "Yes, very probably" does not exclude the bias.
- "As we saw before" clogic. My first draft said the post had shown only one unsourced sentence. A fair defender could reply that the 99% forecasts are near-worst-case forecasts. The note now says: "The nearest thing shown before is the 99% forecasts".
- Outsider note ("much more accurate"). It rests on one study with student observers, not experienced ones, and the note says so. It is the most exposed judgment in the post.
- Last-paragraph note ("This answer is true"). It rests on one study (1994, Study 4, absolute error). I used "claims more than the evidence gives", not "false". The Response's "In short" says the promises were ones "its own 1994 source did not find". That is literally true: the study found no accuracy gain. But the 2002 chapter, which I could not read, might report something else.
- Eurofighter and Denver cost notes may count as nitpicks (STANDARDS 2.4(2)), since the post's argument does not depend on the exact overrun. I kept them because they are factual and the Denver one leads into the GAO's "scope" finding. Cut the Eurofighter note if it seems like padding.
- Reserved words: none in our text after revision. I changed "it can still be wrong" to "it can still miss" in the Response.
- Credit: the Response opens with one sentence of credit ("The post reports real research, and its main claim holds up in the studies it cites"). Leaving it out would mislead, because the core finding is sound.

## 7. Notes on the brief and standards (pilot feedback; applies to all three of my posts)

1. **Required reading conflicts with STANDARDS.** The brief sends agents to `annotated/README.md` sections 2 to 5, but section 5 still carries the superseded stance. 5.1 says "Write each `\cpara` note as a judgment, not a summary." 5.3 says "At most one sentence of credit", "Apply section 1 in full", and that the In-short line "should be the sentence the author would least like to read". STANDARDS 2.1 says the opposite for paragraphs that give no ground for criticism ("plainly describes what the paragraph does"). I followed STANDARDS. A banner at the top of README section 5, or a narrower pointer (5.2 checklists only), would remove the conflict.
2. **Footnote paragraphs.** It is unclear whether footnote paragraphs count as "substantial". The lens model gives them `\cpara`s, so I did too (six trivial citation notes in planning-fallacy). If those are not wanted, say so.
3. **Unverifiable figures in the post.** STANDARDS section 3 covers our own claims ("drop it or say in the note that you could not check it"). It does not say what to do when a figure in the post itself cannot be checked, for example because the primary source is paywalled. I did not flag those in the notes; I listed them in the report (section 5). Where one of my notes relied on something unread, I said so in the note ("I could read only the paper's abstract", "I could not reach the chapter").
4. **Access.** Many primary sources are blocked from this environment: Cambridge Core, ResearchGate, Zenodo (403), parliament.uk and yudkowsky.net (Cloudflare), Semantic Scholar API (429), and PubMed eutils (rate limit of 3 per second). curl plus `pdftotext` worked for university-hosted PDFs (MIT, UCSD) and govinfo.gov. **WebFetch passes pages through a summarizing model**, so its "quotations" are not reliable verbatim. The brief lists WebFetch as a verification tool without that warning. I used it once (the Yehuda page) and marked the result as near-verbatim.
5. **Web search echoes the post.** Several search "results" for the 13/19/45 figures simply restated the post (readthesequences.com, LessWrong). An agent could mistake that for confirmation. Worth a line in the brief.
6. **raz_check noise.** It flags every outside quotation (expected). It flags reserved words inside quotations from the post, and pronouns for fictional characters (Spock). Its quote matcher fails on nested quotes whose inner punctuation differs from the post's (``...`propriety,'\,''), so I rewrote to avoid nesting. A flag that shows whether a reserved word sits inside ``...'' would save time.
7. **Recurring criticisms in book order.** STANDARDS 2.5 says to make a recurring criticism in full "where it matters most" and elsewhere to point to it. The earlier post in book order ("Why Truth?", Map and Territory) now points forward to a later one ("Something to Protect"), whose notes carry the evidence. That seems to be what 2.5 intends, but a reader of the book meets the pointer first. The editor may prefer the full note in the earlier post.
8. **Honest-edition length.** STANDARDS says 150 to 500 words; STYLE.md's checklist says "about 300 to 450". Minor, but they disagree.
9. **Manifest.** The `book` field has a trailing space ("Map and Territory "). This matters if the book generators match on it.
10. **Density.** The brief says "a few sentence notes". Planning-fallacy ended with only one (most points fit a paragraph note). I did not add sentence notes to reach a count.
