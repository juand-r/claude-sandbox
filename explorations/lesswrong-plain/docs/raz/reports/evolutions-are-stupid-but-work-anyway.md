# Report: evolutions-are-stupid-but-work-anyway

## 1. The argument in three sentences

Natural selection is simple enough that population genetics can say how slow it is: a gene
with a 3% advantage needs hundreds of generations to fix and has only about a 6% chance of
fixing at all, and a complex adaptation must wait for each dependent part to become common
before the next can spread. Evolutions cannot plan, coordinate simultaneous changes, or share
inventions with each other, whereas a human designer does all of these in an afternoon. So
evolution is a poor model for human design, and should not be praised beyond what it deserves.

## 2. Sources checked

Saved in `data/sources/b3a_evostupid/`.

- Time to fixation. Kimura and Ohta 1969 (Genetics 61: 763-771) could not be downloaded (Europe
  PMC, NCBI and OUP all returned Cloudflare/5xx pages). Used instead: University of Washington
  GENET 453 lecture summary, 31 Jan 2001,
  https://depts.washington.edu/genetics/courses/genet453/2001/summaries/summary-jan31.html
  (`uw_genet453_jan31.txt`): "Kimura and Ohta found that the average time t of fixation for neutral
  mutations is 4N and under beneficial selection is (2/s) ln(2N) where ln() is the natural
  logarithm. Example: N=10 6 , s=0.01, then ... t(selected) = 2901 generations." Fitness convention
  there: "w(AA)=1, w(Aa)=1+s, w(aa)=1+2s", which matches the post's "bearers ... have 1.03 times
  as many children". Same page: "The fixation of a benefical mutation is independent by the
  population size (under the assumption that the population is not too small)."
- Probability of fixation. Patwa and Wahl 2008, J. R. Soc. Interface, "The fixation probability of
  beneficial mutations", https://pmc.ncbi.nlm.nih.gov/articles/PMC2607448/ (`patwa_wahl2008.txt`):
  "Haldane (1927) demonstrated that the probability of ultimate fixation, π , of an advantageous
  allele is given by π ≈2 s , when the allele is initially present as a single copy in a large
  population. Haldane's elegant result necessarily relies on a number of simplifying assumptions.
  The population size is large and constant, generations are discrete and the number of offspring
  that each individual contributes to the next generation is Poisson distributed."; "π ≈2 sN e / N
  ... Thus, π depends on the ratio of effective population size to census size." Reference list:
  "Haldane J.B.S. The mathematical theory of natural and artificial selection. Proc. Camb. Philos.
  Soc. 1927;23:838–844."
- Haldane's series: Wikipedia "A Mathematical Theory of Natural and Artificial Selection"
  (`wiki_haldane_series.txt`): Part IV, 1927, "Proceedings of the Cambridge Philosophical Society
  23:607-615" (no subtitle); Part V, 1927, "Selection and mutation", "23:838-844". The post's
  footnote gives "IV ... 23:607-615". The footnote cpara says so neutrally.
- Standing variation: Barrett and Schluter 2008, TREE, "Adaptation from standing genetic
  variation" (PMID 18006185), abstract via Europe PMC (`abstracts_bernhardt_powner_barrett.txt`):
  "Compared with new mutations, adaptation from standing genetic variation is likely to lead to
  faster evolution, the fixation of more alleles of small effect and the spread of more recessive
  alleles."
- Mutation rate: Wikipedia "Mutation rate" (`wiki_Mutation_rate.txt`): "the human genome mutation
  rate is similarly estimated to be ~1.1 × 10<sup>&minus;8</sup> per site per generation" (Roach et
  al. 2010).
- Horizontal gene transfer: Wikipedia (`wiki_Horizontal_gene_transfer.txt`): "Genes responsible for
  antibiotic resistance in one species of bacteria can be transferred to another species of
  bacteria through various mechanisms of HGT"; "Inter-bacterial gene transfer was first described in
  Japan in a 1959 publication that demonstrated the transfer of antibiotic resistance between
  different species of [[bacteria]]."
