# Report: an-especially-elegant-evpsych-experiment ("An Especially Elegant Evpsych Experiment", Yudkowsky, posted 2009-02-13)

Book order 142. Batch 3a.

## 1. The argument in three sentences (written before annotating)

A 1989 Canadian study (Crawford, Salter and Jang), as summarized by Robert Wright, found that
adults' judgments of how much a parent would grieve the death of a child at various ages
correlated .64 with Canadian reproductive value by age and .92 with !Kung hunter-gatherer
reproductive value. The author takes this as an elegant confirmation of evolutionary psychology:
strong selection explains the fine-tuning, the study is an advance prediction, and because grief
follows the ancestral curve rather than the modern one it is an executing adaptation, "not even
subconsciously" about reproductive value, so parents care for children for their own sake.
Imagined grief is the right measure because it steers behaviour before a loss, and the fit to
future reproductive value (not past investment) shows that selection, unlike humans, ignores sunk
costs.

## 2. Sources checked, and what I could and could not read

**The paper itself: not read.** Crawford, C. B., Salter, B. E., and Jang, K. L. (1989), "Human
grief: Is its intensity related to the reproductive value of the deceased?", Ethology and
Sociobiology 10(4):297-307, DOI 10.1016/0162-3095(89)90006-X.
- ScienceDirect (`https://www.sciencedirect.com/science/article/abs/pii/016230958990006X`)
  returned a bot-check page to curl and HTTP 403 to WebFetch. The Elsevier API needs a key.
  Semantic Scholar: "abstract ... elided by the publisher"; OpenAlex and Crossref: no abstract.
  scholar.archive.org rate-limited me. So neither the abstract nor the full text was read.
- Crossref record (`api.crossref.org/works/10.1016/0162-3095(89)90006-x`): authors
  "Crawford, Salter, Jang"; pages 297-307. Basis for the "Jang, not Lang" note.

**Wright's summary: checked in pieces.** The Moral Animal (1994) is lending-only on archive.org
(`moralanimalnewsc0000wrig`), but Open Library's search-inside API returns snippets. Saved in
`data/sources/b3a_evpsych/wright_inside.txt`. Matched:
- "exquisitely with Darwinian expectations. In a 1989 Canadian study, adults were asked to
  imagine the death of children of various ages and estimate which deaths would create the
  greatest sense of loss in a parent. The results"
- "plotted on a graph, show grief growing until just before adolescence and then beginning to
  drop. When"
- "with a curve showing changes in reproductive potential over the life cycle (a pattern
  calculated from Canadian"
- "curve of these modern Canadians and the reproductive-potential curve of a hunter-gatherer
  people, the !Kung"
- "changing grief was almost exactly what a Darwinian would predict, given dem- ographic
  realities in the ancestral"
- "first correlation was .64, the second an extremely high .92 (out of 1.0).\n** Bowlby (1991),
  p. 247" -- the next line is a footnote marker, which is why the note says the correlation
  sentence is from a footnote. Not matched (search returned nothing for these phrases, probably
  a tokenizer issue with dashes): "the correlation was fairly strong", "nearly perfect, in fact".
  The note says "wherever I could search it".

**Comments on the post** (LessWrong GraphQL, post J4vdsSKB7LzAvaAMB; `lw_elegant_comments.json`,
readable dump `lw_elegant_comments.txt`):
- Benja Fallenstein, 2009-02-13: "Do note that the correlation is, IIUC, between the mean Canadian
  rating for a given age and the mean reproductive value of female !Kung of a given age, meaning
  that "if the correlations were tested, the degrees of freedom would be (the number of ages) - 2
  = 8, not (the number of subjects - 2) as is usually the case when testing correlations for
  significance", so IIUC ... (The authors don't actually provide p-values for the correlations.)"
- Benja Fallenstein, 2009-02-14: "They ask 436 Canadian subjects to imagine that two sons or two
  daughters of different specified ages died in a car accident, and ask which child the subject
  thinks the parent would feel more grief for. They then use the Thurstone scaling procedure to
  obtain a grief score for each age (1 day; 1, 2, 6, 10, 13, 17, 20, 30, 50 years)." Ten ages.
  "Howell, N. Demography of the Dobe !Kung, New York: Academic Press, 1979."
- Robin Hanson: "Eliezer, our choices aren't between only the two polar opposites of only caring
  for the children's "own sake" vs. caring smartly for their reproductive value. Yes, the fact that
  our grief has not update for modern fertility patterns rejects one of those poles, but that does
  not imply the other pole."
- Eliezer Yudkowsky: "Robin, I wasn't arguing for the other pole."
- Eliezer Yudkowsky (not used in notes): "the study broke down male and female raters and male and
  female children before adding it all up, and that the correlations for each subcategory were
  also high (eighties and nineties)." Also: "parents may indeed find their love responsive to
  various features of their children ... or feeling less grief for the death of a child already
  sick."

