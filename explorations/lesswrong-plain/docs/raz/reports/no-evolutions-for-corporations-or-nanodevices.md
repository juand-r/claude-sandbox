# Report: no-evolutions-for-corporations-or-nanodevices

## 1. The argument in three sentences

"Limited resources and competing replicators" does not by itself give evolution that matters;
by Price's equation, the change in a trait depends on its covariance with relative fitness,
and cumulative change needs faithful heredity over many generations. Corporations are
selected but inherit little and have gone through few generations, so their complex features
come from human design; nanodevices with encrypted, digitally copied instructions would have
almost no heritable variation, and would run out of resources after few generations. Only
when all of a list of conditions hold (replication, variation in traits and in reproduction,
their correlation, faithful long-range heredity, frequent turnover, over many iterations)
does selection build complex adaptations.

## 2. Sources checked

Saved in `data/sources/b3a_evostupid/`.

- Metzger epigraph: not found. Web search returned only this post and mirrors. I fetched all
  comments on this post, Evolving to Extinction, Evolutions Are Stupid and The Wonder of Evolution
  via the LessWrong GraphQL API (`lw_comments_evo4.json`, 44 + 32 + 68 + 85 comments) and searched
  for "gravitation" and "Metzger": no hits. The note says no source is given and none was found.
- Price equation: Wikipedia "Price equation" (`wiki_Price_equation.txt`): full form
  "\Delta{z} = \frac{1}{w}\operatorname{cov}(w_i, z_i) + \frac{1}{w}\operatorname{E}(w_i\,\Delta z_i)";
  "When the characteristic values <math>z_i</math> do not change from the parent to the child
  generation, the second term in the Price equation becomes zero resulting in a simplified
  version"; "\Delta z = \operatorname{cov}\left(v_i, z_i\right)" with "v_i=w_i/w". Dividing the full
  form by w gives cov(v_i, z_i) + E(v_i Δz_i), the term in the note.
- George R. Price: Wikipedia (`wiki_George_R._Price.txt`): "Price converted to [[Christianity]] and
  gave all his possessions to the poor. Struggling with a [[Hypothyroidism|thyroid condition]] in
  conditions of great poverty, he grew increasingly depressed ... and committed suicide."; "Price
  grew increasingly depressed by the implications of his equation." Pronouns for Price (a
  historical figure) follow the source.
- Lewontin 1970, "The Units of Selection", Annual Review of Ecology and Systematics 1: 1-18,
  https://joelvelasco.net/teaching/167/lewontin%2070%20-%20the%20units%20of%20selection.pdf
  (`lewontin1970.txt`): "1. Different individuals in a population have different morphologies,
  physiologies, and behaviors (phenotypic variation). 2. Different phenotypes have different rates
  of survival and reproduction in different environments (differential fitness). 3. There is a
  correlation between parents and offspring in the contribution of each to future generations
  (fitness is heritable). These three principles embody the principle of evolution by natural
  selection. While they hold, a population will undergo evolutionary change." Also: "It is not
  necessary, for example, that resources be in short supply for organisms to struggle for
  existence." (not used).
- Nelson and Winter 1982, An Evolutionary Theory of Economic Change, introduction chapter PDF,
  http://inctpped.ie.ufrj.br/spiderweb/pdf_2/Dosi_1_An_evolutionary-theory-of_economic_change..pdf
  (`nelson_winter1982.txt`, p. 14): "In our evolutionary theory, these routines play the role that
  genes play in biological evolutionary theory. They are a persistent feature of the organism and
  determine its possible behavior ...; they are heritable in the sense that tomorrow's organisms
  generated from today's (for example, by building a new plant) have many of the same
  characteristics, and they are selectable in the sense that organisms with certain routines may do
  better than others, and, if so, their relative importance in the population (industry) is
  augmented over time."
- Pearson correlation: Wikipedia (`wiki_Pearson_correlation_coefficient.txt`): "Pearson's
  correlation coefficient is the [[covariance]] of the two variables divided by the product of their
  standard deviations."