- Rotating wheels: Wikipedia "Rotating locomotion in living systems"
  (`wiki_Rotating_locomotion_in_living_systems.txt`): archaella are "driven by rotary motor
  proteins, which are structurally and evolutionarily distinct from bacterial flagella"; "The
  rotary motor at the base of the flagellum is similar in structure to ATP synthase." No count is
  given. The post's "three" is plausibly bacterial flagellum, archaellum and ATP synthase, but I
  could not source a count, so the note says only that none is given.
- Next post: "Natural Selection's Speed Limit and Complexity Bound", LessWrong id QcnkFgojszmo9k4xk,
  postedAt 2007-11-04T16:54:24Z, fetched via GraphQL (`lw_speed_limit_complexity_bound.md`). After
  two short opening paragraphs: "(Warning:  A simulation I wrote to verify the following arguments
  did not return the expected results.  See addendum and comments.)" Not in the R:A-Z manifest
  (grep for "speed-limit" in data/manifests/rationality_az.json: 0).

## 3. Arithmetic

- Post's formula 2 ln(N)/s: N=100,000, s=0.03: 2 x 11.513 / 0.03 = 767.5 -> 768. N=500,000:
  2 x 13.122 / 0.03 = 874.8 -> 875. N=1,000,000, s=0.01: 2 x 13.816 / 0.01 = 2763.1 -> 2763. All
  match the post.
- Kimura-Ohta (2/s) ln(2N): 813.7, 921.0, 2901.7. The post's values are 5.7%, 5.0% and 4.8% lower.
  Under the fifth threshold (STANDARDS 2.4), so no note on the difference; the "exactly" note says
  "to within about 5 per cent".
- Hunter-gatherer population: Wikipedia "Estimates of historical world population" table, row
  -10000: 2M (HYDE) and 4M. With N = 4,000,000: 2 ln(4e6)/0.01 = 3040 (+10%). Under threshold; the
  post's figure is at the low end but the conclusion is insensitive (logarithm). No note.
- 2s: 2 x 0.03 = 0.06. B example: 0.05 x 0.01 = 0.0005 = 0.05%; 2 x 0.0005 = 0.001 = 0.1%.
- Waiting time: 10^6 genomes x 10^-8 per base = 0.01 new copies of a given mutation per
  generation -> ~100 generations. Counting two copies per diploid person gives 0.02 (50
  generations); requiring a specific one of the three possible base changes gives about 150. The
  post's "may have to wait a hundred generations" is the right order; no note.

## 4. Claims about other posts

- An Alien God (`data/originals/an-alien-god.md`): "There's as many different "evolutions" as
  reproducing populations." and "A human engineer can redesign multiple parts simultaneously, or
  plan ahead for future changes." Both quoted in notes. "Evolution Fairy" appears there several
  times ("There isn't an Evolution Fairy that looks over the current state of Nature").
- The Wonder of Evolution: the quoted block matches the original.
- The pointer from "So, once again" to the evolutionary-algorithm note in The Wonder of Evolution
  matches that note.

## 5. Items not verified

- Graur and Li (2000), the post's source for the fixation time: not accessible. I used the
  Kimura-Ohta formula as given in a lecture summary.
- Kimura and Ohta 1969 itself: blocked (see above).
- Cynthia Kenyon's dinner remark: private, uncheckable; the note says so.
- The University of Tennessee course page (archived link): web.archive.org is blocked here; the
  note says only what the URL shows.

## 6. Judgment calls for the editor

1. Reserved words: none used as verdicts. The afterword's "In short" says the claim "does not hold
   for bacteria"; the claim is general in the post ("Then other evolutions don't imitate it"), and
   the note grants that it is true of the post's examples.
2. The "exactly" clogic: a defender could call "exactly how stupid" a figure of speech. I kept it
   because the previous day's post claims science has "a very exact idea", and the note mainly
   gives credit (figures agree within ~5%) and states the models' assumptions. Consider shortening.
3. The standing-variation clogic: the post's own B example (B's advantage scales with A's
   frequency) implies that B rises as A becomes common; "Only then" is the post's idealization. The
   note says the timetable is "the slower case", not that it is wrong.
4. The Haldane citation (Part IV pages for a Part V result) is in a footnote cpara, neutrally, as
   information; it could be moved to the report only.
5. The footnote-1 cpara says "I could not consult it": first person in a note; the model notes use
   "I could not reach" similarly (Planning Fallacy).