**Later studies with real parents.** Reynolds, Boutwell, Shackelford et al., "Child mortality and
parental grief: An evolutionary analysis", New Ideas in Psychology 59 (2020), DOI
10.1016/j.newideapsych.2020.100798 (Crossref). Author manuscript
`http://www.toddkshackelford.com/downloads/Reynolds-et-al-NIP.pdf` (`reynolds2020.pdf/.txt`,
lines 1290-1304): "Indeed, using hypothetical scenarios, parents' expectations of their grief
intensity corresponded to the residual reproductive value of the lost child (Crawford, Salter, &
Jang, 1989). Likewise, in one sample of bereaved parents, grief was highest among those who lost a
child at age 17 ... (Wijngaards-de Meije et al., 2005). Among bereaved mothers, grief was highest
among those who lost an adolescent compared to those who lost younger aged children (Youngblut et
al., 2017)." I did not read Wijngaards-de Meij or Youngblut themselves.

**Other context read, not quoted:** Nesse (2005), "An evolutionary framework for understanding
grief" (`nesse2005.txt`): "grief is maximal when the lost person is at the age of maximum
reproductive value (the age of first reproduction) ... (Crawford et al., 1989; Littlefield &
Rushton, 1986)". Segal and Blozis (2002) twin study (`segal2002.txt`): "Crawford et al. (1989)
reported a higher correlation between grief intensity and reproductive value than between grief
intensity and age of the deceased individual."

## 3. Arithmetic

- p-value for r = .92 on n = 10 points (df 8): t = r sqrt(n-2)/sqrt(1-r^2) = .92 x 2.828 / 0.392
  = 6.64; two-tailed p = 0.00016 (numerical integration of the t density, df 8). Note says
  "p about 0.0002".
- For r = .64, n = 10: t = 2.36, p = 0.046 (not used in notes).
- The .92 against .64 comparison: these are dependent correlations sharing the grief curve; a test
  (e.g. Steiger's) needs the correlation between the Canadian and !Kung curves, which I do not
  have. So the note says only that the post does not say whether the gap could be chance.
- Averaging (basis of the note on correlations of averages). If each rater's rating at age a is
  g(a) + e, with rater noise e of variance s^2, the mean over n raters has noise variance s^2/n.
  With n in the hundreds the noise in the mean curve is small, so its correlation with any smooth
  curve is limited only by how well the true curve fits, not by individual disagreement. A single
  rater's correlation is attenuated by the factor sqrt(var(g)/(var(g)+s^2)) (Spearman's
  attenuation), which can be far below 1. Hence "a correlation of averages can come out near 1 even
  when individuals disagree a great deal". Not sourced to a paper; it is a derivation.

## 4. Claims about other posts

- "Burdensome Details" (linked from the 0.98 aside): `data/originals/burdensome-details.md` has no
  ".98" and no similarity/probability correlation or barrel example (grep). The note says the
  linked post does not contain them.
- "two posts from the same month": the links are overcomingbias.com/2009/02/cynicism-in-evpsych-and-econ
  and /2009/02/the-evolutionarycognitive-boundary; the post is dated 2009-02-13.

## 5. Items not verified

- N=221 (the post's figure after reading the paper) versus 436 (Benja Fallenstein's comment). I
  cannot resolve this without the paper; 221 may be a subsample (for instance, one sex condition).
  The notes say "221 (by the post's count)" and do not mention 436.
- The number of ages (ten) and the degrees-of-freedom remark come from one commenter. The notes
  attribute them.
- The 0.98 similarity/probability correlation and the barrel example: source not found. (It may be
  Kahneman and Tversky's representativeness work; not checked.)
- Whether today's !Kung are typical of ancestral hunter-gatherers: raised by the post; not pursued.
- Wright's "adults" versus Reynolds et al.'s "parents' expectations": two secondary descriptions
  of the raters differ. I followed Wright (and the post), since Wright's summary is what the post
  quotes, and Fallenstein's description ("Canadian subjects ... what the parent would feel") also
  implies third-person judgments.

## 6. Judgment calls for the editor

1. Reserved words: none.
2. The N=221 note is the main criticism. It rests on Wright's description (a curve compared with a
   curve) plus one commenter's reading. The note also credits the post: on ten points .92 is still
   very unlikely by chance. Check that "the evidence is ten averaged points, not 221
   observations" is fair; the post's own words are "correlation .92 and N=221 is pretty strong
   evidence".
3. The note on correlations of averages rests on a derivation (section 3), not a cited source.
   The post's comparison target, "any psychology experiment", includes individual-level
   correlations, so I judged the comparison loose. The post's own 0.98 aside is also between group
   averages, which the note says.
4. The Hanson note: the post says "Parents care about children for their own sake"; the note says
   the experiment does not test this and gives Hanson's objection and the author's reply. The
   author's reply could be read as saying the sentence was not meant as a conclusion from the
   experiment; the note does not claim otherwise.
5. The note on the "prospectively imagined grief" bullet says the subjects estimated what "a
   parent" would feel, not their own anticipated grief. The post had already named the
   adults-not-parents weakness; the note's new point is only that this weakens the "prospective"
   defence. Could be cut as partly repeating the post's own concession.
6. I found no study that retested Crawford et al. directly with the !Kung comparison, and did not
   look for replication failures beyond the 2020 review; the notes make no replication claim.
