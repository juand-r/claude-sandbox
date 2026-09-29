# Report: typicality-and-asymmetrical-similarity

## 1. The argument in three sentences

People judge some members of a category as more typical than others (robins more than
ostriches), and typicality shows up consistently across measures such as verification times
and direct ratings. Similarity judgments built on typicality are asymmetric (98 is
"approximately" 100 more naturally than the reverse; Mexico is rated more similar to the
United States than the reverse), and the same asymmetry appears where it looks like an error:
people expect a disease to spread from robins to ducks more than from ducks to robins, which
the author explains by an asymmetric similarity heuristic standing in for probability. So the
Aristotelian model of categories as necessary-and-sufficient classes is not a good model of
human thinking; people treat set membership as a matter of degree.

## 2. Sources checked

All saved in `data/sources/b3b_typicality/`.

- Rosch, "Principles of Categorization" (1978), PDF at
  https://commonweb.unifr.ch/artsdean/pub/gestens/f/as/files/4610/9778_083247.pdf
  (`rosch1978.pdf/.txt`; `rosch_lloyd1978.pdf` is the same chapter from a Rice course page).
  Matched: "In such tasks, for natural language categories, responses of true are invariably
  faster for the items that have been rated more prototypical." (txt l. 586-587); "Rosch
  (1975a) showed that when subjects were given sentence frames such as "X is virtually Y," they
  reliably placed the more prototypical member of a pair of items into the referent slot"
  (l. 646-648); also, for balance, "Although logic may treat categories as though membership is
  all or none, natural languages themselves possess linguistic mechanisms for coding and coping
  with gradients of category membership." (l. 634-635; not quoted in the notes).
- Tversky and Gati, "Studies of Similarity" (1978), as reprinted in Tversky, *Preference,
  Belief, and Similarity* (2004), PDF
  https://cseweb.ucsd.edu//~gary/PAPER-SUGGESTIONS/Preference,%20Belief,%20and%20Similarity%20Selected%20Writings%20(Bradford%20Books).pdf
  (`tversky_selected.txt`, Table 3.2, l. 3500-3527). Row "1 U.S.A. Mexico 91.1 6.46 7.65 11.78
  10.58" (s(p,q)=6.46, s(q,p)=7.65, scale "from 1 (no similarity) to 20 (maximal
  similarity)"); "The average difference (.42) was significantly positive: t = 2.99, df = 153,
  p < .01." Also Tversky 1977 "Features of similarity" (`tversky1977.txt`), same study.
- Sadock, "Truth and Approximations", BLS 3 (1977) 430-439, PDF from
  https://journals.linguisticsociety.org/proceedings/index.php/BLS/article/download/2268/2038
  (`sadock1977.pdf`, scanned; I read every page as images `sadock-01..11.png`). No 98/100
  comparison and no test of it. Matched (p. 433): "(11) Odessa has a population of
  approximately one million. (12) Odessa has a population of approximately 990,000." and "(12)
  has more significant figures than (11) and consequently involves a smaller scale." The paper
  does mention "an informal (and probably inept) survey" (p. 438), about the approximators
  circa/about/around/roughly/approximately, not about 98 and 100.
- Rosch 1975 "Cognitive reference points": not read. The claim that its items included round
  and non-round numbers is from a secondary source, Frontiers in Psychology 2016 (PMC4737903,
  `pmc4737903.txt`): "Her studies concerned geometric figures (regular or irregular) or numbers
  (round or not round)." and the 100/103 description.
- Heit, "Properties of inductive reasoning", Psychonomic Bulletin & Review 7 (2000) 569-592,
  http://faculty.ucmerced.edu/eheit/heit2000.pdf (`heit2000_raw.txt`). Matched: "Subjects were
  told to assume that on a small island, it had been discovered that all members of a
  particular species (of birds or mammals) had a new type of contagious disease."; "having
  bluejay as a premise category led to stronger inferences overall than did having goose as a
  premise category."; "Rips (1975) found distinct contributions of premise– conclusion
  similarity and premise typicality."; "This phenomenon follows from the premise typicality
  effect" (said of Osherson et al.'s premise-conclusion asymmetry); multidimensional scaling:
  "deriving multidimensional scaling solutions for different categories of animals, so that
  similarity and typicality measures could be derived from the animals' positions"; Bayesian
  model: "a computational-level analysis of what, given certain assumptions, would be normative
  for inductive inferences"; "atypical categories such as hedgehog would have a number of
  idiosyncratic features. Hence a premise asserting a novel property about hedgehogs would
  suggest that this property is likewise idiosyncratic and not to be widely projected."