- Foresight guidelines: the post's link (foresight.org/guidelines/current.html) now 404s. The
  legacy copy https://legacy.foresight.org/guidelines/current.html (`foresight_legacy_current.txt`)
  is "Draft Version 6: April, 2006": "anti-mutation protections. For example, the information that
  specifies their construction is stored and copied in encoded form, and the encoding is such that
  any error in copying randomizes and thus destroys the decoded information." Also "Encrypted
  molecular manufacturing device instruction sets are utilized to discourage misuse."
- Atoms in the observable universe: Wikipedia "Observable universe" (`wiki_Observable_universe.txt`):
  "approximately 10<sup>80</sup> hydrogen atoms".
- Mutation rate 10^-8: see the Evolutions Are Stupid report (Wikipedia, ~1.1 x 10^-8).

## 3. Arithmetic

- Fixation probability "roughly twice": 2 x 3% = 6%. Matches the previous post.
- Prion: 1000 / 999.99999 = 1.00000001 (to 8 decimals), so s = 1e-8. By Haldane, chance of
  spreading about 2e-8.
- Resource wall: log2(10^80) = 80 x 3.3219 = 265.8, so fewer than 266 doublings from a single
  device would use every atom in the observable universe, fewer if each device holds many atoms.
  The note says "fewer than 270".
- Correlation example: A over 0..9, B = 50.0001 + 0.0001A. cov(A,B)/var(A) = 0.0001 (slope of B on
  A); cov/var(B) = 10,000 (slope of A on B); Pearson r = 1. So covariance over a single variance
  depends on the spread, while r does not; the post's definition lacks the property the example
  needs.
- "768 generations" and "10^-8" match the previous post.

## 4. Claims about other posts

- Evolving to Extinction (`data/originals/evolving-to-extinction.md`, Posted: 2007-11-16; this
  post 2007-11-17): introduces the "Frodo gene" ("Imagine a "Frodo gene" that sacrifices its
  vehicle *to save its entire species* ... It goes down."). Manifest order: this post 136,
  Evolving to Extinction 137. Consistent with the note.
- Einstein's Arrogance (`data/originals/einstein-s-arrogance.md`): "you need an amount of evidence
  roughly equivalent to the complexity of the hypothesis just to locate the hypothesis in
  theory-space." The post's summary ("vast majority", "trivial by comparison") is a fair
  paraphrase of that post's 27-bits-to-locate versus a few more bits for 99% argument.
- Evolutions Are Stupid: "roughly twice" here vs "= 2s" there; the note records the change of
  hedge, as credit.

## 5. Items not verified

- The Metzger quotations (see above).
- Whether "at most ten generations into the RNA World" is meant literally; not calculated in the
  post; no note beyond the paragraph description.
- "Diamond is stabler than proteins held together by van der Waals forces": a protein's chain is
  covalent, and its folded shape is held by hydrogen bonds, the hydrophobic effect and van der
  Waals forces together, so the phrase is loose. The comparison survives, and the point has no
  consequence for the argument (STANDARDS 2.4(2)), so no note. Not sourced beyond standard
  biochemistry.

## 6. Judgment calls for the editor

1. Reserved words: "Misstated" (not reserved) for the correlation definition. The mathematics is
   in section 3. A defender could call it a slip with no consequence; I kept the note because the
   post teaches the reader a definition, and the definition as stated does not support the
   example. The afterword says the paragraph's point survives.
2. The Lewontin clogic reads "an evolution" in the post's sense (cumulative selection), per
   fair-defender test 6, and says the dispute with Metzger is quantitative. It qualifies the
   thesis sentence rather than refuting it. The Response's "worded more broadly than the argument"
   rests on this; check that it is not too strong.
3. The Nelson and Winter note is scope ("does not discuss this line of work"), one sentence of
   fault plus information. A defender could say an essay need not survey economics. Consider
   cutting the last sentence of the note, or the note entirely.
4. The prion note: "the post does not argue that beneficial errors would all be this small". The
   post asks "how much correlation is there likely to be", which a defender could read as an
   argument by example. I kept it as a description of what the example shows.
5. Price: the post is hedged; the note gives supporting facts only. Pronouns he/his refer to
   Price, a historical figure; raz_check flags them.
6. The epigraph cpara says the source could not be found; no further inference.
