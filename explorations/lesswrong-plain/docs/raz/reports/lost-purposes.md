# Report: lost-purposes ("Lost Purposes", Yudkowsky, posted 2007-11-25)

## 1. The argument in three sentences (written before annotating)

People keep track of the purpose behind their own plans (no one keeps opening the car door when
the supermarket is out of chocolate), but when incentives pass through large organizations,
each link rewards a measurable intermediate step, and the original purpose is lost: schools teach
to tests (No Child Left Behind), Soviet factories met quotas with useless output, medical research
aims at p<0.05 publications. Organizations can reward only what is measurable today, so their
intermediate measures are leaky generalizations, and bureaucrats are untrustworthy genies who
do not share the wisher's values. The skill that is needed, which the author says has driven the
author's own life since childhood, is to see how every subgoal cuts through to the final goal,
as Musashi says every sword movement must cut the enemy.

## 2. Sources checked

Local copies in `data/sources/b3a_lost/`.

1. Bay Area science survey. The post's link (sfgate cgi URL) returns 403. The same article at
   https://www.sfgate.com/bayarea/article/Science-courses-nearly-extinct-in-elementary-3236187.php
   (`sfgate2.html`, text `sfgate2.txt`): "a new survey of 923 Bay Area elementary school teachers";
   "About 80 percent of those teachers said they spent less than an hour each week teaching
   science, according to researchers from the Lawrence Hall of Science at UC Berkeley and from
   WestEd"; "About 16 percent of the elementary teachers said they spent no time on science at all.
   (Most taught at schools that had missed the reading and math benchmarks of No Child Left
   Behind and were trying to catch up.)". Byline "Nanette Asimov, Chronicle Staff Writer", datePublished
   2007-10-25, so the article is the San Francisco Chronicle's. The LHS
   research brief PDF returned JavaScript, not read.
2. Center on Education Policy, "Choices, Changes, and Challenges: Curriculum and Instruction in
   the NCLB Era" (revised December 2007; survey 2006-07), via
   https://www.schoolinfosystem.org/pdf/2008/artsed.pdf (`cep2008.pdf/.txt`). Matched: "44% of
   districts reported cutting time from one or more other subjects or activi- ties (social
   studies, science, art and music, physical education, lunch and/or recess) at the elementary
   level"; Table 2, science 178 and social studies 178 minutes per week, ELA 503, math 323;
   "Increased time for tested subjects since 2002". The PDF metadata date is 14 December 2007,
   after the post (25 November 2007); the survey and first release are earlier in 2007. The note
   says "from the same year".
3. Ioannidis (2005), PubMed abstract (PMID 16060722; `ioannidis2005_abstract.txt`): "Simulations
   show that for most study designs and settings, it is more likely for a research claim to be
   false than true"; "a research finding is less likely to be true when the studies conducted in a
   field are smaller".
4. Lyons, "Discovering the Significance of 5σ", arXiv:1310.1284 (`lyons_5sigma.pdf/.txt`): "the
   p-value is no larger than 3 × 10−7 . Indeed, journals are very reluctant to allow the word
   'discovery' to appear in the title, abstract or conclusions of a paper, unless the p-value is
   that small." (arXiv title is misspelt "SIGIFICANCE"; the note gives the intended spelling.)
5. NAEP 2007: Mathematics 2007 (NCES 2007-494) and Reading 2007 (NCES 2007-496),
   https://nces.ed.gov/nationsreportcard/pdf/main2007/2007494.pdf and ...2007496.pdf
   (`2007494.txt`, `2007496.txt`). Matched: "Score higher than in all previous assessments";
   "Fourth-graders in 2007 scored 2 points higher than in 2005 and 27 points higher than in 1990";
   "the average score of 221 in 2007 was higher than in any of the previous assessment years".
   Released September 2007, before the post. Long-term trend 2008 (NCES 2009-479) downloaded,
   not used.
6. Campbell's law, Wikipedia raw (`wiki_campbells_law.txt`): "In 1976, Campbell wrote:
   \"Achievement tests may well be valuable indicators ... But when test scores become the goal of
   the teaching process, they both lose their value as indicators of educational status and
   distort the educational process in undesirable ways.\"" (cited there to Campbell 1979,
   Evaluation and Program Planning 2:67-90). Primary not read; note says "as quoted in Wikipedia".
7. Musashi, Book of Five Rings, Victor Harris translation, archive.org texts
   (`musashi_book_of_five_rings.txt`; `musashi_MiyamotoMusashi-BookOfFiveRingsgoRinNoSho.txt`,
   which says "Translated by Victor Harris"). The post's quotation matches word for word, through
   "You must thoroughly research this."
8. Soviet shoes: the memoir link (migs.concordia.ca, Meyer Kron, "Through the Eye of the Needle",
   chapter 8) does not resolve from here; web.archive.org is blocked. A mirror
   (eilatgordinlevitan.com, `kron_eilat.txt`) stops at the start of chapter 8. The tiny-shoes story
   has no source in the post; I found only retellings (Econlib, c2 wiki, blogs), none reachable
   or primary. Not verified.
9. Cherryh: search results only echo Rationality: A-Z; attributed elsewhere to The Paladin (1988).
   Not verified.
10. The overcomingbias "false findings" link (September 2007) was not fetched.

## 3. Arithmetic

- 80% and 16% match the report. 178 minutes is about three hours (Response: "about three hours a
  week on science").
- Lyons: 5 sigma one-sided is about 2.9e-7; p<0.0001 is about 3.7 sigma. So the particle-physics
  convention is about 350 times stricter than the post's figure.

## 4. Claims about other posts

- "Terminal Values and Instrumental Values" (2007-11-15, data/originals): the car-door and
  chocolate example is there ("If you wanted to go to the supermarket to get chocolate ... would
  you gain entry by ripping off the car door with a steam shovel?"). The note only says the
  paragraph restates that post's point.
- "The Hidden Complexity of Wishes" (the day before) is linked for "untrustworthy genies"; checked.
- "Twelve Virtues of Rationality" (annotated/posts/twelve-virtues-of-rationality.tex, lines 29-31)
  quotes the same Musashi passage without its last sentence.

## 5. Not verified

- The Soviet stories (see 2.8), the Cherryh wording, the "40% of classroom time" recollection
  (the post itself says the source cannot be found; no note).
- The textbook-committee claims (coordination between grades; "a fourth of the textbook"). No
  source found; the note says they come with no evidence, not that they are false.

## 6. Judgment calls

1. cfact "overstated" on "Virtually all classroom time": the national survey measures district
   averages, not the Bay Area; a fair defender could say the sentence is rhetorical. It is
   unhedged and specific, so I kept the note, and it credits the trend the survey did find.
2. clogic on "collapsing": the post distrusts test scores; the note says so. NAEP is a national
   sample test, not the state tests the Act rewards, but I did not find a source stating that it
   carries no stakes, so the note does not claim it.
3. cfact on physics p<0.0001: it is a joke in parentheses (STANDARDS 2.2 test 3). I kept it
   because the joke's contrast rests on a stated fact about journals; the note says "loosely
   stated", not "false", and grants that the real convention is stricter.
4. Campbell credit (old idea uncredited): prior work, given as credit with the post's addition.
5. clogic on the classmates: "thin evidence about adults". A fair defender may call the
   question rhetorical; the sentence offers it as the reason ("or why were..."), so I kept it.
6. The last-paragraph note ("the evidence for the trait is the author's own report") is a
   description, not a motive reading.
7. Reserved word "false" appears only in the title and words of Ioannidis's paper.