- Sadalla, Burroughs and Staplin (1980), PubMed 7430967 abstract (`pubmed_7430967_sadalla1980.txt`):
  "The subjective distance between reference points and nonreference points was found to be
  asymmetrical, with the latter ordered in relation to the former."
- Armstrong, Gleitman and Gleitman (1983): the PDF (upenn) returned 403; the PubMed record has
  no abstract. Used the summary in Rips and Thompson, "Possible number systems" (Cognitive,
  Affective & Behavioral Neuroscience, 2014), PDF
  https://bpb-us-e1.wpmucdn.com/sites.northwestern.edu/dist/4/1328/files/2017/05/Number_system_final-wxgc2z.pdf
  (`rips_thompson.txt` l. 32-41): "some odd numbers (e.g., 3) are judged as being more typical
  than other odd numbers (e.g., 4,284,647), as Armstrong, Gleitman, and Gleitman (1983) first
  demonstrated. Odd numbers are well-defined concepts, at least in the sense that both 3 and
  4,284,647 are definitely odd, not vaguely so. Thus, the fact that people believe that 3 is a
  more typical odd number than 4,284,647 suggests that typicality gradients are not diagnostic
  of a category's lack of precise definition."
- Lakoff's book: Wikipedia raw (`wiki_wfdt.txt`): "is a 1987 non-fiction book by George Lakoff";
  full title "Women, Fire, and Dangerous Things: What Categories Reveal about the Mind".

## 3. Arithmetic

- Tversky and Gati Table 3.2: pairs with s(q,p) < s(p,q): Japan-Philippines (12.37 > 11.95),
  W. Germany-Austria (15.60 > 15.20), USSR-France (5.21 > 5.03), India-Ceylon (13.91 > 13.88),
  France-Israel (7.48 > 7.34), USA-W. Germany (11.30 > 10.70): six of 21. USSR-Poland is 15.12 <
  15.18 (predicted direction). Mexico: 7.65 - 6.46 = 1.19.
- "2350 years": Aristotle's logical works date from the 4th century BC; 2008 + about 350 = about
  2358. Not noted.

## 4. Claims about other posts

- "Words as Hidden Inferences" is only named as the link target of the last paragraph.
- "Similarity Clusters" (same day) is not referred to in my notes.

## 5. Items not verified

- Rips (1975) itself (paywalled; OpenAlex has no abstract). Whether robins and ducks were among
  the species: not checked; the note says so.
- Rosch (1975) "Cognitive reference points" itself (paywalled); used Rosch 1978's summary and a
  2016 secondary summary for the numbers.
- Lakoff (1987) as the post's source for reaction times: not checked (the post itself is unsure).
- Armstrong et al. (1983) itself: only Rips and Thompson's summary.
- The post's "on a scale of 1 to 10" is offered as a way one could ask ("you can also ask");
  Rosch used a 7-point scale. Not noted (it does not report a study).

## 6. Judgment calls for the editor

1. Sadock `\cfact` ("The comparison is not in the cited paper, which I read in full"). I read
   all eight pages as scanned images at modest resolution. I am confident, but a second look at
   `sadock-02..10.png` would settle it. I did not use "misquotes" or "wrong"; the note gives the
   paper's supporting point and the real experimental source. In the Response this is marked as a
   correction whose point survives, and it is not in the "In short" line.
2. Rips `\clogic` ("Stated as a fact about what is reasonable, and disputed"). The post's
   sentence is "in a pragmatic sense, whatever difference ... must also be". Heit's model is
   offered by Heit as normative "given certain assumptions", which the note keeps. The note also
   says that whether subjects reasoned this way is separate, which is the post's own next move.
3. "This is the post's interpretation, not the study's." I first wrote that the data needed no
   asymmetric similarity; I weakened it, because a Tversky-style asymmetric similarity could also
   produce the result. The note now calls the post's mechanism "a possible alternative, but the
   study does not show it".
4. Armstrong `\clogic`. The post's claim is about how people reason ("We don't even reason as
   if set membership is a true-or-false property"). Rosch 1978 itself reads hedges as evidence of
   graded membership, so the note ends "Membership may still be graded for some categories; this
   post does not show it." I did not add McCloskey and Glucksberg (1978), who found inconsistent
   judgments on borderline items (supporting graded membership), because I could not reach the
   abstract (Springer blocked).
5. Kansas cpara gives support (Sadalla et al.), as credit.
6. Reserved words: none used as charges. "disputed" is not reserved.
7. Considered and dropped: Lakoff's year and subtitle (only in the citation cpara, neutrally);
   "1 to 10" versus Rosch's 7-point scale; "2350 years".
